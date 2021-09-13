import pandas as pd
from RQ4_def import *
from plotly.offline import plot

"""
To run this file, please install the package for plotly in this link :https://plotly.com/python/getting-started/
This file generates results for RQ4, including Figure 5.2 (shown in a html), and data for Table 5.5 and Table 5.6
"""

def main():
    """
    This question requires 5 steps:

    1. Initiate a data frame to read the pre-pandemic period datasource

    2. Generate a new data frame like this to put the users;
    
    2-1 find out all pre-pandemic users and put them into a new dataframe (each one is a row)
    2-2 categorise their 'preGroup'  based on 'preEdits' value
    2-3 find out their post-pandemic edits and categorise their 'postGroup' value
        if they did not contribute any edits, the postEdits and postGroup are 0 and 'NA'
    2-4 find out those post-pandemic users who DO NOT contribute in the pre-pandemic,
        append these users to the dataframe. Their postGroup is 'New'

    at this time this new data frame look like this : (e.g.)
	=======================================================================================================================================
	(index) || userId ||  preEdits    ||    preGroup   || postEdits ||  postGroup  || 
	=======================================================================================================================================
	   5328    123           1             'Beginners'       0             'NA'   
       1231    789           0                'NA'          78            'NEW'      

    The length of this dataframe is 1082, while the number of pre-pandemic users are 627. There 455 newcomers in post-pandemic.

    3. Check what proportion of pre-pandemic users migrate to other groups. Data is shown in Table 5.5

    4. Use alluvial diagram to visualise the migration dynamics (Figure 5.2)

    5. Apart from pre-pandemic users, check the engagement level of newcomers in the post-pandemic (Table 5.6)
    """
    # Step 1
    pre = Precovid()
    pre.readFile('../csv_files/precovid_filtered.csv')
    # Step 2-1
    pre.gen_new_df()
    pre.insertColumns()
    # Step 2-2
    pre.group('precovid')
    # Step 2-3
    post = Postcovid()
    post.readFile('../csv_files/postcovid_filtered.csv')
    post.genList()
    pre.appendPostEdits(post.li_post)
    pre.group('postcovid')

    # Step 2-4
    pre.appendNewComers(post.li_post)
    
    # Step 3
    print("\n=== Table 5.5: Summary statistics of the migration dynamics of pre-pandemic users === \n")
    dict_sta = calMig(pre.df_new)

    # Step 4
    print("\n=== Figure 5.2: Alluvial diagram of the dynamics on pre-pandemic users === \n")
    plot_allu(dict_sta)

    # Step 5
    print("=== Table 5.6: Post-pandemic newcomers and its corresponding proportion for each group of engagement level\n")
    newcomersLevel(post.li_post,pre.num_new_comers,pre.li_pre_ids)


