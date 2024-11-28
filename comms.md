# Communication Protocol

## Communication Protocol Backbone
Azure Queue Storage will be used for bidirectional communication between the rover and a central command system. Two queues will be used (existing within the same storage account) - one for sending commands from the central command system ("controller" in this relationship) to the car and one for sending messages from the car to the central command system.

The messages exchanged will be in JSON format. Images can be shared from the car to central command by encoding these images in base64.

The minimum resolution that can be captured on the Logitech C270 is 160x120 (160 pixels in width, 120 pixels in height). This is a combined 19,200 pixels. With each pixel having three values (R,G,B), this would mean each image is 57,600 bytes. However, to save on bandwidth, monochrome (black and white) images will be used. This reduces the footprint of each image from 57,600 bytes down to 19,200 bytes, or one byte per pixel. Here is [an example 160x120 image in full color](https://i.imgur.com/pwf6wCL.jpeg) and here is [the monochrome version of that image](https://i.imgur.com/kpKrpUn.png).

The full image capturing and transmitting process will be the following:
1. Image is capture using fswebcam (saved locally to system).
2. Python script uses PIL to loop through each pixel of the image and "average" each pixel into a single monochrome value. See example [here](https://i.imgur.com/dd0vRru.png).
3. These monochrome byte values are added to a `bytearray`, which will total 19,200 bytes.
4. Python converts this `bytearray` into a base64-encoded string using the `base64` module. 
5. This base64-encoded string is posted as a message to Azure Queue Storage, included within a broader JSON object.
6. This queue message is received and the JSON object is deserialized in the central command system (likely .NET-based). See [this example](https://i.imgur.com/3s78G7d.png) on how to receive a Queue message in C#.
7. The base64-encoded string is extracted from the JSON object and converted to `byte[]`.
7. The central command system, written in .NET, uses `System.Drawing` to reconstruct the monochrome image, looping through each byte in the `byte[]` byte array and filling in each pixel one by one. See [this example](https://i.imgur.com/DMnJx8f.png).
8. The resulting image is saved and/or shown to the user of the central command system.

### Queue Names
- `r2c` = "ranger to command", messages sent from the Ranger car to the computer.
- `c2r` = "command to ranger", messages sent from the computer to the Ranger car.

## "Standard" data points that will be transfered in each data packet (Pi --> PC)
The following data points will be transmitted from the Pi to the PC as part of *every* packet (not a "special" property that has to be requested, but rather always included).
- `memp` - Short for "memory percent", the amount of virtual memory being used as a percentage of overall memory. Can be read by `psutil.virtual_memory().percent`.
- `memu` - Short for "memory used", the amount of virtual memory used, in bytes. Can be read by `psutil.virtual_memory().used`.
- `mema` - Short for "memory available", the amount of virtual memory available, in bytes. Can be read by `psutil.virtual_memory().available`.
- `diska` - Short for "disk available", the space on the disk that is available, in bytes. Can be read by `psutil.disk_usage("/").free`.
- `bsent` - Short for "bytes sent", the number of bytes sent over the network since the program began. Can be read by `psutil.net_io_counters().bytes_sent`, but must be adjusted for program begin time.
- `brecv` - Short for "bytes received", the number of bytes received over the network since the program began. Can be read by `psutil.net_io_counters().bytes_recv`, but must be adjusted for program begin time.
