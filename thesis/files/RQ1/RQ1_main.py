import pandas as pd
from matplotlib import pyplot as plt
from RQ1_def import RQ1

"""
This python file generates preliminary and final results of RQ1, provides the data for Figure 4.1 and Table 5.1
"""

def main():
    """
    This function will be called first, whenever the script is run from the command line.
    There are 3 steps in RQ1:

    1. To study users’ maintenance behaviour, first we investigate whether all users contributed equally.
    We find the number of edits of each contributor in pre- and post-pandemic respectively.

    2. (Figure 4.1) Plot the number of edits for each contributor in both periods, most OSM contributions were made by a small number of core and highly engaged users.
    We group pre-pandemic users and post-pandemic users into four different classes of engagement

    3. (Table 5.1) Obtain the statistics for each engagement group in both periods 

    """
    
    # Step 1
    pre = RQ1('../csv_files/precovid_filtered.csv','precovid')
    post = RQ1('../csv_files/postcovid_filtered.csv','postcovid')
    
    pre.findIdEdits()
    post.findIdEdits()
    # Step 2
    plot(pre.dict_id_edits,post.dict_id_edits)
    # Step 3
    pre.group()
    post.group()

def plot(dict_pre,dict_post):
    """
    Plot the two dictionaries to a figure
    
    Parameters:
    dict_pre - the dictionary stores the user Id and his/her corresponding edits in pre-pandemic 
                keys: userId; value: their number of edits
    dict_post - the dictionary stores the user Id and his/her corresponding edits in post-pandemic 
                keys: userId; value: their number of edits
    """

    ax1 = plt.subplot(121)
    plt.bar(range(len(dict_pre)), list(dict_pre.values()), width=0.5, align='center', color='blue')
    plt.yscale("log")
    plt.title("pre-pandemic users' behaviour",fontsize=10)
    plt.ylabel("Number of edits")
    plt.xlabel("individual user",fontsize=10)

    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

    # horizontal line for easier grouping 
    plt.axhline(y=1,c="g",ls="--",lw=2)
    plt.axhline(y=10,c="r",ls="--",lw=2)
    plt.axhline(y=100,c="y",ls="--",lw=2)

    ax2 = plt.subplot(122,sharey=ax1)
    plt.bar(range(len(dict_post)), list(dict_post.values()), width=0.5, align='center', color='blue')
    plt.title("post-pandemic users' behaviour",fontsize=10)
    plt.xlabel("individual user",fontsize=10)

    plt.tick_params(
    axis='x',          
    which='both',      
    bottom=False,     
    top=False,        
    labelbottom=False)

    # horizontal line for easier grouping 
    plt.axhline(y=1,c="g",ls="--",lw=2)
    plt.axhline(y=10,c="r",ls="--",lw=2)
    plt.axhline(y=100,c="y",ls="--",lw=2)
    plt.savefig('RQ1_group (Figure 4.1).png',dpi=500)
    # plt.show()
    plt.clf()

if __name__ == '__main__':

  main()
