import pandas as pd

def covid(df):

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    real = True
    generate = False

    # generate
    if generate:
        df_housing = pd.read_csv("Incidents_Responded_to_by_Fire_Companies.csv")
        example = df[1:2000]
        example.to_csv("data_example.csv")

    if real:
        df = pd.read_csv("Incidents_Responded_to_by_Fire_Companies.csv")
    else:
        df = pd.read_csv("data_example.csv")

    covid(df)

