import pandas as pd


def setUpBorderPoints(left_top_lat, left_top_lon, right_bot_lat, right_bot_lon):
    """
    This function generates a CSV file with border points.

    :return: DataFrame containing the location of border points: latitude and longitude
    """

    lat = [left_top_lat, right_bot_lat]
    lon = [left_top_lon, right_bot_lon]

    points = {'lat': lat, "lon": lon}
    df = pd.DataFrame(points)
    print(df.head())
    df.to_csv('border_points_v2.csv', index=False)

    return df


def setUpMeasurePoints(size, borderPoints = None):
    """
    This function generates DataFrame with latitude and longitude of measure points, based on the location of border
    points. The location of two border points is read from a CSV file.

    Example of A and B points set up:
            Point A --> (left_top_lat, left_top_lon)
            Point B --> (right_bot_lat, right_bot_lon)

            Covered area:
            A -- -- -- -- --
            |               |
            |               |
            -- -- -- -- -- B

      :return: DataFrame of points with columns: lat, lon
    """
    if borderPoints is not None:
        borderPoints = pd.read_csv('border_points_v2.csv', index_col=False)
    # Point A
    left_top_lat = borderPoints.at[0, 'lat']
    left_top_lon = borderPoints.at[0, 'lon']

    # Point B
    right_bot_lat = borderPoints.at[1, 'lat']
    right_bot_lon = borderPoints.at[1, 'lon']

    # difference of A and B points' latitude and longitude
    diff_lat = left_top_lat - right_bot_lat
    diff_lon = left_top_lon - right_bot_lon

    # value of difference between generated points
    step_lat = diff_lat / size
    step_lon = diff_lon / size

    # lists to save coordinates of generated points
    points_lat = []
    points_lon = []

    # generate points
    for i in range(size):
        curr_lat = left_top_lat - i * step_lat
        for j in range(size):
            curr_lon = left_top_lon - j * step_lon
            points_lat.append(curr_lat)
            points_lon.append(curr_lon)

    # save to dictionary
    points_all = {'lat': points_lat, 'lon': points_lon}

    # convert dictionary to DataFrame
    points_df = pd.DataFrame(points_all)
    points_df.to_csv("Points_size" + str(size) + ".csv", index=False)
    return points_df


if __name__ == "__main__":
    # Point A (left upper corner)
    point_a_lat = 54.44856818820764
    point_a_lon = 18.42538889812534

    # Point B (right bottom corner)
    point_b_lat = 54.26192258463519
    point_b_lon = 18.943841464421837

    # number of "steps" (resolution of the division of the area --> greater value gives more details)
    size = 15

    borderPoints = setUpBorderPoints(point_a_lat, point_a_lon, point_b_lat, point_b_lon)
    setUpMeasurePoints(size, borderPoints)
