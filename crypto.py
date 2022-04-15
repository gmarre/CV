import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
data = pd.read_csv('B.csv')
data['Date'] = pd.to_datetime(data['Date'])
data['Date']
fig = plt.figure(figsize=(15, 5))

plt.tick_params(axis='x',labelsize=10,rotation=90)
plt.scatter(data.Date,data.Close,s = 3) # Your data
plt.xlabel('Date')
plt.ylabel('Stock price')
plt.tight_layout()
plt.show()

import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def achat_vente_simple(stocks,buying_date,selling_date,eur) : 
    mask1 = (stocks['Date'] == buying_date)
    mask2 = (stocks['Date'] == selling_date)
    price_buying = stocks.loc[mask1,'Close'].values[0]
    price_selling = stocks.loc[mask2,'Close'].values[0]
    diff_percentage = (price_selling - price_buying)/price_selling
    
    potential_return = eur + eur*diff_percentage 
    return potential_return


#frequency in days

def DCA(stocks,start_date,end_date,frequency,eur) :
    
    sum_price = 0
    compteur = 0
    t = timedelta(days = frequency)
    current_date = start_date
    diff_percentage = 0
    
    mask2 = (stocks['Date'] == end_date)
    price_selling = stocks.loc[mask2,'Close'].values[0]
    
    while current_date < end_date :
        mask1 = (stocks['Date'] == current_date)
        price_buying = stocks.loc[mask1,'Close'].values[0]
        sum_price = sum_price + price_buying
        compteur = compteur + 1
        current_date = current_date + t
    
    avg_buying_price = sum_price/compteur
    diff_percentage = (price_selling - avg_buying_price)/price_selling
    eur_depense = compteur*eur
    potential_return = eur_depense + eur_depense*diff_percentage 
    
    return potential_return,eur_depense


def average_price_on_x_days_before(stocks,date,x) :
    t = timedelta(days = 1)
    sum_price = 0
    current_date = date
    for i in range(x) :
        mask1 = (stocks['Date'] == current_date)
        price_buying = stocks.loc[mask1,'Close'].values[0]
        sum_price = sum_price + price_buying
        current_date = current_date - t
    avg = sum_price/x
    return avg

def mapping_eur_coef(range_eur,percentage) :
    if percentage > 0.05 :
        eur_invest = range_eur[0]
    elif percentage < -0.05 :
        eur_invest = range_eur[1]
    else :
        #linear evolution
        eur_invest = ((range_eur[1]+range_eur[0])/(-0.05-((range_eur[1]-range_eur[0])/2)))*percentage+((range_eur[1]-range_eur[0])/2)
    
    return eur_invest


def DCA_optimize(stocks,start_date,end_date,frequency,range_eur) :
    sum_price = 0
    sum_euro_invest = 0
    
    t = timedelta(days = frequency)
    current_date = start_date
    diff_percentage = 0
    
    mask2 = (stocks['Date'] == end_date)
    price_selling = stocks.loc[mask2,'Close'].values[0]
    
    while current_date < end_date :
        mask1 = (stocks['Date'] == current_date)
        price_buying = stocks.loc[mask1,'Close'].values[0]
        
        avg_price_5_days = average_price_on_x_days_before(data,current_date,10)
        percentage = (price_buying - avg_price_5_days)/price_buying
        eur_invest = mapping_eur_coef(range_eur,percentage)
        sum_euro_invest = sum_euro_invest + eur_invest
        
        sum_price = sum_price + eur_invest*price_buying
        current_date = current_date + t
    
    avg_buying_price = sum_price/sum_euro_invest
    diff_percentage = (price_selling - avg_buying_price)/price_selling
    
    potential_return = sum_euro_invest + sum_euro_invest*diff_percentage 
    
    return potential_return,sum_euro_invest

start_date = datetime(2021,2,15)
end_date = datetime(2022,4,15)
achat_vente_simple(data,start_date,end_date,1000)
DCA(data,start_date,end_date,3,7)
DCA_optimize(data,start_date,end_date,15,[0,5])
