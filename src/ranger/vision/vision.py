# This command will turn the webcam on and capture a JPG image of size 160x120 every 10 seconds (0.1 fps) and save it as frame_0001.jpg, frame_0002.jpg, etc.
# ffmpeg -video_size 160x120 -i /dev/video0 -vf fps=0.1 ./frame_%04d.jpg

# This command will do the same, but will save it as "capture.jpg" each time, always overwriting (hence the "-update 1", giving it permission to always overwrite)
# ffmpeg -video_size 160x120 -i /dev/video0 -vf fps=0.1 -update 1 capture.jpg

import subprocess
import os

class VisionCaptureService:
    """In the sense of the `VisionCaptureSevice` class, 'streaming' means using ffmpeg to periodically (i.e. once every 10 seconds) capture a photo and save it to the same name. Allowing the program to read this saved file and report it as the most recent image."""

    def __init__(self):
        self.p = None
        self._save_to:str = "./WorkingDirectory/capture.jpg" # the path where the captured image file will be saved to, read from.

    def start_streaming(self) -> None:
        """If streaming has not already started, begins streaming."""
        dir:str = os.path.dirname(self._save_to) # gets all the directories, but just excludes the file name
        os.makedirs(dir, exist_ok=True) # creates the full directory build out... 1 dir, 2 dir, etc. All made. We have to do this so ffmpeg can plop the file in there.
        if self.streaming() == False:
            self.p:subprocess.Popen = subprocess.Popen(['ffmpeg', '-video_size', '160x120', '-i', '/dev/video0', '-vf', 'fps=1', '-update', '1', self._save_to], stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    def streaming(self) -> bool:
        """Checks if the stream is still going"""
        if self.p == None:
            return False
        else:
            return self.p.poll() == None # if poll returns none, it is still going. If it returns a status code, it is finished.

    def stop_streaming(self) -> None:
        """If the stream is still going, stops it."""
        if self.streaming() == True:
            self.p.kill() # kill the process (stops ffmpeg)
            if self.p.poll() != None:
                raise Exception("ffmpeg stream process failed to shut down!")
            self.p = None

    def latest_image(self) -> bytes:
        """Gets the bytes of the latest image"""
        if os.path.exists(self._save_to) == False:
            raise Exception("Unable to get latest image: file '" + self._save_to + "' does not exist! It is possible the FFMPEG streaming process is no longer working, has been turned off, or it is still running but not enough time has elapsed for it to grab the next photo and save it.")
        f = open(self._save_to, "rb")
        data:bytes = f.read()
        f.close()
        os.remove(self._save_to)
        return data
