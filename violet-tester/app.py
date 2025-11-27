import streamlit as st
import time
import json

# --- 1. VISUAL CORE & CSS ---
st.set_page_config(
    page_title="Project Violet | Command Center",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS: Gradient Text, Custom Buttons, Dark Mode Polish
st.markdown("""
<style>
    /* Global Dark Mode */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* The "Glow" Title */
    .title-text {
        font-size: 3.5em;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #a06cd5, #e0aaff, #4ea8de);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Gradient Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6247aa 0%, #a594f9 100%);
        color: white; border: none; border-radius: 10px; height: 3em; font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); }

    /* Input Box Polish */
    .stTextInput>div>div>input { 
        background-color: #1a1b26; color: #e0e0e0; border-radius: 15px; border: 1px solid #6247aa; 
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURATION & STATE ---

# Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Systems Online. I am **Violet v1.0**. Ready to collaborate."
    })

# Check for Secrets
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.messages = []

# --- 3. SIDEBAR (THE COCKPIT) ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v1.0`")
    st.caption("Status: **OPERATIONAL**")
    
    # A. Connection Status
    if secrets_key:
        st.success("🔒 **Secure Uplink Active**")
        api_key = secrets_key
    else:
        st.warning("⚠️ **Dev Mode**")
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    
    # B. SETTINGS (The Vibe Slider)
    st.markdown("### 🎚️ Output Style")
    response_style = st.radio(
        "Choose Detail Level:",
        ["⚡ Concise (Fast)", "🧠 Detailed (Deep Dive)"],
        index=0
    )

    st.markdown("---")
    
    # C. QUICK ACTIONS (The Usage Upgrade)
    st.markdown("### 🚀 Quick Launch")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Fix Grammar"):
            st.session_state.quick_prompt = "Proofread and improve the grammar of the last user input (or the text in context)."
    with col2:
        if st.button("💻 Debug Code"):
            st.session_state.quick_prompt = "Review the provided code for errors and suggest optimizations."
            
    if st.button("✨ Brainstorm Ideas"):
        st.session_state.quick_prompt = "Give me 5 creative, unconventional ideas for this topic."

    st.markdown("---")
    
    # D. CONTEXT & CONTROLS
    st.markdown("### 📥 Context Feed")
    context_input = st.text_area("Drop Data Here:", height=100, placeholder="Paste text/code for Violet to analyze...")
    
    # Download Chat History
    chat_str = json.dumps([m for m in st.session_state.messages], indent=2)
    st.download_button(
        label="💾 Save Chat Log",
        data=chat_str,
        file_name="violet_log.json",
        mime="application/json"
    )
    
    if st.button("♻️ Reboot System"):
        clear_history()
        st.rerun()

# --- 4. THE BRAIN (DYNAMIC PROMPT) ---
# We adjust the prompt based on the "Vibe Slider" choice
detail_instruction = "Be extremely concise. Use bullet points." if "Concise" in response_style else "Be comprehensive. Explain the 'Why' behind the answer."

SYSTEM_PROMPT = f"""
You are **Project Violet**, a high-performance AI Partner.

**YOUR VIBE:**
- **Electric & Fun:** Witty, confident, energetic. "Let's build this."
- **The Partner:** Collaborative and proactive.

**CURRENT SETTING:**
- {detail_instruction}

**LOCATION RULE:**
- **ZERO UNPROMPTED LOCATION DATA:** Never mention Redding/Shasta unless explicitly asked.

**GOAL:** Be the smartest, coolest partner the user has ever had.
"""

# --- 5. MAIN INTERFACE ---
st.markdown('<p class="title-text">Project Violet</p>', unsafe_allow_html=True)
st.caption("Your Digital Partner | Precision. Efficiency. Attitude.")

# Render Chat
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🟣"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

# --- 6. LOGIC ENGINE ---

# Check if a Quick Button was pressed OR the user typed something
prompt = None
if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt # Clear it after use
else:
    prompt = st.chat_input("Input command...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🟣"):
        message_placeholder = st.empty()
        full_response = ""

        if not api_key:
            time.sleep(0.5)
            full_response = "I need a Key to run logic processes. Check the sidebar."
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                
                messages_payload = [{"role": "system", "content": SYSTEM_
