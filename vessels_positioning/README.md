# VESSEL POSITIONING SCRAPPER

This script will acquire vessel information from 
https://www.myshiptracking.com given some identifying information for a vessel.

For this example input and output dataset will be stored in two different CSV files. This could be adapted to be used in conjunction with a database but that is beyond the scope of this example.

Multi threading could be implemented to speed up the process. Multiple queries will be performed at once.
 
## Input
 Input CSV must have the following data (columns) for each vessel (row):
 
 * Name
 * IMO
 * MMSI

## Output
Output CSV will contain the following columns for each vessel.

 * Name
 * MMSI
 * IMO
 * Longitude
 * Latitude
 * Status
 * Speed
 * Course
 * Area
 * Port
 * Station
 * Destination
 * ETA
 * Draught
 * Position Received
 
## Usage

* clone or download the project locally
    *   python git clone git@github.com:javiergarciad/scrappers_examples

* Enter the project directory
    * cd vessels_positioning

* Establish a virtual environment, and install dependencies
    * python3 -m venv venv source venv/bin/activate pip install -r requirements.txt

* Modify the input CSV file:
    * Ensure each row has the required information for each vessel

* Run
    * python vessel_information.py

## License
With MIT open source license

