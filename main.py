import argparse
import hashlib
import json
import os
import sys

from r_handler.login import Login
from r_handler.buildings import Buildings

def open_json(file):
    # Opening JSON file
    with open(file, 'r') as openfile:
        # Reading from json file
        return json.load(openfile)

def split_on_comma(string):
  return string.split(',')

parser = argparse.ArgumentParser(description='AutoBuilder')

if os.path.exists("output.json"):
    # Add a list of strings argument
    login_data = open_json("output.json")
    
    # Create an instance of the Login class
    login = Login(login_data['username'], login_data['password'])
    build = Buildings()
    # get village ID 
    village_id = build.select_village(login.villages_dic())
    buildings = build.pasrse_buildings(village_id)
    
    
    sys.exit(0)

else:
    # Add login args
    parser.add_argument('--usr', type=str, required=True, help='Jméno hráče:')
    parser.add_argument('--pwd', type=str, required=True, help='Heslo:')

    args = parser.parse_args()
    # Data to be written
    dictionary = {
        "username": args.usr,
        "password": hashlib.md5(args.pwd.encode()).hexdigest()
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Open the output file in write mode
    with open("output.json", "w") as output_file:
        # Write the contents of the input file to the output file
        output_file.writelines(json_object)
        os.execv("main.py", [])
        