import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pickle
import matplotlib.pyplot as plt
import random

melbourne_file_path = 'D:\python\Python projects\My projects\Housing price prediction\Model\melb_data.csv'

melbourne_data = pd.read_csv(melbourne_file_path)
melbourne_data = melbourne_data.dropna(axis=0)

# print(melbourne_data.columns)

placeslist = melbourne_data.Suburb.unique().tolist()
placeslist = placeslist[0:11]
pricelist = []
prices = melbourne_data.Price.tolist()
maxprice = max(prices)
minprice = min(prices)

for i in range(len(placeslist)):
    p = random.randint(minprice,maxprice)
    pricelist.append(p)
print(pricelist)

x=np.array(placeslist)
y=np.array(pricelist)

plt.title("Comparision Grapgh Of House Price In Different Areas")
plt.xlabel("PlaceName")
plt.ylabel("Price(in dollors)")

plt.bar(x, y)

plt.show()
