import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from darts.models import FFT

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


for name in df["NOC"].unique():
    country_df = df[df["NOC"]==name]
    
    if len(country_df)>25:
        print(name)
        country_df["Delta_Gold"]   = country_df["Gold"].diff().fillna(value=0)
        country_df["Delta_Silver"] = country_df["Silver"].diff().fillna(value=0)
        country_df["Delta_Bronze"] = country_df["Bronze"].diff().fillna(value=0)
        country_df["Delta_Total"]  = country_df["total_medals"].diff().fillna(value=0)
        
        """
        train_df = country_df.iloc[:len(country_df)-4,:]
        last_date = train_df["Year"].max()
        model = ARIMA(train_df["Delta_Gold"], order=(1, 2, 3)) # Replace p, d, and q with appropriate values try grid search
        model_fit = model.fit()
        print(model_fit.summary())
        forecast = model_fit.forecast(steps=5)
        plt.plot(country_df["Year"], country_df["Delta_Gold"])
        plt.plot([last_date+4*x for x in range(1,6)], forecast)
        plt.show()
        plt.clf()
        #plot_medal_counts(name, country_df)
        """
        

        