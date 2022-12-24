import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import requests
import re
from selenium.webdriver.common.keys import Keys
from PlacesVisualiser import *
import time
from selenium.common.exceptions import NoSuchElementException

googleAcceptButtonClicked = False

# setUpWebDriver
options = webdriver.ChromeOptions()
options.add_argument('headless')  # Make browser open in background
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def scrollDownLeftMenuOnGoogleMaps(counter, waitingTime):
    menu_xpath = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a'

    if check_exists_by_xpath(menu_xpath):
        for i in range(counter):
            wait = WebDriverWait(driver, waitingTime)
            menu_left = wait.until(EC.visibility_of_element_located((By.XPATH, menu_xpath)))
            menu_left.send_keys(Keys.SPACE)


def searchForPlace(url):
    global googleAcceptButtonClicked
    driver.get(url)

    # only at the first page click the "accept all" ("zaakceptuj wszystko") button
    if googleAcceptButtonClicked == False:
        clickAcceptAllButton()

    # scroll down left menu
    scrollDownLeftMenuOnGoogleMaps(counter=3, waitingTime=2)

    # get the source code of the page
    page_content = driver.page_source
    response = Selector(page_content)

    placesResults = []
    place_type = re.search('search/(.*)/@', url).group(1)  # extract the place type from the url
    # print(place_type)

    # save the search results into a dictionary
    for el in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
        placesResults.append({
            'link': el.xpath('./a/@href').extract_first(''),
            'title': el.xpath('./a/@aria-label').extract_first(''),
            'type': place_type
        })

    return placesResults


def clickAcceptAllButton():
    global googleAcceptButtonClicked
    button_path = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
    wait = WebDriverWait(driver, 1)
    button = wait.until(EC.visibility_of_element_located((By.XPATH, button_path)))
    button.click()
    googleAcceptButtonClicked = True


def convertToDataFrame(results):
    df = pd.DataFrame(results)
    return df


def addLonLatToDataFrame(df):
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


def closeDriver():
    driver.quit()


def generateUrls():
    points_df = generatePoints()
    # points_df = pd.read_csv("Points_size20_v2.csv", index_col=False)
    points_df = pd.read_csv("Points_size15_v2.csv", index_col=False)

    # END GENERATE POINTS
    # BEGIN GENERATE URLS
    base = 'https://www.google.com/maps/search/'
    # types_of_places = ['bar', 'restaurant', 'coffee', 'public_transport', 'hotel']
    # types_of_places = ['bar', 'hotel', 'restaurant', 'coffee']  # v2
    # types_of_places = ['church', 'public transport', 'university', 'school']  # v3
    # types_of_places = ['fitness', 'shop', 'shopping mall', 'entertainment']  # v4
    types_of_places = ['lekarz', 'basen', 'sport', 'culture' 'przystanek']  # v5


    generated_urls = []
    for types in types_of_places:
        for index, row in points_df.iterrows():
            point_lat = points_df.at[index, 'lat']
            point_lon = points_df.at[index, 'lon']
            zoom = 16
            #zoom = 14
            url = base
            # url += str(types) + '+near+Gdansk,+Poland/@'
            url += str(types) + '/@'
            url += str(point_lat) + ',' + str(point_lon) + ',' + str(zoom) + 'z'
            # print(url)
            # print('https://www.google.com/maps/search/bars+near+Gdansk,+Poland/@54.37083931588029,18.609653070782628,13z')
            generated_urls.append(url)
    return generated_urls


def generatePoints():
    """
      :return: DataFrame of points with columns: lat, lon

        example of A and B points set up:
            Point A --> (left_top_lat, left_top_lon)
            Point B --> (right_bot_lat, right_bot_lon)

            Covered area:
            A -- -- -- -- --
            |               |
            |               |
            -- -- -- -- -- B
    """
    borderPoints = pd.read_csv('border_points_v2.csv', index_col=False)
    # Point A
    left_top_lat = borderPoints.at[0, 'lat']
    left_top_lon = borderPoints.at[0, 'lon']

    # Point B
    right_bot_lat = borderPoints.at[1, 'lat']
    right_bot_lon = borderPoints.at[1, 'lon']

    print(left_top_lat)
    print(left_top_lon)
    print(right_bot_lat)
    print(right_bot_lon)
    # difference of A and B points' latitude and longitude
    diff_lat = left_top_lat - right_bot_lat
    diff_lon = left_top_lon - right_bot_lon

    # number of "steps" (resolution of division of the area --> greater value gives more details)
    size = 15

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
    start = time.time()

    urls = generateUrls()

    print("total number of points to check:" + str(len(urls)))

    list_of_places = []
    progressCounter = 0
    for url in urls:
        new_places = searchForPlace(url)
        list_of_places += new_places  # concat two lists
        progressCounter += 1
        print("progress: " + str(round(100 * progressCounter / len(urls), 2)) + "%")

    df = convertToDataFrame(list_of_places)

    df = df.drop_duplicates()
    df = addLonLatToDataFrame(df)

    # print(df['title'].unique())
    print("number of places:" + str(df.shape[0]))

    # for index, row in df.iterrows():
    #     print(row['type'], row['title'])

    df.to_csv('results_bar_v4.csv', index=False)

    closeDriver()

    end = time.time()
    print("total time:" + str(end - start) + " seconds --> " + str((end - start) / 60) + " minutes")
