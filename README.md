# Ratatouille
A recipe recomendation system.


## System Requirements
1. Ubuntu 16.04
2. python3.5

## Usage
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