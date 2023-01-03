import os
import argparse
import json
import hashlib

def exist(string: str):
    return os.path.exists(string)

def start():
    parser = argparse.ArgumentParser(description='AutoBuilder')

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
    
def open_json(file: json):
    """_summary_

    Args:
        file (json): _description_

    Returns:
        _type_: _description_
    """
    # Opening JSON file
    with open(file, 'r') as openfile:
        # Reading from json file
        return json.load(openfile)

def split_on_comma(string: str):
    return string.split(',')