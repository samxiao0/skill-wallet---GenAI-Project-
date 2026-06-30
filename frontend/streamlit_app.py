import streamlit as st
import requests
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

API_URL = "https://personalized-networking-api.onrender.com"

# --------------------------------------------------
# PDF Generator
# --------------------------------------------------

def create_pdf(topics, suggestions):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Personalized Networking Assistant Report",
            styles['Title']
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph("Detected Topics", styles['Heading2'])
    )

    for topic in topics:
        story.append(
            Paragraph(f"• {topic}", styles['BodyText'])
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Conversation Starters",
            styles['Heading2']
        )
    )

    for suggestion in suggestions:
        story.append(
            Paragraph(f"• {suggestion}", styles['BodyText'])
        )

    doc.build(story)

    buffer.seek(0)

    return buffer


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "topics" not in st.session_state:
    st.session_state.topics = []

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    color: #1e3a8a;
}

h2, h3 {
    color: #1e40af;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white !important;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#1d4ed8,#6d28d9);
    color: white !important;
}

.topic-card {
    background-color: #dbeafe;
    color: #111827 !important;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

.suggestion-card {
    background-color: #ffffff;
    color: #111827 !important;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    font-size: 16px;
    font-weight: 500;
    line-height: 1.6;
}

.fact-box {
    background-color: #fef9c3;
    color: #111827 !important;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #eab308;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤝 Personalized Networking Assistant")

st.markdown(
    "Generate personalized networking conversation starters using AI and NLP."
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("ℹ️ About")

st.sidebar.info("""
This AI assistant helps users:

✅ Analyze networking events

✅ Detect important topics

✅ Generate conversation starters

✅ Verify topics using Wikipedia

✅ Save conversation history
""")

st.sidebar.markdown("---")

st.sidebar.success(
    "Built using FastAPI + Streamlit + NLP"
)

# --------------------------------------------------
# History
# --------------------------------------------------

st.sidebar.markdown("---")

if st.sidebar.button("📜 View History"):

    try:

        response = requests.get(
            f"{API_URL}/history"
        )

        if response.status_code == 200:

            history = response.json()

            st.sidebar.subheader(
                "Recent Conversations"
            )

            if len(history) == 0:
                st.sidebar.info(
                    "No history found."
                )

            for item in reversed(history[-5:]):

                st.sidebar.markdown(
                    f"""
                    **Event:** {item['description'][:50]}...

                    **Topics:** {', '.join(item['topics'])}
                    """
                )

                st.sidebar.markdown("---")

    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# --------------------------------------------------
# User Inputs
# --------------------------------------------------

st.header("📝 Event Details")

event_description = st.text_area(
    "Event Description",
    placeholder="Example: AI conference discussing Generative AI and Cloud technologies.",
    height=150
)

interests = st.text_input(
    "Your Interests (comma separated)",
    placeholder="AI, Machine Learning, Startups"
)

# --------------------------------------------------
# Generate Suggestions
# --------------------------------------------------

if st.button("🚀 Generate Conversation Starters"):

    if not event_description or not interests:

        st.warning(
            "Please fill all fields."
        )

    else:

        payload = {
            "description": event_description,
            "interests": [
                i.strip()
                for i in interests.split(",")
            ]
        }

        with st.spinner(
            "Analyzing event and generating suggestions..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.topics = data["topics"]
                    st.session_state.suggestions = data["suggestions"]

                    st.success(
                        "Conversation suggestions generated successfully!"
                    )

                else:
                    st.error(
                        "Failed to generate suggestions."
                    )

            except Exception as e:
                st.error(f"Error: {e}")

# --------------------------------------------------
# Topics
# --------------------------------------------------

if st.session_state.topics:

    st.subheader("📌 Detected Topics")

    for topic in st.session_state.topics:

        st.markdown(
            f"""
            <div class='topic-card' style='color:#111827;'>
                📍 {topic}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# Suggestions + Feedback
# --------------------------------------------------

if st.session_state.suggestions:

    st.subheader(
        "💬 Suggested Conversation Starters"
    )

    for idx, suggestion in enumerate(
            st.session_state.suggestions):

        st.markdown(
            f"""
            <div class='suggestion-card' style='color:#111827;'>
                {suggestion}
            </div>
            """,
            unsafe_allow_html=True
)

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                    "👍 Like",
                    key=f"like_{idx}"):

                requests.post(
                    f"{API_URL}/feedback",
                    json={
                        "suggestion": suggestion,
                        "rating": "like"
                    }
                )

                st.success(
                    "Feedback saved!"
                )

        with col2:

            if st.button(
                    "👎 Dislike",
                    key=f"dislike_{idx}"):

                requests.post(
                    f"{API_URL}/feedback",
                    json={
                        "suggestion": suggestion,
                        "rating": "dislike"
                    }
                )

                st.warning(
                    "Feedback saved!"
                )

    # --------------------------------------------------
    # PDF Download
    # --------------------------------------------------

    st.markdown("---")

    st.subheader("📄 Download Report")

    pdf = create_pdf(
        st.session_state.topics,
        st.session_state.suggestions
    )

    st.download_button(
        label="📥 Download Suggestions as PDF",
        data=pdf,
        file_name="networking_suggestions.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# Fact Checker
# --------------------------------------------------

st.markdown("---")

st.header("🔎 Fact Checker")

query = st.text_input(
    "Enter a topic to verify",
    placeholder="Artificial Intelligence"
)

if st.button("✅ Fact Check"):

    if query:

        with st.spinner(
                "Verifying information..."):

            try:

                response = requests.post(
                    f"{API_URL}/fact-check",
                    json={"query": query}
                )

                if response.status_code == 200:

                    result = response.json()

                    st.subheader(
                        "📚 Verified Information"
                    )

                    st.markdown(
                        f"""
                        <div class='fact-box'>
                        {result['summary']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                    st.error(
                        "Unable to verify topic."
                    )

            except Exception as e:
                st.error(f"Error: {e}")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("""
<div class='footer'>
<hr>
Personalized Networking Assistant | Internship Project
</div>
""", unsafe_allow_html=True)
