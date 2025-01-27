import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from darts.models import FFT
import numpy as np

from xgboost import XGBRegressor
#from sklearn.svm import SVR       
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def plot_medal_counts(name, country_df):
    
        plt.plot(country_df["Year"], country_df["Gold"], label="Gold",)
        plt.plot(country_df["Year"], country_df["Delta_Gold"], label="Delta Gold")
        #plt.plot(country_df["Year"], country_df["Silver"], color="k", label="Silver")
        #plt.plot(country_df["Year"], country_df["Bronze"], color="r", label="Bronze")
        plt.plot(country_df["Year"], country_df["total_medals"], label="Total")
        plt.plot(country_df["Year"], country_df["Delta_Total"], label="Delta Total")
        

        plt.legend()
        plt.title(f"{name} medal count")
        plt.savefig(f"imgs/MC_countries/{name}_medal_count.png")
        plt.clf()

base = "2025_Problem_C_Data"
# Rank	NOC	Gold	Silver	Bronze	Total	Year
countries_path = f"{base}/summerOly_medal_counts.csv"


df = pd.read_csv(countries_path)
df["NOC"] = df["NOC"].str.strip()
df["total_medals"] = df["Gold"]+df["Silver"]+df["Bronze"]
df = df.sort_values(by=["NOC", "Year"]).reset_index()
#print(df.head(30))
X = []
y = []
for name in df["NOC"].unique():
    country_df = df[df["NOC"]==name]
    
    if len(country_df)>5:
        
        country_df["Delta_Gold"]   = country_df["Gold"].diff().fillna(value=0)
        country_df["Delta_Silver"] = country_df["Silver"].diff().fillna(value=0)
        country_df["Delta_Bronze"] = country_df["Bronze"].diff().fillna(value=0)
        country_df["Delta_Total"]  = country_df["total_medals"].diff().fillna(value=0)
        
        country_df["percent_Delta_Gold"] = (country_df["Delta_Gold"]/country_df["Delta_Gold"].abs().mean()).fillna(value=0)
        country_df["percent_Delta_Silver"] = country_df["Delta_Silver"]/country_df["Delta_Silver"].abs().mean()
        country_df["percent_Delta_Bronze"] = country_df["Delta_Bronze"]/country_df["Delta_Bronze"].abs().mean()
        country_df["percent_Delta_Total"] = country_df["Delta_Total"]/country_df["Delta_Total"].abs().mean()
        
        
        #plot_medal_counts(name, country_df)
        #print(country_df[["NOC","Delta_Gold","Delta_Silver", "Delta_Bronze", "Delta_Total","percent_Delta_Gold","percent_Delta_Silver", "percent_Delta_Bronze", "percent_Delta_Total"]].head(30))
        for i in range(len(country_df)-6):
            #print(i)
            X.append(country_df[["percent_Delta_Gold","percent_Delta_Silver", "percent_Delta_Bronze", "percent_Delta_Total"]].iloc[i:i+5].to_numpy().reshape(-1))
            y.append(country_df[["percent_Delta_Gold","percent_Delta_Total"]].iloc[i+6].to_numpy())


X = np.array(X)
y = np.array(y)

print(y.shape)
print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from tensorflow import keras
#xgb = XGBRegressor(n_estimators=2000, max_depth=7, eta=0.1, subsample=.70, colsample_bytree=0.8)
#xgb.fit(X_train, y_train)
#y_pred = xgb.predict(X_test)
# Make predictions on the test data
#labels = [i for i in range(len(y_pred))]
#plt.bar(labels, y_pred[:,0])
#plt.bar(labels, y_test[:,0])
#plt.show()

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
