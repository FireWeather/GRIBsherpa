#GRIBsherpa
GRIBsherpa is a tool that gathers meteorological forecast data for the use in a wildfire prediction tool. The program will query, schedule, download, extract, verify and store meteorological data in a database for real time and historical analysis.  The project will be written in python.  Contributions welcome.

##Installation
This framework is installed on Ubuntu 13.04 (server or desktop).

The first steps for using these tools involve installing necessary dependencies.  A shell script is provided in this repo (Vagrant/bootstrap.sh) which can be run from the command-line and will install all necessary dependencies.  If you would like to manually install these, refer to this script for details.  

As this project is developed and run on a virtual machine, the above script is the latest/most up-to-date way that the dependencies are being installed.  The development of this project is done with Vagrant and, as would be expected, a VagrantFile is available that assists in provisioning a working VM.

##Troubleshooting
Issues were noticed when trying to install libraries for the project.  In particular there were issues linking grib_api and the openjpeg libraries.  After much fussing, upgrading to Ubuntu 13.04 and rebuilding solved the problems.

