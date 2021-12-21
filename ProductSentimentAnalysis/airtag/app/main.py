# import streamlit.cli
from app.src.launch import app

if __name__ == "__main__":
    # streamlit.cli._main_run_clExplicit("./src/launch.py", "streamlit run")
    app.run()
