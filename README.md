# Thesis
COMP0073 MSc CS project for OSM user online post-pandemic changes

![image](https://github.com/CSpharm/Thesis/blob/main/code_listing.png)

This zip file is submitted for COMP0073 MSc Computer Science project.

	
## Required Tools
In order to execute the zip file, several tools are required to install, including: 

Python 3.8.5 : https://www.python.org/downloads/ 

Osmium 1.13.1 (development version) : https://osmcode.org/osmium-tool/

Levenshtein 0.12.2 : https://pypi.org/project/python-Levenshtein/

Rank-biased Overlap (RBO) package 0.1.2 : https://package.wiki/rbo

Plotly 5.3.1: https://plotly.com/python/getting-started/

(Note: once Python and Osmium are successfully installed, the PyOsmium module should be available without additional installation.)

## Code structure 
The zip is structured as shown in the above figure. The pre-process procedure in this project contains three phases with distinct aims: 
1) reduction phase; 2) transformation phase; 3) ﬁltering phase to identify and remove those edits not conducted by a human. 

As the original data source (greater-london-internal.osh.pbf) exceeds the limit of the zip (150 MB), 
the original data had been removed from the zip after the reduction phase. It can be downloaded on the Geofabrik server.

There are two main steps to execute this zip file: 

1) Execute gen_csv.py to transform and filter the data into csv files for different periods 
    (the csv files are already been generated so this is an optional step);
    
2) Execute the main.py in each folder (the command for seeing RQ1 results is 'python RQ1_main.py’); 
     these main files generate results including figures of each corresponding question.
