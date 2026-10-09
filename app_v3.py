"""
GreenPow challenge: a scrolling story page (page.html) hosted in Streamlit.

Run:  pip install -r requirements.txt  &&  streamlit run app.py
Present: scroll, or use the arrow keys / Page Down / space to step through slides.

All text, numbers and design live in page.html.
"""

import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GreenPow: private AI for brain research",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
header[data-testid="stHeader"], footer, #MainMenu, [data-testid="stToolbar"] { display: none !important; }
.stApp, [data-testid="stAppViewContainer"] { background: #F3F6FA; }
.block-container, [data-testid="stMainBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
iframe { display: block; border: 0; width: 100%; }
</style>
""",
    unsafe_allow_html=True,
)

page = (pathlib.Path(__file__).parent / "page.html").read_text(encoding="utf-8")

# The page resizes its own frame to fit the content; this height is just the starting value.
components.html(page, height=5200, scrolling=False)
