"""
GreenPow challenge: one Streamlit app that is both the 3-minute pitch and the prototype.

Run:  pip install -r requirements.txt  &&  streamlit run app.py
Present: use the Back / Next buttons or the left / right arrow keys.

Edit the CONFIG block below before presenting (survey result, assumptions).
"""

import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# CONFIG: edit these
# =====================================================================
SURVEY = {
    "n": None,    # e.g. 24  (number of respondents)
    "pct": None,  # e.g. 71  (percent who agreed)
    "claim": "say power or grid limits are holding back their growth",
}

# Numbers from the GreenPow CEO meeting: +8% to +16% compute from the same power.
UPLIFT_LOW = 8
UPLIFT_HIGH = 16

# Placeholders, NOT sourced. Replace with a figure you can defend.
DEFAULT_SITE_MW = 10
DEFAULT_REVENUE_PER_MW = 1_000_000   # EUR per MW per year (placeholder)
DEFAULT_SHARE_PCT = 20               # GreenPow's share of extra revenue (our proposal)

# Pilot decision thresholds (our proposal)
STOP_BELOW = 8
PAY_FROM = 12

SLIDES = ["Problem", "Solution", "Demo", "Business model", "Pilot and ask", "Backup"]

# =====================================================================
# Page setup and styling
# =====================================================================
st.set_page_config(
    page_title="GreenPow: compute without more megawatts",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
  --ink: #0B2A4A;
  --ink-soft: #4A6078;
  --paper: #F2F5F8;
  --line: #D3DCE6;
  --blue: #1F7AE0;
  --gain: #7CC62C;
  --gain-ink: #3F7A0F;
}

html, body, [class*="stApp"] { background: var(--paper); color: var(--ink); font-family: 'IBM Plex Sans', sans-serif; }
header[data-testid="stHeader"], footer, #MainMenu { display: none; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1180px; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); letter-spacing: -0.01em; }
.slide h1 { font-size: 2.6rem; line-height: 1.12; font-weight: 700; margin: 1.2rem 0 0.6rem 0; max-width: 20ch; }
.slide .lead { font-size: 1.2rem; line-height: 1.5; color: var(--ink-soft); max-width: 62ch; margin-bottom: 1.4rem; }

.stat { font-family: 'Space Grotesk', sans-serif; font-size: 6.5rem; font-weight: 700; line-height: 1; color: var(--blue); }
.stat.placeholder { color: var(--line); }
.stat-note { font-size: 1.1rem; color: var(--ink-soft); max-width: 40ch; margin-top: 0.4rem; }

.fact { border-left: 3px solid var(--blue); padding: 0.1rem 0 0.1rem 0.9rem; margin-bottom: 1rem; }
.fact b { font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; display: block; margin-bottom: 0.15rem; }
.fact span { color: var(--ink-soft); line-height: 1.45; }

.col-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.25rem; margin-bottom: 0.2rem; }
.col-body { color: var(--ink-soft); line-height: 1.45; }