def calMig(df_final):
    """
    Calculate the exact number of users and their corresponding proportion for group migration dynamics. (Table 5.5)
    e.g., len_begin_total :the number of pre-pandemic beginner users 
          len_begin_gone :the number of pre-pandemic beginner users who left OSM in post-pandemic
          len_begin_light: the number of pre-pandemic beginner users who became light users in post-pandemic
          len_begin_remain: the number of pre-pandemic beginner users who remain in the same group in post-pandemic
          len_begin_incre: the number of pre-pandemic beginner users who increase their edits in post-pandemic
          (this can be derived from len_begin_total - len_begin_gone - len_begin_remain)

    """

    dict_sta = {}

    len_begin_total = len(df_final[df_final['pre_group'] == 'Beginners'])
    len_begin_gone = len(df_final[(df_final['pre_group'] == 'Beginners') &(df_final['post_group'] == 'NA')])
    len_begin_remain = len(df_final[(df_final['pre_group'] == 'Beginners') &(df_final['post_group'] == 'Beginners')])
    len_begin_light =  len(df_final[(df_final['pre_group'] == 'Beginners') &(df_final['post_group'] == 'Light users')])
    len_begin_mid =  len(df_final[(df_final['pre_group'] == 'Beginners') &(df_final['post_group'] == 'Middle users')])
    len_begin_heavy =  len(df_final[(df_final['pre_group'] == 'Beginners') &(df_final['post_group'] == 'Heavy users')])
    len_begin_incre = len_begin_total - len_begin_gone - len_begin_remain

    dict_sta['beginners'] = (len_begin_gone,len_begin_remain,len_begin_light,len_begin_mid,len_begin_heavy)

    li_begin_per = []
    for length in [len_begin_gone,len_begin_remain,len_begin_incre]:
        li_begin_per.append(str(round((length/len_begin_total *100),1)) +' %')
    print("The orders of columns: % left OSM, % lowered edits, % remained edits, % increased edits ")
    print(f'Beginners: {li_begin_per[0]} Not applicable {li_begin_per[1]} {li_begin_per[2]}')

    len_light_total = len(df_final[df_final['pre_group'] == 'Light users'])
    len_light_gone = len(df_final[(df_final['pre_group'] == 'Light users') &(df_final['post_group'] == 'NA')])
    len_light_lower = len(df_final[(df_final['pre_group'] == 'Light users') &(df_final['post_group'] == 'Beginners')])
    len_light_remain = len(df_final[(df_final['pre_group'] == 'Light users') &(df_final['post_group'] == 'Light users')])
    len_light_mid = len(df_final[(df_final['pre_group'] == 'Light users') &(df_final['post_group'] == 'Middle users')])
    len_light_heavy = len(df_final[(df_final['pre_group'] == 'Light users') &(df_final['post_group'] == 'Heavy users')])
    len_light_incre = len_light_total - len_light_gone - len_light_lower - len_light_remain

    dict_sta['light users'] = (len_light_gone,len_light_lower,len_light_remain,len_light_mid,len_light_heavy)

    li_light_per = []
    for length in [len_light_gone,len_light_lower,len_light_remain,len_light_incre]:
        li_light_per.append(str(round((length/len_light_total *100),1)) +' %')
    print(f'Light users: {li_light_per[0]} {li_light_per[1]} {li_light_per[2]} {li_light_per[3]}')

    len_mid_total = len(df_final[df_final['pre_group'] == 'Middle users'])
    len_mid_gone = len(df_final[(df_final['pre_group'] == 'Middle users') &(df_final['post_group'] == 'NA')])
    len_mid_begin = len(df_final[(df_final['pre_group'] == 'Middle users') &(df_final['post_group'] == 'Beginners')])
    len_mid_light = len(df_final[(df_final['pre_group'] == 'Middle users') &(df_final['post_group'] == 'Light users')])
    len_mid_remain = len(df_final[(df_final['pre_group'] == 'Middle users') &(df_final['post_group'] == 'Middle users')])
    len_mid_incre = len(df_final[(df_final['pre_group'] == 'Middle users') &(df_final['post_group'] == 'Heavy users')])
    len_mid_lower = len_mid_total - len_mid_gone - len_mid_remain - len_mid_incre 

    dict_sta['middle users'] = (len_mid_gone,len_mid_begin,len_mid_light,len_mid_remain,len_mid_incre)

    li_mid_per = []
    for length in [len_mid_gone,len_mid_lower, len_mid_remain,len_mid_incre]:
        li_mid_per.append(str(round((length/len_mid_total *100),1)) +' %')
    print(f'Middle users: {li_mid_per[0]} {li_mid_per[1]} {li_mid_per[2]} {li_mid_per[3]}')

    len_heavy_total = len(df_final[df_final['pre_group'] == 'Heavy users'])
    len_heavy_gone = len(df_final[(df_final['pre_group'] == 'Heavy users') &(df_final['post_group'] == 'NA')])
    len_heavy_begin = len(df_final[(df_final['pre_group'] == 'Heavy users') &(df_final['post_group'] == 'Beginners')])
    len_heavy_light = len(df_final[(df_final['pre_group'] == 'Heavy users') &(df_final['post_group'] == 'Light users')])
    len_heavy_mid = len(df_final[(df_final['pre_group'] == 'Heavy users') &(df_final['post_group'] == 'Middle users')])
    len_heavy_remain = len(df_final[(df_final['pre_group'] == 'Heavy users') &(df_final['post_group'] == 'Heavy users')])
    len_heavy_lower = len_heavy_total - len_heavy_gone - len_heavy_remain 

    dict_sta['heavy users'] = (len_heavy_gone,len_heavy_begin,len_heavy_light,len_heavy_mid,len_heavy_remain)
    li_heavy_per = []
    for length in [len_heavy_gone, len_heavy_lower, len_heavy_remain]:
        li_heavy_per.append(str(round((length/len_heavy_total *100),1)) +' %')
    print(f'Heavy users: {li_heavy_per[0]} {li_heavy_per[1]} {li_heavy_per[2]} Not applicable')

    return dict_sta

