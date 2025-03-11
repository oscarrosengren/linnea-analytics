import streamlit as st
import os
import subprocess



# Streamlit UI
st.title("Linnea Script")

def list_python_scripts(directory):
    """
    Returns a list of Python script filenames in the given directory.
    Excludes the current file.
    """
    current_file = os.path.basename(__file__)
    return [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) 
        and f.endswith('.py') 
        and f != current_file
    ]

def run_script(script_path):
    """
    Executes the given script using subprocess and returns stdout and stderr.
    """
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(script_path)
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def main():
    st.title("Script Homepage")
    st.write("This page lists all Python scripts in the current directory and allows you to run them.")

    # Get the current directory.
    current_directory = os.path.dirname(os.path.abspath(__file__))
    st.write(f"Current directory: `{current_directory}`")

    # List Python scripts, excluding this homepage script.
    scripts = list_python_scripts(current_directory)
    
    if scripts:
        # Allow the user to select a script.
        selected_script = st.selectbox("Select a script to run", scripts)
        if st.button("Run Script"):
            st.write(f"Running `{selected_script}` ...")
            stdout, stderr = run_script(os.path.join(current_directory, selected_script))
            if stdout:
                st.subheader("Output")
                st.code(stdout)
            if stderr:
                st.subheader("Errors")
                st.code(stderr)
    else:
        st.write("No Python scripts found in this directory.")

if __name__ == "__main__":
    main()

