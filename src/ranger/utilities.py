import subprocess

def pigpiod_running() -> bool:
    """Checks if the `pigpiod` daemon is running."""
    output:bytes = subprocess.run(["pgrep", "pigpiod"], capture_output=True).stdout
    return len(output) > 0 # if the pgrep search returned a process ID, that means it is running. If it returned nothing, that means a matching process ID wasn't found.

def start_pigpiod() -> None:
    """Attempts to start the `pigpiod` daemon by running `sudo pigpiod`."""
    subprocess.run(["sudo", "pigpiod"])

def webcam_connected() -> None:
    """Trys to determine if a USB webcam is connected, simply be seeing if any USB is connected"""
    output:bytes = subprocess.run(["lsusb"], capture_output=True).stdout
    outputs:str = output.decode()
    return outputs.count("\n") >= 2 # if there are 2 or more lines, a USB must be connected, so we'll just assume it is a webcam. if not, it is not connected
