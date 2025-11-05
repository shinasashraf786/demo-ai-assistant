# Copyright 2025
# HR Shortlister Streamlit Application

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# -------------------------------------------------
# Environment Setup
# -------------------------------------------------

# Load environment variables from .env
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use your assistant ID
ASSISTANT_ID = "asst_bBLvW1TIJ2lBYTjCYlfftrhu"

# Streamlit configuration
st.set_page_config(page_title="HR Shortlister", page_icon="🤖")

# -------------------------------------------------
# App Header
# -------------------------------------------------

st.title("HR Shortlister 🤖")
st.caption("Use this assistant to evaluate and shortlist job candidates efficiently.")

st.markdown("""
This tool connects to your **OpenAI Assistant** to help review candidate resumes,
generate shortlist recommendations, and assist with HR decision support.
""")

# -------------------------------------------------
# Input Area
# -------------------------------------------------

st.subheader("Enter Candidate Query")
user_input = st.text_area(
    "Example: Evaluate John's resume for a marketing role, or shortlist candidates for a data analyst position."
)

# -------------------------------------------------
# Process Query
# -------------------------------------------------

if st.button("Ask HR Shortlister"):
    if not user_input.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Analyzing candidate data..."):
            try:
                # Create a new thread for conversation
                thread = client.beta.threads.create()

                # Add user message
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_input
                )

                # Run the assistant
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=ASSISTANT_ID
                )

                # Wait until the assistant completes
                while True:
                    status = client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                    if status.status == "completed":
                        break
                    time.sleep(1)

                # Fetch response
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                reply = messages.data[0].content[0].text.value

                # Display assistant reply
                st.subheader("HR Shortlister’s Response:")
                st.write(reply)

            except Exception as e:
                st.error(f"An error occurred: {e}")

# -------------------------------------------------
# Sidebar Information
# -------------------------------------------------

st.sidebar.header("About HR Shortlister")
st.sidebar.write("""
**HR Shortlister** uses OpenAI's API to provide intelligent support for candidate evaluations.

You can:
- Analyse resumes or candidate summaries.
- Generate shortlist recommendations.
- Draft hiring feedback or evaluation criteria.
""")

st.sidebar.divider()

st.sidebar.header("Tips for Best Results")
st.sidebar.write("""
- Use clear role descriptions.
- Provide relevant candidate details.
- Ask specific, measurable questions.
""")

st.sidebar.divider()
st.sidebar.caption("Built with ❤️ using Streamlit and OpenAI.")
