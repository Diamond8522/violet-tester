import streamlit as st
import time
import requests
import feedparser
import pytz
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Project Violet | Live Dashboard",
    page_icon="🟣",
    layout="wide"
)

# --- LIVE DATA FUNCTIONS ---

def get_redding_time():
    """Fetches real-time PST for Shasta County."""
    tz = pytz.timezone('US/Pacific')
    return datetime.now(tz).strftime("%I:%M %p | %B %d, %Y")

def get_quote():
    """Fetches a live inspirational quote."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        return f"**\"{data[0]['q']}\"** — *{data[0]['a']}*"
    except:
        return "**\"The obstacle is the way.\"** — *Marcus Aurelius*"

def get_news(topic):
    """Parses Google News RSS for live headlines."""
    try:
        # URL encode the topic
        safe_topic = topic.replace(" ", "+")
        rss_url = f"https://news.google.com/rss/search?q={safe_topic}+when:7d&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        
        news_items = []
        for entry in feed.entries[:3]: # Get top 3
            news_items.append(f"• [{entry.title}]({entry.link})")
            
        return "\n".join(news_items)
    except:
        return "• *Signal Interrupted: Unable to fetch live news feed.*"

# --- SIDEBAR: MONITORING STATION ---
with st.sidebar:
    st.title("🟣 Project Violet")
    st.caption("v0.3 Live Beta")
    
    st.markdown("---")
    
    # 1. LIVE CLOCK
    st.subheader("📍 Local Status")
    st.markdown(f"**Redding, CA**")
    st.markdown(f"`{get_redding_time()}`")
    
    st.markdown("---")
    
    # 2. LIVE QUOTE
    st.subheader("🧠 Daily Insight")
    if 'quote' not in st.session_state:
        st.session_state.quote = get_quote()
    st.markdown(st.session_state.quote)
    if st.button("Refresh Insight"):
        st.session_state.quote = get_quote()
        st.rerun()

    st.markdown("---")
    api_key = st.text_input("OpenAI API Key (Optional)", type="password")

# --- MAIN INTERFACE ---
st.title("Project Violet")
st.markdown("#### Human-Centric AI | Situational Awareness Dashboard")

# --- TABBED INTERFACE ---
tab1, tab2 = st.tabs(["💬 Conversation", "📡 Live Intel Streams"])

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.success("Monitoring: Shasta County")
        st.markdown(get_news("Redding California"))
    with col2:
        st.info("Monitoring: Artificial Intelligence")
        st.markdown(get_news("Artificial Intelligence"))

with tab1:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "I am online. My dashboard is monitoring live news from Redding and the AI sector. How can I help you?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Command or Inquiry..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # --- SIMULATION MODE ---
            if not api_key:
                time.sleep(0.5)
                if "news" in prompt.lower():
                    full_response = "I have displayed the latest headlines in the **Live Intel Streams** tab above. I am tracking events in Redding and AI developments."
                elif "time" in prompt.lower():
                    full_response = f"The current local time in Redding is **{get_redding_time()}**."
                else:
                    full_response = (
                        "**System Note:** I am running in Free Mode. \n\n"
                        "I can show you live news (check the Tabs above) and local time, "
                        "but for complex reasoning or coding, I require an API Key."
                    )
            
            # --- LIVE BRAIN MODE ---
            else:
                try:
                    import openai
                    client = openai.OpenAI(api_key=api_key)
                    stream = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are Project Violet. You have access to the user's local time and news feeds contextually."},
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
