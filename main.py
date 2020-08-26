#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import matplotlib.pyplot as plt
"""
Created on Wed Aug 26 09:11:14 2020

@author: alejandro
"""

def get_derivatives(state, parameter):
    derivative = {"dV_w"   :    0,
                   "dv"     :   0,
                   "dx"     :   0}

    derivative["dV_w"] = -parameter["exit_area"] * state["escape_velocity"]
    
    total_mass = parameter["mass_bottle"] + state["water_volume"] * parameter["rho_water"]
    derivative["dv"]   = 0.98 * (parameter["exit_area"]*(state["escape_velocity"]**2)\
                          * parameter["rho_water"]) \
                          /total_mass
    derivative["dx"]   = state["velocity"] 
    
    return derivative


def update_state(state, parameter, delta_t):
    state["air_pressure"]   =   parameter["initial_air_pressure"] \
                              * ((parameter["total_volume"]*(1-parameter["water_ratio"]) \
                              / (parameter["total_volume"] - state["water_volume"])) ** parameter["gamma"])
    
    state["escape_velocity"] = (2*(state["air_pressure"]-parameter["atm_pressure"])/parameter["rho_water"])**0.5
    
    derivative = get_derivatives(state, parameter)
    
    state["water_volume"]   = state["water_volume"] + delta_t * derivative["dV_w"]
    state["velocity"]       = state["velocity"] + delta_t * derivative["dv"]
    state["position"]       = state["position"] + delta_t * derivative["dx"]
    
    return state


def get_first_state(parameter):
    state = {"air_pressure"     :   0,
             "water_volume"     :   parameter["total_volume"] * parameter["water_ratio"],
             "position"         :   0,
             "velocity"         :   0,
             "escape_velocity"  :   0}
    
    state["air_pressure"]   =   parameter["initial_air_pressure"] \
                              * ((parameter["total_volume"]*(1-parameter["water_ratio"]) \
                              / (parameter["total_volume"] - state["water_volume"])) ** parameter["gamma"])
    
    state["escape_velocity"] = (2*(state["air_pressure"]-parameter["atm_pressure"])/parameter["rho_water"])**0.5
    
    return state


def main_loop(parameter):
    
    state = get_first_state(parameter)
    state_array = [state]
    
    while (type(state["water_volume"]) is float) and state["water_volume"] > 0:
        state = copy.copy(state)
        state = update_state(state, parameter, delta_t)
        state_array.append(state)
        
    return state_array
        
    
delta_t = 0.0001
parameter = {"initial_air_pressure" :   600000,
             "water_ratio"          :   0.5,
             "gamma"                :   1,
             "total_volume"         :   0.002,
             "exit_area"            :   3.141592*0.01**2,
             "atm_pressure"         :   100000,
             "rho_water"            :   1000,
             "mass_bottle"          :   0.1}

state_array = main_loop(parameter)
print(state_array[-1]["velocity"])

time_array = [i*delta_t for i in range(len(state_array))]

plt.plot(time_array, [step["escape_velocity"] for step in state_array])

# speed_array = []
# ratio_array = [0.1*i for i in range(1,10)]

# for ratio in ratio_array:
#     parameter["water_ratio"] = ratio
#     state_array = main_loop(parameter)
#     speed_array.append(state_array[-1]["velocity"])