def plot_allu(dict_sta):
    """
    Use plotly package and the data in table 5.5 to plot
    """
    nodes = [
        ['ID', 'Label', 'Color'],
        [0,'Pre_Beginners','#F27420'],
        [1,'Pre_Light users','#adcfe9'],
        [2,'Pre_Middle users','#c469da'],
        [3,'Pre_Heavy users','#29c205'],
        [4,'Post_Beginners','#F27420'],
        [5,'Post_Light users','#4994CE'],
        [6,'Post_Middle users','#9e05c2'],
        [7,'Post_Heavy users','#29c205'],
        [8,'Left OSM in post-pandemic','#D3D3D3']
    ]
    links = [
        ['Source','Target','Value','Link Color'],
        [0,8,dict_sta['beginners'][0],'rgba(253, 227, 212, 0.5)'],
        [0,4,dict_sta['beginners'][1],'rgba(242, 116, 32, 0.5)'],
        [0,5,dict_sta['beginners'][2],'rgba(242, 116, 32, 0.5)'],
        [0,6,dict_sta['beginners'][3],'rgba(242, 116, 32, 0.5)'],
        [0,7,dict_sta['beginners'][4],'rgba(242, 116, 32, 0.5)'], 
        [1,8,dict_sta['light users'][0],'rgba(173, 207, 233, 0.5)'],
        [1,4,dict_sta['light users'][1],'rgba(173, 207, 233, 0.5)'],
        [1,5,dict_sta['light users'][2],'rgba(173, 207, 233, 0.5)'],
        [1,6,dict_sta['light users'][3],'rgba(173, 207, 233, 0.5)'],
        [1,7,dict_sta['light users'][4],'rgba(7173, 207, 233, 0.5)'],  
        [2,8,dict_sta['middle users'][0],'rgba(196, 105, 218, 0.5)'],
        [2,4,dict_sta['middle users'][1],'rgba(196, 105, 218, 0.5)'],
        [2,5,dict_sta['middle users'][2],'rgba(196, 105, 218, 0.5)'],
        [2,6,dict_sta['middle users'][3],'rgba(196, 105, 218, 0.5)'],
        [2,7,dict_sta['middle users'][4],'rgba(196, 105, 218, 0.5)'], 
        [3,8,dict_sta['heavy users'][0],'rgba(41, 194, 5, 0.5)'],
        [3,4,dict_sta['heavy users'][1],'rgba(41, 194, 5, 0.5)'],
        [3,5,dict_sta['heavy users'][2],'rgba(41, 194, 5, 0.5)'],
        [3,6,dict_sta['heavy users'][3],'rgba(41, 194, 5, 0.5)'],
        [3,7,dict_sta['heavy users'][4],'rgba(41, 194, 5, 0.5)'], 
    ]

    nodes_headers = nodes.pop(0)
    nodes_df = pd.DataFrame(nodes, columns = nodes_headers)
    links_headers = links.pop(0)
    links_df = pd.DataFrame(links, columns = links_headers)

    data_trace = dict(
        type='sankey',
        domain = dict(
          x =  [0,1],
          y =  [0,1]
        ),
        orientation = "h",
        valueformat = ".0f",
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0
          ),
          label =  nodes_df['Label'].dropna(axis=0, how='any'),
          color = nodes_df['Color']
        ),
        link = dict(
          source = links_df['Source'].dropna(axis=0, how='any'),
          target = links_df['Target'].dropna(axis=0, how='any'),
          value = links_df['Value'].dropna(axis=0, how='any'),
          color = links_df['Link Color'].dropna(axis=0, how='any'),
      )
    )

    layout =  dict(
        title = "How did pre-pandemic users change their behaviour in post-pandemic",
        height = 700,
        font = dict(
          size = 20
        ),    
    )

    fig = dict(data=[data_trace], layout=layout)
    plot(fig, validate=False)

def newcomersLevel(li_post,num_newcomers,li_pre_ids):
    """
    Analyse the engagement level of newcomers
    li_post: post-pandemic users and their edits :[ [userId1, edits1],[userId2,edits2],..]
    num_newcomers: number of users appeared in post-pandemic without any contribution in pre-pandemic
    li_pre_ids: list of pre-pandemic userIds 
    """
    d = {'Newcomers in the post-pandemic period':[],'Number of users':[],'Percentage':[]}
    df_new = pd.DataFrame(data=d)

    len_begin = 0
    len_light = 0
    len_mid = 0
    len_heavy = 0

    for user_post in li_post:
        if user_post[0] not in li_pre_ids:
            userid_new = user_post[0]

            if user_post[1] ==1:
                len_begin +=1
            elif 1 < user_post[1] <= 10:
                len_light +=1
            elif 10 < user_post[1] <= 100:
                len_mid +=1
            elif 100 < user_post[1] <= 10000:
                len_heavy +=1
    
    li_begin = ['Beginners', len_begin, str(round(len_begin/num_newcomers *100,1))+' %']
    li_light = ['Light users', len_light, str(round(len_light/num_newcomers *100,1))+' %']
    li_mid = ['Middle users', len_mid, str(round(len_mid/num_newcomers *100,1))+' %']
    li_heavy = ['Heavy users', len_heavy, str(round(len_heavy/num_newcomers *100,1))+' %']
    li_all = ['All', num_newcomers, '100 % ']

    for li in [li_begin,li_light,li_mid,li_heavy,li_all]:
        df_new.loc[len(df_new)] = li
        df_new = df_new.astype({'Number of users': 'int64'})

    print(df_new)
    
if __name__ == '__main__':
    main()