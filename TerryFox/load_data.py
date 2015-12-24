'''
Created on Nov 28, 2015

@author: hakuna
'''
b_list_files = 0
b_load_fundrasier_data = 1
b_load_donar_data = 0
b_create_hist = 0
b_show_chart =0
b_write_csv = 0
b_write_csv_in_one_file = 0
b_write_total_sum_and_count = 1
b_pivot_sum_cnt_by_prov = 1

#Campaign Name    Type    Amount Raised (Online)    Run Site Name (Artez)    City    Province    Postal Code
import pandas as pd
from os import listdir
from os.path import isfile, join
import seaborn as sns
import math
import numpy as np

folder_in = '/home/hakuna/git/terryfox/'
folder_out = folder_in + 'out/'
file_in_1 = 'Data for Good - column headers, definitions and limitations.xlsx'

if b_list_files:
    onlyfiles = [f for f in listdir(folder_in) if isfile(join(folder_in, f))]
    for f in onlyfiles:
        print (f)

#print f_in1.head(10)
#CDE_data = pd.read_excel(sFilePath,'CDE List', header = 0, parse_cols=7)

#final_terry.csv
#.project
#address_names.csv

if b_load_fundrasier_data:
    file_1 = 'TFR 2014 online fundraisers.xlsx'
    file_2 = 'NSRD paper data.xlsx'
    file_3 = 'NSRD 2014 School sites.xlsx' #    NSRD 2014 School sites
    file_4 = 'TFR 2014 Run sites.xlsx' #    TFR Run sites
    file_5 = 'TFR 2014 participant and option 1 data.xlsx' #   TFR 2014 participant and option 1 data
    file_6 = 'NSRD online data.xlsx' #  TFR 2014 online fundraisers
    file_8 = 'TFR online donations 2015.xlsx' #  TFR 2014 online fundraisers
    file_9 = 'NSRD online donations 2015.xlsx' #  TFR 2014 online fundraisers
    file_10 = 'international data.xlsx' #  TFR 2014 online fundraisers
    
    
    
    #load data
    df1 = pd.read_excel(folder_in + file_1)
    df2 = pd.read_excel(folder_in + file_2)
    #df3 = pd.read_excel(folder_in + file_3)
    #df4 = pd.read_excel(folder_in + file_4)
    df5 = pd.read_excel(folder_in + file_5)
    df6 = pd.read_excel(folder_in + file_6)
    df8 = pd.read_excel(folder_in + file_8)
    df9 = pd.read_excel(folder_in + file_9)
    df10 = pd.read_excel(folder_in + file_10)
    
    
    #Paper data per school
    df1.columns = [c.replace(' ', '_').replace('(','').replace(')','') for c in df1.columns]
    df2.columns = [c.replace(' ', '_') for c in df2.columns]
    df5.columns = [c.replace(' ', '_') for c in df5.columns]
    df6.columns = [c.replace(' ', '_').replace('(','').replace(')','') for c in df6.columns]
    df8.columns = [c.replace(' ', '_') for c in df8.columns]
    df9.columns = [c.replace(' ', '_') for c in df9.columns]
    df10.columns = [c.replace(' ', '_') for c in df10.columns]
    #print (df2.columns)
    
    #remove blank rows
    df1 = df1[np.isfinite(df1['Amount_Raised_Online'])]    
    df2 = df2.query("Amount >0")
    df5 = df5.query("Amount >0")
    df6 = df6[np.isfinite(df6['Amount_Raised_Online'])]   
    df8 = df8[np.isfinite(df8['Personal_Amount_Raised_Total'])]    
    df9 = df9[np.isfinite(df9['Personal_Amount_Raised_Total'])]    
    df10 = df10[np.isfinite(df10['Amount__c'])]
    
    #str to num
    df8['Personal_Amount_Raised_Total'] = df8['Personal_Amount_Raised_Total'].map(lambda x: float(str(x).lstrip('$').replace(',','')))
    df9['Personal_Amount_Raised_Total'] = df9['Personal_Amount_Raised_Total'].map(lambda x: float(str(x).lstrip('$').replace(',','')))
    
    
    
