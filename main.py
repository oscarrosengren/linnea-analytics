import streamlit as st
import os
import runpy

def run_script(script_path):
    """
    Run the given script as if it were executed as the main program.
    This allows scripts without a main() function to run.
    """
    try:
        runpy.run_path(script_path, run_name="__main__")
    except Exception as e:
        st.error(f"Error running script {script_path}: {e}")

def list_python_scripts(directory):
    """
    Return a list of Python scripts in the directory,
    excluding the current homepage file.
    """
    homepage = os.path.basename(__file__)
    return [f for f in os.listdir(directory) if f.endswith(".py") and f != homepage]

# Create a sidebar for multipage navigation.
st.sidebar.title("Multipage Navigation")
scripts = list_python_scripts(".")

if scripts:
    selected_script = st.sidebar.selectbox("Select a script to run", scripts)
    st.sidebar.write("You selected:", selected_script)
    st.header(f"Running: {selected_script}")
    run_script(selected_script)
else:
    st.sidebar.info("No Python scripts found in the directory.")
    st.title("Homepage")
    st.info("Please add more scripts to the directory to use multipage navigation.")
