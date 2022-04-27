# SPS-30
Monitoring air pollution and viewing the results with a web-app

## Description
A reading is taken from the SPS-30 each hour and passed to a web-server running a web-app, using a http GET request. The web-app stores the in-coming data in a sqlite3 database and creates an up-to-date graph of the pollution versus time. Initially the web-app is hosted on the local network, but eventually a remote server will be used. 