if b_write_total_sum_and_count:
    for df_num in [1,2,5,6,8,9,10]:
        if df_num==1:
            file_name = file_1
            df = df1
            TFR_or_NSRD = 'TFR'
            online_or_paper = 'online'
            amt_col = 'Amount_Raised_Online'
            year = '2014'
        elif df_num==2:
            file_name = file_2
            df = df2
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'paper'
            amt_col = 'Amount'
            year = '2014'
        elif df_num==5:
            file_name = file_5
            df = df5
            online_or_paper = 'paper'
            TFR_or_NSRD = 'TFR'
            amt_col = 'Amount'
            year = '2014'
        elif df_num==6:
            file_name = file_6
            df = df6
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'online'
            amt_col =  'Amount_Raised_Online'
            year = '2014'
        elif df_num==8:
            file_name = file_8
            df = df8
            TFR_or_NSRD = 'TFR'
            online_or_paper = 'online'
            amt_col = 'Personal_Amount_Raised_Total'
            year = '2015'
        elif df_num==9:
            file_name = file_9
            df = df9
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'online'
            amt_col = 'Personal_Amount_Raised_Total'
            year = '2015'
        elif df_num==10:
            file_name = file_10
            df = df10
            TFR_or_NSRD = 'TFR'
            amt_col = 'Amount__c'
            year = '2014'
        
        
        df_sum =  (df[amt_col].sum())
        df_cnt =  (len(df.index))
        print (df_num, file_name, df_cnt, math.floor(df_sum))
        

if b_create_hist:
    
    if b_write_csv_in_one_file:
        print ('wrote to: '+folder_out + 'MS_terry_hist.csv')
        f_out = open(folder_out + 'MS_terry_hist.csv','w')
        f_out.write('quantile, DollarsPerBucket, X..Of.Total, Method, Percentil.Size, Percentile.Name, Event.Type, Year')
        
    for df_num in [1,2,5,6]:
        for bucket_size in [5,10,20,25]:
            #df_num=1
            if df_num==1:
                file_name = file_1
                df = df1
                TFR_or_NSRD = 'TFR'
                online_or_paper = 'online'
                amt_col = 'Amount_Raised_Online'
                year = '2014'
            elif df_num==2:
                file_name = file_2
                df = df2
                TFR_or_NSRD = 'NSRD'
                online_or_paper = 'paper'
                amt_col = 'Amount'
                year = '2014'
            elif df_num==5:
                file_name = file_5
                df = df5
                online_or_paper = 'paper'
                TFR_or_NSRD = 'TFR'
                amt_col = 'Amount'
                year = '2014'
            elif df_num==6:
                file_name = file_6
                df = df6
                TFR_or_NSRD = 'NSRD'
                online_or_paper = 'online'
                amt_col =  'Amount_Raised_Online'
                year = '2014'
            elif df_num==8:
                file_name = file_8
                df = df1
                TFR_or_NSRD = 'TFR'
                online_or_paper = 'online'
                amt_col = 'Personal_Amount_Raised_Total'
                year = '2015'
            elif df_num==9:
                file_name = file_9
                df = df1
                TFR_or_NSRD = 'NSRD'
                online_or_paper = 'online'
                amt_col = 'Personal_Amount_Raised_Total'
                year = '2015'
            elif df_num==10:
                file_name = file_10
                df = df1
                TFR_or_NSRD = 'NSRD'
                online_or_paper = 'online'
                amt_col = 'Personal_Amount_Raised_Total'
                year = '2014'
                 
            
            #get total sum
            df_sum =  (df[amt_col].sum())
            
            #get amt by bucket
            #bucket_size = 20
            buckets = [x*.01 for x in range(0,100,bucket_size)]
            df_quantile = df[amt_col].quantile(q=buckets)
            #print (df_quantile)
            
            cum_amount = [0]
            delta_amount = [0]
            for i in range(len(buckets)-1): 
                #print (df1_quantile[buckets[i+1]])
                #print (df1.loc[df1['Amount_Raised_(Online)'] < df1_quantile[buckets[i]+bucket_size*.01]]['Amount_Raised_(Online)'].sum())
                #print (df1.loc[df1['Amount_Raised_(Online)'] < df1_quantile[buckets[i+1]]]['Amount_Raised_(Online)'].sum())
                cum_amount.append(df.loc[df[amt_col] < df_quantile[buckets[i+1]]][amt_col].sum())
                delta_amount.append(cum_amount[i+1]-cum_amount[i])
                #amount_subtotal.append()
            delta_amount.append(df_sum-max(cum_amount))
            cum_amount.append(df_sum)
            
            #name the buckets
            bucket_names = [str(i) + 'pct to ' + str(i+bucket_size) + ' pct' for i in range(0,100,bucket_size)]
            
            df_chart = pd.DataFrame(df_quantile, columns = ['quantile'])
            df_chart['delta_amount'] = [delta_amount[i] for i in range(1,len(delta_amount))]
            df_chart['cum_amount'] = [cum_amount[i] for i in range(1,len(cum_amount))]
            df_chart['pct_amount'] = df_chart['delta_amount'].map(lambda x: x/df_sum)
            df_chart['bucket'] = df_chart.index
            #print (df1_chart)
            #print ([x/df1_sum for x in delta_amount])
            
            #add label to dataframe
            df_chart['online_or_paper'] = [online_or_paper for i in range(len(df_chart.index))]
            df_chart['bucket_size'] = [bucket_size for i in range(len(df_chart.index))]
            df_chart['bucket_names'] = [x for x in bucket_names]
            df_chart['TFR_or_NSRD'] = [TFR_or_NSRD for i in range(len(df_chart.index))]
            df_chart['year'] = [year for i in range(len(df_chart.index))]
            #print (df_chart.columns)
            
            #remove unneeded columns
            df_chart.drop('cum_amount', axis=1, inplace=True)
            df_chart.drop('bucket', axis=1, inplace=True)
            
            if b_write_csv:
                df_chart.to_csv(folder_out + out_file + '_bucket' +str(bucket_size) + '.csv')
                print ('wrote to: '+folder_out + out_file + '_bucket' +str(bucket_size) + '.csv')
            
            if b_write_csv_in_one_file:
                for index, row in df_chart.iterrows():
                    f_out.write('\n')
                    f_out.write(str(', '.join([str(item) for item in row])))
                    
            if b_show_chart:
                g = sns.barplot(x='bucket', y='cum_amount', data=df_chart)
                #g = sns.distplot(pd.Series(df2['Amount']))
                sns.plt.show()
        
    


