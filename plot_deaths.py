import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.colors as colors
from datetime import datetime

def func(x, a, k):
    return a * np.exp(x * k) 


plt.switch_backend('agg')

# fetch data from Github
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
print "loaded data from Github"

# useful to debug, data format keeps changing
# print df

set = "Nordics"
set = "EU"
set = "exponential"

if set == "Nordics":
    countries = ["Denmark", "Finland", "Iceland", "Norway", "Sweden"]

if set == "EU":
    countries = ["Finland", "France", "Germany", "Italy", "Sweden", "Spain", "United Kingdom"]          

if set == "exponential":
    countries = ["China", "Italy", "Iran", "Spain", "France", "US", "United Kingdom", "Netherlands", "Switzerland", "Germany", "Indonesia", "Belgium", "Iraq", "Sweden", "Japan"]


days = 11 # "today until today - 10

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_yscale('log')
colors = plt.cm.tab20(np.linspace(0,1,len(countries)))

for country in range (0, len(countries)):
    print "country:", countries[country]

    # We need to sum sup all the values for the country, in case they are split over different lines

    # First, select all that match the country.
    dc = df.loc[ (df['Country/Region'] == countries[country]) ]
    
    # sum up
    y = np.array(dc[dc.columns[-days:]].values).sum(axis=0)

    #select range to include minimum of three deaths
    selection = np.ravel(np.where( y >= 3))
    
    # and for a minimum of five days
    if len(selection) >= 5:
       
        y = y[selection]
        x = np.array(range (0,days))
        x = x[selection]

        popt, pcov = curve_fit(func, x, y, sigma=np.sqrt(y), maxfev=5000)
        
        perr = np.sqrt(np.diag(pcov))

        #doubling time, min / max
        t2= np.log(2.)/popt[1]
        t2max= np.log(2.)/(popt[1]+perr[1])
        t2min= np.log(2.)/(popt[1]-perr[1])
    
        #plot fit
        ax.plot(x, func(x, *popt) , color=colors[country], zorder=2, alpha=1., linewidth = 2.)
        
        #plot data and label
        ax.plot(x, y, color=colors[country], label=countries[country]+" ("+("%.2f" % t2)+"$^{"+("%.2f" % t2max)+"}_{"+("%.2f" % t2min)+"}$"+")", zorder=2, alpha=1., marker="o", linestyle="none", markersize=5)

        plt.fill_between(x, y-np.sqrt(y), y+np.sqrt(y), color=colors[country], alpha=.3, zorder=1)

        # labels 1, 10, 100, not 1E0, 1E1, 1E2, etc.
        plt.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax.set_xticks([0,5,10])
ax.set_xticklabels(['-10', '-5', 'today'])

plt.legend(loc='upper center', prop={'size': 7}, ncol=3)
plt.xlabel('Days', fontsize=10)
plt.ylabel('Deaths', fontsize=10)

plt.grid(b=None, which='major', axis='both')

ax.text(0.2, 1.05, "Data: https://github.com/CSSEGISandData/COVID-19", transform=ax.transAxes, fontsize=8, color='grey')

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M UTC)")
 
ax.text(0.35, 1.1, timestampStr, transform=ax.transAxes, fontsize=8, color='black')

ax.set_ylim([1,100000])
plt.savefig('deaths_'+set+'.png', dpi=300)

exit()
