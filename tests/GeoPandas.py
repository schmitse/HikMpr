import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


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
    test()
