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
    # Additional app-specific styles (moved from app.py)
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Source+Sans+3:wght@400;600&display=swap');

        :root {
            --ink: #0f172a;
            --muted: #64748b;
            --bg: #f5f3ee;
            --panel: #ffffff;
            --shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
            --accent: #0ea5e9;
            --happy: #10b981;
            --angry: #ef4444;
            --surprised: #f59e0b;
        }

        .stApp {
            background: radial-gradient(1200px 700px at 15% 0%, #fff8e6 0%, var(--bg) 55%, #eef2ff 100%);
            color: var(--ink);
            font-family: 'Source Sans 3', sans-serif;
        }

        .app-shell {
            max-width: 1100px;
            margin: 0 auto;
            padding: 12px 0 28px 0;
        }

        .title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: clamp(2.1rem, 3.2vw, 3.2rem);
            letter-spacing: -0.02em;
            text-align: center;
            margin-bottom: 6px;
        }

        .subtitle {
            text-align: center;
            color: var(--muted);
            font-size: 1.05rem;
            margin-bottom: 18px;
        }

        .instruction {
            text-align: center;
            color: var(--muted);
            font-size: 0.95rem;
            margin-bottom: 18px;
        }

        .capture-panel {
            background: var(--panel);
            border-radius: 22px;
            box-shadow: var(--shadow);
            padding: 18px;
            animation: fadeUp 600ms ease;
        }

        .result-panel {
            border-radius: 22px;
            padding: 18px;
            min-height: 120px;
            box-shadow: var(--shadow);
            animation: fadeUp 700ms ease;
        }

        .result-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 10px;
        }

        .result-emoji {
            font-size: 2.8rem;
            margin-right: 8px;
        }

        .result-main {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .result-confidence {
            font-size: 1.05rem;
            color: rgba(15, 23, 42, 0.8);
            margin-top: 6px;
        }

        .result-note {
            color: var(--muted);
            margin-top: 10px;
            font-size: 0.95rem;
        }

        .upload-hint {
            text-align: center;
            color: var(--muted);
            font-size: 0.95rem;
            margin-top: 8px;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        section[data-testid="stFileUploader"] {
            padding: 10px 0 2px 0;
        }

        section[data-testid="stCameraInput"] {
            padding: 12px 0 2px 0;
        }

        section[data-testid="stCameraInput"] label {
            font-weight: 700;
        }

        button[kind="secondary"] {
            border-radius: 12px;
        }

        .st-emotion-cache-1v0mbdj img {
            border-radius: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
