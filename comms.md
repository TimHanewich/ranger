# Communication Protocol

## "Standard" data points that will be transfered in each data packet (Pi --> PC)
The following data points will be transmitted from the Pi to the PC as part of *every* packet (not a "special" property that has to be requested, but rather always included).
- `memp` - Short for "memory percent", the amount of virtual memory being used as a percentage of overall memory. Can be read by `psutil.virtual_memory().percent`.
- `memu` - Short for "memory used", the amount of virtual memory used, in bytes. Can be read by `psutil.virtual_memory().used`.
- `mema` - Short for "memory available", the amount of virtual memory available, in bytes. Can be read by `psutil.virtual_memory().available`.
- `diska` - Short for "disk available", the space on the disk that is available, in bytes. Can be read by `psutil.disk_usage("/").free`.
- `bsent` - Short for "bytes sent", the number of bytes sent over the network since the program began. Can be read by `psutil.net_io_counters().bytes_sent`, but must be adjusted for program begin time.
- `brecv` - Short for "bytes received", the number of bytes received over the network since the program began. Can be read by `psutil.net_io_counters().bytes_recv`, but must be adjusted for program begin time.
