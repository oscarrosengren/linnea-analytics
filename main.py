import streamlit as st
import os
import shutil

st.set_page_config(page_title="📜 Script Launcher", layout="wide")

st.title("📜 Script Launcher")

repo_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current repo
pages_dir = os.path.join(repo_dir, "pages")  # Directory for Streamlit pages

# Ensure the "pages" directory exists
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

def get_python_scripts(directory):
    """Returns a list of Python script filenames in the given directory (excluding itself)."""
    return [f for f in os.listdir(directory) if f.endswith(".py") and f != "app.py"]

scripts = get_python_scripts(repo_dir)

# Generate pages dynamically
for script in scripts:
    script_path = os.path.join(repo_dir, script)
    page_path = os.path.join(pages_dir, script)

    # Copy each script into the "pages" directory so Streamlit treats them as separate pages
    shutil.copy(script_path, page_path)

st.success(f"📄 {len(scripts)} script pages created! Check the sidebar to navigate.")

st.write("Select a script from the sidebar to execute.")
