import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from RQ2_def import *
from scipy import stats
from scipy.stats import mannwhitneyu

"""
This python file generates preliminary and final results of RQ2, including a distribution plot (Figure 4.8), a boxplot (Figure 5.1) and the data for Table 5.2
Total executing is around 5-6 mins for this file.
"""

def main():
    """
    This function will be called first, whenever the script is run from the command line. There are 6 steps in this research question.
    1. 
    Read the datasource into a dataframe, compare it to its previous edits, categorise the actions of adding, updating, or removal.
    The detail is in actions_definition.py

    2. Levenshtein distance is used to determine the difference between two names. After manual checking the records (Use li_detail), 
    most records at a distance from 1 to 5 were genuine updating actions, while others at higher distance represent a removal and an addition.
    Thus 5 is chosen as the threshold; once the distance is over 5, the record is recognised as a removal and an addition.

    3. There are several misclassificated cases, use 'manFix' function to fix them.

    4. The actions were grouped on the editor's contribution frequency; 
    If a record was edited by user 1234 and he / she had 200 edits in that period (assume the record is in pre-pandemic),
    this action (add/update/remove) would be counted in the heavy user group in pre-pandemic.

    5. Mean significance test for both periods: generates the data in Table 5.2;
    To determine whether the mean values from pre-and post-pandemic periods are statistically siginficant,Mann-Whitney U test is conducted.

    6. Use boxplot (Figure 5.1) to visualise the actions of adding, updating, and removal between 4 engagement groups of users 
    """

    # Pre-pandemic period
    # Step 1 (might take 2-3 mins to categorise 16724 records)
    pre = RQ2('../csv_files/precovid_filtered.csv')
    pre.cateActions()

    # Step 2
    for detail in pre.li_detail[:10]:
        print(detail)
    plot_lev(pre.od)

    # Step 3
    df_new_fixed_pre = manFix(pre.df_new,option='precovid')

    # Step 4 
    li_pre_final = cal_group_actions(df_new_fixed_pre,option='precovid')

    # ================================================================
    # Post-pandemic period
    # Step 1 (might take 2-3 mins to categorise 25827 records)
    post = RQ2('../csv_files/postcovid_filtered.csv')
    post.cateActions()

    # Step 2 is similar to pre-pandemic period (commented to keep the result clear)
    # for detail in post.li_detail[:10]:
    #     print(detail)

    # Step 3
    df_new_fixed_post = manFix(post.df_new, option='postcovid')

    # Step 4 
    li_post_final = cal_group_actions(df_new_fixed_post,option='postcovid')

    # ================================================================
    # Step 5
    meanTest(li_pre_final,li_post_final)

    # Step 6
    li_merge = li_pre_final + li_post_final
    boxplot(li_merge)

    
def manFix(df_new,option):
    """
    In pre-pandemic period, record 5999 or those in li_change_to_rem_add are misclassified, which need to be categorised as removal and adding;
    records in li_change_to_update are misclassfications requiring to be defined as an update instead. Same in post-pandemic period.

    Parameters:
    df_new - the table for our actions categorisation
    option - specify which period

    Returns:
    df_new - the table for our actions categorisation
    """

    if option == 'precovid':
            
        df_new_fixed = change_to_remove_add(df_new,5999)
        li_change_to_rem_add = [158,1152,818,7096,9952,14550,10416]

        for i in li_change_to_rem_add:
            df_new_fixed = change_to_remove_add(df_new_fixed,i)

        li_change_to_update = [10584,9860,7385,6715,13829,13252,13364,12859,11891,7393,16602,9940,13484,11526]
        for j in li_change_to_update:
            df_new_fixed = change_to_update(df_new_fixed,j)

        return df_new_fixed
    
    elif option =='postcovid':

        df_new_fixed = change_to_remove_add(df_new,13736)
        li_change_to_rem_add = [13607,12773,11217,12127,7572,22734,14125]

        for i in li_change_to_rem_add:
            df_new_fixed = change_to_remove_add(df_new_fixed,i)

        li_change_to_update = [5444,14033,9916,24930,10006,20335,16263,14611,9914,3174,12031]

        for j in li_change_to_update:
            df_new_fixed = change_to_update(df_new_fixed,j)

        return df_new_fixed


