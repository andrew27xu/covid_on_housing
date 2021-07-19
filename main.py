import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime as dt


def covid(df_z,df_p,df_d,df_c):
    #pre processing
    df_z.drop(df_z.iloc[:, 0:8], axis = 1, inplace = True)
    #print(df_z)

    #rearrange columns
    cols = df_z.columns.tolist()
    cols = cols[-30:]+cols[0:1]
    df_z = df_z[cols]
    #print(df_z)
    for col in cols[:-1]:
        df_z[col] = df_z[col].astype('float')

    #arrange back and transpose
    cols = cols[-1:] + cols[0:-1]
    df_z = df_z[cols]
    df_z_T = df_z.T

    #remove header
    new_header = df_z_T.iloc[0]
    df_z_T = df_z_T[1:]
    df_z_T.columns = new_header

    #calculate average
    df_z_T.index = pd.to_datetime(df_z_T.index)
    df_z_T["average"] = df_z_T.mean(axis=1)

    #linear regression
    date_converted = np.array(df_z_T.index.map(dt.datetime.toordinal)).reshape(-1,1)
    date_pre = date_converted[:15] #up to 2020/3
    linear_regressor = LinearRegression()
    linear_regressor.fit(date_pre, df_z_T["average"][:15])
    Y_pred = linear_regressor.predict(date_converted)

    #plot average
    average_plot = df_z_T['average']
    f1 = average_plot.plot( )
    f1.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.title ("National Trend From Jan 2019 to June 2021",fontsize=16)
    plt.xlabel("Time [date]", fontsize=14)
    plt.ylabel ("Average Housing Price [$]",fontsize=14)
    plt.tight_layout()
    plt.show()





if __name__ == '__main__':
    real = False
    generate = False

    # generate
    if generate:
        df_z = pd.read_csv("zillow.csv",index_col=0)
        example_z = df_z[1:2000]
        example_z.to_csv("zillow_example.csv")

        df_covid_death = pd.read_csv("covid_deaths_usafacts.csv",index_col=0)
        example_covid_death = df_covid_death[1:2000]
        example_covid_death.to_csv("death_example.csv")

        df_p = pd.read_csv("covid_county_population_usafacts.csv",index_col=0)
        example_p = df_p[1:2000]
        example_p.to_csv("pop_example.csv")

        df_covid_case = pd.read_csv("covid_confirmed_usafacts.csv",index_col=0)
        example_covid_case = df_covid_case[1:2000]
        example_covid_case.to_csv("case_example.csv")



    if real:
        df_z = pd.read_csv("zillow.csv")
        df_d = pd.read_csv("covid_deaths_usafacts.csv")
        df_p = pd.read_csv("covid_county_population_usafacts.csv")
        df_c = pd.read_csv("covid_confirmed_usafacts.csv")
    else:
        df_z = pd.read_csv("zillow_example.csv")
        df_p = pd.read_csv("pop_example.csv")
        df_c = pd.read_csv("case_example.csv")
        df_d = pd.read_csv("death_example.csv")

    covid(df_z,df_p,df_d,df_c)

