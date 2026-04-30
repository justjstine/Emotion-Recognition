from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Sora:wght@400;600;700&display=swap');

            :root {
                --bg: #f7f6f2;
                --panel: #ffffff;
                --ink: #1b1f24;
                --muted: #5d6670;
                --brand: #1f7a8c;
                --brand-soft: #daf1f5;
                --accent: #ffb703;
                --danger: #d1495b;
                --radius: 18px;
            }

            html, body, .stApp {
                background:
                    radial-gradient(circle at 10% 10%, rgba(255,183,3,0.17), transparent 35%),
                    radial-gradient(circle at 85% 20%, rgba(31,122,140,0.18), transparent 30%),
                    linear-gradient(180deg, #fcfbf8 0%, #f3f6f7 100%);
                color: var(--ink);
                font-family: 'Sora', sans-serif;
            }

            .block-container {
                padding-top: 1.6rem;
                padding-bottom: 1.6rem;
                max-width: 1120px;
            }

            .app-title {
                font-family: 'Space Grotesk', sans-serif;
                font-size: clamp(1.8rem, 3vw, 2.8rem);
                font-weight: 700;
                color: var(--ink);
                margin-bottom: 0.3rem;
                letter-spacing: -0.03em;
            }

            .app-subtitle {
                color: var(--muted);
                font-size: 1.02rem;
                margin-bottom: 1.1rem;
                max-width: 760px;
            }

            .result-card {
                border-radius: var(--radius);
                padding: 1rem 1.1rem;
                background: linear-gradient(165deg, #ffffff 0%, #f7fbfc 100%);
                border: 1px solid #deebee;
                box-shadow: 0 10px 30px rgba(24, 36, 42, 0.07);
                animation: rise 420ms ease-out;
            }

            .result-chip {
                display: inline-block;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: var(--brand);
                background: var(--brand-soft);
                padding: 0.27rem 0.5rem;
                border-radius: 999px;
                margin-bottom: 0.6rem;
            }

            .result-emotion {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .result-confidence {
                color: var(--ink);
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 0.4rem;
            }

            .result-meta {
                color: var(--muted);
                font-size: 0.9rem;
            }

            .result-note {
                margin-top: 0.55rem;
                color: #3d464f;
                background: #f6f7f8;
                border-radius: 10px;
                padding: 0.5rem 0.6rem;
                font-size: 0.85rem;
            }

            @keyframes rise {
                from { transform: translateY(6px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            @media (max-width: 900px) {
                .block-container {
                    padding-top: 1rem;
                    padding-left: 0.9rem;
                    padding-right: 0.9rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
