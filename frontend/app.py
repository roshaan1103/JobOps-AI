import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000",
)


st.set_page_config(
    page_title="JobOps AI",
    page_icon="💼",
    layout="wide",
)


st.title("JobOps AI")

st.subheader("AI-Powered Job Search & Application Automation")

st.write(
    """
    JobOps AI is being built as a local-first platform for
    intelligent job discovery, matching, resume customization,
    application preparation, and workflow automation.
    """
)


st.divider()

st.subheader("System Status")


if st.button("Check Backend"):

    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5,
        )

        if response.ok:
            data = response.json()

            st.success("Backend is reachable.")

            st.json(data)

        else:
            st.error(
                f"Backend returned HTTP {response.status_code}."
            )

    except requests.RequestException as exc:

        st.error(
            f"Could not connect to backend: {exc}"
        )


st.divider()

st.caption(
    "Phase 1 — Engineering Foundation"
)