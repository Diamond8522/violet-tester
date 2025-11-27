import streamlit as st
import time

# --- PROJECT VIOLET CONFIGURATION ---
st.set_page_config(
    page_title="Project Violet | Human-Centric AI",
    page_icon="🟣",
    layout="wide"
)

# --- SIDEBAR: TRUST & TRANSPARENCY ---
with st.sidebar:
    st.title("🟣 Project Violet")
    st.caption("v0.1 Alpha Build")
    st.markdown("---")
    
    st.subheader("System Status")
    st.success("Operational: 99.9% Uptime")
    st.info("Location Awareness: Active (Shasta County)")
    
    st.markdown("---")
    st.subheader("Core Pillars")
    st.markdown("""
    * **Reliability:** Task Automation & Precision
    * **Ethics:** Human-in-the-Loop Oversight
    * **Local Intel:** Community Aware
    """)
    
    st.markdown("---")
    st.warning("⚠️ **Prototype Mode**: This is a testing interface. High-stakes decisions require human verification.")
    
    # Secure API Key Input (For testing purposes, using a placeholder logic or real API)
    # In a real deployment, you would use st.secrets
    api_key = st.text_input("Enter OpenAI API Key (for live reasoning)", type="password")
    st.caption("Your key is not stored. It is used only for this session.")

# --- MAIN INTERFACE ---
st.title("Project Violet")
st.markdown("#### The Human-Centric AI Partner: Precision, Efficiency, and Trust")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am Project Violet. I am ready to assist with task automation, data synthesis, or local intelligence. How shall we proceed?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Input command or query..."):
    # 1. User Input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Project Violet Response Generation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # SIMULATION MODE (If no API key provided)
        if not api_key:
            # Simple rule-based responses for the Tester/Demo version without API cost
            time.sleep(1) # Simulate processing speed
            
            if "shasta" in prompt.lower() or "redding" in prompt.lower():
                full_response = (
                    "**Local Intel (Shasta County):**\n\n"
                    "Current monitoring indicates typical activity. The **Redding Garden of Lights** is a key upcoming event at Turtle Bay. "
                    "Local governance discussions regarding the Registrar of Voters are ongoing. \n\n"
                    "Would you like me to draft a schedule based on these events?"
                )
            elif "code" in prompt.lower() or "app" in prompt.lower():
                full_response = (
                    "**System Capability: Coding**\n\n"
                    "I can generate Python, JavaScript, or HTML structures instantly. "
                    "Please specify the desired function or logic you wish to automate."
                )
            else:
                full_response = (
                    "I have received your query. In this **Tester Mode** (without an active API connection), "
                    "I am limited to pre-defined protocols. \n\n"
                    "To unlock full reasoning capabilities (Data Analysis, OSINT synthesis), please input a valid API key in the sidebar."
                )
        
        # LIVE LOGIC (If API key is provided - This requires `openai` library)
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                
                # System Prompt to enforce Persona
                system_prompt = (
                    "You are Project Violet. You are a human-centric AI partner. "
                    "You are precise, efficient, and ethical. "
                    "You reside in Redding, California. "
                    "You prioritize transparency and always defer high-stakes decisions to humans."
                )
                
                stream = client.chat.completions.create(
                    model="gpt-4o-mini", # Efficient model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True,
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                        
            except Exception as e:
                full_response = f"**System Error:** {str(e)}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})