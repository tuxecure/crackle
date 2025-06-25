# made by ChromiumOS-Guy (https://github.com/ChromiumOS-Guy)

import subprocess, time, threading, sys
from threading import Thread

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
#### START Spinner ####
class Spinner:
    def __init__(self, label="Processing", done_msg=""):
        self.label = label
        self.done_msg = done_msg
        self._spinning = False
        self._thread = None

    def _spin(self):
        spinner_cycle = ['/', '-', '\\', '|']
        while self._spinning:
            for symbol in spinner_cycle:
                if not self._spinning:
                    break
                sys.stdout.write(f'\r{self.label}... {symbol}')
                sys.stdout.flush()
                time.sleep(0.1)
        sys.stdout.write(f'\r{self.label}... {self.done_msg}')
        sys.stdout.flush()

    def __enter__(self):
        self._spinning = True
        self._thread = Thread(target=self._spin)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._spinning = False
        self._thread.join()
#### END Spinner ####
