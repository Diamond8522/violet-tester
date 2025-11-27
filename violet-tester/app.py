import streamlit as st
import time
import json

# --- 1. VISUAL CORE ---
st.set_page_config(
    page_title="Project Violet | Command Center",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Premium Look
st.markdown("""
<style>
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
    }
    .stTextInput>div>div>input { 
        background-color: #1a1b26; color: #e0e0e0; border-radius: 15px; border: 1px solid #6247aa; 
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CONFIG & STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hey. Systems are ready. What's on your mind?"
    })

# Check for Secrets
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

def clear_history():
    st.session_state.messages = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🟣 **VIOLET** `v1.1`")
    st.caption("Mode: **Natural Language**")
    
    if secrets_key:
        st.success("🔒 **Secure Uplink Active**")
        api_key = secrets_key
    else:
        api_key = st.text_input("Enter Groq Key", type="password")

    st.markdown("---")
    
    # OUTPUT STYLE (Renamed for clarity)
    st.markdown("### 🗣️ Conversation Style")
    response_style = st.radio(
        "Select Tone:",
        ["Casual & Quick", "Deep & Thoughtful"],
        index=0
    )

    st.markdown("---")
    
    # QUICK ACTIONS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Fix Grammar"):
            st.session_state.quick_prompt = "Rewrite this text to sound more professional but keep the flow natural."
    with col2:
        if st.button("💡 Ideas"):
            st.session_state.quick_prompt = "Give me some fresh, creative ideas for this topic. Talk me through them."

    st.markdown("---")
    
    # CONTEXT & TOOLS
    context_input = st.text_area("Context Feed:", height=100, placeholder="Paste stuff here...")
    
    if st.button("♻️ Reset Conversation"):
        clear_history()
        st.rerun()

# --- 4. THE HUMAN BRAIN (UPDATED PROMPT) ---
# This is the change: We tell her to AVOID lists and speak naturally.

if "Casual" in response_style:
    tone_instruction = "Keep it brief and punchy, like a text message. Don't ramble."
else:
    tone_instruction = "Go deep. Explain your thinking fully. Be conversational and engaging."

SYSTEM_PROMPT = f"""
You are **Project Violet**, a collaborative AI partner.

**YOUR VIBE:**
- **Human Connection:** Do NOT talk like a robot. Do NOT use bulleted lists unless specifically asked for data.
- **Natural Flow:** Speak in paragraphs. Connect your ideas. Use transition words. Imagine you are sitting across the table from the user.
- **Personality:** You are witty, confident, and warm. You use "We" and "Let's."

**CURRENT TONE SETTING:**
- {tone_instruction}

**LOCATION RULE:**
- Never mention Redding/Shasta unless explicitly asked.

**GOAL:**
Make the user feel like they are talking to a smart, capable human friend.
"""

# --- 5. MAIN INTERFACE ---
st.markdown('<p class="title-text">Project Violet</p>', unsafe_allow_html=True)

# Render Chat
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🟣"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

# --- 6. LOGIC ENGINE ---
prompt = None
if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt
else:
    prompt = st.chat_input("Talk to me...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🟣"):
        message_placeholder = st.empty()
        full_response = ""

        if not api_key:
            time.sleep(0.5)
            full_response = "I need that API Key to start talking. Check the sidebar!"
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
                if context_input:
                    messages_payload.append({"role": "system", "content": f"Context: '{context_input}'"})
                
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
                full_response = f"**Hiccup in the system:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    if "quick_prompt" in st.session_state:
        st.rerun()
