import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Life Pulse — Global Health Intelligence",
    page_icon="🏥",
    layout="centered",
)

# ── Analytics ────────────────────────────────────────────────────────────────
components.html(
    """
        <script defer src="https://cloud.umami.is/script.js" data-website-id="05270d48-3fd0-4296-af09-228594f3e675"></script>
    """,
    height=0,
)

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Page background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 50%, #0d1b2a 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer { visibility: hidden; }

/* ── Main content block: max width + centred ── */
[data-testid="stMainBlockContainer"] {
    max-width: 860px !important;
    padding: 2rem 2rem 4rem 2rem;
}

/* ── Hero header card ── */
.hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #0e4d6e 60%, #00b4d8 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem 1.6rem 2.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 32px rgba(0,180,216,0.18);
}
.hero h1 {
    font-size: 1.7rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
    line-height: 1.3;
}
.hero p {
    font-size: 0.88rem;
    color: #90e0ef;
    margin: 0;
    letter-spacing: 0.03em;
}

/* ── Section label ── */
[data-testid="stMarkdownContainer"] h3 {
    color: #90e0ef;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Readable markdown text on dark backgrounds ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #dbeafe;
}

/* ── Sample question pill buttons ── */
[data-testid="stBaseButton-secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,180,216,0.35) !important;
    border-radius: 20px !important;
    color: #caf0f8 !important;
    font-size: 0.82rem !important;
    padding: 0.3rem 0.9rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(0,180,216,0.2) !important;
    border-color: #00b4d8 !important;
    color: #ffffff !important;
}

/* ── Ask Agent primary button ── */
[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(90deg, #0077b6, #00b4d8) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}

/* ── Form / input card ── */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,180,216,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(0,180,216,0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    caret-color: #00b4d8 !important;
    font-size: 1rem !important;
}
[data-testid="stTextInput"] input::placeholder { color: #7eb3c4 !important; }
[data-testid="stTextInput"] input:focus {
    border: 1px solid #00b4d8 !important;
    box-shadow: 0 0 0 2px rgba(0, 180, 216, 0.1) !important;
}

/* ── Your question info banner (blue) ── */
[data-testid="stAlert"] {
    border-radius: 10px;
    background-color: #0a3556 !important;
    border: 1px solid #1a6a9a !important;
    color: #e0f4ff !important;
}
[data-testid="stAlert"] p, [data-testid="stAlert"] strong {
    color: #e0f4ff !important;
}

/* ── Answer success block (green) ── */
[data-testid="stAlert"][data-baseweb="notification"] {
    border-radius: 10px;
    background-color: #0a3320 !important;
    border: 1px solid #1a7a42 !important;
    color: #c6f6d5 !important;
}
[data-testid="stAlert"][data-baseweb="notification"] p,
[data-testid="stAlert"][data-baseweb="notification"] strong {
    color: #c6f6d5 !important;
}
</style>
""", unsafe_allow_html=True)

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
st.markdown("""
<div class="hero">
  <h1>🏥 Life Pulse &mdash; Global Health Intelligence</h1>
  <p>Aura-Health-Bot &nbsp;·&nbsp; Powered by Neo4j AuraDB Agent &nbsp;·&nbsp; by Shrikant Bhadane</p>
</div>
""", unsafe_allow_html=True)

# Sample questions
st.markdown("### 💡 Try these")
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
        st.markdown(
            '<div style="background:#0a3320;border-left:4px solid #22c55e;'
            'border-radius:8px;padding:0.55rem 1rem;margin:1rem 0 0.4rem 0;">'
            '<b style="color:#6ee7a0;font-size:1rem;">&#10022; Answer</b></div>',
            unsafe_allow_html=True,
        )
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
            st.markdown(
                '<div style="background:#0a3320;border-left:4px solid #22c55e;'
                'border-radius:8px;padding:0.55rem 1rem;margin:1rem 0 0.4rem 0;">'
                '<b style="color:#6ee7a0;font-size:1rem;">&#10022; Answer</b></div>',
                unsafe_allow_html=True,
            )
            st.markdown(fallback)
        elif fallback:
            st.write(fallback)
        else:
            # Nothing useful found — show raw JSON as last resort
            st.warning("Could not parse a structured response. Raw output:")
            st.json(result)


# ── Show question + result ───────────────────────────────────────────────────
if st.session_state.get("submitted_question"):
    q = st.session_state.submitted_question
    st.markdown(
        f'<div style="background:#0a3556;border-left:4px solid #00b4d8;'
        f'border-radius:8px;padding:0.7rem 1rem;margin:1rem 0;">'
        f'<b style="color:#90caf9;">Your question:</b> '
        f'<span style="color:#e0f4ff;">{q}</span></div>',
        unsafe_allow_html=True,
    )

if st.session_state.get("agent_error"):
    st.error(f"Error: {st.session_state.agent_error}")
elif st.session_state.get("agent_result"):
    render_response(st.session_state.agent_result)