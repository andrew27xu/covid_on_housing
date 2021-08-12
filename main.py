import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime as dt
from textwrap import wrap


def covid(df_z,df_p,df_d,df_c):
    #pre processing
    df_z.drop(df_z.iloc[:, 0:5], axis = 1, inplace = True)
    df_z.drop(df_z.iloc[:, 1:3], axis=1, inplace=True)

    #rearrange columns
    #dz
    cols = df_z.columns.tolist()
    cols = cols[-30:]+cols[0:1] #chose data and state
    df_z_average= df_z[cols]
    for col in cols[:-1]:
        df_z_average[col] = df_z_average[col].astype('float')
    #dc and d_d

    #arrange back and transpose
    cols = cols[-1:] + cols[0:-1]
    df_z_average = df_z_average[cols]
    df_z_average_T = df_z_average.T

    #remove header
    new_header = df_z_average_T.iloc[0]
    df_z_average_T = df_z_average_T[1:]
    df_z_average_T.columns = new_header

    #calculate average
    df_z_average_T.index = pd.to_datetime(df_z_average_T.index)
    df_z_average_T["average"] = df_z_average_T.mean(axis=1)
    # linear regression
    date_converted = np.array(df_z_average_T.index.map(dt.datetime.toordinal)).reshape(-1, 1)
    date_pre = date_converted[:15]  # up to 2020/3
    linear_regressor = LinearRegression()
    linear_regressor.fit(date_pre, df_z_average_T["average"][:15])
    y_pred = linear_regressor.predict(date_converted)
    y_pred = np.expand_dims(y_pred, axis=1)
    df_z_average_T['predicted'] = y_pred
    df_z_average_T['difference'] = df_z_average_T["average"] - df_z_average_T['predicted']

    # plot covid death
    df_c.drop(["countyFIPS", "StateFIPS"], axis=1, inplace=True)
    df_d.drop(["countyFIPS", "StateFIPS"], axis=1, inplace=True)
    df_c_average = df_c[1:].groupby("State").mean()
    df_d_average = df_d[1:].groupby("State").mean()
    df_c_average_T = df_c_average.T
    df_d_average_T = df_d_average.T
    #calculate average
    df_c_average_T.index = pd.to_datetime(df_c_average_T.index)
    df_c_average_T["average"] = df_c_average_T.mean(axis=1)
    df_d_average_T.index = pd.to_datetime(df_d_average_T.index)
    df_d_average_T["average"] = df_d_average_T.mean(axis=1)


    #plot average
    average_plot = df_z_average_T[['average','predicted']]
    fig, ax = plt.subplots()
    #fig =  average_plot.plot( )
    styles = ['b-',  'r--']
    linewidths = [2, 2]
    for col, style, lw in zip(average_plot.columns, styles, linewidths):
        average_plot[col].plot(style=style, lw=lw, ax=ax)
    ax.legend()
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_title ("National Trend From Jan 2019 to June 2021",fontsize=16)
    ax.set_xlabel("Time [date]", fontsize=14)
    ax.set_ylabel ("Average Housing Price [$]",fontsize=14)
    plt.tight_layout()
    plt.savefig("image1.png")

    # plot difference
    diff_plot = df_z_average_T['difference']
    fig2, ax2 = plt.subplots()
    ax2.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax2.set_title("\n".join(wrap("Difference Between Average Housing Price and Predicted Price",35)), fontsize=16)
    ax2.set_xlabel("Time [date]", fontsize=14)
    ax2.set_ylabel("\n".join(wrap("Average Housing Price - Predicted Housing Price [$]",35)), fontsize=14)
    diff_plot.plot()
    plt.tight_layout()
    plt.savefig("image2.png")
    #plt.show()




    df_p.drop(df_p.iloc[:, 0:1], axis = 1, inplace = True)
    df_p = df_p[df_p["population"]>0]
    df_p_mean = df_p.groupby("State").mean()


    df_c_mean = df_c.groupby("State").mean()
    df_d_mean = df_d.groupby("State").mean()










if __name__ == '__main__':
    real =False
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

