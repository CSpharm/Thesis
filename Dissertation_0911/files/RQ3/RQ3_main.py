import rbo
from scipy.stats import spearmanr as spe
from RQ3_def import *

"""
To run this file, please install rbo package in this link: https://package.wiki/rbo 
This Python file generates preliminary and final results for RQ3, including Figure 4.9, Figure 4.10, and the data for Table 5.3 and Table 5.4
"""

def main():
    """
    RQ3 requires 6 steps:

    1. Count the number of records of each amenity categories in pre- and post-pandemic respectively,
    store the category name and its number of edits in the dictionary

    2. Pair each category to its meta-category shown on OSM wiki page: https://wiki.openstreetmap.org/wiki/Key:amenity

    3. Plot all meta-categories and their corresponding number of edits in Figure 4.9,
       Plot top 20 categories and their corresponding number of edits in Figure 4.10.

    4. Use Spearman to check the correlation between two meta-category lists in pre- and post-pandemic

    5. As the two ranking lists were highly related in step 4, we switch to observe categories ranking;
       Move our focus from top 20 most edited ones --> top 10 most edited ones --> top 5 most edited ones 
       Use RBO in this step (Table 5.3)

    6. As there is a difference for the ranking of top 5 categories, 
    observe number of edits of top 5 edited categories and their percentage to all edits
    """

    # Step 1
    pre = RQ3('pre-pandemic')
    post = RQ3('post-pandemic')

    pre.extract_to_dict('../csv_files/precovid_filtered.csv')
    post.extract_to_dict('../csv_files/postcovid_filtered.csv')

    # Step 2 
    pre.pair_to_meta()
    post.pair_to_meta()
    
    # Step 3 
    pre.meta_plot()
    post.meta_plot()
    print("=== Figure 4.9 (All meta-categories in the pre-pandemic and post-pandemic) saved in the same folder === \n")
    pre.plot_cate()
    post.plot_cate()
    print("\n=== Figure 4.10 (Top 20 categories in the pre-pandemic and post-pandemic) saved in the same folder === \n")

    # Step 4
    print("\n=== Spearman rank-order correlation for meta-categories analysis === \n")
    compute_rank_meta(pre.meta_names, post.meta_names)
     
    # Step 5
    print("=== Table 5.3: Rank-biased overlap results at a category level (top 20, top 10, top 5) \n")
    compute_rank_cate(pre.cate_names, post.cate_names)

    # Step 6
    print("\n=== Table 5.4: Top 5 most edited categories statistics in the pre-pandemic and post-pandemic  === \n")
    pre.observe_top5()
    post.observe_top5()

def compute_rank_meta(meta_pre, meta_post):

    """
    To use Spearman rank-order to calculate the correlation between two rankings, we numbered the content of the ranking list.
    For instance, the pre-pandemic ranking list is ['sustenance', 'transportation', 'Facilities', 'Public Service',...]
    the post-pandemic ranking list is ['Facilities', 'sustenance', 'transportation', 'Public Service', ...]
    We replace each string with its ranking number as below. 

    The p value is 0.000055 and thus the rankings of the meta-categories were highly related. 
    """
    # Replace with the ranking number:
    li_meta_pre = [1,2,3,4,5,6,7,8,9,10]
    li_meta_post = [3,1,2,4,6,5,7,8,10,9]

    coef, p = spe(li_meta_pre, li_meta_post)
    print('Spearmans correlation coefficient: %.3f' % coef)

    # interpret the significance
    alpha = 0.05
    if p <= alpha:
        print('Samples are correlated (reject H0); p=%.6f' % p)
    else:
    	print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
    	

def compute_rank_cate(cate_names_pre, cate_names_post):
    """
    Use RBO to compute the similarity of the two ranking list of categories
    We caculate it for top 20 most edited ones, then for top 10, then for top 5 to see if there is a ranking difference
    Results shown in Table 5.3. Rbo value = 1 means completely identical; RBO value = 0 means completely different.
    """

    # first focus on top 20 categories, then top 10, then top 5 
    for i in [20,10,5]:
        sim = rbo.RankingSimilarity(cate_names_pre[:i], cate_names_post[:i]).rbo()
        print(f'rbo ranking similarity for top {i} is:{round(sim,3)}') 

if __name__ == '__main__':
    main()