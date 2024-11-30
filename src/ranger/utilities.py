import subprocess

def pigpiod_running() -> bool:
    """Checks if the `pigpiod` daemon is running."""
    output:bytes = subprocess.run(["pgrep", "pigpiod"], capture_output=True).stdout
    return len(output) > 0 # if the pgrep search returned a process ID, that means it is running. If it returned nothing, that means a matching process ID wasn't found.

def start_pigpiod() -> None:
    """Attempts to start the `pigpiod` daemon by running `sudo pigpiod`."""
    subprocess.run(["sudo", "pigpiod"])