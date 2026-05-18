import streamlit as st
import requests

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
        st.session_state.question = q

question = st.text_input("Or ask your own question:", 
                          value=st.session_state.get("question", ""))

if st.button("Ask Agent", key="ask_agent_btn", type="primary") and question:
    with st.spinner("Agent is thinking..."):
        try:
            result = ask_agent(question)
            st.success("Response:")
            st.write(result.get("output") or result.get("response") or result)
        except Exception as e:
            st.error(f"Error: {e}")