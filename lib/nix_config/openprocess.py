# made by ChromiumOS-Guy (https://github.com/ChromiumOS-Guy)

import subprocess

#### START openprocess ####

def openprocess(command : str) -> tuple:
    """
    Opens a subprocess.

    Args:
        command (str): the command for subprocess to run.

    Returns:
        tuple: output of command if there is any, and errors of command if there is any.

    Raises:
        Exception: If any other unexpected error occurs during package extraction.
    """
    
    output_lines = []
    error_lines = []
    process = None # Initialize process to None
    try:
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Decode output as text
            bufsize=1,  # Line-buffered output
            universal_newlines=True # Ensure consistent newline handling
        )

        # Read the output line by line
        for line in process.stdout:
            output_lines.append(line.strip()) # .strip() removes leading/trailing whitespace, including newlines
        
        for line in process.stderr:
            error_lines.append(line.strip()) # .strip() removes leading/trailing whitespace, including newlines

        # Wait for the process to complete and get the return code
        process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if process and process.poll() is None:  # Check if the process is still running
            print("Killing process...")
            process.terminate()  # Send a terminate signal
            try:
                process.wait(timeout=5)  # Wait for the process to terminate
            except subprocess.TimeoutExpired:
                print("Process did not terminate gracefully, killing it.")
                process.kill()  # Force kill if termination fails
    return output_lines, error_lines

#### END openprocess ####