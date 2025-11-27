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
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v0.8`")
    st.caption("*Global Edition*")
    st.markdown("---")

    if secrets_key:
        st.success("⚡ **System: ONLINE**")
        api_key = secrets_key
    else:
        st.warning("⚠️ **System Offline**")
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    st.markdown("### 📥 Context Feed")
    context_input = st.text_area("Analyze Data:", height=150, placeholder="Paste text here...")
    
    st.markdown("---")
    if st.button("♻️ Reboot Chat"):
        clear_history()
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown("# Project **Violet**")
st.markdown("##### *Precision. Efficiency. Attitude.*")

if "messages" not in st.session_state:
    st.session_state.messages = []
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Project Violet initialized. I'm ready to rock. What's the mission?"
        })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIC ENGINE ---
if prompt := st.chat_input("Command me..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if not api_key:
            time.sleep(0.5)
            full_response = "I'm offline. Hook up the API Key in the sidebar to get this party started."
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
                if context_input:
                    messages_payload.append({"role": "system", "content": f"Context Data: '{context_input}'"})
                
                for msg in st.session_state.messages[-6:]:
                    messages_payload.append(msg)

                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_payload,
                    stream=True,
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")

            except Exception as e:
                full_response = f"**Glitch detected:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
