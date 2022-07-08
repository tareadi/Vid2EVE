# Vid2EVE

A simple pysimulator for events generation from video recorded from conventional camera. 

A full theory description of this code/source can be found in project file [Link]

## Repository Source
All dependencies are located in the source folder. Change working directory to this repository's home folder and run the __init__.py

## Running and Installation
clone github repo using following command

```bash
git clone https://github.com/tareadi/Vid2EVE.git
```

install 
    * [Anaconda Python 3.9 or above](https://www.anaconda.com/products/individual)

```bash
conda create --name vid2EVE
conda activate Vid2EVE
pip install -r vid2EVE/requirements.txt
```


Run on Terminal with activated Conda Env.
```base
python3 __init__.py
```

## Result
This will generate frames `vid2EVE/frames` and events in text format as "events.text" in source file.
