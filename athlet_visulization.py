import pandas as pd 
import matplotlib.pyplot as plt



base = "2025_Problem_C_Data"
# Name, Sex,  Team,  NOC,  Year, City, Sport, Event,  Medal
athletes_path = f"{base}/summerOly_athletes.csv"

df = pd.read_csv(athletes_path)

medal_map = {"No medal":0, "Bronze":1, "Silver":2, "Gold":3}

df["Medal_score"] = df["Medal"].map(medal_map)
grouping_cols  = ["Name","Sex","Year","Team", "Sport"]



counts = df[grouping_cols].value_counts()
#print(counts)
new_df = df.groupby(grouping_cols)[["Medal_score"]].sum()
new_df["num_events"] = counts
new_df = new_df.reset_index()


print(new_df[new_df["num_events"]>=2].head(40))





#new_df.sort_values(by=["Name","Year"], ascending=True)

#print(new_df.sort_values(by="Medal_score", ascending=False))


