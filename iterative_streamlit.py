import streamlit as st
from iterative_tools import app

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="LinkedIn AI Writer",
    page_icon="✍️",
    layout="wide",
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main{
    padding-top:2rem;
}

.block-container{
    max-width:1100px;
}

.title{
    font-size:42px;
    font-weight:700;
}

.subtitle{
    color:#808080;
    margin-bottom:30px;
}

div[data-testid="stTextArea"] textarea{
    font-size:16px;
}

.stButton>button{
    width:100%;
    height:50px;
    font-size:18px;
    border-radius:12px;
}

.resultBox{
    background:#f5f7fb;
    padding:20px;
    border-radius:12px;
    border:1px solid #ddd;
}

.reviewBox{
    background:#eef8ff;
    padding:15px;
    border-radius:12px;
    border-left:6px solid #1f77b4;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(
"""
<div class="title">
✍️ LinkedIn AI Post Generator
</div>

<div class="subtitle">
Generate → Review → Improve automatically using LangGraph
</div>
""",
unsafe_allow_html=True)

# =========================
# INPUT
# =========================
topic = st.text_input(
    "Enter your LinkedIn topic",
    placeholder="Example: AI Agents replacing SaaS..."
)

generate = st.button("🚀 Generate Post")

# =========================
# GENERATE
# =========================
if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    progress = st.progress(0)

    status = st.empty()

    status.info("Initializing Agent...")
    progress.progress(10)

    initial_state = {
        "topic": topic,
        "messages": [],
        "draft": "",
        "review_feedback": "",
        "is_approved": False,
        "attempt": 0,
    }

    status.info("Writer Agent is generating...")
    progress.progress(35)

    final_state = app.invoke(initial_state)

    progress.progress(100)
    status.success("Completed!")

    draft = final_state["draft"]
    feedback = final_state["review_feedback"]
    attempts = final_state["attempt"]
    approved = final_state["is_approved"]

    st.divider()

    col1, col2 = st.columns([3,1])

    with col1:

        st.subheader("📄 Final LinkedIn Post")

        st.text_area(
            "",
            value=draft,
            height=400
        )

        st.download_button(
            "📥 Download Post",
            draft,
            file_name="linkedin_post.txt"
        )

    with col2:

        st.metric(
            "Attempts",
            attempts
        )

        if approved:
            st.success("✅ Approved")
        else:
            st.error("❌ Not Approved")

        st.markdown("### Reviewer Feedback")

        st.info(feedback)