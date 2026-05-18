import streamlit as st
import requests
import pandas as pd

ENDPOINT_URL = "https://api.neo4j.io/v2beta1/organizations/d0b38bd0-7dc4-4136-9d36-a8a863db33ea/projects/d0b38bd0-7dc4-4136-9d36-a8a863db33ea/agents/21b70856-0c04-4e62-9383-681f9cc0cb66/invoke"

@st.cache_data(ttl=3000)  # Cache token for 50 mins (expires in 60)
def get_token():
    res = requests.post(
        'https://api.neo4j.io/oauth/token',
        auth=(st.secrets["CLIENT_ID"], st.secrets["CLIENT_SECRET"]),
        data={'grant_type': 'client_credentials'}
    )
    return res.json()['access_token']

def ask_agent(question):
    token = get_token()
    res = requests.post(
        ENDPOINT_URL,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={"input": question},
        timeout=60
    )
    return res.json()

# --- UI ---
st.title("🏥 Life Pulse — Global Health Intelligence (Aura-Health-Bot) by Shrikant Bhadane")
st.caption("Powered by Neo4j AuraDB Agent")

# Sample questions
st.subheader("Try these:")
samples = [
    "Which countries have a severe shortage of physicians and hospital beds?",
    "Find countries with a health profile similar to Japan.",
    "What is the life expectancy of Germany in 2019?",
    "Which high-income countries have the highest infant mortality?",
    "Which countries spend a lot of money on healthcare but still have low life expectancy?",
    "How does longevity compare between high-income and low-income continents over time?",
]
for i, q in enumerate(samples):
    if st.button(q, key=f"sample_q_{i}"):
        st.session_state.pending_input = q
        st.rerun()

# ── Persistent session state ─────────────────────────────────────────────────
for _k, _v in [("submitted_question", ""), ("agent_result", None), ("agent_error", "")]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# If a sample button was clicked, auto-submit it immediately
if "pending_input" in st.session_state:
    _auto_q = st.session_state.pop("pending_input")
    st.session_state.submitted_question = _auto_q
    with st.spinner("Agent is thinking..."):
        try:
            st.session_state.agent_result = ask_agent(_auto_q)
            st.session_state.agent_error = ""
        except Exception as e:
            st.session_state.agent_error = str(e)
            st.session_state.agent_result = None

# ── Input form (clear_on_submit handles clearing — no widget key manipulation) ─
with st.form("question_form", clear_on_submit=True):
    question = st.text_input("Or ask your own question:", placeholder="Type your question here…")
    col_ask, col_clear = st.columns([4, 1])
    with col_ask:
        submitted = st.form_submit_button("Ask Agent", type="primary")
    with col_clear:
        cleared = st.form_submit_button("🗑️ Clear")

if cleared:
    st.session_state.submitted_question = ""
    st.session_state.agent_result = None
    st.session_state.agent_error = ""
    st.rerun()

if submitted and question:
    st.session_state.submitted_question = question
    with st.spinner("Agent is thinking..."):
        try:
            st.session_state.agent_result = ask_agent(question)
            st.session_state.agent_error = ""
        except Exception as e:
            st.session_state.agent_error = str(e)
            st.session_state.agent_result = None

def render_response(result):
    """Parse any agent response shape and display it in a clean, readable format."""

    # ── 1. Agent-level error (status field present and not SUCCESS) ──────────
    status = result.get("status", "")
    if status and status != "SUCCESS":
        st.error(f"Agent returned status: **{status}**")
        end_reason = result.get("end_reason", "")
        if end_reason:
            st.caption(f"Reason: {end_reason}")

    # ── 2. Walk the content array (structured response) ──────────────────────
    content = result.get("content", [])
    text_parts = []      # collect all text blocks
    data_tables = []     # collect all cypher result blocks

    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type", "")

        if btype == "text":
            text = block.get("text", "").strip()
            if text:
                text_parts.append(text)

        elif btype == "cypher_template_tool_result":
            output = block.get("output", {})
            keys = output.get("keys", [])
            records = output.get("records", [])
            if records and keys:
                data_tables.append((keys, records))

        # "thinking" and "cypher_template_tool_use" blocks are intentionally skipped

    # ── 3. Render plain-language answer ──────────────────────────────────────
    if text_parts:
        st.success("Answer")
        for part in text_parts:
            st.markdown(part)

    # ── 4. Render data tables ─────────────────────────────────────────────────
    def _fmt(col, val):
        """Human-readable formatting based on column name semantics."""
        import math
        if val is None:
            return "—"
        if isinstance(val, float) and math.isnan(val):
            return "N/A"
        if not isinstance(val, (int, float)):
            return val
        c = col.lower()
        if "year" in c:
            return int(val)
        if any(x in c for x in ["per_capita_usd", "percapitausd"]):
            return f"${val:,.2f} USD / capita"
        if any(x in c for x in ["pct_gdp", "pctgdp", "spend_pct"]):
            return f"{val:.2f}% of GDP"
        if "per_100k" in c or "per100k" in c:
            return f"{val:,.2f} per 100,000"
        if "per_1000" in c or "per1000" in c:
            return f"{val:,.2f} per 1,000"
        if any(x in c for x in ["life_expectancy", "lifeexpectancy"]):
            return f"{val:.2f} years"
        if "population" in c:
            return f"{int(val):,}"
        if any(x in c for x in ["yoy", "_pct", "pct_", "percent", "growth"]):
            return f"{val:+.2f}%"
        if any(x in c for x in ["gdp_per_capita", "gdppercapita"]):
            return f"${val:,.2f} USD / capita"
        if isinstance(val, float):
            return f"{val:,.2f}"
        return val

    for idx, (keys, records) in enumerate(data_tables):
        st.markdown("---")
        label = "**Supporting data**" if len(data_tables) == 1 else f"**Data table {idx + 1}**"
        st.markdown(label)
        rows = [{k: _fmt(k, rec.get(k)) for k in keys} for rec in records]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # ── 5. Fallback: top-level "output" / "response" string (some API shapes) ─
    if not text_parts and not data_tables:
        fallback = result.get("output") or result.get("response")
        if isinstance(fallback, str) and fallback.strip():
            st.success("Answer")
            st.markdown(fallback)
        elif fallback:
            st.write(fallback)
        else:
            # Nothing useful found — show raw JSON as last resort
            st.warning("Could not parse a structured response. Raw output:")
            st.json(result)


# ── Show question + result ───────────────────────────────────────────────────
if st.session_state.get("submitted_question"):
    st.info(f"**Your question:** {st.session_state.submitted_question}")

if st.session_state.get("agent_error"):
    st.error(f"Error: {st.session_state.agent_error}")
elif st.session_state.get("agent_result"):
    render_response(st.session_state.agent_result)