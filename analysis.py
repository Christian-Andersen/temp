import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('temp_all.csv', parse_dates=[1])
df = df.set_index(df.date)
df['year'] = df.date.dt.year
df['month'] = df.date.dt.month
df['day'] = df.date.dt.day


df1 = df[df.location == 'PERTH METRO']
rolled = df1.rolling(14, min_periods=1, on='date').mean(numeric_only=True)['max_temp']
rolled.loc['2019']


locations = ['NAMBOUR DAFF - HILLSIDE',
             'SYDNEY (OBSERVATORY HILL)',
             'BRISBANE',
             'CANBERRA AIRPORT',
             'DARWIN AIRPORT',
             'ADELAIDE (WEST TERRACE _ NGAYIRDAPIRA)',
             'HOBART AIRPORT',
             'MELBOURNE (OLYMPIC PARK)',
             'PERTH METRO']
for location in locations:
    for column, name in {'max_temp': 'Maximum Temperature', 'max_humidity': 'Maximum Humidity'}.items():
        df_location = df[df.location == location]
        df_rolling = df_location.rolling(
            14, min_periods=1).mean(numeric_only=True)[column]
        x = df_location.loc['2023'].date.dt.strftime('%d/%m').to_list()
        plt.plot(x, df_rolling.loc['2022'].iloc[:len(x)], label=2022)
        plt.plot(x, df_rolling.loc['2023'].iloc[:len(x)], label=2023)
        plt.legend(loc="upper left")
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title(location.split()[0]+'\nRolling 14 Day Average '+name)
        xticks = []
        for idx, day in enumerate(x):
            if day.startswith('01') or day.startswith('15'):
                xticks.append(idx)
        if (len(x)-1) not in xticks:
            xticks.append(len(x)-1)
        if xticks[-1]-xticks[-2] < 10:
            xticks.pop(-2)
        plt.xticks(xticks)
        plt.savefig('images/'+location.split()[0]+'_'+column, dpi=400)
        plt.clf()
