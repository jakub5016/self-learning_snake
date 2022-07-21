import numpy as np 
import pandas as pd


weights_and_baias = pd.read_csv("w_and_b.csv")

print(weights_and_baias)

weigths = weights_and_baias["weight"].values

weights_and_baias.to_csv("data.csv", index=0)

print(weigths)