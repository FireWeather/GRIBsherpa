#GRIBsherpa
GRIBsherpa is a tool/framework that gathers meteorological forecast data for the use in a wildfire prediction tool. The program will:
* Provide the ability to automate (schedule) the download of various meteorlogical models (GFS, NAM, ECMWF)
* Provide tools for the extraction and verification of data
* Store extracted data into a relational database and create stored procedures for common use cases

The project is written in python and utilizes various open source tools.  Contributions welcome.

##Installation
This framework is installed on Ubuntu 13.04 (server or desktop).

The first steps for using these tools involve installing necessary dependencies.  A shell script is provided in this repo (Vagrant/bootstrap.sh) which can be run from the command-line and will install all necessary dependencies.  If you would like to manually install these, refer to this script for details.  

As this project is developed and run on a virtual machine, the above script is the latest/most up-to-date way that the dependencies are being installed.  The development of this project is done with Vagrant and, as would be expected, a VagrantFile is available that assists in provisioning a working VM (this VM includes a working install of all dependencies). See the project website for details.

Note: initially this project was going to utilize Ubuntu 12.04 LTS, however, issues were encountered with linking to certain libraries in the system (when installing the various dependences).  There should be a way to make 12.04 work, but for the sake of expediency it was decided that Ubuntu 13.04 would be used.  No further problems were encountered.

##Project Plan
The below details (loosely) the plan of attack for the project.  

|Item        |Priority       |Status      |
|------------|:-------------:|------------|
|Finalize method for interpolation | High | In progress
|Create db interface class using psycopg2 | High | In progress
|Verify db insertions work well | High | 



