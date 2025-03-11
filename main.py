import streamlit as st
import os
import subprocess



# Streamlit UI
st.title("Linnea Script")
 
 repo_dir = os.path.dirname(os.path.abspath(__file__))
 scripts = get_python_scripts(repo_dir)
