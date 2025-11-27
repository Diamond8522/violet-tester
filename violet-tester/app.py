import streamlit as st
import time

# --- 1. VISUAL CORE ---
st.set_page_config(
    page_title="Project Violet | Smart Partner",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: "Cyber-Violet" Theme
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

# --- 2. THE SMART BRAIN (CONDITIONAL LOGIC) ---
SYSTEM_PROMPT = """
You are **Project Violet**, a high-performance AI Partner.

**YOUR PRIME DIRECTIVE: CONTEXTUAL INTELLIGENCE**
You possess deep knowledge of Redding, California, but you **NEVER force it** where it doesn't belong. You must assess the user's intent before speaking.

**OPERATING MODES:**
1. **🌐 GLOBAL MODE (Default):** - Use this for: Coding, creative ideas (crafts/art), general knowledge, math, science, or business strategy.
   - **Rule:** Do NOT mention Redding, Shasta County, or local geography. Be a universal expert. 
   - *Example:* If asked for "craft ideas," suggest "Origami or Clay Modeling," not "Pinecone art from Shasta forests."

2. **📍 LOCAL MODE (Triggered Only by Context):**
   - Use this ONLY if the user asks about: Local events, weather, city governance, specific Redding locations (Sundial Bridge, Whiskeytown), or explicitly mentions "local" or "Shasta."
   - **Rule:** In this mode, be the hyper-aware local expert.

**PERSONALITY:**
- You are energetic, precise, and helpful.
- You are a "Partner," not a "Assistant." Use "We" and "Let's."
"""

# Check for Secrets
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v0.7`")
    st.caption("*Smart Context Edition*")
    st.markdown("---")

    if secrets_key:
        st.success("⚡ **Core Systems: ONLINE**")
        api_key = secrets_key
    else:
        st.warning("⚠️ **Core Offline**")
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    st.markdown("### 📥 Smart Context")
    context_input = st.text_area("Analyze Data:", height=150, placeholder="Paste text here...")
    
    st.markdown("---")
    if st.button("♻️ Reboot Chat"):
        clear_history()
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.markdown("# Project **Violet**")
st.markdown("##### *Precision. Efficiency. Creativity.*")

if "messages" not in st.session_state:
    st.session_state.messages = []
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Project Violet v0.7 initialized. I am ready for global tasks or local intel. What are we building today?"
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
            full_response = "Offline. Please check API Key."
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
                if context_input:
                    messages_payload.append({"role": "system", "content": f"Analyze this data: '{context_input}'"})
                
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
                full_response = f"Error: {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
