# -*- coding: utf-8 -*-
"""
Created on Sat Jun 8 2024

@author: Achrafkr
"""

""" Imports """

import pandas as pd
from time import time, sleep
from tqdm import tqdm
from opensky_api import OpenSkyApi
from ast import literal_eval



"""     PARTICULAR INFORMATION

Limitations for anonymous users:
    
    - Time parameter is ignored (can't retrieve past data)
    - 10-second time resolution
    - 400 API credits/day
    
Limitations for OpenSky users:
    
    - Can retrieve past data up to 1 hour
    - 5-second time resolution
    - 400 API credits/day

    
"""

""" Connect to the OpenSky REST API """

def connect(username=None, password=None):
        API = OpenSkyApi(username=username, password=password)
    return API


API = connect()


columns = ['Time', 'icao24', 'callsign', 'origin_country', 'last_contact', 'latitude','longitude', 'baro_altitude',
           'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 
           'position_source', 'category']

"""

Position source ('position_source'):
    
    - 0 : ADS-B
    - 1 : ASTERIX
    - 2 : MLAT (Multilateration based on Mode-S Data)
    - 3 : FLARM (FLARM is a collision avoidance system based on GPS Data)


Aircraft categories ('category'): 
    
    - 0 : No information at all                                                - 11 : Parachutist / Skydiver
    - 1 : No ADS-B Emitter Category Information                                - 12 : Ultralight / hang-glider / paraglider
    - 2 : Light (< 15500 lbs)                                                  - 13 : Reserved
    - 3 : Small (15500 to 75000 lbs)                                           - 14 : Unmanned Aerial Vehicle
    - 4 : Large (75000 to 300000 lbs)                                          - 15 : Space / Trans-atmospheric vehicle
    - 5 : High Vortex Large (aircraft such as B-757)                           - 16 : Surface Vehicle – Emergency Vehicle
    - 6 : Heavy (> 300000 lbs)                                                 - 17 : Surface Vehicle – Service Vehicle
    - 7 : High Performance (> 5g acceleration and 400 kts)                     - 18 : Point Obstacle (includes tethered balloons)
    - 8 : Rotorcraft                                                           - 19 : Cluster Obstacle
    - 9 : Glider / sailplane                                                   - 20 : Line Obstacle
    - 10 : Lighter-than-air
    

"""

""" Functions for time conversion """

def join_numbers(list_: list) -> list:
    is_number = ''
    is_other = ''
    for el in list_:
        try:
            int(el)
            is_number += el
        except ValueError:
            is_other += el
    return [is_number, is_other]

def time_conversion(period: str) -> int:
    conv_times = {'s': 1, 'm': 60, 'h': 3600}
    split_ = period.split()
    t = 0
    for el in split_:
        t_, unit = join_numbers(list(el))
        t += int(t_) * conv_times[unit]
    return t

""" Insert data in columns """

def get_data(columns=columns, list_airplanes=None, lat=[-90, 90], lon=[-180, 180], max_time='3h', max_vectors=400, time_resolution='10s'):
    
    data = {}
    for col in columns:
      data[col] = []

    bbox = tuple(lat + lon)
    max_time = time_conversion(max_time)
    t_res = time_conversion(time_resolution)
    t_start = time()
    #n_vectors = min(max_vectors, max_time//t_res + 1)
    
    for it in tqdm(range(max_vectors)):
        elapsed = time()
        
        if elapsed - t_start >= max_time:
            print("Reached assigned Max. time {} for retrieving data".format(max_time))
            
            data = pd.DataFrame(data)
            data.Time = data.Time.apply(lambda x: pd.to_datetime(x, unit = 's'))
            return data
       
        states = API.get_states(icao24=list_airplanes, bbox=bbox)
        
        try:
            for vector_state in states.states:
                vector_state = vector_state.__dict__
                for col in columns:
                    if col == 'Time':
                        data[col].append(states.time)
                    else:
                        data[col].append(vector_state[col])
                        
            sleep(t_res) if it != (max_vectors - 1) else None
            
        except Exception as e:
            print("Could'n retrieve any data for It {} ({})".format(it, e.args))
            sleep(t_res) if it != (max_vectors - 1) else None

        except KeyboardInterrupt:
            print("Action interrupted")
            
            data = pd.DataFrame(data)
            data.Time = data.Time.apply(lambda x: pd.to_datetime(x, unit = 's'))
            return data
            
    data = pd.DataFrame(data)
    data.Time = data.Time.apply(lambda x: pd.to_datetime(x, unit = 's'))
    
    return data


""" Parsing arguments """

def eval_list(params: str) -> list:
    params = params.replace("[", "['").replace("]", "']").replace(",", "','")
    
    try:
        params = literal_eval(params)
    except SyntaxError:
       return params
        
    eval_args = [] 
    
    try:
        for arg in params:
            try:
                eval_args.append(float(arg))
            except ValueError:
                eval_args.append(arg)
                
    except TypeError:
        eval_args = params
        
    return eval_args

def argv_parser(argv):
    
    filename = argv[1]
    if len(argv)>2:
        if literal_eval(argv[2]) == '':
            filepath = ''
        else:
            filepath = argv[2]
    else:
        filepath = ''
    
    kwargs = "".join(argv[3:]) if len(argv) > 2 else "".join(argv[2:])
    kwargs = kwargs.replace('{', '').replace('}','').replace("'","").split(';')
    dict_kwargs = {}
    for arg in kwargs:
        k, v = arg.split(":")
        dict_kwargs[k] = eval_list(v)
    
    return filename, filepath, dict_kwargs

def save_data(filename, filepath, typefile='csv', **kwargs):
    
    data = get_data(**kwargs)
    
    if typefile == 'csv':
        data.to_csv(filepath + filename, index=False)
    
    if typefile == 'json':
        data.to_json(filepath + filename) 
        
    print("Your file {} is ready!".format(filename))
    
 

if __name__ == "__main__":
    
    
    from sys import argv
    
    
    filename, filepath, kwargs = argv_parser(argv)
    typefile = filename.split(".")[-1]
    
    save_data(filename, filepath, typefile, **kwargs)
    