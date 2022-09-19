#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 06:26:15 2022

@author: sdas
"""

import flask
from flask import request
from datetime import datetime
from dateutil import parser

from sunpy.coordinates import sun
import math

import sunpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from scipy import stats

import astropy.units as u
import astropy.constants as const
from astropy.coordinates import SkyCoord

import sunpy.map
import pfsspy

from pfsspy import tracing
from sunpy.coordinates import frames
from scipy.interpolate import interp1d

import requests
from bs4 import BeautifulSoup
import html5lib

import sys
import os
from os.path import exists

def convert(x):
    y=0
    try:
        y=parser.parse(x, fuzzy=True)
    except:
        if("now" in x or "today" in x):
            y=datetime.now()
        else:
            print("date not understood")

    if y:
        return math.floor(sun.carrington_rotation_number(y))
    else:
        return 0




#%% Enter the CR and magnetogram

def func(cr):
    
    URL = "https://gong.nso.edu/data/magmap/crmap.html"
    r = requests.get(URL)
    
    #cr = 2053           # Carrignton rotation number
    mag = 'GONG'        # Magnetogram type (GONG/HMI)

    soup = BeautifulSoup(r.content, 'html5lib')
    fileurl=''
    alla=soup.find_all("a", href=True)
    data = '' 
    for data in alla:
    	if(str(cr) in data['href']) :
    		fileurl="https://gong.nso.edu"+data['href']

    #%% Magnetogram input for a CR with res = 360 x 180

    gong_map = sunpy.map.Map(fileurl)
    #header = sunpy.io.fits.get_header(fileurl)

    # transforming fits file into sunpy map
    input_map = sunpy.map.Map(gong_map.data- np.mean(gong_map.data), gong_map.meta)

    #%% Define pfsspy Grid

    nrho = 100
    rss = 2.50                      #Setting source surface (ss) = 2.50 Rsun

    #%% Solving PFSS model to get the Output at source surface

    input = pfsspy.Input(input_map, nrho, rss)
    output = pfsspy.pfss(input)

    #%% Plotting

    # Input map at 1.0 R
    m = input.map
    fig = plt.figure()
    ax = plt.subplot(projection=m)
    m.plot(vmax=-50, vmin =50)
    plt.colorbar()
    ax.set_title('Input field')
    plt.savefig("./static/images/inp_"+str(cr)+".png")
    plt.close()
    # Output map at 2.5 R
    ss_br = output.source_surface_br
    fig = plt.figure()
    ax = plt.subplot(projection=ss_br)

    ss_br.plot()
    # Plot the polarity inversion line (i.e. where B changes its sign or where B=0)
    ax.plot_coord(output.source_surface_pils[0])

    plt.colorbar()
    ax.set_title('Source surface magnetic field')
    plt.savefig("./static/images/outp_"+str(cr)+".png")
    plt.close()
    #%% Calculating coordinate of Earth (SBE points) for each hour of CR

    t_start = sunpy.coordinates.sun.carrington_rotation_time(cr)
    t_end = sunpy.coordinates.sun.carrington_rotation_time(cr+1)		
    dt = t_end - t_start

    n_hr = int(dt.value * 24)   # no. of hours in CR (you can decrease as you wish)

    # Generating evenly spaced grid points for longitude for each hour (excluding last hr)
    # In carrington frame 0 and 360 represents the same location, that's why we must ignore one
     
    SBE_points = n_hr
    obs_time = t_start + dt*np.linspace(10**(-6), 1-10**(-6), SBE_points, endpoint=False)
    SBElat = np.zeros(len(obs_time))
    SBElon = np.zeros(len(obs_time))
    i = 0
    for t in obs_time:
        #obst = Time(t, format='jd')
       coord = sunpy.coordinates.ephemeris.get_earth(time=t).transform_to(frames.HeliographicCarrington(observer='earth'))
       #coord2 = sunpy.coordinates.ephemeris.get_earth(time=t).transform_to(output.coordinate_frame)
       SBElat[i] = coord.lat.value * np.pi/180
       SBElon[i] = coord.lon.value * np.pi/180
       i+=1

    # Real date starts from 360 and ends at 0. That's why flipping is required to plot with increasing time
    SBElon = np.flip(SBElon)
    SBElat = np.flip(SBElat)

    #%% Generating meshgrid to trace fieldlines

    r = 2.50 * const.R_sun            #setting cusp radius (rcp) to 2.50 Rsun

    lon, lat = SBElon*u.rad, SBElat*u.rad
    seeds = SkyCoord(lon, lat, r, frame=output.coordinate_frame)

    #Plotting the seed points (SBE points)
    #plt.scatter(lon*180/np.pi, lat*180/np.pi, s=0.1)
    #plt.show()

    #%% Generating fieldlines and tracing it

    print('\n\nTracing field lines ... ... ...')
    tracer = tracing.FortranTracer(max_steps=1000, step_size=0.03)  # can play around here
    field_lines = tracer.trace(seeds, output)
   

    #%% ############# DONT FOCUS MUCH HERE, JUST ON "Br_rss" list ################# 
    # Solving to get the EXACT required coordinates of required filedlines

    Total_field_count = 0
    Open_field_count = 0
    Closed_field_count = 0

    #r0 : solar radius
    lon_open_r0, lat_open_r0 = [], []
    lon_rcp, lat_rcp = [], []               #rcp : radius of cusp, here 2.50 Rsun
    Br_r0 = []
    Br_rss = []         # Magnetic field at 2.5R (i.e. at source surface)
    exp_factor_pfsspy = []
    ss_points = []

    for field_line in field_lines:
        Total_field_count += 1
        field_coords = field_line.coords
        field_coords.representation_type = 'spherical'
        #solving for open fieldlines:-
        if field_line.is_open:
            sol_point = field_line.solar_footpoint
            sol_point.representation_type = 'spherical'
            lon_open_r0.append(sol_point.lon.value)
            lat_open_r0.append(sol_point.lat.value)
            ss_points.append(sol_point.radius/const.R_sun)
            #Br_r0.append(output.get_bvec(sol_point)[0].value)
            Open_field_count += 1
            i = 0                           #radial index to get r = 2.50
            exp_factor_pfsspy.append(field_line.expansion_factor)
            radius_ss = field_coords[0].radius.value/const.R_sun.value
            if radius_ss < 2:               #Case for outgoing fieldlines
                radius_ss = field_coords[-1].radius.value/const.R_sun.value
                while radius_ss > 2.51:     #condition to get r = 2.50
                    radius_ss = field_coords[-i-1].radius.value/const.R_sun.value
                    i += 1                  #appropriate index = i-1
                lat_rcp.append(field_coords[-i].lat.value)
                lon_rcp.append(field_coords[-i].lon.value)
                Br_rss.append(field_line.b_along_fline[-i][0])
                #print(field_coords[-i].radius.value/const.R_sun.value)
            else:                           #Case for incoming fieldlines
                while radius_ss > 2.51:     #condition to get r = 2.50
                    radius_ss = field_coords[i].radius.value/const.R_sun.value
                    i += 1                  #appropriate index = i-1
                lat_rcp.append(field_coords[i-1].lat.value)
                lon_rcp.append(field_coords[i-1].lon.value)
                Br_rss.append(field_line.b_along_fline[i-1][0])
                #print(field_coords[i-1].radius.value/const.R_sun.value)
            
            if field_line.polarity == 1:
                Br_r0.append(field_line.b_along_fline[1][0])
                #print(field_coords[1].radius/const.R_sun)
            elif field_line.polarity == -1:
                #print(field_coords[-2].radius/const.R_sun)
                Br_r0.append(field_line.b_along_fline[-2][0])
        #print(radius_ss)

    #print("\n\nTotal no. fieldlines",Total_field_count, "\nNo. of open fieldlines", Open_field_count)

    ### NOTE: Here, Br_rss is containing 2D magnetic field information, but it's a 1D list.
    #         But you also have the corresponding latitude and longitude list. Use it.
    #%%
    plt.scatter(lon_rcp, Br_rss, s=3)
    #plt.show()
    plt.savefig("./static/images/Brrss_"+str(cr)+".png")
    plt.close()
    if (Br_rss):
        return "success"
    else:
        return "fail"
    
 
address="http://127.0.0.1:2222/" #"http://127.0.0.1:2222/"
app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    x = str(request.args['text'])
    cr=convert(x)
    if (not os.path.exists("./static/images/Brrss_"+str(cr)+".png")):
        ret=func(int(cr))
    ret="success"
    try:
        if ret=="success":
            response = flask.jsonify({
                "cr_number" : cr,
                "plot" : "Brrss",
                "message" : "the graphs you requested can be found at the following urls",
                "input_map":address+"getplot/?graph=inp_"+str(cr),
                "solar_surface_map":address+"getplot/?graph=outp_"+str(cr),
                "solar_surface_magnetic_field":address+"getplot/?graph=Brrss_"+str(cr),
                "velocity_at_1AU":address+"getplot/?graph=velocity_2053.png"
             })

    # Enable Access-Control-Allow-Origin
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
           return flask.jsonify({
               "cr number": cr,
               "message":"there was an error in processing your request"})
           
    except KeyError:
        return 'bye'
    

    
@app.route('/getplot/',methods=['GET'])
def getplot():
    loc=str(request.args['graph']).split("_")
    cr=loc[1]
    plot=loc[0]
    url="./static/images/"+str(plot)+"_"+str(cr)+".png"
    try:
        if url:
            return flask.send_file(url, mimetype='image/png')
        else:
            return flask.jsonify(
                {"cr number" : cr,
                 "plot" : plot,
                 "message" : "the graph you requested has either not been computed or doesn't exist"})
    except KeyError:
        return 'bye'
class A:
    def one(port):
        app.run(port=port)
        print("something")

    one(port=2222)