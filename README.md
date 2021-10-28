# T17-API-D175: OGC API - EDR client

## Deployment script

This client is fully deployed by executing a simple bash script, or by executing all the commands one by one in the command line. You can save the following in a .sh executable file and launch it, or execute step by step:

```
#!/bin/bash

# Client settings:
TILESERVER=https://tile.openstreetmap.org/{z}/{x}/{y}.png
DEFAULT_ZOOM=1
DEFAULT_CENTER=[0,0]
API_ENDPOINT=https://aws4ogc17.webmapengine.com/edr/
# ENV settings
PYTHON_PATH=/usr/bin/python3
PROJECT_PATH=./edr-ogc-api-client

# Download repo
git clone https://github.com/opengeospatial/T17-API-D175-EDR.git $PROJECT_PATH
# Generate virtual env.
virtualenv --python=$PYTHON_PATH $PROJECT_PATH
# Go inside the repo folder
cd $PROJECT_PATH
# Enable virtual env
source bin/activate
# Install requirements
pip install -r requirements.txt
# Set tileserver url
sed -i "s#TILESERVER_URL =.*#TILESERVER_URL = \"${TILESERVER}\"#" app.py
# Set api base url
sed -i "s#API_BASE_URL =.*#API_BASE_URL = \"${API_ENDPOINT}\"#" app.py
# Set default zoom
sed -i "s#DEFAULT_ZOOM =.*#DEFAULT_ZOOM = \"${DEFAULT_ZOOM}\"#" app.py
# Set default map coords
sed -i "s#DEFAULT_CENTER =.*#DEFAULT_CENTER = \"${DEFAULT_CENTER}\"#" app.py
# Run client
flask run -p 5050 --host=0.0.0.0
```

These commands execute the following steps:

1. Clone the client's github repository
2. Generate and activate a python virtual environment
3. Install all the dependencies and libraries in this environment without affecting the user's environment
4. Set the variables values in the Python scripts
5. Launch flask to run the web client in localhost, navigable through the user's browser

**WARNING:** Before executing the script, make sure that python virtualenv is installed in your computer, and that the path to your python installation is correct.

## System requirements

Before running the deployment script, the following requirements need to be met:

1. Operative system: Linux or MacOS with Python 3.
1. The following installed packages:
* git
* pip3
* virtualenv
1. Access to the Internet.

## Installation

In order to run the script in an environment that meets the aforementioned requisites, follow these steps:

1. Upload or download the script to the machine where you want to deploy the client.
2. Create an empty directory and copy the script:

```
mkdir -v ~/api_client
cp -v deploy_edr_client.sh ~/api_client/
```

**NOTE:** The characters `~/` indicate the user's personal directory.

3. Give execution permissions to the script.

```
sudo chmod 0750 ~/api_client/deploy_edr_client.sh
```

4. Modify the configuration variables in the beginning of the script to adapt them to your environment. The meaning of these variables is as follows:

    | Variable       | Description                                              |
    |----------------|----------------------------------------------------------|
    | PYTHON_PATH    | Location of your Python binary                           |
    | PROJECT_PATH   | Location of the directory with the client's source code  |
    | TILESERVER     | URL to your tile server                                  |
    | DEFAULT_CENTER | Coordinates to center the map by default                 |
    | DEFAULT_ZOOM   | Default zoom level on the map                            |

You can find the location of your Python binary by executing the command `which python3`.

The value of the `PROJECT_PATH` variable can remain unchanged: the script will create the directory if it does not exist.

5. Once the script has been adapted, you can just execute it:

```
bash ~/api_client/deploy_edr_client.sh
```

**NOTE:** If you want to execute it in debug mode, you can do so with the following command:
```
bash -x ~/api_client/deploy_edr_client.sh
```

In case of issues during the script execution, make sure the environment meets the requirements, then delete all files and launch the script again using the debug mode.
