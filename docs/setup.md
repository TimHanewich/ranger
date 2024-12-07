## Setting up a Raspberry Pi to run Ranger
- Enable serial (UART) communications via `sudo rasp-config` (see instructions [here](https://timhanewich.medium.com/using-uart-between-a-raspberry-pi-pico-and-raspberry-pi-3b-raspbian-71095d1b259f))
- `sudo apt update` & `sudo apt upgrade`
- Install `pigpio`: `sudo apt install pigpio`
- Install `ffmpeg`: `sudo apt install ffmpeg`
- Install `libjpeg-dev`, a JPEG development library required for Python's `pillow`: `sudo apt-get install libjpeg-dev`
- Create and activate a Python virtual environment to install the following Python packages:
    - Install Python's `requests`: `python3 -m pip install requests`
    - Install Python's `pyserial`: `python3 -m pip install pyserial`
    - Install Python's `RPi.GPIO`: `python3 -m pip install RPi.GPIO` *(this normally comes with the Raspberry Pi, built in, but since we are in a virtual environment, need to install it explicitly)*
    - Install Python's `pigpio`: `python3 -m pip install pigpio`
    - Install Python's `psutil`: `python3 -m pip install psutil`
    - Install Python's `pillow` (`PIL`) library: `python3 -m pip install pillow`

## Running Ranger
Firstly, start the `command` program, a .NET console app that acts as "Central Command" in receiving telemetry from the rover and controlling the rover. You can find the `command` program in [this folder](../src/command/).

Run the `command` console app twice, in side-by-side winows. One side will be for receiving the telemetry from the rover, one will be for sending. See the selection prompts it gives you to select which "mode" each instance is in.

With the `command` program running and open to receiving telemetry, now it is time to run the `ranger` program. This is the program, in python, that controls the overall system - from receiving commands and sending telemetry.

### Running Ranger: Manually
If you are SSH'ed into Ranger, you can simply activate the virtual environment and then run the [main.py](../src/ranger/main.py) program. This should take care of everything, including starting up the pigpiod daemon.

### Running Ranger: With `.sh` Bash Script
The very simple bash script, [run.sh](../src/ranger/run.sh), will activate the virtual environment *and* run `main.py` for you. After giving the `run.sh` script run permissions with `chmod +x run.sh`, simply run it with `source sun.sh` or simply `./run.sh` to start the ranger program!