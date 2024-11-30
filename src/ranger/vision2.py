# This command will turn the webcam on and capture a JPG image of size 160x120 every 10 seconds (0.1 fps) and save it as frame_0001.jpg, frame_0002.jpg, etc.
# ffmpeg -video_size 160x120 -i /dev/video0 -vf fps=0.1 ./frame_%04d.jpg

# This command will do the same, but will save it as "capture.jpg" each time, always overwriting (hence the "-update 1", giving it permission to always overwrite)
# ffmpeg -video_size 160x120 -i /dev/video0 -vf fps=0.1 -update 1 capture.jpg

import subprocess

class VisionCaptureStream:

    def __init__(self):
        self.p = None

    def start_streaming(self) -> None:
        self.p:subprocess.Popen = subprocess.Popen(['ffmpeg', '-video_size', '160x120', '-i', '/dev/video0', '-vf', 'fps=0.1', '-update', '1', './capture.jpg'], stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    def stop_streaming(self) -> None:
        self.p.kill() # kill the process (stops ffmpeg)
        self.p = None