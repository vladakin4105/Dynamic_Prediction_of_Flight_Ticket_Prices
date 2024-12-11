import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def prediction():
    # extrag informatiile din data_flights.csv sub forma de dictionar
    df = pd.read_csv(r"data_flights.csv")
    prices_dict = df.iloc[0].to_dict()

    # preiau lista valorilor din dictionar
    prices_list = prices_dict.values()

    # folosim Regresia Liniară, deoarece predictia o facem deocamdata doar la nivel de valori ale preturilor
    # !Dacă vrem să dezvoltăm condițiile în care avem prețurile, folosim KNN

    # *configurăm regresia
    regress = LinearRegression()
    X = np.array(range(len(prices_list))).reshape(-1, 1)
    y = np.array(prices_list)
    regress.fit(X,y)

    # setăm pretul pentru următoarea săptămână
    # !Dacă vrem prețul pentru o altă săptămână, folosim regress.coef_ (panta dreptei de regresie) si regress.intercept_ (coeficientul liber)
    last = len(prices_list) - 1
    nextList = [[last + 1]]
    predictie = regress.predict(nextList)
    return predictie

