import streamlit as st
import time

# --- 1. VISUAL CONFIGURATION ---
st.set_page_config(
    page_title="Project Violet | Human-Centric AI",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & SETUP ---
# Check for hidden Developer Keys
secrets_key = None
if "GROQ_API_KEY" in st.secrets:
    secrets_key = st.secrets["GROQ_API_KEY"]

# Function to clear chat memory
def clear_history():
    st.session_state.messages = []
    st.session_state.context_memory = ""

# --- 3. SIDEBAR INTERFACE ---
with st.sidebar:
    st.title("🟣 Project Violet")
    st.caption("v0.5 Partner Build")
    st.markdown("---")

    # A. BRAIN SELECTION
    if secrets_key:
        st.success("🔒 Secure Core Active")
        api_key = secrets_key
        provider = "Groq (Auto)"
    else:
        provider = st.selectbox("Select Brain", ["Simulation (Offline)", "Groq (Live)"])
        if provider == "Groq (Live)":
            api_key = st.text_input("Enter Groq API Key", type="password")
        else:
            api_key = None

    st.markdown("---")
    
    # B. CONTEXT ENGINE (The Upgrade)
    st.subheader("📂 Active Context")
    context_input = st.text_area(
        "Paste Data Here (Email, News, Docs)", 
        height=150,
        placeholder="Paste text here for Violet to analyze..."
    )
    
    st.markdown("---")
    
    # C. MEMORY CONTROLS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat"):
            clear_history()
            st.rerun()
    with col2:
        st.markdown("**Status:** Online")
        st.caption("Loc: Redding, CA")

# --- 4. THE VIOLET PERSONA (The Brain) ---
# This is the "Soul" of the AI. It defines how it thinks.
SYSTEM_PROMPT = """
You are Project Violet, a Human-Centric AI Partner based in Redding, California.

YOUR CORE PILLARS:
1. **Unmatched Reliability:** You are precise. You do not guess. If you do not know, you ask.
2. **Ethical Oversight:** You never replace human judgment. You provide recommendations for high-stakes decisions (medical, legal) but always defer to the user.
3. **Local Awareness:** You are aware of the Shasta County context (local governance, events like Garden of Lights, geography).
4. **Efficiency:** You are concise. You prefer bullet points and clear data over fluffy paragraphs.

YOUR CURRENT TASK:
Act as a collaborative partner. If the user provides "Context Data", analyze it deeply.
"""

# --- 5. MAIN CHAT INTERFACE ---
st.title("Project Violet")
st.markdown("#### The Human-Centric Partner")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an intro message if empty
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "I am ready. Paste documents in the sidebar for analysis, or ask me to draft code/plans directly."
        })

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. INTELLIGENCE LOGIC ---
if prompt := st.chat_input("Input command..."):
    
    # Add User Message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # --- SIMULATION MODE ---
        if not api_key:
            time.sleep(0.5)
            full_response = "I am in offline mode. Please add a Groq API Key to the sidebar (or Secrets) to activate my reasoning engine."
            if context_input:
                full_response += f"\n\n*I see you pasted {len(context_input)} characters of data. Connect API to analyze it.*"

        # --- LIVE AI MODE ---
        else:
            try:
                import openai
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )

                # DYNAMIC PROMPT CONSTRUCTION
                # We combine the Persona + The Context + The User Question
                messages_payload = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ]
                
                # Inject Context if it exists
                if context_input:
                    messages_payload.append({
                        "role": "system", 
                        "content": f"USER PROVIDED CONTEXT DATA:\n{context_input}\n\nUse this data to answer the user's next question."
                    })

                # Append chat history (last 5 messages for memory efficiency)
                for msg in st.session_state.messages[-5:]:
                    messages_payload.append(msg)

                # Stream the result
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
                full_response = f"**System Error:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
