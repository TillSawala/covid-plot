import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.colors as colors
from datetime import datetime

plt.switch_backend('agg')

# fetch data from Github
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
print "loaded data from Github"

set = "Nordics"

#indexing is by country name, so the order doesn't matter.
populations = np.array([["Denmark", 5792202], ["Finland", 5540720], ["Iceland", 341243], ["Norway", 5421241], ["Sweden", 10099265] ])

if set == "Nordics":
    countries = ["Denmark", "Finland", "Iceland", "Norway", "Sweden"]
if set == "EU":
    countries = ["Finland", "France", "Germany", "Italy", "Sweden", "Spain"]                                                 

days = 16 # "today until today - 15

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_yscale('log')
colors = plt.cm.tab10(np.linspace(0,1,len(countries)))

for country in range (0, len(countries)):
    print "country:", countries[country]

    # population                                                                                                                                                 
    p = float(populations[np.ravel(np.where (populations[:,0] == countries[country])),1])

    # select the whole country - some countries are listed more than once, if there is province/state data available.
    # In that case, the province/state is the name of the country, otherwise, Province/state is NaN.
    dc = df.loc[ (df['Country/Region'] == countries[country]) & ( (df['Province/State'] == countries[country]) | (pd.isna(df['Province/State']) ) ) ]    

    # normalise to 1M population
    y = np.ravel(dc[dc.columns[-days:]].values) / p * 1E6
    x = range (0,days)

    ax.plot(x, y, color=colors[country], label=countries[country], zorder=2, alpha=1., linewidth = 2.)

    # labels 1, 10, 100, not 1E0, 1E1, 1E2, etc.
    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax.set_xticks([0,5,10,15])
ax.set_xticklabels(['-15', '-10', '-5', 'today'])

plt.legend(loc='upper left', prop={'size': 12}, ncol=1)
plt.xlabel('Days', fontsize=12)
plt.ylabel('Cases / 1M', fontsize=12)

ax.text(0.3, 0.05, "Data: https://github.com/CSSEGISandData/COVID-19", transform=ax.transAxes, fontsize=8, color='grey')

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M UTC)")
 
ax.text(0.35, 0.95, timestampStr, transform=ax.transAxes, fontsize=12, color='black')

plt.savefig('cases_'+set+'.png', pad_inches=1)

exit()
