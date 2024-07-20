# SOTComms
Sea of thieves communication

This uses a server with a bunch of clients to commicate the current status of the ship in Sea of Thieves. 

It piggybacks on port 80 to connect.

Very Very basic currently only does steering with very little keybinds.

# How to install
For Windows users, go to the "releases" tab of this page and click the newest one.
Then install the zip, extract it and run main.exe

## If it fails
"Virus detected" may happen, this is due to code signing issues.
If this happens, you have to build the game yourself, using the following steps:

Execute build.py

Build.py requires install python (version 3.12 or later). Python must also be on the system path.