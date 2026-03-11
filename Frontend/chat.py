import streamlit as st
import requests
import time

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="AAU AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Session State
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ------------------------------
# Dynamic CSS based on theme
# ------------------------------
def get_css(theme):
    if theme == "Light":
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Main app background – soft light gradient */
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(145deg, #f9fafb 0%, #f3f4f6 100%) !important;
        }

        /* Sidebar – light glass */
        section[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(8px);
            border-right: 1px solid rgba(0,0,0,0.05);
        }

        section[data-testid="stSidebar"] * {
            color: #1f2937 !important;
        }

        /* Titles */
        h1 {
            text-align: center;
            font-weight: 700;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            text-align: center;
            color: #4b5563;
            font-size: 1.2rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        /* Chat messages */
        [data-testid="chatMessage"] {
            background: white !important;
            border-radius: 20px !important;
            padding: 15px 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            border: 1px solid rgba(0,0,0,0.03) !important;
            margin: 10px 0 !important;
        }

        /* User message specific */
        [data-testid="chatMessage"][data-testid*="user"] {
            background: #eef2ff !important;
            border-left: 5px solid #4f46e5 !important;
        }

        /* Assistant message specific */
        [data-testid="chatMessage"][data-testid*="assistant"] {
            background: white !important;
            border-left: 5px solid #10b981 !important;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            border-radius: 40px !important;
            border: 1px solid #e5e7eb !important;
            background: white !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
        }
        [data-testid="stChatInput"] input {
            color: #111827 !important;
        }

        /* Sidebar elements */
        .stButton > button {
            width: 100%;
            border-radius: 40px;
            background: white;
            border: 1px solid #e5e7eb;
            color: #1f2937;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            border-color: #4f46e5;
            background: #f9fafb;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #9ca3af;
            font-size: 0.8rem;
        }
        </style>
        """
    else:  # Dark theme
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Main app background – dark gradient */
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%) !important;
        }

        /* Sidebar – dark glass */
        section[data-testid="stSidebar"] {
            background: rgba(20, 20, 20, 0.8) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        section[data-testid="stSidebar"] * {
            color: #e5e7eb !important;
        }

        /* Titles */
        h1 {
            text-align: center;
            font-weight: 700;
            background: linear-gradient(135deg, #00fff0, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 1.2rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        /* Chat messages */
        [data-testid="chatMessage"] {
            background: #1f2937 !important;
            border-radius: 20px !important;
            padding: 15px 20px !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.5) !important;
            border: 1px solid #374151 !important;
            margin: 10px 0 !important;
            color: #f3f4f6 !important;
        }

        /* User message specific */
        [data-testid="chatMessage"][data-testid*="user"] {
            background: #111827 !important;
            border-left: 5px solid #00fff0 !important;
        }

        /* Assistant message specific */
        [data-testid="chatMessage"][data-testid*="assistant"] {
            background: #1f2937 !important;
            border-left: 5px solid #10b981 !important;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            border-radius: 40px !important;
            border: 1px solid #374151 !important;
            background: #111827 !important;
            box-shadow: 0 2px 8px rgba(0,255,240,0.1) !important;
        }
        [data-testid="stChatInput"] input {
            color: #f9fafb !important;
        }

        /* Sidebar elements */
        .stButton > button {
            width: 100%;
            border-radius: 40px;
            background: #1f2937;
            border: 1px solid #374151;
            color: #e5e7eb;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            border-color: #00fff0;
            background: #111827;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #4b5563;
            font-size: 0.8rem;
        }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    # Logo
    try:
        st.image("images/img.png", width=50)
    except:
        st.markdown("# 🎓")

    st.markdown("## AAU Assistant")
    st.markdown("---")

    # Theme selector
    themes = ["Dark", "Light"]
    selected_theme = st.selectbox("🎨 Theme", themes, index=themes.index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.markdown("---")

    # Clear chat button (functionality unchanged)
    if st.button("🗑 Clear Chat"):
        try:
            requests.get("https://chataau-2.onrender.com/clear_chat?session_id=user1")
        except:
            pass
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("💡 Ask anything about Addis Ababa University")

# ------------------------------
# Main Page
# ------------------------------
st.markdown("# 🎓 AAU General AI Assistant")
st.markdown(
    '<p class="subtitle">Ask anything about Addis Ababa University</p>',
    unsafe_allow_html=True
)

# ------------------------------
# Display Messages with Avatars
# ------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍🎓" if message["role"] == "user" else "🎓"):
        st.markdown(message["content"])

# ------------------------------
# Chat Input
# ------------------------------
if prompt := st.chat_input("Ask me anything about AAU..."):

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        full_response = ""

        # Show spinner while waiting for backend
        with st.spinner("Thinking..."):
            try:
                backend_url = "https://chataau-2.onrender.com/stream_answer"
                session_id = "user1"
                response = requests.get(
                    f"{backend_url}?question={prompt}&session_id={session_id}"
                )
                data = response.json()
                full_response = data["answer"]
                source = data["source"]
            except Exception:
                full_response = "⚠️ Backend server is not running."

        try:
            placeholder.markdown(f"{full_response}\n\n **source:**\n\n{source}")
        except:
            placeholder.markdown(f"{full_response}\n\n **source:**\n\nNo source")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Powered by The IS hub team • @abel • @almaw • @meron </p>",
    unsafe_allow_html=True
)