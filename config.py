import streamlit as st
from pathlib import Path
import toml


def setup_page_config():
    """Configure basic Streamlit page settings"""
    st.set_page_config(
        page_title="AI Code Challenge Generator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_custom_css():
    """Load custom CSS styles"""
    custom_css = """
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .stTitle {
            color: #0f4c81;
            font-size: 2.5rem !important;
            padding-bottom: 2rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f1f3f6;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 1rem;
            font-family: 'Courier New', monospace;
        }
        
        /* Code block styling */
        .stCodeBlock {
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #c3e6cb;
        }
        
        /* Error message styling */
        .stError {
            background-color: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #f5c6cb;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: #0f4c81;
        }
        
        /* Multiselect styling */
        .stMultiSelect {
            border-radius: 8px;
        }
        
        /* Spinner styling */
        .stSpinner > div {
            border-color: #0f4c81;
        }
        
        /* Section headers */
        h3 {
            color: #0f4c81;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e0e0e0;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def create_config():
    """Create default Streamlit config file if it doesn't exist"""
    config_path = Path.home() / ".streamlit/config.toml"
    config_path.parent.mkdir(exist_ok=True)

    if not config_path.exists():
        config = {
            "theme": {
                "primaryColor": "#0f4c81",
                "backgroundColor": "#ffffff",
                "secondaryBackgroundColor": "#f1f3f6",
                "textColor": "#31333F",
                "font": "sans serif",
            },
            "server": {
                "maxUploadSize": 5,
                "enableXsrfProtection": True,
                "enableCORS": False,
            },
        }

        with open(config_path, "w") as f:
            toml.dump(config, f)


def setup_streamlit():
    """Main function to set up Streamlit configuration"""
    setup_page_config()
    load_custom_css()
    create_config()


if __name__ == "__main__":
    setup_streamlit()
