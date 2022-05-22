import tkinter as tk
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import pyproj
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def test_topomap():
    lat = 47.136040305555554
    lon = 13.119993583333335

    gdf = gpd.read_file('tests/NUTS_RG_01M_2021_4326.json')
    print([col for col in gdf.columns])
    gdf.crs = 'EPSG:4326'
    gdf = gdf.to_crs('EPSG:4326')
    
    fig, ax = plt.subplots()

    gdf.plot(ax=ax, kind='geo', alpha=0.5)

    ax.set_xlim(lon-3, lon+3)
    ax.set_ylim(lat-3, lat+3)

    ax.scatter([lon], [lat], color='crimson')

    fig.savefig('tests/GeoPandasTopo.pdf')
    return None


def test():
    lat = 47.136040305555554
    lon = 13.119993583333335

    gdf = gpd.read_file('tests/NUTS_RG_01M_2021_3035.json')
    gdf.crs = 'EPSG:3035'
    gdf = gdf.to_crs('EPSG:4326')

    gdf1 = gdf[gdf.CNTR_CODE == "AT"]
    gdf2 = gdf[gdf.CNTR_CODE != "AT"]

    fig, ax = plt.subplots()
    gdf1.plot(ax=ax, alpha=0.0)

    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    
    gdf2.plot(ax=ax, alpha=1.0)

    ax.scatter([lon], [lat], color='crimson')    

    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.HOT, crs=gdf1.crs)
    
    fig.savefig('tests/geopandas_NUTS_2021_EUROPE.pdf')
    
    return None


def test_ctx(zoom=13):
    root = tk.Tk()

    plt.rcParams['figure.dpi'] = 100
    print('Loading Map..')
    place = ctx.Place("Bad Gastein", source=ctx.providers.OpenTopoMap, zoom=zoom)
    print('..Loaded Map!')

    fig, ax = plt.subplots(figsize=(20,20))
    ax.axis('off')

    chart_type = FigureCanvasTkAgg(fig, root)
    chart_type.get_tk_widget().pack(side='top', fill=tk.BOTH)

    place.plot(ax)
    lon = 13.119993583333335
    lat = 47.136040305555554
    transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3857')
    lat_w, lon_w = transformer.transform(lat, lon)

    ax.scatter([lat_w], [lon_w], color='crimson')

    fig.savefig('tests/TestPlace.pdf')
    print('saved tests/TestPlace.pdf')

    root.mainloop()
    return None


def test_wholeworld():
    lat = 47.136040305555554
    lon = 13.119993583333335

    df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    print(df)

    fig, ax = plt.subplots()
    df.plot(ax=ax)

    ax.scatter([lon], [lat], color='crimson')

    ax.set_xlim((lon-5, lon+5))
    ax.set_ylim((lat-5, lat+5))
    
    fig.savefig('tests/geopandas_setrange.pdf')

    
    
    return None


if __name__=='__main__':
    # test()
    test_ctx()
    # test_topomap()
