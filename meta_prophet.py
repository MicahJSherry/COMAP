import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt


from prophet import Prophet

from sklearn.metrics import mean_squared_error

base = "2025_Problem_C_Data"
# Rank	NOC	Gold	Silver	Bronze	Total	Year
countries_path = f"{base}/summerOly_medal_counts.csv"


df = pd.read_csv(countries_path)
df["Year"] = pd.to_datetime(df["Year"],format="%Y")
print(df["Year"])
df["NOC"] = df["NOC"].str.strip()
df["total_medals"] = df["Gold"]+df["Silver"]+df["Bronze"]
df = df.sort_values(by=["NOC", "Year"]).reset_index()
#print(df.head(30))
X = []
y = []
for name in df["NOC"].unique():
    country_df = df[df["NOC"]==name]
    
    if len(country_df)>6:
        country_df = country_df.sort_values("Year")
        country_df["Delta_Gold"]   = country_df["Gold"].diff().fillna(value=0)
        country_df["Delta_Silver"] = country_df["Silver"].diff().fillna(value=0)
        country_df["Delta_Bronze"] = country_df["Bronze"].diff().fillna(value=0)
        country_df["Delta_Total"]  = country_df["total_medals"].diff().fillna(value=0)
        
        country_df["percent_Delta_Gold"] = (country_df["Delta_Gold"]/country_df["Delta_Gold"].abs().mean()).fillna(value=0)
        country_df["percent_Delta_Silver"] = country_df["Delta_Silver"]/country_df["Delta_Silver"].abs().mean()
        country_df["percent_Delta_Bronze"] = country_df["Delta_Bronze"]/country_df["Delta_Bronze"].abs().mean()
        country_df["percent_Delta_Total"] = country_df["Delta_Total"]/country_df["Delta_Total"].abs().mean()

        gold = country_df[["Year","Delta_Gold"]].rename(columns={'Year': 'ds', 'Delta_Gold': 'y'}).reset_index(drop=True).iloc[:-2]
        print(gold)
        model = Prophet()
        model.fit(gold)        
        future = model.make_future_dataframe(periods=3,freq="4Y")
        print(future)
        plt.plot(gold["ds"],gold["y"],label= "gold")
        #plt.plot(pred_gold,label="predicted")
        plt.legend()
        plt.show()
        exit()