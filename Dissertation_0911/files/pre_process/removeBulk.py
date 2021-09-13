import pandas as pd
import time 

"""
This file defines the principle to recognise bulk imports:
if a user conducts more than 60 edits in a minute, these edits were recognised as bulk imports
We need to remove them. This is a mix of manual check and programming check
"""

def removeBulk(option,df):

    # Add a new_timestamp column 
    def addTime(df):
        new_t = [int(time.mktime(time.strptime(str_t[:str_t.index('+')], "%Y-%m-%d %H:%M:%S"))) for str_t in df.timestamp]
        df['new_timestamp'] = new_t

        return df

    def filter_threshold(df, period: int = 60, num_threshold: int = 60) -> pd.DataFrame:
        """
        parameters
        df :a DataFrame.
        period: seconds
        num_threshold: the number of records edited by the user
        
        Output:
        return the result of df add dropout column.
        """

        res = []

        for userid in sorted(set(df.userId)):
            length = len(df[df['userId'] == userid])

            if length < num_threshold:   
                res += [False] * length 
            else:                        
                ts_list = df[df['userId'] == userid].new_timestamp.tolist()
                idx, record = 0, set()

                while idx < length:
                    temp = [i for i, j in enumerate(ts_list) if ts_list[idx] <= j <= ts_list[idx] + period]
                    temp_length = len(temp)
                    if temp_length >= num_threshold:
                        record = record | set(temp)
                    idx += 1
                temp_list = [True if i in record else False for i in range(length)]
                res += temp_list

        df['dropout'] = res
        # Keep the records that 'dropout' = false
        res_df = df[(df['dropout'] == False)].iloc[:, 0:9]
        
        return res_df

    def remove_agents(df,userid1, userid2):
        df = df[(df.userId != userid1) & (df.userId != userid2)]
        return df
    
    
    # After manual check, we found that there was not any auto-agent in precovid,
    # So we only remove those bulk imports (>60 edits/ a minute) in precovid
    if option == 'precovid':
        df_pre = addTime(df)
        df_pre_filtered = filter_threshold(df=df_pre, period=60, num_threshold = 60)
        df_pre_filtered = df_pre_filtered.astype({'nodeId': 'int64','version':'int64','numEdits':'int64','userId':'int64'})
        df_pre_filtered.index = df_pre_filtered.index + 1
        return df_pre_filtered

    # For postcovid, we manually found two autoagents and thus we removed them
    elif option == 'postcovid':
        df_post = remove_agents(df,5743376,11427273)
        df_post = addTime(df_post)
        df_post_filtered = filter_threshold(df=df_post, period=60, num_threshold = 60)
        df_post_filtered = df_post_filtered.astype({'nodeId': 'int64','version':'int64','numEdits':'int64','userId':'int64'})
        df_post_filtered.index = df_post_filtered.index + 1
        
        return df_post_filtered

