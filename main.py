#!usr/bin/env python3
import argparse
import app
import sys
from buildings import Buildings
from login import Login

if not app.exist("output.json"):
    #TODO - ADD option for server
    app.start()
else:
    parser = argparse.ArgumentParser(description='AutoBuilder')
    # Add a list of strings argument
    login_data = app.open_json("output.json")

    # Create an instance of the Login class
    login = Login(login_data['username'], login_data['password'])
    login.set_session()
    build = Buildings(login)

    # get & select village ID
    village_id = build.select_village(login.villages_list())
    # Building list
    buildings = build.pasrse_buildings(village_id, login.service_url)

    building_name = parser.add_argument(
        '--build', type=str, required=False, help='hrad,kamen,pila,ruda,sklad,mlyn')

    args = parser.parse_args()
    class_name = args.build
    build.init_buildings(buildings, class_name)
    #TODO - After all functions are finished I will automate this 
    if (class_name == 'hrad'):
        build.hrad.request_link(login.session, build)
    elif (class_name == 'kamen'):
        build.hrad.request_link(login.session, build)
    elif (class_name == 'pila'):
        build.hrad.request_link(login.session, build)
    elif (class_name == 'ruda'):
        build.hrad.request_link(login.session, build)
    if (class_name == 'sklad'):
        build.hrad.request_link(login.session, build)
    if (class_name == 'mlyn'):
        build.hrad.request_link(login.session, build)