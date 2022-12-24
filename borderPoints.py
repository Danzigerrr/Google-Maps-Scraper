import pandas as pd


def setUpBorderPoints():
    # Point A
    left_top_lat = 54.44856818820764
    left_top_lon = 18.42538889812534
    # Point B
    right_bot_lat = 54.26192258463519
    right_bot_lon = 18.943841464421837

    lat = [left_top_lat, right_bot_lat]
    lon = [left_top_lon, right_bot_lon]

    points = {'lat': lat, "lon": lon}
    df = pd.DataFrame(points)
    print(df.head())
    df.to_csv('border_points_v2.csv', index=False)

    # Point A
    print(df.at[0, 'lat'])
    print(df.at[0, 'lon'])

    # Point B
    print(df.at[1, 'lat'])
    print(df.at[1, 'lon'])

if __name__ == "__main__":
    setUpBorderPoints()


