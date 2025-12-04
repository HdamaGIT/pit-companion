# pit_companion/ui/streamlit_app.py

import pandas as pd
import streamlit as st

from pit_companion.core.service import TemperatureService
from pit_companion.hardware.probes_mock import MockProbeReader

# --- Single shared service for all sessions ---------------------------------


@st.cache_resource
def get_service() -> TemperatureService:
    reader = MockProbeReader()
    return TemperatureService(reader=reader, max_points=6 * 60)

service = get_service()


# --- Helpers -----------------------------------------------------------------


def compute_status(pit: float, meat: float, pit_target: float = 110.0, meat_done: float = 95.0) -> dict:
    """
    Very simple status logic for now. We can refine later.
    Returns dict with 'label' and 'level' in {"ok", "warn", "alert", "done"}.
    """
    status = {"label": "Running", "level": "ok"}

    # Pit too high / low
    if pit > pit_target + 15:
        status = {"label": "Pit too hot", "level": "alert"}
    elif pit > pit_target + 8:
        status = {"label": "Pit warm", "level": "warn"}
    elif pit < pit_target - 15:
        status = {"label": "Pit too cool", "level": "warn"}

    # Meat done overrides pit status
    if meat >= meat_done:
        status = {"label": "Cook finished", "level": "done"}

    return status


def status_color(level: str) -> str:
    return {
        "ok": "#1b5e20",        # green
        "warn": "#f9a825",      # amber
        "alert": "#b71c1c",     # red
        "done": "#004d40",      # teal-ish
    }.get(level, "#263238")     # default dark grey


def make_block(title: str, main: str, subtitle: str, bg: str) -> None:
    st.markdown(
        f"""
        <div style="
            padding: 1.5rem;
            border-radius: 1rem;
            background-color: {bg};
            color: white;
            text-align: center;
            min-height: 180px;
        ">
            <div style="font-size: 1.0rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 0.1em;">
                {title}
            </div>
            <div style="font-size: 3.2rem; font-weight: 700; margin-top: 0.2rem;">
                {main}
            </div>
            <div style="font-size: 1.0rem; margin-top: 0.4rem; opacity: 0.9;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- Streamlit layout --------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="Pit Companion",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Auto-refresh every 5 seconds
    st_autorefresh = st.experimental_memo(lambda: None)  # dummy to avoid linting
    st_autorefresh()
    st.experimental_rerun  # noqa: just a placeholder hint

    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0.5rem;'>Pit Companion</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; opacity: 0.7; margin-bottom: 1.5rem;'>Mock data – probes not connected</p>",
        unsafe_allow_html=True,
    )

    # Take a reading on each run
    reading = service.poll_once()
    pit = reading.values["pit"]
    meat = reading.values["meat"]

    stat = compute_status(pit, meat)
    col_pit, col_meat, col_status = st.columns(3)

    # Cook view tiles
    with col_pit:
        make_block(
            title="Pit Temp",
            main=f"{pit:.1f}°C",
            subtitle="Target ~110°C",
            bg="#37474f",
        )

    with col_meat:
        make_block(
            title="Meat Temp",
            main=f"{meat:.1f}°C",
            subtitle="Target ~95°C",
            bg="#263238",
        )

    with col_status:
        make_block(
            title="Status",
            main=stat["label"],
            subtitle="Mock cook in progress",
            bg=status_color(stat["level"]),
        )

    st.markdown("---")

    # History chart
    tab_cook, tab_charts = st.tabs(["Cook View", "Charts"])

    with tab_cook:
        st.markdown(
            "<p style='text-align: center; margin-top: 1rem;'>This is your touchscreen view. We can refine layout/colour later.</p>",
            unsafe_allow_html=True,
        )

    with tab_charts:
        st.subheader("Temperature over time (mock data)")

        pit_series = service.get_series("pit")
        meat_series = service.get_series("meat")

        if pit_series and meat_series:
            df = pd.DataFrame(
                {
                    "timestamp": [t for t, _ in pit_series],
                    "pit": [v for _, v in pit_series],
                    "meat": [v for _, v in meat_series],
                }
            ).set_index("timestamp")

            st.line_chart(df)
        else:
            st.info("No history yet – give it a minute to record some readings.")


if __name__ == "__main__":
    main()