def change_to_remove_add(df_new, recordId):
    """
    Change those misclassfications to the actions of a removal and an adding

    Parameters:
    df_new - the table for our actions categorisation
    recordId - the identifier of a specific record

    Returns:
    df_new - the table for our actions categorisation
    """

    df_one = df_new[df_new.recordId == recordId]
    df_rem = df_one.copy()
    df_rem['action'] = 'remove'
    df_add = df_one.copy()
    df_add['action'] = 'add'

    df_new_filtered = df_new[df_new.recordId != recordId]
    df_new_filtered = df_new_filtered.append(df_rem)
    df_new_filtered = df_new_filtered.append(df_add)

    return df_new_filtered

def change_to_update(df_new,recordId):
    """
    Change those misclassfications to the actions of an update

    Parameters:
    df_new - the table for our actions categorisation
    recordId - the identifier of a specific record

    Returns:
    df_new - the table for our actions categorisation
    """

    df_one = df_new[df_new.recordId == recordId]
    df_upd = df_one.iloc[0:1,:].copy()
    df_upd['action'] = 'update'
    
    df_drop = df_new[df_new.recordId != recordId]
    df_new_filtered = df_drop.append(df_upd)
    
    return df_new_filtered

def plot_lev(od):
    """
    Use the dictionary derived from the comparison to plot the levenshtein distance distribution plot 

    Parameters:
    od - a dictionary
        keys: the value of levenshtein distance, from 1 to 39;
        values: the number of the records with that distance
    
    """
    plt.bar(*zip(*od.items()))
    plt.title("Levenshtein distance distribution in the pre-pandemic period")
    plt.xlabel("Levenshtein distance")
    plt.ylabel("Number of pairs of edits")
    plt.savefig('RQ2_lavenshtein_dis(Figure 4.8).png',dpi=500)
    
