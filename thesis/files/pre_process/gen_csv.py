import sys
import osmium as osm
import pandas as pd
import time
from removeBulk import removeBulk

"""
To run this file, please download:
(1) Osmium library in this link: https://osmcode.org/osmium-tool/
This file pre-process the data source (amenities.osh.pbf) to the required csv files for the analyses.
"""

def main():
    """
    transform and extract the records in that period, then filter out those auto-agents and bulk imports
    
    1. Transformation phase:
    Transform the 'amenities.osh.pbf' to the history, pre-pandemic period, and post-pandemic period,
    observe whether there is an auto-agent 

    2. filtering phase:
    Remove bulk imports in pre-pandemic and post-pandemic.
    In post-pandemic, 2 auto-agents were found and removed while no autoagents was found in pre-pandemic .
    """

    # Step 1: might take 3-4 mins to transform 200000 records in total to 3 csv files
    transformation('history', '2006-01-01','2020-04-01')
    transformation('precovid', '2019-04-01','2020-04-01')
    transformation('postcovid', '2020-04-01','2021-04-01')

    # Step 2 : might take 3-4 mins to filter these records
    # df_pre = pd.read_csv('../csv_files/precovid.csv')
    # df_filtered = removeBulk('precovid',df_pre)
    # export_modEdits_csv(df_filtered, outputname='precovid_filtered')

    # df_post = pd.read_csv('../csv_files/postcovid.csv')
    # df_filtered = removeBulk('postcovid',df_post)
    # export_modEdits_csv(df_filtered,outputname='postcovid_filtered')


class TimelineHandler(osm.SimpleHandler):
    """
    Use the simplehandler inherited from Osmium to copy the OSM information in the data source to a Python list (self.records)
    required tags include: node_id, version, timestamp, userId, amenity type, name, disused
    """
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.records = []

    def node(self,n):
        self.records.append([n.id, n.version, pd.Timestamp(n.timestamp), n.uid, n.tags['amenity'], n.tags.get('name',''),n.tags.get('disused','')])


def readToDF(tlhandler):
    """
    Read the timelinehandler into a Pandas dataframe and sort the records by timestamp
    """
    colnames = ['nodeId','version','timestamp','userId','amenityType','name','disused']

    df = pd.DataFrame(tlhandler.records, columns = colnames)
    df.index = df.index + 1
    df = df.sort_values(by=['timestamp'])
    return df

def timeFilter(df,time_start,time_end):
    """
    Extract the corresponding period: pre-pandemic and post-pandemic 
    """
    df = df[(df['timestamp'] > time_start) & (df['timestamp'] <= time_end)]
    df.index = df.index + 1
    df = df.sort_values(by=['timestamp'])
  
    return df

def appendCol(df_old,columnName):
    """
    Append a new column for aggregated edits of each user;
    two sceneraios:
    1. Append a 'numEdits' column when generating 'precovid.csv' or 'postcovid.csv'
    2. Append a 'mod_numEdits' column when generating 'precovid_filtered.csv' or 'postcovid_filtered.csv'

    the column name is specified in the parameter: columnName
    """

    df_new = blankDF()

    # Calculate the number of edits for each user
    dict_ids_edits = {}
    for userid in sorted(set(df_old.userId)):
        edits = len(df_old[df_old['userId'] == userid])
        dict_ids_edits[userid] = edits

    # Iterate over each user to find all their edits
    for key in dict_ids_edits:
        df_user = df_old[df_old['userId'] == key]
        
        for i in range(len(df_user)):
            # transform the record in the dataframe to a dictionary
            dict_new = {h:k for k,h in zip(df_user.iloc[i],df_new.columns)}
            dict_new[columnName] = dict_ids_edits[key]
            # Append the records(dict form) to the new dataframe
            df_new = df_new.append(dict_new,ignore_index=True)

    return df_new

def blankDF():
    """
    Create a new blank dataframe with the required columns 
    """
    d = {'nodeId': [],'version':[],'timestamp':[],'userId':[],'amenityType':[],'name':[],'disused':[],'numEdits':[]}
    df_new = pd.DataFrame(data=d)
    
    return df_new

def export_numEdits_csv(df_filtered, outputname):
    """
    In the transformation phase, this function exports a csv with a 'numEdits' column
    The numEdits value is the number of edits for the user editing that record
    """
    
    df_appended = appendCol(df_filtered,columnName='numEdits')
    df_appended.index = df_appended.index +1
    df_appended = df_appended.astype({'nodeId': 'int64','version':'int64','numEdits':'int64','userId':'int64'})
    df_appended = df_appended.sort_values(by=['userId'])
    # Export it to a csv file
    df_appended.to_csv('../csv_files/'+outputname+'.csv',index=False)

# Output a csv with 'mod_numEdits' column
def export_modEdits_csv(df_filtered,outputname):
    """
    In the filtering phase, this function exports a csv with an additional 'mod_numEdits' column.
    As we remove some edits when filtering, we need to re-calculate the number of edits for each user.
    """

    df_filtered_app = appendCol(df_filtered,columnName='mod_numEdits')
    df_filtered_app = df_filtered_app.astype({'nodeId': 'int64','version':'int64','userId':'int64','numEdits':'int64','mod_numEdits':'int64'})
    df_filtered_app = df_filtered_app.sort_values(by=['timestamp'])
    df_filtered_app.to_csv('../csv_files/'+outputname+'.csv')

def transformation(option, time_start, time_end):
    """
    transform 'amenities.osh.pbf' to csv files based on the period (option)and its corresponding time (time_start, time_end)
    
    1. Transform the amenities.osh.pbf into a timelinehandler

    2. Read the handler to a dataframe containing all history amenities

    3. Filter out by the period
    """
    # 1
    tlhandler = TimelineHandler()
    tlhandler.apply_file("../pbf_files/amenities.osh.pbf",locations=False)

    # 2
    df_all_amenities = readToDF(tlhandler)
    df_time_filtered = timeFilter(df_all_amenities,time_start,time_end)

    # 3
    if option == 'history':
        df_time_filtered.to_csv('../csv_files/'+option+'.csv',index=False)
    else:
        df_blank = blankDF()
        export_numEdits_csv(df_time_filtered, outputname=option)


if __name__ == '__main__':

    main()