if b_load_donar_data:
    file_7 = 'final_terry.csv'
    df7 = pd.read_csv(folder_in + file_7,header=0)
    #print (df7.columns)
    df7.columns = [c.replace(' ', '_') for c in df7.columns]
    #print (7, df7.index.size)
    df7['donation'] = df7['donation'].map(lambda x: float(x.lstrip('$').replace(',','')))
    #df2 = df2.query("donation>0")
    print (7, df7.index.size)
    print (df7['donation'].sum())


if b_pivot_sum_cnt_by_prov:
    #for df_num in [1,2,5,6,8,9]:
    for df_num in [1]:
        
        if df_num==1:
            file_name = file_1
            df = df1
            TFR_or_NSRD = 'TFR'
            online_or_paper = 'online'
            amt_col = 'Amount_Raised_Online'
            year = '2014'
        elif df_num==2:
            file_name = file_2
            df = df2
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'paper'
            amt_col = 'Amount'
            year = '2014'
        elif df_num==5:
            file_name = file_5
            df = df5
            online_or_paper = 'paper'
            TFR_or_NSRD = 'TFR'
            amt_col = 'Amount'
            year = '2014'
        elif df_num==6:
            file_name = file_6
            df = df6
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'online'
            amt_col =  'Amount_Raised_Online'
            year = '2014'
        elif df_num==8:
            file_name = file_8
            df = df8
            TFR_or_NSRD = 'TFR'
            online_or_paper = 'online'
            amt_col = 'Personal_Amount_Raised_Total'
            year = '2015'
        elif df_num==9:
            file_name = file_9
            df = df9
            TFR_or_NSRD = 'NSRD'
            online_or_paper = 'online'
            amt_col = 'Personal_Amount_Raised_Total'
            year = '2015'
        elif df_num==10:
            file_name = file_10
            df = df10
            TFR_or_NSRD = 'TFR'
            amt_col = 'Amount__c'
            year = '2014'
        
        df = df.groupby(['Province'], sort=False)[amt_col].sum()
        print (df)
        #df_group.columns = ['Province']

        df_data = pd.DataFrame(df_group,columns = ['Province'])
        df_data['Prov'] = [a for a in df_group.index]
        df_data['TFR_or_NSRD'] = [TFR_or_NSRD for i in range(len(df_data.index))]
        df_data['online_or_paper'] = [online_or_paper for i in range(len(df_data.index))]
        df_data['year'] = [year for i in range(len(df_data.index))]
        print (df_data)
        for index, row in df_data.iterrows():
            print(str(', '.join([str(item) for item in row])))
        
print ('done')
    