import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt

base = "2025_Problem_C_Data"
# Rank	NOC	Gold	Silver	Bronze	Total	Year
countries_path = f"{base}/summerOly_medal_counts.csv"


df = pd.read_csv(countries_path)
df["NOC"] = df["NOC"].str.strip()
df["total_medals"] = df["Gold"]+df["Silver"]+df["Bronze"]
df = df.sort_values(by=["total_medals"]).reset_index()

print(df.head(30))