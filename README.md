#GRIBsherpa
GRIBsherpa is a tool/framework that gathers meteorological forecast data for use in a wildfire prediction tool. The program will:
* Provide the ability to automate the download of various meteorlogical models (GFS, NAM, ECMWF)
* Provide tools for the extraction and verification of data
* Store extracted data into a relational database and create stored procedures for common use cases

The project uses python, postgres, shell, Vagrant, psycopg2 and a host of other open source libraries such as [PyGrib](http://code.google.com/p/pygrib/).  Contributions to this project are welcome. Any questions regarding the project contact Matt Pate (mattpate at gmail.com) or Dan Catalano (daniel.w.catalano at gmail.com).

##Installation
The application framework is currently installed on a virtual machine (VM) which acts as the development environment through the use of [Vagrant](http://www.vagrantup.com). There are only two requirements for the host machine to get started developing: 1) VirtualBox (4.2.16) and 2) Vagrant (1.2.4 -> up). This project can be developed on any OS so long as the two requirements are met. To get started:

    git clone https://github.com/FireWeather/GRIBsherpa.git

## Usage & Setup

To build the VM from the base image and ssh into it: (Note - first time will take 20/40 minutes as it is downloading and provisioning the VM.

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

For other actions see the Vagrant documentation.

The first steps for using the GRIBsherpa tool/framework involves installing the necessary dependencies which is done automatically via the `vagrant up` command. The shell script that provisions the VM during the `vagrant up` call is in this repo (.vmconfig/bootstrap.sh).  If you would like to manually install these dependencies, edit the Vagrantfile (which calls the bootstrap.sh script) to prevent the script from running automatically.

The above script (bootstrap.sh) is the latest/most up-to-date way that the dependencies are being installed.  Therefore, if you're feeling jiggy and want to forget about Vagrant all together and install everything locally/manually, that script will point you to "what" and "when".

Note: initially this project was going to utilize Ubuntu 12.04 LTS, however, issues were encountered with linking to certain libraries in the system (when installing the various dependences).  There should be a way to make 12.04 work, but for the sake of expediency it was decided that Ubuntu 13.04 would be used.  No further problems were encountered.

##Project Plan
The below details (loosely) the plan of attack for the project.  

|Item        |Priority       |Status      |
|------------|:-------------:|------------|
|Move logging functionality off the terminal | High | In progress
|Finalize method for interpolation | High | 
|Create db interface class using psycopg2 | High | In progress
|Verify db insertions work well | High | 



