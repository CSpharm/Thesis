##  Pre-process procedures

Before executing gen_csv.py, ensure the Osmium 1.13.1 (https://osmcode.org/osmium-tool/) is installed.

(![image](https://github.com/CSpharm/Thesis/blob/main/thesis/files/pre_process/readme_preprocess.png))


(or see the readme_preprocess.png in this folder)

As the original data source is too big, this zip file only contains the data in phase 2 and phase 3.

Phase 2: Use gen_csv.py to transform 'amenities.osh.pbf' to different periods including history, pre-pandemic, and post-pandemic

Phase 3: Use gen_csv.py to filter genuine edits in 'precovid.csv' and 'postcovid.csv' into 'precovid_filtered.csv' and 'postcovid_filtered.csv'

(Note: These csv files were already generated and put in the csv_files folder. This is an optional step.) 


(For supplement: In phase 1, we use Osmium to filter out the nodes with an amenity value; 
the command is osmium tags-filter -o amenities.osh.pbf  greater-london-internal.osh.pbf  n/amenity)
