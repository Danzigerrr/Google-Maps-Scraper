import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def setPlaces(points):
    points['size'] = 1000
    # df.drop('link', axis=1)
    points['color'] = 1

    color_scale = [(0, 'green'), (1, 'red')]

    fig = px.scatter_mapbox(points,
                            lat="lat",
                            lon="lon",
                            hover_name="title",
                            # hover_data=["title", "size"],
                            # color="Listed",
                            color_continuous_scale=color_scale,
                            color='type',
                            size="size",
                            zoom=14,
                            height=800,
                            width=800)

    return fig


def showMap(fig):
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def setBorderPoints(borders):
    borders['size'] = 5000
    borders['info'] = 'Border point'
    # df.drop('link', axis=1)
    borders['color'] = 0.3
    borders['type'] = 'border point'
    color_scale = [(0, 'green'), (1, 'red')]

    figWithBorders = px.scatter_mapbox(borders,
                                       lat="lat",
                                       lon="lon",
                                       hover_name="info",
                                       # hover_data=["title", "size"],
                                       # color="Listed",
                                       color_continuous_scale=color_scale,
                                       color='type',
                                       size="size",
                                       zoom=10,
                                       height=800,
                                       width=800)

    return figWithBorders


def visualiseCollectedPoints():
    columns = ['church', 'public transport', 'university', 'school', 'bar', 'hotel', 'restaurant', 'coffee']
    all_places = pd.DataFrame()
    for c in columns:
        places = pd.read_csv('database/' + c + '_v1.csv', index_col=False)
        frames = [all_places, places]
        all_places = pd.concat(frames)

    borderPoints = pd.read_csv('border_points_v2.csv', index_col=False)
    bordersMap = setBorderPoints(borderPoints)

    placesMap = setPlaces(all_places)

    placesMap.add_trace(bordersMap.data[0])
    showMap(placesMap)


def visualiseMeasurePoints():
    size = 15
    borderPoints = pd.read_csv('Points_size' + str(size) + '_v2.csv', index_col=False)
    bordersMap = setBorderPoints(borderPoints)
    showMap(bordersMap)


if __name__ == "__main__":
    visualiseCollectedPoints()
    #visualiseMeasurePoints()
