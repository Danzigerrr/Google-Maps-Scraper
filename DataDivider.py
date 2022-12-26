"""
This program was used in the previous stages of this project. Currently, it is not needed. It was used to divide
the data from bigger CSV files into smaller CSV files and save them in the correct directory.
"""
import pandas as pd

if __name__ == "__main__":
    df1 = pd.read_csv("results_bar_v3.csv", index_col=False)
    df2 = pd.read_csv("results_bar_v2.csv", index_col=False)

    frames = [df1, df2]

    # result = pd.concat(frames)
    result = pd.read_csv("results_bar_v2.csv", index_col=False)
    print(result.info())
    print(result.head())

    types = result['type'].unique()
    print(types)
    list_df = []
    for t in types:
        print("type", t)
        df = result[result['type'] == t]
        list_df.append(df)

    for df in list_df:
        # print(df.info())
        place_type = df['type'].unique()
        place_type = " ".join(place_type)
        print(df.shape[0], place_type)
        df.to_csv('database/' + place_type + "_v1.csv", index=False)
