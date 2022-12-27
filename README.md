# Google Maps Scraper

Google Maps Scrapper allows you to collect data from the given area about places of the specified type from Google Maps. The user needs to set the points which set the area of interest - the points are opposite corners of a rectangle.
The user also sets the zoom as well as the resolution of the search - the area is divided into X columns and Y rows. The program will search for the places at each of the points with a set zoom.
Finally, the collected data is saved in a CSV file.

The time needed to collect the data depends on the number of measure points and the number of results returned by Google Maps. It takes approximately 15 minutes to scrape area of city of Gdańsk in Poland with 175 measure points.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries used in the project specified in the requirements.txt file.

```bash
pip install requirements.txt
```

## Usage
### Define the area of interest - set the border and measure points
Use the file *BorderAndMeasurePoints.py* to set the location of two points: point A (left upper corner) and Point B (bottom right corner) - the opposite corners of a rectangle covering the area of interest. Use the parameter *numberOfColumns* and *numberOfRows* to set the number of columns and rows which divide the area. Finally, use the *setUpBorderPoints()* and *setUpMeasurePoints()* functions to generate the points.

```python
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

```

### Visualise the measure points
Use the method *visualiseMeasurePoints()* to see the measure points on the map. The program will open the map using the Chrome browser. Measure points are represented as circles.

The measure points look like this:
![measurePointsVisualised_1.jpg](readmeImages/measurePointsVisualised_1.jpg)

Since the measure points are saved into a CSV file, it is easy to delete the location of points that are not needed in the search process, for example points at sea. Manually deleting unneeded points will optimize the search process and reduce the time needed to analyze the given area. 
The optimized measure points look like this:
![measurePointsVisualised_2.jpg](readmeImages/measurePointsVisualised_2.jpg)

### Collect the data from the Google Maps
Use the *MainScraper.py* file to collect the data from the area using the generated measure points. The program generates a URL for each measure point. The URL contains:
- the type of the searched place
- longitude and latitude of the measure point
- the zoom of search


The program opens the browser and inserts each URL. The Google Maps are searching for places nearby the measure point. The results of the search are visible in the vertical menu on the left. The menu is scrolled down several times and then the search results are saved. The scraper collects information about each place:
- link to Google Maps describing the place
- the name of the place
- the type of the place

```python
    placesResults = []
    # save the search results into a dictionary
    for el in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
        placesResults.append({
            'link': el.xpath('./a/@href').extract_first(''),
            'title': el.xpath('./a/@aria-label').extract_first(''),
            'type': typeOfPlace
        })
```

Then the location (longitude and latitude) is extracted from the link to Google Maps describing the place and assigned to the place. All of the places are saved in a DataFrame and saved into a CSV file. 

```python
    lat = []
    lon = []
    for index, row in df.iterrows():
        link = df.at[index, 'link']
        # print(link, "\n")
        latLon = re.search('!3d(.*)!16', link).group(1).split('!4d')
        # print(latLon[0], latLon[0])
        lat.append(latLon[0])
        lon.append(latLon[1])

    df['lat'] = lat
    df['lon'] = lon

    df = df[['lat', 'lon', 'type', 'title', 'link']]  # set order of columns

    return df
```
### Visualise collected points
Use the *PlacesVisualiser.py* file to visualise the points. The function *visualiseCollectedPoints()* reads all CSV files from the *database* directory and opens the browser with a map showing all the points. The legend show the color of the circle corresponding to the type of place.

![collectedPointsVisualised_1.jpg](readmeImages/collectedPointsVisualised_1.jpg)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
