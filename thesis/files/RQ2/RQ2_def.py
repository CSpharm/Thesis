import pandas as pd
import collections
from Levenshtein import distance as lev

"""
This file defines the principles to distinguish three types of actions: add, update, and remove.
To execute this file, please download the levenshtein package here: https://pypi.org/project/python-Levenshtein/
"""
	
class RQ2():

	def __init__(self,filename):
		"""
		self.df : 
			the dataframe to be examined

		self.dict_distance: 
			count the number of records at each distance; key: distance; value: corresponding number of records 

		self.num_no_previous: 
			count the number of the records that do not have their previous version in a whole period

		self.li_detail: 
			observe those records with a levenshtein distance to see if there are some misclassifications;
			it stores tuples of (node_id, distance_lev, name_old, name_new, self.df_node_recId) and looks like:
			[(3217489962, 1, 'Papa Johns', "Papa John's", 1751),(6432424587, 1, 'The pyramid', 'The Pyramid', 10749),...] 

		self.df_new:
			a new dataframe to put the records and their corresponding action

		self.df_history:
			a history dataframe from the history period
			(the method will compare a record with its previous version; we use the history file containing all edits from 2006 to Mar 30 2020)
		"""
		
		self.df = pd.read_csv(filename)
		self.df = self.df.rename(columns = {'Unnamed: 0':'recordId'})

		self.dict_distance = {} 
		self.num_no_previous = 0
		self.li_detail = []
		self.data = {'recordId': [], 'nodeId': [],'version':[],'timestamp':[],'userId':[],'amenityType':[],'name':[],'disused':[],'numEdits':[],'mod_numEdits':[],'action':[]}
		self.df_new = pd.DataFrame(data=self.data)
		self.df_new = self.df_new.astype({'recordId': 'int64', 'nodeId': 'int64','version':'int64','numEdits':'int64','mod_numEdits':'int64'})
		
		self.df_history = pd.read_csv('../csv_files/history.csv')
		self.df_history = self.df_history.sort_values(['timestamp'], ascending=True)

	def cateActions(self):
		"""
		For each node in the dataframe, examine each record for that particular node, 
		then categorise its corresponding action and insert that record into a new dataframe (self.df_new) 
		there are mainly 5 steps when examining a record:

		1. Check if 'disused' in 'amenity type' tag or 'disused' tag is 'yes': If so, consider as a removal
		2. Check if 'version' is 1: If so, consider it as an adding
		3. Check if the node has only one record in that period: If so, search its history from the history dataframe to compare
		4. Check if its version is the smallest in that period: If so, search its history from the history dataframe to compare
		5. If all the conditions above are not statisfied, the version must not be the smallest one of the records;
		   its previous record must be in this dataframe and thus we do not have to search from the history dataframe. 
		   Instead, use the self.df_node to compare 

		* If the previous edits of a record is missing, we add it to the self.num_no_previous; 
		  there are 199 and 319 records in pre- and post-pandemic respectively
		"""

		for node_id in set(self.df.nodeId):
			"""
			self.df_node looks like:
			=======================================================================================================================================
			recordId || nodeId || version ||        timestamp         || userId || amenityType  || name || disused || numEdits || mod_numEdits ||
			=======================================================================================================================================
			5328      7251951619      1     2020-02-29 00:02:53+00:00     322039  bicycle_parking   NaN      NaN       4826           965
			5305      7251951619      2     2020-03-05 02:03:58+00:00     322039  bicycle_parking   NaN      NaN       4826           965
			"""
			
			self.df_node = self.df[self.df['nodeId'] == node_id]

			for i in range(len(self.df_node)):
				self.df_node_recId = self.df_node.iloc[i,0]
				self.df_node_ver =  self.df_node.iloc[i,2]
				self.df_node_type =  self.df_node.iloc[i,5]
				self.df_node_dis =  self.df_node.iloc[i,7]

				if ('disused' in self.df_node_type) or (self.df_node_dis == 'yes'):
					self.action(i,"remove")

				elif self.df_node_ver == 1:
					self.action(i,"add")

				elif len(self.df_node) ==1:
					self.searchFromHis(i,node_id)
					break

				else:
					if i==0:
						self.searchFromHis(i,node_id)

					else:
						"""
						1. Check if the amenity type is different: 
							If so, consider it as a removal and a addition.

						2.  If not, analyse the amenity name
						"""
						type_new = self.df_node.iloc[i,5] 
						type_old = self.df_node.iloc[i-1,5]

						if type_new != type_old :
							self.action(i,"remove")
							self.action(i,"add")

						else:
							name_new = self.df_node.iloc[i,6]
							name_old = self.df_node.iloc[i-1,6]
							self.nameAnalysis(i,name_old,name_new,node_id)

		print(f'the number of the data failed to find their previous version: {self.num_no_previous}')

		# As we aim to observe the distance from 1 to 10, use distance value x[1] to sort the list (ascending)
		self.li_detail.sort(key = lambda x: x[1]) 
		# Use distance value to sort the dict_distance (ascending)
		self.od = collections.OrderedDict(sorted(self.dict_distance.items()))

	def searchFromHis(self,i,node_id):
		"""
		Search the node's history records in the history dataframe, check all existing versions and transform it to a list (li_h_node)

		self.df_h_node looks like this:
		=====================================================================================================================
		(Index, not a column) || nodeId || version ||        timestamp         || userId || amenityType  || name || disused ||
		=====================================================================================================================
		27240    				587759630        1    2009-12-12 16:37:59+00:00     1185        bank        NatWest     NaN
		42744    				587759630        2    2011-03-28 23:37:47+00:00    72963        bank        NatWest     NaN  
		"""
		
		self.df_h_node = self.df_history[self.df_history['nodeId']== node_id]
		self.li_h_node = sorted(self.df_h_node['version'].tolist(),reverse = True)
		self.compare_his(i,node_id)

	def action(self,i,action):
		"""
		Append the record with its corresponding action to the new dataframe (self.df_new)
		"""
		dict_temp = {k:h for h,k in zip(self.df_node.iloc[i],self.df_new.columns)}
		dict_temp['action'] = action
		self.df_new = self.df_new.append(dict_temp,ignore_index=True)

	def compare_his(self,i,node_id):
		
		"""
		Assume now we examine this record:
		=======================================================================================================================================
		recordId || nodeId || version ||        timestamp         || userId || amenityType  ||  name  || disused || numEdits || mod_numEdits ||
		=======================================================================================================================================
		17464	   247328377	9		2019-04-02 15:26:52+00:00	 9451067	   pub	      The Alex		NaN       14	       14

		As its current version (= self.df_node_ver) is 9, we need to find out its version 8 to compare.
		If version 8 is missing we need to find its version 7....until we find it.
		If all versions include 1 to 8 are not found then we add 1 to num_no_previous. 
		"""

		# In this case, w will change from 8, 7, 6,..., to 1 if no record is found 
		for w in range(self.df_node_ver-1,0,-1):

			# li_h_node contains existing versions in the history period, in this case it's [8,7,6,5,4,3,2,1]
			if w in self.li_h_node:

				# Check if amenity type is different: If so, it was a removal and an addition
				if self.df_node.iloc[i,5] != self.df_h_node[self.df_h_node['version'] == w].iloc[0,4]:
					self.action(i,"remove")
					self.action(i,"add")
					break
					
				else:
					#(2)Check amenity name
					name_new = self.df_node.iloc[i,6]
					name_old = self.df_h_node[self.df_h_node['version'] == w].iloc[0,5]

					self.nameAnalysis(i,name_old,name_new,node_id)
					break
		else:
			self.num_no_previous +=1

	def dis_cal(self,i,name_old,name_new,node_id):
		"""
		Calculate the levenshtein distance to determine whether it's an update or a removal and an addition,
		then call the action function to insert the record with its corresponding action to self.df_new

		** Import the levenshtein distance package to run this function
		
		name_old: the name value of the previous record
		name_new: the name value of the current examined record 
		i: the location of the self.df_node
		node_id: the nodeId of this current examined record

		self.li_detail: list to store the details of records with a levenshtein distance
		self.dict_distance: dictionary to store the number of records at each distance 
		"""
		distance_lev = lev(name_old, name_new)

		self.li_detail.append((node_id, distance_lev, name_old, name_new, self.df_node_recId))

		if distance_lev not in self.dict_distance:
			self.dict_distance[distance_lev] = 1
		else:
			self.dict_distance[distance_lev] += 1

		if distance_lev <= 5:
			self.action(i,"update")
		else:
			self.action(i,"remove")
			self.action(i,"add")

	def nameAnalysis(self,i,name_old,name_new,node_id):
		"""
		Categorise the actions based on the two names
		* when a name is NaN (empty value), its data type in Python is float
		
		4 steps:

		1. Check if the old name is empty; if so : an update action
		2. If the old name is not empty, check if the new name is empty; 
			if so, this means the name was removed: a removal
		3. If the two names are both not empty, check if one is the substring of the other;
			if so: an update action; if not: use Levenshtein distance to analyse
		"""

		if type(name_old) == float:
			self.action(i,"update")

		elif type(name_new) == float:
			self.action(i,"remove")

		elif (type(name_new) == str) &(type(name_old) == str) :

			if (name_old.find(name_new) != -1) or (name_new.find(name_old) != -1):
				self.action(i,"update")
			else:

				self.dis_cal(i,name_old,name_new,node_id)
	