.flex-row { display: grid; grid-template-columns: 11rem 1fr; gap: 0.2rem 1rem; padding: 0.7rem 0; border-top: 1px solid var(--line); }
.flex-row .tag { font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
.flex-row .tag.move { color: var(--blue); }
.flex-row .tag.wait { color: var(--gain-ink); }
.flex-row .desc { color: var(--ink-soft); line-height: 1.45; }

.tile { border-top: 3px solid var(--ink); padding-top: 0.5rem; }
.tile.gain { border-top-color: var(--gain); }
.tile .label { color: var(--ink-soft); font-size: 0.95rem; }
.tile .value { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; line-height: 1.15; }

.bmc { display: grid; grid-template-columns: repeat(10, 1fr);
  grid-template-areas:
    "kp kp ka ka vp vp cr cr cs cs"
    "kp kp kr kr vp vp ch ch cs cs"
    "co co co co co rs rs rs rs rs";
  gap: 0.5rem; margin-top: 0.8rem; }
.bmc > div { border: 1px solid var(--line); background: #fff; padding: 0.6rem 0.75rem; font-size: 0.88rem; line-height: 1.4; color: var(--ink-soft); }
.bmc > div b { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 0.98rem; color: var(--ink); margin-bottom: 0.2rem; }
.bmc .vp { background: var(--ink); color: #DCE6F1; border-color: var(--ink); }
.bmc .vp b { color: #fff; }
.bmc .rs { border-color: var(--gain); border-width: 2px; }

.verdict { font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; }
.verdict.stop { color: #B3402A; }
.verdict.go { color: var(--blue); }
.verdict.pay { color: var(--gain-ink); }

table.plain { border-collapse: collapse; width: 100%; }
table.plain td, table.plain th { text-align: left; padding: 0.5rem 0.6rem; border-top: 1px solid var(--line); vertical-align: top; }
table.plain th { font-family: 'Space Grotesk', sans-serif; color: var(--ink); }
table.plain td { color: var(--ink-soft); }

.nav-dots { display: flex; gap: 1.1rem; justify-content: center; align-items: center; padding-top: 0.5rem; font-size: 0.95rem; color: var(--ink-soft); flex-wrap: wrap; }
.nav-dots .on { color: var(--ink); font-weight: 600; border-bottom: 2px solid var(--blue); padding-bottom: 2px; }

.stButton > button { border-radius: 6px; border: 1px solid var(--ink); background: #fff; color: var(--ink); font-family: 'Space Grotesk', sans-serif; font-weight: 500; }
.stButton > button:hover { background: var(--ink); color: #fff; border-color: var(--ink); }
.stButton > button:focus-visible { outline: 3px solid var(--blue); outline-offset: 2px; }

@media (max-width: 760px) {
  .slide h1 { font-size: 1.9rem; }
  .stat { font-size: 4.5rem; }
  .flex-row { grid-template-columns: 1fr; }
  .bmc { grid-template-columns: 1fr; grid-template-areas: none; }
  .bmc > div { grid-area: auto !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =====================================================================
# Helpers
# =====================================================================
def html(s: str) -> None:
    """Render HTML without Markdown turning indented lines into code blocks."""
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def eur(x: float) -> str:
    if x >= 1_000_000:
        return f"€{x / 1_000_000:.2f}M"
    if x >= 1_000:
        return f"€{x / 1_000:.0f}k"
    return f"€{x:.0f}"


def power_bar(site_mw: float, extra_mw: float, uplift_pct: float) -> None:
    """Animated bar: existing power vs. extra compute capacity gained."""
    total = site_mw + extra_mw
    base_pct = site_mw / total * 100
    extra_pct = 100 - base_pct
    template = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400&display=swap');
body { margin: 0; font-family: 'IBM Plex Sans', sans-serif; color: #0B2A4A; background: transparent; }
.top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; gap: 12px; flex-wrap: wrap; }
.left { font-size: 15px; color: #4A6078; }
.right { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 34px; color: #3F7A0F; }
.right small { font-size: 15px; font-weight: 500; color: #4A6078; }
.bar { display: flex; height: 54px; border-radius: 6px; overflow: hidden; background: #DDE5EE; }
.base { background: #0B2A4A; width: __BASE__%; }
.extra { background: #7CC62C; width: 0%; transition: width 1.1s cubic-bezier(.2,.8,.2,1); }
.under { margin-top: 8px; font-size: 14px; color: #4A6078; }
@media (prefers-reduced-motion: reduce) { .extra { transition: none; } }
</style>
<div class="top">
  <div class="left">Same grid connection: __SITE__ MW</div>
  <div class="right">+<span id="n">0.0</span> MW <small>more compute (+__UP__%)</small></div>
</div>
<div class="bar"><div class="base"></div><div class="extra" id="e"></div></div>
<div class="under">Dark: power the site already has. Green: extra compute capacity from orchestration.</div>
<script>
const target = __EXTRA__, dur = 1100, el = document.getElementById('n');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
requestAnimationFrame(() => { document.getElementById('e').style.width = '__EXTRAPCT__%'; });
if (reduce) { el.textContent = target.toFixed(1); }
else {
  const t0 = performance.now();
  (function tick(t) {
    const p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
    el.textContent = (target * eased).toFixed(1);
    if (p < 1) requestAnimationFrame(tick);
  })(t0);
}
</script>
"""
    out = (template.replace("__BASE__", f"{base_pct:.2f}")
                   .replace("__SITE__", f"{site_mw:g}")
                   .replace("__UP__", f"{uplift_pct:g}")
                   .replace("__EXTRA__", f"{extra_mw:.3f}")
                   .replace("__EXTRAPCT__", f"{extra_pct:.2f}"))
    components.html(out, height=140)


def go(delta: int) -> None:
    st.session_state.slide = max(0, min(len(SLIDES) - 1, st.session_state.slide + delta))


# =====================================================================
# Slides
# =====================================================================
def slide_problem() -> None:
    left, right = st.columns([3, 2], gap="large")
    with left:
        html("""
        <div class="slide">
        <h1>Data centers can't get the power they need to grow.</h1>
        <p class="lead">AI demand keeps rising. Grid capacity in cities like Berlin and Stockholm does not, and some new data centers are being blocked by public backlash.</p>
        </div>
        """)
        html("""
        <div class="fact"><b>Who pays</b><span>The data center operator, who carries the energy bill. Not the building owner.</span></div>
        <div class="fact"><b>The constraint</b><span>The site has no spare megawatts, so it can't sell more compute.</span></div>
        <div class="fact"><b>Today's alternative</b><span>Wait for a grid upgrade, or build a new site.</span></div>
        """)
    with right:
        if SURVEY["pct"] is None:
            html("""
            <div class="stat placeholder">?%</div>
            <div class="stat-note">Add the survey result to SURVEY at the top of app.py.</div>
            """)
        else:
            n_txt = f" (n={SURVEY['n']})" if SURVEY["n"] else ""
            html(f"""
            <div class="stat">{SURVEY['pct']}%</div>
            <div class="stat-note">{SURVEY['claim']}{n_txt}.</div>
            """)


def slide_solution() -> None:
    html("""
    <div class="slide">
    <h1>GreenPow moves flexible compute across time and sites.</h1>
    <p class="lead">An orchestration layer that plugs into the operator's existing setup. Unlike Google's internal system or a GPU marketplace, GreenPow sells it as a service.</p>
    </div>
    """)
    c1, c2, c3 = st.columns(3, gap="large")
    c1.markdown('<div class="col-title">Signals</div><div class="col-body">Energy availability, electricity cost, compute capacity and infrastructure availability.</div>', unsafe_allow_html=True)
    c2.markdown('<div class="col-title">Guardrails</div><div class="col-body">Performance, latency, availability, security, data sovereignty and operating policies.</div>', unsafe_allow_html=True)
    c3.markdown('<div class="col-title">Orchestration</div><div class="col-body">Eligible workloads shift across time, approved locations and compatible infrastructure. Batteries buffer energy peaks.</div>', unsafe_allow_html=True)
    st.write("")
    html("""
    <div class="flex-row"><div class="tag">Runs now</div><div class="desc">Latency-critical tenant workloads. They stay exactly where they are.</div></div>
    <div class="flex-row"><div class="tag wait">Can wait</div><div class="desc">Batch AI training and batch inference. Scheduled for when energy and capacity allow.</div></div>
    <div class="flex-row"><div class="tag move">Can move</div><div class="desc">The same batch jobs, offloaded to other sites or public clouds when this site is full.</div></div>
    <div class="flex-row"><div class="tag">Stays fixed</div><div class="desc">Tenants with data sovereignty or strict region requirements.</div></div>
    """)
    st.caption("Replace these examples with the common workload examples from the challenge sheet if you have them.")


def slide_demo() -> None:
    html('<div class="slide"><h1>What more compute is worth to one operator.</h1></div>')
    ctrl, out = st.columns([2, 3], gap="large")
    with ctrl:
        site_mw = st.slider("Site size (MW)", 1, 50, DEFAULT_SITE_MW, key="site_mw")
        scenario = st.radio(
            "Uplift scenario",
            [f"Conservative ({UPLIFT_LOW}%)", f"GreenPow case ({UPLIFT_HIGH}%)", "Custom"],
            index=1, horizontal=True, key="scenario",
        )
        if scenario.startswith("Conservative"):
            uplift = UPLIFT_LOW
        elif scenario.startswith("GreenPow"):
            uplift = UPLIFT_HIGH
        else:
            uplift = st.slider("Custom uplift (%)", 0, 25, 12, key="custom_uplift")
        rev = st.number_input(
            "Revenue per MW per year (EUR, placeholder)", min_value=0,
            value=DEFAULT_REVENUE_PER_MW, step=50_000, key="rev",
        )
        share = st.slider("GreenPow share of extra revenue (%)", 0, 50, DEFAULT_SHARE_PCT, key="share")

    extra_mw = site_mw * uplift / 100
    gain = extra_mw * rev
    gp_rev = gain * share / 100
    keep = gain - gp_rev
    sites_for_1m = (1_000_000 / gp_rev) if gp_rev > 0 else None

    with out:
        power_bar(site_mw, extra_mw, uplift)
        t1, t2, t3 = st.columns(3)
        t1.markdown(f'<div class="tile gain"><div class="label">Extra revenue for the operator</div><div class="value">{eur(gain)}/yr</div></div>', unsafe_allow_html=True)
        t2.markdown(f'<div class="tile"><div class="label">Operator keeps</div><div class="value">{eur(keep)}/yr</div></div>', unsafe_allow_html=True)
        t3.markdown(f'<div class="tile"><div class="label">GreenPow earns</div><div class="value">{eur(gp_rev)}/yr</div></div>', unsafe_allow_html=True)
        st.write("")
        if sites_for_1m:
            st.markdown(f"At this setup, about **{sites_for_1m:.0f} sites** would give GreenPow €1M a year.")
    st.caption(
        "Uplift range from the GreenPow CEO (+8% to +16% compute from the same power). "
        "Revenue per MW and GreenPow's share are our assumptions, not sourced figures."
    )


def slide_model() -> None:
    html("""
    <div class="slide"><h1>GreenPow only earns when the operator gains.</h1></div>
    <div class="bmc">
      <div style="grid-area:kp"><b>Key partners</b>Data center management (DCIM) software vendors. Battery and energy storage providers. Public and private clouds for offload.</div>
      <div style="grid-area:ka"><b>Key activities</b>Tune orchestration per site. Forecast energy peaks. Integrate and monitor.</div>
      <div style="grid-area:kr"><b>Key resources</b>Orchestration engine. Leased bare-metal servers and private cloud. Energy and workload data.</div>
      <div class="vp" style="grid-area:vp"><b>Value proposition</b>Up to 16% more compute from the power the site already has. No change to the operator's setup.</div>
      <div style="grid-area:cr"><b>Customer relationships</b>Pilot first, then a managed service that keeps optimizing.</div>
      <div style="grid-area:ch"><b>Channels</b>Direct to operators. Pilot group of data centers. DCIM partners.</div>
      <div style="grid-area:cs"><b>Customer segments</b>Power-constrained colocation and bare-metal operators first. Enterprises and governments later.</div>
      <div style="grid-area:co"><b>Cost structure</b>Leased servers. Engineering and integration. Energy data. Battery partner costs.</div>
      <div class="rs" style="grid-area:rs"><b>Revenue streams</b>A share of the extra capacity revenue. Optional fee per managed MW.</div>
    </div>
    """)
    st.write("")
    st.markdown(
        "**Where it scales:** enterprises are the entry wedge, since once GreenPow runs the compute it keeps optimizing it. "
        "Governments follow, because they want to avoid new grid lines and transformers (for example Watt-Bit in Japan)."
    )


def slide_pilot() -> None:
    html("""
    <div class="slide">
    <h1>One site, 8 to 12 weeks, one metric.</h1>
    <p class="lead">Hypothesis: orchestration gives this operator between 8% and 16% more compute from the same power.</p>
    </div>
    """)
    left, right = st.columns([3, 2], gap="large")
    with left:
        html(f"""
        <table class="plain">
        <tr><th>Pilot customer</th><td>One power-constrained operator, ideally from GreenPow's current data center pilot group.</td></tr>
        <tr><th>Information needed</th><td>Site power allocation, tenant workload mix, share of batch work, energy prices.</td></tr>
        <tr><th>Key metric</th><td>Extra compute per MW compared with the baseline.</td></tr>
        <tr><th>Decision</th><td>Below {STOP_BELOW}%: stop. {STOP_BELOW}% to {PAY_FROM}%: continue. {PAY_FROM}% or more: operator pays.</td></tr>
        </table>
        """)
        st.write("")
        st.markdown("**The ask:** an introduction to one operator in GreenPow's pilot group.")
    with right:
        measured = st.slider("Try it: measured uplift (%)", 0, 20, 10, key="measured")
        if measured < STOP_BELOW:
            html('<div class="verdict stop">Stop</div>')
        elif measured < PAY_FROM:
            html('<div class="verdict go">Continue the pilot</div>')
        else:
            html('<div class="verdict pay">Operator pays</div>')
        st.caption("Thresholds are our proposal.")


def slide_backup() -> None:
    html("""
    <div class="slide"><h1>Backup: assumptions and competitors.</h1></div>
    <table class="plain">
    <tr><th>Assumption</th><th>Value</th><th>Source</th></tr>
    <tr><td>Compute gain, data centers</td><td>+8% to +16% (use 16%)</td><td>GreenPow CEO meeting. A 10 MW site gains the equivalent of 1.6 MW.</td></tr>
    <tr><td>Revenue per MW per year</td><td>Placeholder</td><td>Our assumption. Replace with a sourced figure.</td></tr>
    <tr><td>GreenPow revenue share</td><td>20%</td><td>Our proposal, to validate.</td></tr>
    <tr><td>Pilot thresholds</td><td>Stop below 8%, pay from 12%</td><td>Our proposal.</td></tr>
    </table>
    """)
    st.write("")
    html("""
    <table class="plain">
    <tr><th>Competitor</th><th>What they do</th><th>Difference from GreenPow</th></tr>
    <tr><td>Emerald AI</td><td>Optimizes energy between the grid and AI factories</td><td>Doesn't move compute between sites</td></tr>
    <tr><td>Verda</td><td>GPU marketplace</td><td>Doesn't orchestrate across hybrid infrastructure</td></tr>
    <tr><td>Google</td><td>Orchestration across its own data centers</td><td>Internal only. GreenPow sells it as a service.</td></tr>
    </table>
    """)


RENDER = [slide_problem, slide_solution, slide_demo, slide_model, slide_pilot, slide_backup]

# =====================================================================
# Navigation and main
# =====================================================================
if "slide" not in st.session_state:
    st.session_state.slide = 0

cur = st.session_state.slide
b1, mid, b2 = st.columns([1, 8, 1])
b1.button("Back", on_click=go, args=(-1,), key="nav_back", disabled=cur == 0, use_container_width=True)
dots = " ".join(
    f'<span class="{"on" if i == cur else ""}">{name}</span>' for i, name in enumerate(SLIDES)
)
mid.markdown(f'<div class="nav-dots">{dots}</div>', unsafe_allow_html=True)
b2.button("Next", on_click=go, args=(1,), key="nav_next", disabled=cur == len(SLIDES) - 1, use_container_width=True)

RENDER[cur]()

# Arrow-key navigation (ignored while a slider or input has focus).
components.html(
    """
<script>
const doc = window.parent.document;
if (!window.parent.__gpKeys) {
  window.parent.__gpKeys = true;
  doc.addEventListener('keydown', (e) => {
    const t = e.target;
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.getAttribute('role') === 'slider') return;
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const label = e.key === 'ArrowRight' ? 'Next' : 'Back';
    const btn = [...doc.querySelectorAll('button')].find(b => b.innerText.trim() === label);
    if (btn && !btn.disabled) btn.click();
  });
}
</script>
""",
    height=0,
)
