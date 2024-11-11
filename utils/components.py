import streamlit as st


def confirm_dialog(message: str, key: str) -> bool:
    """Show a confirmation dialog"""
    col1, col2 = st.columns([1, 3])

    with col1:
        confirm = st.button("Confirm", key=f"confirm_{key}")
    with col2:
        st.markdown(f"**{message}**")

    return confirm


def card(content: str, key: str = None):
    """Display content in a styled card container"""
    styles = """
        <style>
            .stCard {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    """

    st.markdown(styles, unsafe_allow_html=True)
    st.markdown(f'<div class="stCard">{content}</div>', unsafe_allow_html=True)
