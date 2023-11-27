import matplotlib.dates as mdates
from matplotlib.colors import ListedColormap

def Get_Date_Formatter():
    return mdates.DateFormatter('%b-%Y')

def Get_Custom_Colormap():
    colorList = [
    '#C1D08A', '#B0C1B3', '#F08080', '#9EA1D4', '#FFA07A',
    '#7CB46B', '#A8D1D1', '#FEC868', '#97ECF1', '#FF6347',
    '#96845A', '#FF4500', '#1E90FF', '#8FBC8F', '#FFD700',
    '#FF69B4', '#FFE4B5', '#20B2AA', '#87CEEB', '#FFD700',
    '#FF6347', '#9370DB', '#3CB371', '#FFD700', '#FFA07A',
    '#FF4500', '#FF69B4', '#20B2AA', '#9370DB', '#32CD32']
    return colorList

