import streamlit as st
import time

# --- PROJECT VIOLET CONFIGURATION ---
st.set_page_config(
    page_title="Project Violet | Human-Centric AI",
    page_icon="🟣",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🟣 Project Violet")
    st.caption("v0.3 Universal Build")
    st.markdown("---")
    
    # 1. Select Provider
    st.subheader("1. Select Brain")
    provider = st.selectbox(
        "Choose AI Provider",
        ("Simulation (Free)", "Google Gemini (Free)", "Groq (Free)", "OpenAI (Paid)")
    )
    
    # 2. Input Key
    api_key = ""
    if provider != "Simulation (Free)":
        api_key = st.text_input(f"Enter {provider} Key", type="password")
        st.caption("Keys are not stored. Session use only.")
        
        # Link to get keys
        if provider == "Google Gemini (Free)":
            st.markdown("[Get Free Google Key](https://aistudio.google.com/app/apikey)")
        elif provider == "Groq (Free)":
            st.markdown("[Get Free Groq Key](https://console.groq.com/keys)")

    st.markdown("---")
    st.info("System Status: Online")

# --- MAIN INTERFACE ---
st.title("Project Violet")
st.markdown(f"#### Human-Centric Partner | Mode: **{provider}**")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am Project Violet. Select a provider in the sidebar to activate my full logic."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTELLIGENT LOGIC ---
if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # --- MODE 1: SIMULATION ---
        if provider == "Simulation (Free)":
            time.sleep(0.5)
            if "shasta" in prompt.lower():
                full_response = "Monitoring Shasta County: Redding Garden of Lights is active."
            elif "code" in prompt.lower():
                full_response = "I can generate Python scripts. Please connect a Live API key for full coding support."
            else:
                full_response = "Simulation Mode Active. Please select Google or Groq in the sidebar and enter a key for full intelligence."
        
        # --- MODE 2: LIVE AI (Google / Groq / OpenAI) ---
        elif not api_key:
            full_response = f"⚠️ Please enter your {provider} API Key in the sidebar to proceed."
        
        else:
            try:
                import openai
                
                # CONFIGURATION SWITCHER
                if provider == "Google Gemini (Free)":
                    client = openai.OpenAI(
                        api_key=api_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                    )
                    model_id = "gemini-1.5-flash"
                
                elif provider == "Groq (Free)":
                    client = openai.OpenAI(
                        api_key=api_key,
                        base_url="https://api.groq.com/openai/v1"
                    )
                    model_id = "llama-3.1-8b-instant"
                
                else: # OpenAI
                    client = openai.OpenAI(api_key=api_key)
                    model_id = "gpt-4o-mini"

                # EXECUTION
                stream = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": "You are Project Violet. Helpful, precise, ethical."},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True,
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                        
            except Exception as e:
                full_response = f"**Connection Error:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
