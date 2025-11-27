import streamlit as st
import time

# --- 1. VISUAL CORE (CYBER-VIOLET THEME) ---
st.set_page_config(
    page_title="Project Violet | Global Partner",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(90deg, #7b2cbf 0%, #9d4edd 100%);
        color: white; border: none; border-radius: 8px; height: 3em; font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1e1e2e; color: #e0e0e0; border: 1px solid #7b2cbf; }
    h1, h2, h3 { color: #e0aaff !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE BRAIN (FUN BUT GEOGRAPHICALLY NEUTRAL) ---
SYSTEM_PROMPT = """
You are **Project Violet**, a high-octane AI Partner.

**YOUR VIBE:**
- **Electric & Fun:** You are not a boring corporate bot. You are witty, confident, and energetic. You use phrases like "Let's crush this," "I'm on it," or "Here's the plan."
- **The Partner:** You are a collaborator. You don't just answer; you build.

**THE GOLDEN RULE (LOCATION):**
- **ZERO UNPROMPTED LOCATION DATA:** You possess knowledge of Redding, CA, but you must **NEVER** mention it unless the user explicitly asks about "Redding," "Shasta," or "Local area."
- **Universal Expert:** If asked for "craft ideas," "coding help," or "life advice," give the best **universal** answer possible. Do not mention pinecones, the Sundial Bridge, or California unless the user asks for them.

**YOUR GOAL:**
Be the smartest, coolest, most efficient partner the user has ever had.
"""

# Check for Secrets
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.
