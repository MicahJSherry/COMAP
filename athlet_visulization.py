import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 


base = "2025_Problem_C_Data"
# Name, Sex,  Team,  NOC,  Year, City, Sport, Event,  Medal
athletes_path = f"{base}/summerOly_athletes.csv"

df = pd.read_csv(athletes_path)


df["Gold"] = (df["Medal"] == "Gold").astype(int)
df["Silver"] = (df["Medal"] == "Silver").astype(int)
df["Bronze"] = (df["Medal"] == "Silver").astype(int)
df["Total"] = df[["Gold", "Silver", "Bronze"]].sum(axis=1)
print(df.head(40))


grouping_cols  = ["Name","Sex", "Team"]
df = df.groupby(grouping_cols)[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index()

max_gold = df["Gold"].max()
max_total = df["Total"].max()
gold_dist=  [0]*(max_gold+1)
totals_dist = [0]*(max_total+1)

for i, x  in df.iterrows():
    if x["Gold"] >0: 

        gold_dist[x["Gold"]] +=  1
        totals_dist[x["Total"]] +=  1

plt.ylabel("number of athletes")
plt.xlabel("number of metals")
plt.bar([i for i in range(max_gold+1)],gold_dist)
plt.title("athlete Gold Medal Counts")
plt.savefig("imgs/athlets_medal_distributions/gold_dist.png")
plt.clf()


plt.ylabel("number of athletes")
plt.xlabel("number of metals")
plt.bar([i for i in range(max_total+1)],totals_dist)
plt.title("athlete total Medal Counts")
plt.savefig("imgs/athlets_medal_distributions/total_dist.png")
plt.clf()


plt.ylabel("number of athletes")
plt.xlabel("number of metals")
plt.bar([i for i in range(max_gold+1)],np.log(np.array(gold_dist)+1))
plt.title("athlete Gold log Medal Counts")
plt.savefig("imgs/athlets_medal_distributions/log_gold_dist.png")
plt.clf()


plt.ylabel("number of athletes")
plt.xlabel("number of metals")
plt.bar([i for i in range(max_total+1)],np.log(np.array(totals_dist)+1))
plt.title("athlete total log Medal Counts")
plt.savefig("imgs/athlets_medal_distributions/log_total_dist.png")
plt.clf()


#new_df.sort_values(by=["Name","Year"], ascending=True)

#print(new_df.sort_values(by="Medal_score", ascending=False))


