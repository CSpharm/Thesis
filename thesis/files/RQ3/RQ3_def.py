import pandas as pd
from matplotlib import pyplot as plt
import operator as op
import collections as co

"""
This Python file defines the methods in RQ3
"""

class RQ3():

    def __init__(self, option):
        """
        self.dict_cate: a dictionary stores the category name and its corresponding nubmer of edits.
            It is sorted by the edits in a descending order. eg. {'bicycle parking': 2962,'bench':2411, ..}

        self.cate_names: a list of category names in a descending order of their edits; the rank list
            eg. ['bicycle parking', 'bench', and so on]: the most edited type is bicycle parking, 
            and the second most edited type is bench..

        self.cate_values: a list of number of edits for each corresponding category;
            eg. [2962, 2411,..] 

        self.dict_meta: a sorted dictionary to store all meta-category names and number of corresponding edits 
            key: meta-category name
            value: number of the edits for that meta-category
        
        self.meta_names: a rank list to store the rank of all meta-categories
            eg. ['sustenance', 'transportation',..]

        self.meta_values: a list to store the edits of all meta-categories in a descending order
            eg. [edits for 'sustenance', edits for 'transportation',..]

        self.li_top5 : a list to store the statistics for top 5 most edited POIs, including
            Category names, number of edits, % of total edits. Used for Table 5.4 
        """

        self.option = option
        self.dict_cate = {} 
        self.cate_names = []
        self.cate_values = []

        self.dict_meta = {}
        self.meta_names = []
        self.meta_values = []

        self.total_edits = 0
        self.li_top5 = []
       
    def extract_to_dict(self,filename):
        """
        Calculate the edits of each amenity category, 
        store the category name and the number of the corresponding edits to self.dict_cate,
        sort self.dict_cate by the number of edits in a descending order
        """
        self.df = pd.read_csv(filename)
        
        for i in range(len(self.df)):
            amenity_type = self.df.iloc[i,5]

            if amenity_type not in self.dict_cate:
                self.dict_cate[amenity_type] = 1
            else:
                self.dict_cate[amenity_type] += 1
        
        self.dict_cate = dict(sorted(self.dict_cate.items(), key=op.itemgetter(1),reverse=True))
        self.total_edits = sum(self.dict_cate.values())

    def pair_to_meta(self):
        """
        Pair each category to their corresponding meta-category according to the OSM wiki page
        E.g. 'pub', 'restaurant', 'cafe' all belong to the 'sustenance' meta-category,
        so we store 'sustenance' meta-category as the key and all its corresponding categories as the value in dict_ame_kinds.
        """
        dict_ame_kinds = {}

        dict_ame_kinds['sustenance'] = [ "bar", "biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant"]
        dict_ame_kinds['education'] = [ "college", "driving_school", "kindergarten", "language_school", "library", "toy_library", "school", "music_school", "university"]
        dict_ame_kinds['transportation'] = [ "bicycle_parking", "bicycle_repair_station", "bicycle_rental", "boat_rental", "boat_sharing"," bus_station", "car_rental"
        , "car_sharing", "car_wash", "vehicle_inspection", "charging_station", "ferry_terminal", "fuel", "grit_bin", "motorcycle_parking", "parking", "parking_entrance"
        , "parking_space", "taxi"]

        dict_ame_kinds['Financial'] = [ "atm", "bank", "bureau_de_change"]
        dict_ame_kinds['Healthcare'] = [ "clinic", "dentist", "doctors", "hospital", "nursing_home", "pharmacy", "social_facility", "veterinary"]
        dict_ame_kinds['Entertainment, Arts & Culture'] = [ "arts_centre", "brothel", "casino", "cinema", "community_centre", "conference_centre",
                                                           "events_venue", "fountain", "gambling", "love_hotel", "nightclub", "planetarium",
                                                           "public_bookcase", "social_centre", "stripclub", "studio", "theatre"]
        dict_ame_kinds['Public Service'] = [ "courthouse", "embassy", "fire_station", "police", "post_box", "post_office", "prison", "townhall"]
        dict_ame_kinds['Facilities'] = [ "bbq", "bench", "drinking_water", "shelter"," shower", "telephone", "toilets", "water_point", "watering_place"]
        dict_ame_kinds['Waste Management'] = [ "sanitary_dump_station", "recycling", "waste_basket", "waste_disposal", "waste_transfer_station"]
      
        # for each category, pair it and its edits to the corresponding meta-category in self.dict_meta[k]
        for key, values in self.dict_cate.items():
            for k, v in dict_ame_kinds.items():
                if key in v:
                    if k not in self.dict_meta:
                        self.dict_meta[k] = values
                    else:
                        self.dict_meta[k] += values

        # There are 10 meta-categories including 'other'.
        # Number of edits for 'other' meta-category: use total edits - the rest of 9 categories
        len_other = self.total_edits - sum(self.dict_meta.values())
        self.dict_meta['Others'] = len_other
        self.dict_meta = dict(sorted(self.dict_meta.items(), key=op.itemgetter(1),reverse=True))
        
    def meta_plot(self):
        """
        Plot the names of all meta-categories and their corresponding number of edits (Figure 4.9)
        """

        self.meta_names = list(self.dict_meta.keys())
        self.meta_values  = list(self.dict_meta.values())

        plt.bar(self.meta_names, self.meta_values, width=0.5, align='center')
        plt.xticks(rotation = 45,fontsize=7)

        plt.title('All meta-categories in the ' + self.option + ' period')
        plt.xlabel('Meta-category',fontsize=10)
        plt.ylabel('Number of edits',fontsize=10)
        plt.savefig('RQ3_meta_'+ self.option+'.png',dpi=500, bbox_inches='tight')
        plt.clf()

    def plot_cate(self):
        """
        Plot the names of top 20 most edited categories and their corresponding number of edits (Figure 4.10)
        """

        self.cate_names = list(self.dict_cate.keys())
        self.cate_values = list(self.dict_cate.values())

        plt.bar(self.cate_names[:20], self.cate_values[:20], width=0.5, align='center')
        plt.xticks(rotation = 'vertical',fontsize=8)
        plt.title("Top 20 categories in the "+ self.option +" period")
        plt.xlabel("Category",fontsize=10)
        plt.ylabel("Number of edits",fontsize=10)
        plt.savefig("RQ3_top20_cate_" + self.option+ ".png",dpi=500, bbox_inches='tight')
        plt.clf()

    def observe_top5(self):
        """
        Among top 5 most edited categories, print the category name, the number of edits for it, 
        and the percentage of total edits (the number of edits/ total edits); 
        generates the data in Table 5.4
        """

        for i in range(5):

            cate_name = self.cate_names[i]
            cate_values = self.cate_values[i]
            percent = self.cate_values[i] / self.total_edits *100
            percent_format = str(round(percent,1)) + '%'
            self.li_top5.append((cate_name,cate_values,percent_format))

        # Append the data for total edits
        self.li_top5.append(('All categories',self.total_edits, '100%'))
        print(f"The order of the data: Category names, number of edits, % of total edits")
        
        for tuple in self.li_top5:
            print(tuple)