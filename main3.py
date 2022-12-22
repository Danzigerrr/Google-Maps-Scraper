import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import requests
import re
googleAcceptButtonClicked = False

# setUpWebDriver
options = webdriver.ChromeOptions()
options.add_argument('headless')  # Make browser open in background
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())


def searchForPlace(url):
    global googleAcceptButtonClicked
    driver.get(url)

    if googleAcceptButtonClicked == False:
    # click "zaakceptuj wszystko"
        button_path = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
        wait = WebDriverWait(driver, 1)
        button = wait.until(EC.visibility_of_element_located((By.XPATH, button_path)))
        button.click()
        wait = WebDriverWait(driver, 1)
        googleAcceptButtonClicked = True
    ### koniec

    page_content = driver.page_source

    response = Selector(page_content)
    results = []

    place_type = re.search('search/(.*)/@', url).group(1)
    print(place_type)
    #place_type = place_type[1:len(place_type)-1] # delete first and last character from string
    #place_type = place_type[1:] # delete first and last character from string
    for el in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
        results.append({
            'link': el.xpath('./a/@href').extract_first(''),
            'title': el.xpath('./a/@aria-label').extract_first(''),
            'type': place_type
        })

    return results


def convertToDataFrame(results):
    df = pd.DataFrame(results)

    # print(df, df.shape[0], df.shape[1])

    return df


def addLonLatToDataFrame(df):
    lat = []
    lon = []
    for index, row in df.iterrows():
        link = df.at[index, 'link']
        #print(link, "\n")
        latLon = re.search('!3d(.*)!16', link).group(1).split('!4d')
        #print(latLon[0], latLon[0])
        lat.append(latLon[0])
        lon.append(latLon[1])

    df['lat'] = lat
    df['lon'] = lon

    df = df[['lat', 'lon', 'type', 'title', 'link']]  # set order of columns

    return df

def finish():
    driver.quit()


def generateUrls():

    # BEGIN GENERATE POINTS
    """
    example:
    Point A --> (left_top_lat, left_top_lon)
    Point B --> (right_bot_lat, right_bot_lon)

    Covered area:
        A -- -- -- -- --
        |               |
        |               |
        -- -- -- -- -- B
    """
    left_top_lat = 54.35256034012475
    left_top_lon = 18.649113973109433
    right_bot_lat = 54.34451657944786
    right_bot_lon = 18.660621261438457

    diff_lat = left_top_lat - right_bot_lat
    diff_lon = left_top_lon - right_bot_lon

    size = 3 #number of "steps" (resolution of division of the area --> greater value gives more details)
    step_lat = diff_lat/size
    step_lon = diff_lon/size

    points_lat = []
    points_lon = []
    for i in range(size):
        curr_lat = left_top_lat - i*step_lat
        for j in range(size):
            curr_lon = left_top_lon - j*step_lon
            points_lat.append(curr_lat)
            points_lon.append(curr_lon)

    points_all = {'lat': points_lat, 'lon': points_lon}
    points_df = pd.DataFrame(points_all)

    # END GENERATE POINTS
    # BEGIN GENERATE URLS
    base = 'https://www.google.com/maps/search/'
    #types_of_places = ['bar', 'restaurant', 'coffee', 'public_transport', 'hotel']
    types_of_places = ['bar']

    generated_urls = []
    for types in types_of_places:
        for index, row in points_df.iterrows():
            point_lat = points_df.at[index, 'lat']
            point_lon = points_df.at[index, 'lon']
            zoom = 18
            url = base
            #url += str(types) + '+near+Gdansk,+Poland/@'
            url += str(types) + '/@'
            url += str(point_lat) + ',' + str(point_lon) + ',' +str(zoom) + 'z'
            print(url)
            #print('https://www.google.com/maps/search/bars+near+Gdansk,+Poland/@54.37083931588029,18.609653070782628,13z')
            generated_urls.append(url)
    return generated_urls

if __name__ == "__main__":

    urls = generateUrls()

    list_of_places = []
    for url in urls:
        new_places = searchForPlace(url)
        list_of_places += new_places  # concat two lists

    df = convertToDataFrame(list_of_places)

    df = df.drop_duplicates()
    df = addLonLatToDataFrame(df)

    print(df['title'].unique())
    print(df.shape[0], df.shape[1])

    for index, row in df.iterrows():
        print(row['type'], row['title'])


    finish()
