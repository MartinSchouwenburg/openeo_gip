This project is a backend for OpenEo clients(https://openeo.org/). It facilitates processing of geo spatial data (for the moment raster data) in a cloud enviroment. The goal of the project is to eventually realize a backend that can be used(and deployed) by typical users in a academical enviroment for research, teaching and projects.

## Setup
### Installation.
 - pull the repository from github to a suitable location on your server
 - make sure the packages below are installed
   
| Package            | Installation Command                          |
|--------------------|----------------------------------------------|
| OpenEO           | `pip install openeo`                         |
| Flask           | `pip install -U Flask`                        |
| Flask-RESTful   | `sudo apt-get install -y python-flask-restful` |
| Flask-HTTPAuth  | `pip install Flask-HTTPAuth`                  |
| PyNaCl          | `pip install pynacl`                          |
| JSON Schema     | `pip install jsonschema`                      |
| EOReader        | `pip install eoreader`                        |
| ILWISPy    | `pip install ilwis`                       |
| Qt5            | `sudo apt install -y qtbase5-dev`              |
| GDAL           | `sudo apt-get install gdal-bin`                |
| NetCDF         | `sudo apt -y install netcdf-bin`               |

- the file app.py starts the server on port 5000
- The file config.json describes locations that the server needs to find and write information/data. Modify this to suit your own needs.
