# SPS-30
Monitoring particulate density in the air and viewing the results over the internet

## Description
A reading is taken from the SPS-30 particulate sensor each hour and passed to a web-server. The server stores the in-coming data and creates an up-to-date graph of the particulate density versus time. Initially the server is hosted on the local network, limiting access to the data to this domain, but eventually a remote server will be used, making the data publically accessible.

The *local_server* directory contains the files needed to run a flask app on the local server.

The *sensor* directory contains the that read the sensor and sent its data to the local server.