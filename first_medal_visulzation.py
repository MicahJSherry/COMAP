import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt

base = "2025_Problem_C_Data"
# Rank	NOC	Gold	Silver	Bronze	Total	Year
countries_path = f"{base}/summerOly_medal_counts.csv"


df = pd.read_csv(countries_path)
df["NOC"] = df["NOC"].str.strip()
df["total_medals"] = df["Gold"]+df["Silver"]+df["Bronze"]
df = df.sort_values(by=["Year"]).reset_index()

have_medals = []
years = df["Year"].unique()
first_medals = []

for year in years:
    x = 0 
    for c in df[df["Year"]==year]["NOC"].unique():
        if c not in have_medals:
            print(c)
            have_medals.append(c)
            x+=1
    first_medals.append(x)  
print(years)
print(first_medals)

plt.bar(years.astype(str), first_medals)
plt.xticks(rotation=90)
plt.savefig("imgs/first_medal_count.png")