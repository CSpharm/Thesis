import pandas as pd

"""
This file defines the methods to obtain required statistics of the records in pre-pandemic and post-pandemic for RQ1 
"""

class RQ1():

	def __init__(self,filename, option):
		"""
		self.df: the dataframe in the period

		self.dict_id_edits: store the user Id and their edits 
			key: userId
			value: number of edits
		
		self.total_num_users: number of total users in the period

		self.option: specify pre-pandemic or post-pandemic
		"""

		self.df = pd.read_csv(filename)
		self.dict_id_edits = {}
		self.total_num_users = 0
		self.option = option

	def findIdEdits(self):
		"""
		Find each user in the corresponding dataframe(period) and calculate the number of their edits,
		(descending sort in self.dict_id_edits). 
		"""

		for userid in sorted(set(self.df.userId)):
			num_edits = len(self.df[self.df['userId'] == userid])
			self.dict_id_edits[userid] = num_edits

		self.dict_id_edits = dict(sorted(self.dict_id_edits.items(), key=lambda item: item[1],reverse=True))
		
	def group(self):
		"""
		Calculate the total length (= the total number of users in the dataframe),
		group the edits based on the user's contribution frequency
		"""

		print(f'This is the {self.option} ')
		self.total_num_users = len(set(self.df.userId))
		print(f'The number of the total users in the {self.option} :{self.total_num_users}')
		
		self.cal_proportion()

	def cal_proportion(self):

		self.df_begin = self.df[self.df['mod_numEdits'] == 1]
		self.df_light = self.df[(self.df['mod_numEdits'] >1) & (self.df['mod_numEdits'] <=10)]
		self.df_mid = self.df[(self.df['mod_numEdits'] >10) & (self.df['mod_numEdits'] <=100)]
		self.df_heavy = self.df[(self.df['mod_numEdits'] >100) & (self.df['mod_numEdits'] <=10000)]

		df_li = [self.df_begin, self.df_light, self.df_mid, self.df_heavy]
		
		for dataframe in df_li:

			num_users = len(set(dataframe.userId))
			percentage = num_users / self.total_num_users * 100

			print(f'Number of users in this group : {num_users}')
			print('Number of users / total users : {:.1f}%'.format(percentage))

