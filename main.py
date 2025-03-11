import streamlit as st
import os
import importlib.util

def run_script(script_path):
    """Dynamically load and run a script that defines a main() function."""
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "main"):
        module.main()
    else:
        st.error(f"Script {script_path} has no main() function to run.")

def list_python_scripts(directory):
    """Return a list of Python scripts in the directory, excluding the homepage."""
    homepage = os.path.basename(__file__)
    return [f for f in os.listdir(directory) 
            if f.endswith(".py") and f != homepage]

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
