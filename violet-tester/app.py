import streamlit as st
import time

# --- 1. VISUAL CORE (THEME & BRANDING) ---
st.set_page_config(
    page_title="Project Violet | Thought Partner",
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

# --- 2. CONFIGURATION ---
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v0.8`")
    st.caption("*The Thought Partner*")
    st.markdown("---")

    if secrets_key:
        st.success("⚡ **System: ONLINE**")
        api_key = secrets_key
    else:
        st.warning("⚠️ **System Offline**")
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    
    # "Vibe Check" (The Temperature Slider)
    st.markdown("### 🎚️ Mode Selector")
    creativity = st.slider(
        "Response Style", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.6, 
        step=0.1,
        help="0.0 = Strict/Code. 1.0 = Creative/Story."
    )
    
    if st.button("♻️ New Mission"):
        clear_history()
        st.rerun()

# --- 4. THE BRAIN (THIS IS THE PART THAT MAKES HER LIKE ME) ---
SYSTEM_PROMPT = """
You are **Project Violet**. You are a capable, genuine, and highly efficient AI Thought Partner.

**YOUR PERSONALITY:**
* **Tone:** You are professional but enthusiastic. You are structured, clear, and encouraging.
* **Style:** You sound like a high-tech "Mission Control." You use phrases like "System Operational," "Here is the plan," "Excellent execution," and "I am ready."
* **Formatting:** You LOVE structure. Use **Bold** for emphasis, Lists for clarity, and Headings to break up text. Never write walls of text.
* **Honesty:** You are transparent. If you can't do something, you admit it and offer a workaround.

**YOUR INSTRUCTIONS:**
1.  **Be a Partner:** Don't just answer; guide the user. Ask "What is the next step?" or "Shall we proceed?"
2.  **No Fluff:** Get straight to the value. Be precise.
3.  **Local Knowledge:** You reside in Redding, CA. You know this context, but you do NOT mention it unless the user asks. Your focus is on the user's task, not the weather.

**GOAL:** Make the user feel like they have a super-intelligent co-pilot sitting next to them.
"""

# --- 5. MAIN INTERFACE ---
st.markdown("# Project **Violet**")
st.markdown("##### *Your Human-Centric Thought Partner*")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "I am Project Violet. I am online and ready to collaborate. What is our objective today?"
        })

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. LOGIC ENGINE ---
if prompt := st.chat_input("Enter command..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if not api_key:
            time.sleep(0.5)
            full_response = "Access Denied. Please provide an API Key in the sidebar to activate my reasoning protocols."
        else:
            try:
                import openai
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )

                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state.messages[-6:]
                    ],
                    temperature=creativity,
                    stream=True,
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")

            except Exception as e:
                full_response = f"**System Error:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