def cal_group_actions(df,option):
    """
    Calculate the group behaviour in terms of actions of adding, updating, and removal
    Naming: A= beginners, B = light users, C = middle users, D = heavy users
    Classfication standard: A: (0,1], B: (1,10], C: (10,100], D: (100,10k]

    li_add, li_upd, li_rem are all nested lists. 
    E.g., li_add consists of four lists: li_add_A, li_add_B, li_add_C, li_add_D
    li_add_A stores the number of adding actions for each user in group A, which looks like [1,1,1,1,1,..]
    while li_upd_A stores the number of updating actions for each user in group A, and so on.

    We then calculate the mean of each type of actions for each user group for the data in Table 5.2
    """

    if option == 'precovid':
        print('This is the pre-pandemic period:')
    elif option == 'postcovid':
        print('This is the post-pandemic period:')

    A = df[df['mod_numEdits'] == 1]
    B = df[(df['mod_numEdits'] > 1) & (df['mod_numEdits'] <= 10)]
    C = df[(df['mod_numEdits'] > 10) & (df['mod_numEdits'] <= 100)]
    D = df[(df['mod_numEdits'] >= 100)]
    
    A.insert(11,'group','A')
    B.insert(11,'group','B')
    C.insert(11,'group','C')
    D.insert(11,'group','D')

    li_add_A = []
    li_upd_A = []
    li_rem_A = []

    li_add_B = []
    li_upd_B = []
    li_rem_B = []

    li_add_C = []
    li_upd_C = []
    li_rem_C = []

    li_add_D = []
    li_upd_D = []
    li_rem_D = []

    for userid in set(A.userId):
        
        li_add_A.append(len(A[(A['action'] == 'add') & (A['userId'] == userid)]))
        li_upd_A.append(len(A[(A['action'] == 'update') & (A['userId'] == userid)]))
        li_rem_A.append(len(A[(A['action'] == 'remove') & (A['userId'] == userid)]))
    
    for userid in set(B.userId):
        
        li_add_B.append(len(B[(B['action'] == 'add') & (B['userId'] == userid)]))
        li_upd_B.append(len(B[(B['action'] == 'update') & (B['userId'] == userid)]))
        li_rem_B.append(len(B[(B['action'] == 'remove') & (B['userId'] == userid)]))
        
    for userid in set(C.userId):
        
        li_add_C.append(len(C[(C['action'] == 'add') & (C['userId'] == userid)]))
        li_upd_C.append(len(C[(C['action'] == 'update') & (C['userId'] == userid)]))
        li_rem_C.append(len(C[(C['action'] == 'remove') & (C['userId'] == userid)]))

    for userid in set(D.userId):
        
        li_add_D.append(len(D[(D['action'] == 'add') & (D['userId'] == userid)]))
        li_upd_D.append(len(D[(D['action'] == 'update') & (D['userId'] == userid)]))
        li_rem_D.append(len(D[(D['action'] == 'remove') & (D['userId'] == userid)]))
    
    li_add = [li_add_A, li_add_B, li_add_C, li_add_D]
    li_upd = [li_upd_A, li_upd_B, li_upd_C, li_upd_D]
    li_rem = [li_rem_A, li_rem_B, li_rem_C, li_rem_D]

    print(f'the mean of li_add_A is:{round(np.mean(li_add_A, dtype=np.float64),2)}')
    print(f'the mean of li_add_B is:{round(np.mean(li_add_B, dtype=np.float64),2)}')
    print(f'the mean of li_add_C is:{round(np.mean(li_add_C, dtype=np.float64),2)}')
    print(f'the mean of li_add_D is:{round(np.mean(li_add_D, dtype=np.float64),2)}')

    print(f'the mean of li_upd_A is:{round(np.mean(li_upd_A, dtype=np.float64),2)}')
    print(f'the mean of li_upd_B is:{round(np.mean(li_upd_B, dtype=np.float64),2)}')
    print(f'the mean of li_upd_C is:{round(np.mean(li_upd_C, dtype=np.float64),2)}')
    print(f'the mean of li_upd_D is:{round(np.mean(li_upd_D, dtype=np.float64),2)}')

    print(f'the mean of li_rem_A is:{round(np.mean(li_rem_A, dtype=np.float64),2)}')
    print(f'the mean of li_rem_B is:{round(np.mean(li_rem_B, dtype=np.float64),2)}')
    print(f'the mean of li_rem_C is:{round(np.mean(li_rem_C, dtype=np.float64),2)}')
    print(f'the mean of li_rem_D is:{round(np.mean(li_rem_D, dtype=np.float64),2)}')

    return li_add, li_upd, li_rem

