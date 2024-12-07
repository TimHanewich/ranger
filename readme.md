# Ranger 
**A prototype long-range rover, controllable over the world wide web, from anywhere.**

![ranger](https://i.imgur.com/Hpy5jZg.jpeg)

With a low-power consumption TT motor, 4S LiPo, and onboard camera system, Ranger is a prototype vehicle I designed to test the theory of remotely controlling a rover (RC car) from anywhere in the world through the world wide web. In a nutshell, ranger uses Azure Queue Storage to facilitate bidirectional communication between the rover vehicle and the driver in command. 

On a regular basis (i.e. once every 10 seconds), ranger sends telemetry to a specific Azure Queue storage queue where it is then retrieved, parsed, and presented to the remote pilot. In this telemetry package is a base64-encoded representation of an image captured by the onboard webcam. The pilot in control of the rover can also use another program to send commands to the rover, instructing it on how to move. By continuously monitoring the incoming telemetry and issuing movement commands, a pilot can control ranger from anywhere in the world.

How would ranger maintain an internet connection? There is a "slot" built into its design (see right side of photo, two black frames) that are meant to sort of hold in a smart phone. The Raspberry Pi that serves as Ranger's "brain" can connect to this smartphone while serving in a hotspot capacity, allowing Ranger to effectively operate from anywhere, as long as the cell phone maintains cell service.

Data consumption over the hotspot is minimal. As part of the standard telemetry data package, Ranger continuously reports back how many bytes the system has both received and sent. Even with imagery included (photos captured by webcam), I've observed this only to reach ~50 MB after a number of hours of operating at a send frequency of 8-10 seconds. The photos are encoded in base64, but are grayscale only, splitting the space required for an image of color into a third.

## 3D Design
I completely designed Ranger from the ground up myself in [Blender](https://www.blender.org/). You can find Ranger's Blender save file [here in the /design folder](./design/ranger.blend). 

![blender](https://i.imgur.com/uh4KGfu.jpeg)

Ranger is completely 3D printed. You can open this in Blender and export any component from Ranger that you need as an STL before 3D-printing.

## Communication Protocol
Ranger's communication protocol, using Azure Queue storage, is thoroughly documented [here](./docs/comms.md).