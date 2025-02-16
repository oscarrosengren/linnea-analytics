import streamlit as st
import os
import subprocess

def get_python_scripts(directory):
    """Returns a list of Python script filenames in the given directory, excluding the main script."""
    main_script = os.path.basename(__file__)
    excluded_files = [main_script, "main.py", "app.py"]  # Ensure main script and known entry points are excluded
    return [f for f in os.listdir(directory) if f.endswith(".py") and f not in excluded_files]

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

if not scripts:
    st.warning("No Python scripts found in the repository.")
else:
    selected_script = st.selectbox("Select a script to run:", scripts)
    if st.button("Run Script"):
        run_script(selected_script)
