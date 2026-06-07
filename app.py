import streamlit as st

from utils.page_helpers import initialize_session_state
from utils.theme import apply_global_theme, render_footer, render_navigation_sidebar, render_navigation_tutorial


def render_main_page() -> None:
    st.markdown(
        """
        <div class="hero-shell">
            <div>
                <div class="hero-kicker">Statistical Computing Environment</div>
                <div class="hero-title">Data Analysis Toolkit</div>
                <div class="hero-meta">
                    <p>
                        One single place to explore, test and create reports on your data.
                        Upload a dataset, run statistical tests, visualise distributions,
                        and export a full PDF report.
                    </p>
                    <div class="hero-stats">
                        <div class="hero-stat"><span class="hero-stat-num">12</span><span class="hero-stat-label">Modules</span></div>
                        <div class="hero-stat"><span class="hero-stat-num">9</span><span class="hero-stat-label">Test types</span></div>
                        <div class="hero-stat"><span class="hero-stat-num">3</span><span class="hero-stat-label">Distributions</span></div>
                        <div class="hero-stat"><span class="hero-stat-num">PDF</span><span class="hero-stat-label">Export</span></div>
                    </div>
                    <div class="hero-creator">Created by &nbsp;<span>Joel Payyappilly Elias</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_navigation_tutorial()
    render_footer()


def main() -> None:
    st.set_page_config(
        page_title="Main",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_session_state()
    apply_global_theme()
    render_navigation_sidebar("Main")
    render_main_page()


if __name__ == "__main__":
    main()