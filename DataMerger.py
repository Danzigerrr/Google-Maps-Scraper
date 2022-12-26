import os
import pandas as pd


def mergeAllPlaces():
    """
    This function allows to merge all found places into a DataFrame.
    All CSV files from the database directory are read and then the data is merged.

    :return: Dataframe contacting all found places
    """
    path = "database"

    # get list of files in the directory
    files = os.listdir(path)

    allPlaces = pd.DataFrame()
    df_list = []
    # loop through each file
    for filename in files:
        df = pd.read_csv(path + '/' + filename, index_col=False)
        df_list.append(df)
        # print(df.shape[0], filename)

        frames = [allPlaces, df]
        allPlaces = pd.concat(frames)

    print(allPlaces.info())

    df_list_sorted = sorted(df_list, key=lambda df: len(df), reverse=True)
    for df in df_list_sorted:
        print(df.shape[0], df.at[4, 'type'])

    return allPlaces


if __name__ == "__main__":
    mergeAllPlaces()
