#GRIBsherpa
GRIBsherpa is a tool/framework that gathers meteorological forecast data for the use in a wildfire prediction tool. The program will:
* Provide the ability to automate the download of various meteorlogical models (GFS, NAM, ECMWF)
* Provide tools for the extraction and verification of data
* Store extracted data into a relational database and create stored procedures for common use cases

The project uses python, postgres, shell, Vagrant, psycopg2 and a host of other open source libraries such as [PyGrib](http://code.google.com/p/pygrib/).  Contributions welcome. Any questions regarding the project contact Matt Pate mattpate at gmail.com or Dan Catalano daniel.w.catalano at gmail.com.

##Installation
The application framework is currently installed on a virtual machine (VM) which acts as the development environment through the use of Vagrant. There are only two requirements for the host machine to get started developing: 1) VirtualBox (4.2.16) and 2) Vagrant (1.2.4 -> up). To reiterate, this project can be developed on any OS so long as the two requirements are met. TO get started:

    git clone https://github.com/FireWeather/GRIBsherpa.git

## Usage & Setup

to build the VM from the base image and ssh into it: (Note - first time will take 20/40 minutes as it is downloading and provisioning the VM.

    cd GRIBsherpa/.vmconfig
    vagrant up
    vagrant ssh

exiting ssh from the VM:

    exit

or to stop it from the host:

    vagrant suspend
    
or stop it from the VM:

    shutdown -h now

to destroy the VM from the host:

    vagrant destroy

then to (completely) rebuild everything:

    vagrant up

The first steps for using these tools involve installing necessary dependencies which is done automatically via the vagrant up command. The shell script that provisions the VM is in this repo (.vmconfig/bootstrap.sh).  If you would like to manually install these, edit the Vagrantfile to prevent the script from running automatically.

As this project is developed and run on a virtual machine, the above script is the latest/most up-to-date way that the dependencies are being installed.  The development of this project is done with Vagrant and, as would be expected, a VagrantFile is available that assists in provisioning a working VM (this VM includes a working install of all dependencies). See the project website for details.

Note: initially this project was going to utilize Ubuntu 12.04 LTS, however, issues were encountered with linking to certain libraries in the system (when installing the various dependences).  There should be a way to make 12.04 work, but for the sake of expediency it was decided that Ubuntu 13.04 would be used.  No further problems were encountered.

##Project Plan
The below details (loosely) the plan of attack for the project.  

|Item        |Priority       |Status      |
|------------|:-------------:|------------|
|Finalize method for interpolation | High | In progress
|Create db interface class using psycopg2 | High | In progress
|Verify db insertions work well | High | 



