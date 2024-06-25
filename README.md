# Aero

<p align = "center" >
<img
src = "https://i.imgur.com/VnzsLOe.gif"
width="820" height="350">
</p>
<!-- "https://64.media.tumblr.com/abd72a218e862bd086a77f691489ff7e/tumblr_o7zzex1bXk1v3yf2mo1_500.gifv" -->

![Python version](https://img.shields.io/badge/python-blue)
![OpenSky version](https://img.shields.io/badge/opensky_api-gray)


## Table of Contents
1. About
2. Requirements
3. Examples
4. Project Status

## 1. About
In this repository we gather various projects focusing on aviation and aeronautical topics. To achieve this, we make use of a wide range of tools and techniques to approach real life scenarios or to make our own models. 

Each project is distinguised by its own directory and comprises a series of annotated notebooks detailing the objectives and explanations for each step of the workflow. Notebooks may be supplemented by Python scripts for instances where code automation is necessary.

Since the data is collected from a variety of sources, a specific folder for the data shall be created for every project. In recognition of the work done by the community, and to facilitate access to the data for future efforts, all sources will be acknowledged and source links will be provided when possible. Note, however, that some datasets are processed using multiple data sources. In such cases, the sources shall be disclosed, with varying degrees of detail. Additionally, we reserve the right to disclose the processing code when relevant to the project. It will also be clarified if the used data was artificially produced.

## 2. Requirements

For the correct execution and reproducibility of the notebooks, we recommend the use of the [Anaconda](https://www.anaconda.com/download) distribution system.

It is advisable to use systems with hardware capable of supporting the demands of complex algorithms, which may require significant memory and processing power. 
Alternatively, cloud environments can be employed. 

The required libraries are listed at the beginning of each notebook. We also recommend installing [`OpenSkyApi`](https://openskynetwork.github.io/opensky-api/python.html),  [`Folium`](https://python-visualization.github.io/folium/latest/getting_started.html) and/or [`Cartopy`](https://scitools.org.uk/cartopy/docs/latest/installing.html) libraries.

## 3. Examples

### 1. Retrieve Air Traffic data using the OpenSky REST API

We present below an example for collecting real time data using the `Extract_air_traffic_data.py` script on console: 

```
python Extract_air_traffic_data.py Test_dataset.json '' {"columns" : ["Time", "icao24"]; "lat" : [-45, 45]; "max_vectors" : 2}
          
```
> - The first three arguments are the script name, the file name and file extension (as of now, only **.csv** and **.json** files are supported), and the file directory. If the latter parameter is empty **('')**, the generated file will be saved into the same directory as the script.
> - One should note that **parameters are entered as a dictionary, and must be separated by ";" instead of ","**. <br>
>  If no parameters are provided, the data retrieved will cover all the information available of the air traffic **around the globe**, updated every **10 seconds** (approx.) and limited by a time span of **3 hours** or a maximum of **400 calls**. 

## 4. Project Status
- The script allowing to collect real time air traffic data from the **OpenSky REST API** is complete. 

<br>


[Ongoing ...]

<p>
<img 
src = "https://i.makeagif.com/media/11-02-2015/k6LT-1.gif">
</p>

<!-- https://i.pinimg.com/originals/95/50/7b/95507b24e2a22b8eb9afc06d453693cd.gif -->
