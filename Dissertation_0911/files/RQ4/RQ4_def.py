import pandas as pd

"""
This file defines the methods in RQ4
"""

class Precovid():

    def __init__(self):
        pass

    def readFile(self,file):
        self.df = pd.read_csv(file)
        self.df = self.df.sort_values(by=['userId'])
        self.num_new_comers = 0
        self.li_pre_ids = []
        self.li_pre_id_edits = []

    def gen_new_df(self):
        """
        Initiate a new dataframe (self.df_new) to put the users for statistics 
        after this function it looks like this but its length = 627 (total number of pre-pandemic users)
        =============================================
        	(index) || userId ||  preEdits    
        =============================================
        	   5328    123           1            
               1231    789           0                 
        """

        self.df_dropped = self.df[['userId','mod_numEdits']]
        self.df_dropped = self.df_dropped.astype({'userId': 'int64', 'mod_numEdits': 'int64'})

        for userId in sorted(set(self.df_dropped.userId)):

            num_edits = len(self.df_dropped[self.df_dropped['userId'] == userId])
            self.li_pre_id_edits.append((userId,num_edits))

        self.df_new = pd.DataFrame.from_records(self.li_pre_id_edits,columns=['userId','preEdits'])
        self.df_new.index += 1

    def insertColumns(self):
        """
        After this function, it looks like this:
        
        ==================================================================================
        	(index) || userId ||  preEdits  ||  pre_group ||  post_edits || post_group ||
        ==================================================================================
        	   5328    123           1            'NA'              0           'NA'
               1231    789           0            'NA'              0           'NA'
        """

        self.df_new.insert(2,'pre_group','NA')
        self.df_new.insert(3,'post_edits','0')
        self.df_new.insert(4,'post_group','NA')
       

    def group(self, option):
        """
        option = precovid:   obtain the preGroup value  based on the preEdits value
        option = postcovid:  obtain the postGroup value based on the postEdits value
        """

        if option == 'precovid':
            loc_edits = 1
            loc_group = 2
        
        elif option == 'postcovid':
            loc_edits = 3
            loc_group = 4
        
        for i in range(len(self.df_new)):
            
            num_edits = int(self.df_new.iloc[i,loc_edits])

            if num_edits ==1:
                self.df_new.iloc[i,loc_group] = 'Beginners'

            elif 1 < num_edits <= 10:
                self.df_new.iloc[i,loc_group]  = 'Light users'

            elif 10 < num_edits <= 100:
                self.df_new.iloc[i,loc_group] = 'Middle users'

            elif 100 < num_edits <= 10000:
                self.df_new.iloc[i,loc_group]  = 'Heavy users'

    def appendPostEdits(self,li_post):
        """
        Find out those who contribute both in pre-pandemic and post-pandemic,
        append their post-pandemic number of edits to 'postEdits' in self.df_new
        """
        for h in range(len(self.df_new)):
            userid_pre = self.df_new.iloc[h,0]

            for i in range(len(li_post)):
                userid_post = li_post[i][0]

                if userid_post == userid_pre:
                    
                    self.df_new.iloc[h,3] = li_post[i][1]
                    break
    
    def appendNewComers(self,li_post):
        """
        Find out those post-pandemic contributors who do not have any edits in pre-pandemic,
        append their records with a 'NEW' postGroup value to the df_new
        """
        
        for i in range(len(self.df_new)):
            self.li_pre_ids.append(self.df_new.iloc[i,0])
        
        for user_post in li_post:
            if user_post[0] not in self.li_pre_ids:
                li_appended = [user_post[0], 0, 'NA', user_post[1], 'NEW']
                ser_appended = pd.Series(li_appended, index= self.df_new.columns)
                self.df_new = self.df_new.append(ser_appended, ignore_index=True)
                self.num_new_comers +=1
                
        
class Postcovid(Precovid):

    def __init__(self):
        pass

    def readFile(self,file):
        self.df = pd.read_csv(file)
        self.df = self.df.sort_values(by=['userId'])
        self.num_new_comers = 0
        self.li_pre_id_edits = []
        self.li_post = []
    
    def genList(self):
        """
        Generates a list that consists of post-pandemic users' Ids and edits
        [[userId1, edit1], [userId2, edit2],...]
        """

        for userId in sorted(set(self.df.userId)):
            num_edits = len(self.df[self.df['userId'] == userId])
            self.li_post.append([userId,num_edits])
