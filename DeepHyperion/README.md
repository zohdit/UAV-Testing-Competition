# DeepHyperion
DeepHyperion is a tool for generating test inputs and feature maps using illumination-search algorithm.

## General Information ##
This folder contains the application of the DeepHyperion approach to the Unmanned Aerial Vehicles (UAVs).

## Installation on Ubuntu ##

### Installing Python 3.8 ###
Install Python 3.8:

``` 
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install -y python3.8
```

And check if it is correctly installed, by typing the following command:

``` 
python3 -V

Python 3.8.10
```

Check that the version of python matches `3.8.*`.

### Installing pip ###

Use the following commands to install pip and upgrade it to the latest version:

``` 
apt install -y python3-pip
python3 -m pip install --upgrade pip
```

Once the installation is complete, verify the installation by checking the pip version:

``` 
python3 -m pip --version

pip 21.1.1 from /usr/local/lib/python3.8/dist-packages/pip (python 3.8)
```
### Creating a Python virtual environment ###

Install the `venv` module in the docker container:

``` 
apt install -y python3-venv
```

Create the python virtual environment:

```
cd /DeepHyperion
python3 -m venv .venv
```

Activate the python virtual environment and updated `pip` again (venv comes with an old version of the tool):

```
. .venv/bin/activate
pip install --upgrade pip
```

### Installing Dependencies ###

This tool has other dependencies, that can be installed via `pip`:

```
pip install -r requirements.txt
``` 

## Usage ##

### Input ###

* A case study with `.yaml` format in the folder `case_studies`;
* `config.py` containing the configuration of the tool selected by the user, the user related parameters are:
```
NUM_EXEC          = int(os.getenv('DH_EXEC', '100'))  # simulation budget
CASE_STUDY        = str(os.getenv('DH_CASE_STUDY', "case_studies/mission1.yaml")) # case study
NAME = "DeepHyperion" # folder name
RUN = "1"             # run id
```

### Run the Tool ###

To run the tool use the following command:

```
python mapelites_uav.py
```

### Output ###

When the run is finished, the tool produces the following outputs in the `logs` folder:

* maps representing inputs distribution;
* json files containing the final reports of the run;
* folders containing the generated inputs:
  * all: all the inputs generated during the run
  * archive: inputs from the final feature map
  * misbehaviours: all the inputs that cause misbehviours (collisions or below safety distance)

### Command Line Interface ###

Alternatively you can use the Command Line interface to run the tool with predefined case study and budget:
```
python cli.py generate case_studies/mission1.yaml 100
```
 
using this option, the tool outputs only misbehaviours in the folder `generated_tests` and log files in the folder `logs`.



## Reference

```
@article{zohdinasab2023efficient,
  title={Efficient and effective feature space exploration for testing deep learning systems},
  author={Zohdinasab, Tahereh and Riccio, Vincenzo and Gambi, Alessio and Tonella, Paolo},
  journal={ACM Transactions on Software Engineering and Methodology},
  volume={32},
  number={2},
  pages={1--38},
  year={2023},
  publisher={ACM New York, NY}
}
```

## Contacts

For any related question, please contact its authors: 
* Tahereh Zohdinasab ([tahereh.zohdinasab@usi.ch](mailto:tahereh.zohdinasab@usi.ch)) 
* Andrea Doreste ([andrea.doreste@usi.ch](mailto:andrea.doreste@usi.ch)) 

