import streamlit as st
import os
import subprocess

def get_python_scripts(directory):
    """Returns a list of Python script filenames in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith(".py") and f != os.path.basename(__file__)]

def run_script(script_name):
    """Executes a selected Python script."""
    try:
        result = subprocess.run(["python", script_name], capture_output=True, text=True)
        st.text_area("Output:", result.stdout + result.stderr, height=300)
    except Exception as e:
        st.error(f"Error running script: {e}")

# Streamlit UI
st.title("📜 Script Launcher")

repo_dir = os.path.dirname(os.path.abspath(__file__))
scripts = get_python_scripts(repo_dir)
