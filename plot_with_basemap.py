# pip | conda install basemap
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

db_path = "data/minard.db"

# STEP: Acquire Dataframes from SQL-------------------------------------
connection = sqlite3.connect(db_path)

city_df = pd.read_sql('''SELECT * FROM cities;''', con=connection)
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""", con=connection)
troop_df = pd.read_sql("""SELECT * FROM troops;""", con=connection) # lonp latp surviv direc division

connection.close()

# STEP: Prepare data in ndArray-------------------------------------
loncs = city_df['lonc'].values
latcs = city_df['latc'].values
city_names = city_df['city'].values

rows = troop_df.shape[0]    # 48
lonqs = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values

# STEP: Draw basemap, cities on Axes[0]-------------------------------------
fig, axes = plt.subplots(nrows=2, figsize=(25, 12), gridspec_kw={"height_ratios":[4, 1]})

m = Basemap(projection="lcc", 
            resolution="i", 
            width=1000000, height=400000,
            lon_0=31, lat_0=55,
            ax=axes[0])
m.drawcoastlines()
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58, 1), labels=[1, 0, 0, 0])         # draw latitudes range and labeling position on (left, right, up, down)
m.drawmeridians(range(23, 56, 2), labels=[0, 0, 0, 1])         # draw longitudes range and labeling position on (left, right, up, down)

# Label city names on map on Axes[0]-------------------------------------
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name, xy=(xi, yi), fontsize=14, zorder=2)

# Draw troops direction lines on Axes[0]
j, k = m(lonqs, latps)
for i in range(rows-1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "red"

    line_lonqs = (j[i], j[i+1])
    line_latps = (k[i], k[i+1])

    axes[0].plot(line_lonqs,
                 line_latps,
                 color=line_color,
                 linewidth=survivals[i]/10000,
                 zorder=1
                )

# STEP: Drawing temperatures on Axes[1]
temp_celcius = (temperature_df["temp"] * 5/4)    # convert temp to Celcius
lonts = temperature_df["lont"]

date_str = temperature_df["date"]
annotations = temp_celcius.astype(int).astype(str).str.cat(date_str, sep="°C ") # str.cat(series, sep="") is a method from pandas

axes[1].plot(lonts, temp_celcius, linestyle="dotted", color="blue")
for lont, temp_c, annotation in zip(lonts, temp_celcius, annotations):
    axes[1].annotate(annotation, xy=(lont, temp_c), fontsize=14)

axes[1].set_xlim(24, 38)
axes[1].set_ylim(-40, 5)
axes[1].spines["top"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].grid(True, which="major", axis="both")
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])

# plt.show()
fig.savefig("minard_clone_viz")




