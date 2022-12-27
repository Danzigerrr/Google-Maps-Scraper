import pandas as pd


def setUpBorderPoints(savingDirectory, pointA, pointB, ):
    """
    This function generates a CSV file with border points.

    :return: DataFrame containing the location of border points: latitude and longitude
    """

    lat = [pointA[0], pointB[0]]
    lon = [pointA[1], pointB[1]]

    points = {'lat': lat, "lon": lon}
    df = pd.DataFrame(points)
    print(df.head())
    df.to_csv(savingDirectory + 'border_points_gdansk.csv', index=False)

    return df


def setUpMeasurePoints(savingDirectory, numberOfRows, numberOfColumns, borderPoints=None):
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
        borderPoints = pd.read_csv(savingDirectory + 'border_points_gdansk.csv', index_col=False)
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
    step_lat = diff_lat / numberOfRows
    step_lon = diff_lon / numberOfColumns

    # lists to save coordinates of generated points
    points_lat = []
    points_lon = []

    # generate points
    for i in range(numberOfRows):
        curr_lat = left_top_lat - i * step_lat
        for j in range(numberOfColumns):
            curr_lon = left_top_lon - j * step_lon
            points_lat.append(curr_lat)
            points_lon.append(curr_lon)

    # save to dictionary
    points_all = {'lat': points_lat, 'lon': points_lon}

    # convert dictionary to DataFrame
    points_df = pd.DataFrame(points_all)
    points_df.to_csv(
        savingDirectory + "measure_points" + '_' + str(numberOfRows) + 'r_' + str(numberOfColumns) + "c" + ".csv",
        index=False)
    return points_df


def checkLocationOfBorderPoints(pointA, pointB):
    """
    This function checks if the border points are set correctly - pointA is the left upper corner, pointB is the
    right bottom corner.

    Latitude of pointA must be greater than the latitude of pointB.
    Longitude of pointA must be smaller than the longitude of pointB.

    Example of A and B points set up:
        Point A --> (left_top_lat, left_top_lon)
        Point B --> (right_bot_lat, right_bot_lon)

        Covered area:
        A -- -- -- -- --
        |               |
        |               |
        -- -- -- -- -- B

    :return: boolean value - True if points are set correctly
    """

    if pointA[0] > pointB[0] and pointA[1] < pointB[1]:
        print("PointA and PointB are set correctly.")
        return True  # Points are set correctly
    else:
        errorMessage = """
        Error: PointA and PointB are set incorrectly.
        
        Latitude of pointA must be greater than the latitude of pointB.
        Longitude of pointA must be smaller than the longitude of pointB.
    
        Example of A and B points set up:
            Point A --> (left_top_lat, left_top_lon)
            Point B --> (right_bot_lat, right_bot_lon)

            Covered area:
            A -- -- -- -- --
            |               |
            |               |
            -- -- -- -- -- B
        """
        print(errorMessage)
        return False  # Points are set incorrectly


if __name__ == "__main__":
    savingDirectory = "generatedPoints/"

    # Point A (left upper corner)
    pointA = (54.44856818820764, 18.42538889812534)

    # Point B (right bottom corner)
    pointB = (54.26192258463519, 18.943841464421837)

    # number of "steps" (resolution of the division of the area --> greater value gives more details)
    numberOfColumns = 15
    numberOfRows = 3

    if checkLocationOfBorderPoints(pointA, pointB):
        borderPoints = setUpBorderPoints(savingDirectory, pointA, pointB)
        setUpMeasurePoints(savingDirectory, numberOfRows, numberOfColumns, borderPoints)
