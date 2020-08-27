# Ratatouille
A recipe recomendation system.


## System Requirements
1. Ubuntu 16.04
2. python3.5

## Usage

### Tutorials
This section explains how to install the system and use the pre-trained model  
*Note, we use Tensorflow Object Detection API in this project*  
*Tensorflow Object Detection API has full credit for all the code in directories 'object_detection' and 'slim'*

#### Installation
clone this project and run the install.sh script  
  
**when using GPU**

	./install.sh -gpu
    
**when using CPU**

	./install.sh -cpu
    

After the installation process, make sure to add the directories to the PYTHONPATH.  

	# From project home dir
    export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
    
You need to add this line everytime you open a new terminal.  
Adding this line to bashrc would be better.  
In that case, change `pwd` with the absolute path.  
Then, run runserver.py to run the server.

	python3 runserver.py

### How to crawl images
settings.json contains all the information about the crawlling.

```json
    "number_of_files" : 200,
    "class_id" : ".rg_i.Q4LuWd",
    "items" : {
        "keyword":"id"
    }
```

|key|value|
|---|---|
|number_of_files|indicates the number of files to download|
|class_id|the name of the class where the images are located|
|items|a dictionary of items|
|keyword|the keyword for searching images|
|id|the name of label that we use for classification|

Run the python script in the following directory  

Ratatouille  
->crawller  
&nbsp;&nbsp;&nbsp;&nbsp;->crawlled_images  
&nbsp;&nbsp;&nbsp;&nbsp;-settings.json  
&nbsp;&nbsp;&nbsp;&nbsp;-crawller.py  

	python3 crawller.py
    
The downloaded files are saved in subdirectories in crawlled_images.  
The id's in "settings.json" are the names of subdirectories
