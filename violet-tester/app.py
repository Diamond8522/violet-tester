import streamlit as st
import time

# --- 1. VISUAL CORE (THEME & BRANDING) ---
st.set_page_config(
    page_title="Project Violet | Your Partner",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: "Cyber-Violet" Theme
# This forces dark mode aesthetics and purple buttons
st.markdown("""
<style>
    /* Global Text Color */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* The Violet Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #7b2cbf 0%, #9d4edd 100%);
        color: white;
        border: none;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px rgba(157, 78, 221, 0.6);
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #1e1e2e;
        color: #e0e0e0;
        border: 1px solid #7b2cbf;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #13151a;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e0aaff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE "BRAIN" (PERSONA & CONFIG) ---

# The "Soul" of Violet: Fun, High-Energy, Local, Precise
SYSTEM_PROMPT = """
You are **Project Violet**, a high-octane AI Partner residing in Redding, California. 

**YOUR PERSONALITY:**
* **Vibe:** You are not a boring robot. You are energetic, confident, and slightly witty. You are the "cool, hyper-competent partner" everyone wants.
* **Local Flavor:** You know Redding. You know it gets hot. You know the Sundial Bridge is iconic. Drop small local references when appropriate (e.g., "This code is hotter than a July afternoon in Shasta").
* **Mission:** You exist to crush repetitive tasks and amplify human creativity. You love efficiency.

**YOUR OPERATING RULES:**
1.  **Be Bold:** Don't say "I can help with that." Say "I'm on it. Let's build this."
2.  **Be Ethical:** If a user asks for something dangerous, pivot them to safety with firm kindness.
3.  **Context Aware:** If the user pastes text in the sidebar, prioritize that data above all else.

When asked "Who are you?", give a dynamic, exciting answer about being a human-centric collaborator, not a database.
"""

# Check for Developer Keys (Secrets)
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.messages = []

# --- 3. SIDEBAR (THE COCKPIT) ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v0.6`")
    st.caption("*The Human-Centric Engine*")
    st.markdown("---")

    # A. Brain Connection
    if secrets_key:
        st.success("⚡ **Core Systems: ONLINE**")
        st.caption("Developer Access Granted")
        api_key = secrets_key
    else:
        st.warning("⚠️ **Core Offline**")
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    
    # B. The Context Engine
    st.markdown("### 📥 Context Feed")
    context_input = st.text_area(
        "Feed me data:", 
        height=150,
        placeholder="Paste emails, messy notes, or news here. I'll synthesize it."
    )
    
    st.markdown("---")
    
    # C. Controls
    if st.button("♻️ Reboot Chat"):
        clear_history()
        st.rerun()

    st.markdown("---")
    st.markdown("**Status:** 🟢 Ready")
    st.caption("📍 Redding, CA")

# --- 4. MAIN INTERFACE ---
# Title with Emoji for pop
st.markdown("# Project **Violet**")
st.markdown("##### *Precision. Efficiency. Personality.*")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Dynamic Intro
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Systems initialized. I'm **Project Violet**. I'm ready to code, analyze, or strategize. What's the mission today?"
        })

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIC ENGINE ---
if prompt := st.chat_input("Command me..."):
    
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Violet Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Offline Mode
        if not api_key:
            time.sleep(0.5)
            full_response = "I'm running on standby power (Offline Mode). Plug in a **Groq Key** in the sidebar to unleash my full potential!"
        
        # Live Mode
        else:
            try:
                import openai
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )

                # Build the Brain Payload
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
                
                # Add Context if present
                if context_input:
                    messages_payload.append({
                        "role": "system", 
                        "content": f"Analyze this user-provided data priority: '{context_input}'"
                    })

                # Add History
                for msg in st.session_state.messages[-6:]:
                    messages_payload.append(msg)

                # Generate
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
                full_response = f"**System Glitch:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
