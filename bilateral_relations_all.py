# -*- coding: utf-8 -*-
"""
CSS 625 

Conflict and Cooperation Code
"""

import pandas as pd
import glob
import numpy as np
import scipy
from powerlaw import * #plot_pdf, Fit, pdf
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as dt


count = 1
#event_list = []
country_list = [("Afghanistan", "United States"), ("United States", "Afghanistan"), ("Iraq", "United States"), ("United States", "Iraq"), 
                ("Mexico", "United States"), ("United States", "Mexico"), ("Ukraine", "Russian Federation"), ("Russian Federation", "Ukraine"),
                ("China", "India"), ("India", "China")]
#country_list = [("Afghanistan", "United States"), ("United States", "Afghanistan")]


#uterate through country list
for pair in country_list:
    
    event_list = []    
    #iterate through ICEWS files 
    for file in glob.glob("dataverse_files/*"):
        # read in file
        #name = "events" + str(count)
        name = pd.read_csv(file, sep = '\t' )
        
        
        #Do bilateral comparisons of tuples from country list
        name = name[name['Source Country'] == pair[0]]
        name = name[name['Target Country'] == pair[1]]
        
        # reset index
        name = name.reset_index()
        del name['index']
        
        # delete duplicates
        print (len(name['Event ID']))
        idx = 0
        dup_list = []
        for i in range(len(name['Event Date'])-1):
        #print (name.iloc[i, 1])
            if (name.iloc[i, 1]) == (name.iloc[i+1, 1]): # if event date matches
                if (name.iloc[i, 2]) == (name.iloc[i+1, 2]): # if source name matches
                    if (name.iloc[i, 5]) == (name.iloc[i+1, 5]): # if event text matches
                        if (name.iloc[i, 6]) == (name.iloc[i+1, 6]): # if CAMEO code matches
                            if (name.iloc[i, 7]) == (name.iloc[i+1, 7]): # if intesnity matches
                                #print (name['Event ID'].iloc[i+1])
                                #print (name['Event ID'].index[i+1])
                                dup_list.append(name.index[i+1])
                                #name.drop(name.index[i+1], inplace = True)
                                idx +=1
        
        minus_count = 0
        for id in dup_list: 
            name.drop(name.index[id- minus_count], inplace = True)
            minus_count += 1
             
        print (len(name['Event ID']))
        print (idx)
        print (minus_count)
        event_list.append(name)
        count += 1
    #print (event_list)
    # merge all data together save to csv
    df = pd.concat(event_list)
    df.to_csv( pair[0] +'to' + pair[1]+ '.csv', encoding = 'utf-8')
    #df= df.drop(df.iloc[:, :], inplace = True)
    #print (df)

    '''
    Process to get by month data, conduct tail comparison distribution and save to a table
    
    '''
    #get data and test against powerlaws, starts with 1997 in order to have enough data to codnuct tests
    test_list = pd.DataFrame(columns = ("Last Year",'Ratio-lognormal/exponential','P-Value-lognormal/exponential', 'Ratio-lognormal/power law', 'P-Value-lognormal/power law', 'Ratio-power law/exponential', 'P-Value-power law/ exponential', 'Distribution Type'))  
    year_list = ['1997-01-01', '1998-01-01', '1999-01-01', '2000-01-01', '2001-01-01', '2002-01-01', '2003-01-01',
                 '2004-01-01', '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01', 
                 '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-02-01' ]
    
    
    count = 0
    for year in year_list: 
        temp_frame = pd.DataFrame(df[df['Event Date'] <= year])
        date_list = []
        # drop days off list to get by month
        for date in temp_frame['Event Date']:
             date_list.append(date[:-3])
        
        freq_by_month = {}
        for date in date_list:
        #print (date)
            if date not in freq_by_month: 
                freq_by_month[date] = 1
            else: 
                freq_by_month[date] += 1
    # run compariosn distribution using powerlaw dictionary
        freq_list = list(freq_by_month.values())
        
        fit = Fit(freq_list, discrete=True)
        l_e_r, l_e_p = fit.distribution_compare('lognormal', 'exponential')
        l_p_r, l_p_p = fit.distribution_compare('lognormal', 'power_law')
        e_p_r, e_p_p = fit.distribution_compare('power_law', 'exponential')
    
    
        # column to say type of curve
        tail = ""
        if l_e_r > 0 and l_p_r > 0: 
            tail = "lognormal"
        elif l_e_r < 0 and e_p_r < 0 :
            tail = 'exponential'
        elif l_p_r < 0 and e_p_r > 0: 
            tail = 'power_law'
        else: tail ='check'
        
        
        
        
        test_list.loc[count] = [year, l_e_r, l_e_p, l_p_r, l_p_p, e_p_r, e_p_p, tail]
        count += 1
    
    test_list.to_csv(pair[0] + pair[1] +'tailcomparison.csv', encoding = 'utf-8')
    

    '''
    GRAPHS   GRAPHS
    '''
    print (freq_list)
    # Frequency graph
    col = "red"
    spot = country_list.index(pair)
    if spot % 2 == 0: 
        col = 'blue'
    else:
        col = 'red'
    
    month_list = [x for x in range(0, len(freq_list))]
    axes = plt.gca()
    axes.set_ylim([0,3500])
    plt.plot(month_list, freq_list, color = col)
    plt.title("Number of Events Per Month " +  pair[0] + ' to ' + pair[1])
    plt.xlabel("Months") 
    plt.ylabel("Number of Events")     
    plt.savefig(pair[0] + "to" + pair[1] + "freq.png")
    plt.clf()
    #histogram
    #plt.hist(freq_list, bins = 40, color = 'red')
    plt.title("Type II: " + pair[0] + " to " + pair[1] + " Events per Month")
    ax2 = plt.gca()
    ax2.set_ylim([0,120])
    ax2.set_xlim([0,3600])
    plt.ylabel('phi(t)- Frequency of Events per month')
    plt.xlabel('t - Instances of Events per Month')
    #plt.hist(freq_list, bins = 40)
    plt.hist(freq_list, bins = 40, color = col)
    plt.savefig(pair[0] + pair[1] +"hist.png")
    plt.clf()
    #tail graph
    #col_list = []
    #for col in df: 
    #    col_list.append(col)
    #test_list = test_list.drop(test_list.iloc[:], inplace = True)
    #df= df.drop(col_list, axis =1, inplace = True )
    #print (df)
    #print
    #add graphs? 
    

   

