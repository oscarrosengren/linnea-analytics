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

# Check if a script is selected via query parameter
params = st.query_params()  # Updated API: st.query_params() is the new method.
if "page" in params:
    script_to_run = params["page"][0]
    st.header(f"Running {script_to_run}")
    run_script(script_to_run)
else:
    st.title("Homepage")
    st.write("Select a script to run:")

    # List available scripts
    scripts = list_python_scripts(".")
    if scripts:
        for script in scripts:
            # Create a clickable link that sets a query parameter.
            st.markdown(f"[{script}](?page={script})")
    else:
        st.info("No Python scripts found in the directory.")
