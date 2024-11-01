import streamlit as st


def confirm_dialog(message: str, key: str) -> bool:
    """Show a confirmation dialog"""
    col1, col2 = st.columns([1, 3])

    with col1:
        confirm = st.button("Confirm", key=f"confirm_{key}")
    with col2:
        st.markdown(f"**{message}**")

    return confirm
