# Build an Item Catalog Application
***
#### Project Overview

>The project's goal was to develop an application that provides a list of items within a variety of categories as well as a user registration and authentication system. Registered users are supposed to have the ability to post, edit and delete their own items.

#### Application Description
>My idea to match the project requirements was to develop an application which stores my favorite meals, their recipes and all the necessary ingredients. Additionally for every ingredient you can add the price and the shop it can be bought in.

#### Execute the sourcecode

##### Prerequisites:
* Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)    
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* Use [Python 2](https://www.python.org/downloads/)

##### Prepare software and data:
1. Install `Vagrant` and `VirtualBox`
2. Put all the files from this repo into the `vagrant` directory, which is shared with your virtual machine
3. Launch the virtual machine
4. Set up the database
5. Add some initial data to the database

Detailed information for steps 3 to 5 can be found below.

###### Launching the Virtual Machine:
For much more details or troubleshooting see this [Udacity course](https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/303a271d-bc69-4eba-ae38-e9875f841604/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0).  
Below you will find the main tasks you need to execute:

1. Make sure Virtualization is allowed on your computer. For help read this [stackoverflow entry ](https://stackoverflow.com/questions/46723611/vagrant-timed-out-while-waiting-for-the-machine-to-boot-in-windows-10)

2. From your terminal, inside the vagrant subdirectory, run the command `vagrant up`.
> `$ vagrant up`  
This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

3. Log in to the virtual machine by using `vagrant ssh`
> `$ vagrant ssh`  
When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

4. Change directory to /vagrant and look around with ls.
> `$ cd /vagrant` and `$ ls`   
The files you see here are the same as the ones in the vagrant subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM. Files in the VM's /vagrant directory are shared with the vagrant folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.

###### Setting up the database for this project:
In the virtual machine navigate to the shared directory which contains all the project files and run the following command:
> `python database_setup.py`


The generated database includes three tables:
1. users
2. meal
3. meal_ingredient

The users table includes information about the users of the application:

|id|name|email|picture|
| -
||||||

The meal table includes the meal recipe:  

|id|name|recipe|
| -
|||||

The meal_ingredient table includes all the necessary ingredients for a meal and metadata for each of these ingredietns:

|name|id|price|supermarket|meal_id|meal|
| -
||||||||



###### Add initial data to the database:

To add some initial data to the tables in the database run `lotsofmeals.py`

##### Run the application:
To run the application from the file `project.py` (in the /vagrant directory in your VM) use this command:  
> `$ python project.py`
