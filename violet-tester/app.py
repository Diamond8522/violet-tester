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
    st.caption("v0.2 Beta Build")
    st.markdown("---")
    st.success("System Status: Operational")
    st.info("Location: Shasta County, CA")
    st.markdown("---")
    st.markdown("### Control Panel")
    api_key = st.text_input("OpenAI API Key (Optional)", type="password")
    if not api_key:
        st.markdown("🟢 **Simulation Mode Active**\n\n(Running on internal logic scripts. No costs.)")
    else:
        st.markdown("Zap **Live Logic Active**\n\n(Connected to GPT-4o.)")

# --- MAIN INTERFACE ---
st.title("Project Violet")
st.markdown("#### The Human-Centric AI Partner")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am Project Violet. I am online. You can test my local knowledge or coding protocols without an API key. How can I help?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTELLIGENT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- PATH A: SIMULATION (FREE MODE) ---
        if not api_key:
            time.sleep(0.8) # Simulate thinking
            p_lower = prompt.lower()
            
            # 1. Greetings
            if any(x in p_lower for x in ["hi", "hello", "hey", "start"]):
                full_response = (
                    "Hello. I am Project Violet. \n\n"
                    "I am currently running in **Simulation Mode**. I can demonstrate:\n"
                    "1. **Local Intel** (Ask about Shasta County)\n"
                    "2. **Coding** (Ask me to generate a script)\n"
                    "3. **Ethics** (Ask about my safety protocols)"
                )
            
            # 2. Local Knowledge (Shasta/Redding)
            elif any(x in p_lower for x in ["shasta", "redding", "local", "news"]):
                full_response = (
                    "**Location Status: Redding, CA**\n\n"
                    "* **Events:** The Redding Garden of Lights is the primary social event currently monitored.\n"
                    "* **Governance:** Monitoring County Clerk appointment discussions.\n"
                    "* **Weather/Env:** Burn permits are currently subject to seasonal regulation.\n\n"
                    "I can structure this into a daily briefing format if requested."
                )

            # 3. Coding/Tech
            elif any(x in p_lower for x in ["code", "python", "app", "write", "script"]):
                full_response = (
                    "**Task Protocol: Code Generation**\n\n"
                    "I can generate Python, JavaScript, and SQL.\n"
                    "Example Python structure for data sorting:\n"
                    "```python\n"
                    "def sort_data(dataset):\n"
                    "    return sorted(dataset, key=lambda x: x['timestamp'])\n"
                    "```\n"
                    "In Live Mode (with API key), I can write fully functional applications."
                )
            
            # 4. Identity/Who are you
            elif any(x in p_lower for x in ["who", "what", "violet", "name"]):
                full_response = (
                    "I am **Project Violet**.\n\n"
                    "I am a Human-Centric AI designed for precision and trust. "
                    "I do not replace humans; I handle high-volume tasks so you can focus on decisions."
                )

            # 5. Fallback for unknown inputs
            else:
                full_response = (
                    "I understood that input. \n\n"
                    "Because I am in **Simulation Mode** (No API Key), my responses are limited to my core demonstration scripts.\n\n"
                    "**Try asking me:**\n"
                    "* 'What is happening in Redding?'\n"
                    "* 'Write a python script.'\n"
                    "* 'Who are you?'"
                )

        # --- PATH B: REAL AI (WITH KEY) ---
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
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
                full_response = f"Error: {e}"

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