def meanTest(li_pre_final,li_post_final):
    """
    Use Mann-Whitney U test to conduct the mean signficance test

    parameters:
    li_pre_final: the nested list result from pre-pandemic period;
    li_post_final: the nested list result from post-pandemic period;

    they both look like this but one is pre-pandemic and the other is post-pandemic:
    [[li_add_A, li_add_B, li_add_C, li_add_D],[li_upd_A, li_upd_B, li_upd_C, li_upd_D],[li_rem_A, li_rem_B, li_rem_C, li_rem_D]]

    Hypothesis:
    H0:null hypothesis: No difference between sample means from two periods (Not statstically signficant)
    H1:alternative hypothesis: when we reject H0

    The confidence interval is 95%, we reject H0 if p-value < 0.05 
    """ 
    li_add_A_pre = li_pre_final[0][0]
    li_add_B_pre = li_pre_final[0][1] 
    li_add_C_pre = li_pre_final[0][2] 
    li_add_D_pre = li_pre_final[0][3]

    li_upd_A_pre = li_pre_final[1][0] 
    li_upd_B_pre = li_pre_final[1][1]
    li_upd_C_pre = li_pre_final[1][2]
    li_upd_D_pre = li_pre_final[1][3]

    li_rem_A_pre = li_pre_final[2][0] 
    li_rem_B_pre = li_pre_final[2][1]
    li_rem_C_pre = li_pre_final[2][2]
    li_rem_D_pre = li_pre_final[2][3]

    li_add_A_post = li_post_final[0][0]
    li_add_B_post = li_post_final[0][1] 
    li_add_C_post = li_post_final[0][2] 
    li_add_D_post = li_post_final[0][3] 

    li_upd_A_post = li_post_final[1][0] 
    li_upd_B_post = li_post_final[1][1]
    li_upd_C_post = li_post_final[1][2]
    li_upd_D_post = li_post_final[1][3] 

    li_rem_A_post = li_post_final[2][0] 
    li_rem_B_post = li_post_final[2][1]
    li_rem_C_post = li_post_final[2][2]
    li_rem_D_post = li_post_final[2][3] 

    li_p_values = [i for i in range(12)]
    
    U1, li_p_values[0] = mannwhitneyu(li_add_A_pre,li_add_A_post)
    U1, li_p_values[1] = mannwhitneyu(li_add_B_pre,li_add_B_post)    
    U1, li_p_values[2] = mannwhitneyu(li_add_C_pre,li_add_C_post)
    U1, li_p_values[3] = mannwhitneyu(li_add_D_pre,li_add_D_post)

    U1, li_p_values[4] = mannwhitneyu(li_upd_A_pre,li_upd_A_post)
    U1, li_p_values[5] = mannwhitneyu(li_upd_B_pre,li_upd_B_post)
    U1, li_p_values[6] = mannwhitneyu(li_upd_C_pre,li_upd_C_post)
    U1, li_p_values[7] = mannwhitneyu(li_upd_D_pre,li_upd_D_post)

    U1, li_p_values[8] = mannwhitneyu(li_rem_A_pre,li_rem_A_post)
    U1, li_p_values[9] = mannwhitneyu(li_rem_B_pre,li_rem_B_post)
    U1, li_p_values[10] = mannwhitneyu(li_rem_C_pre,li_rem_C_post)
    U1, li_p_values[11] = mannwhitneyu(li_rem_D_pre,li_rem_D_post)

    for p_value in li_p_values:
        if p_value < 0.05:
            print("reject H0: statistically different")
        else:
            print("accept H0: not statistically different")

def boxplot(li_merge):
    """
    Plot the group behaviour for the actions of adding, updating, and removal

    parameters:
    li_merge: a 3-layer list consists of li_pre_final and li_post_final:

    it look like this
    [[[li_add_A_pre, li_add_B_pre, li_add_C_pre, li_add_D_pre],[li_upd_A_pre, li_upd_B_pre, li_upd_C_pre, li_upd_D_pre],[li_rem_A_pre, li_rem_B_pre, li_rem_C_pre, li_rem_D_pre]],
    [[li_add_A_post, li_add_B_post, li_add_C_post, li_add_D_post],[li_upd_A_post, li_upd_B_post, li_upd_C_post, li_upd_D_post],[li_rem_A_post, li_rem_B_post, li_rem_C_post, li_rem_D_post]]]
    """
    
    classes = ['add', 'update', 'remove']

    # Draw 2rows x 3cols subplots.
    fig, ax = plt.subplots(int(len(li_merge)/len(classes)), len(classes), figsize=(12, 8), sharey='all')
    fig.suptitle('3 types of actions for each user group in the post-pandemic (row 1) and post-pandemic (row 2)', fontsize=16)

    for i_row in range(int(len(li_merge)/len(classes))):        
        for i_class in range(len(classes)):                       
            ax[i_row, i_class].boxplot(li_merge[3*i_row+i_class])  
            ax[i_row, i_class].set_title(f"user's behaviour: {classes[i_class]}", fontsize=14)
            ax[i_row, i_class].set_xlabel('user Group', fontsize=12)
            ax[i_row, i_class].set_ylabel(f"Number of {classes[i_class]}(s)", fontsize=12)
            ax[i_row, i_class].set_yscale("log")
            ax[i_row, i_class].set_xticks([1, 2, 3, 4])
            ax[i_row, i_class].set_xticklabels(['Beginners', 'Light users', 'Middle users', 'Heavy users'],fontsize=7)
            ax[i_row, i_class].grid(axis='y', linestyle='--', linewidth=1)

    # plt.xticks(fontsize= 8) 
    plt.subplots_adjust(hspace=0.5)
    plt.savefig("RQ2_boxplots(Figure 5.1).png", dpi=500)
    plt.show()
    plt.clf()

if __name__ == '__main__':
    main()