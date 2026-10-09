"""
GreenPow challenge: a 3-minute pitch deck (page.html) hosted in Streamlit.

Run:  pip install -r requirements.txt  &&  streamlit run app.py
Present: arrow keys / space / Page Down for the next slide, arrow left / Page Up to go back,
mouse wheel or swipe also work, and the dots at the bottom jump to a slide.

All text, numbers and design live in page.html.
"""

import base64
import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GreenPow for Estonian health AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
header[data-testid="stHeader"], footer, #MainMenu, [data-testid="stToolbar"] { display: none !important; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #F3F6FA; overflow: hidden !important; }
.block-container, [data-testid="stMainBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
/* The deck fills the whole window, so the page itself never scrolls. */
iframe { position: fixed !important; top: 0; left: 0; width: 100vw !important; height: 100vh !important; border: 0; z-index: 999; }
</style>
""",
    unsafe_allow_html=True,
)

project_dir = pathlib.Path(__file__).parent
page = (project_dir / "page.html").read_text(encoding="utf-8")
logo = base64.b64encode((project_dir / "logo.png").read_bytes()).decode("ascii")
page = page.replace('src="logo.png"', f'src="data:image/png;base64,{logo}"')

components.html(page, height=600, scrolling=False)
