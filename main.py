import streamlit as st
import os
import importlib.util

# Set Streamlit page title
st.set_page_config(page_title="Multi-Page Streamlit App", layout="wide")

# Function to get the repository root
def get_repo_root():
    current_dir = os.path.abspath(os.getcwd())
    while not os.path.exists(os.path.join(current_dir, ".git")):
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            return os.getcwd()  # Fallback if not in a Git repo
        current_dir = parent_dir
    return current_dir

# Get repository root directory
repo_root = get_repo_root()
pages_dir = os.path.join(repo_root, "pages")

# Ensure the "pages" directory exists
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

# List Python files in the "pages" directory
page_files = [f for f in os.listdir(pages_dir) if f.endswith(".py")]

# Load selected page
page_filename = selected_page.lower().replace(" ", "_") + ".py"
page_path = os.path.join(pages_dir, page_filename)

if os.path.exists(page_path):
    spec = importlib.util.spec_from_file_location("page_module", page_path)
    page_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page_module)
else:
    st.error("Page not found!")

