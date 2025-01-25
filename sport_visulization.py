import pandas as pd 
pd.options.mode.copy_on_write = True
import matplotlib.pyplot as plt

base = "2025_Problem_C_Data"


# Rank, NOC, Gold, Silver,  Bronze, Total, Year

#countries_path = f"{base}/summerOly_medal_counts.csv"
#countries_df = pd.read_csv(countries_path)
#countries_df["NOC"] = countries_df["NOC"].str.strip()

# Name, Sex,  Team,  NOC,  Year, City, Sport, Event,  Medal
athletes_path = f"{base}/summerOly_athletes.csv"
athletes_df = pd.read_csv(athletes_path)

#Sport,Discipline,Code,Sports Governing Body, [1896...2024]

programs_path = f"{base}/summerOly_programs.csv"
programs_df = pd.read_csv(programs_path)

athletes_df["Gold"] = (athletes_df["Medal"] == "Gold").astype(int)
athletes_df["Silver"] = (athletes_df["Medal"] == "Silver").astype(int)
athletes_df["Bronze"] = (athletes_df["Medal"] == "Silver").astype(int)
athletes_df["Total"] = athletes_df[["Gold", "Silver", "Bronze"]].sum(axis=1)

grouping_cols  = ["NOC","Sport","Sex", "Year"]
athletes_df = athletes_df.groupby(grouping_cols)[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index()
#athletes_df = athletes_df[athletes_df["Total"]>1]
athletes_df = athletes_df.sort_values(["NOC","Sport","Sex", "Year"])


for sport in programs_df["Sport"].unique():
    print(sport)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title(f"Male {sport} by Country")
    ax2.set_title(f"Female {sport} by Country")

    for team in athletes_df["NOC"].unique():
        
        M_df = athletes_df[(athletes_df["NOC"]==team) & (athletes_df["Sport"]==sport)& (athletes_df["Sex"]=="M")]
        F_df = athletes_df[(athletes_df["NOC"]==team) & (athletes_df["Sport"]==sport)& (athletes_df["Sex"]=="F")]
        print(team, sport)
        if M_df["Total"].max()>0:
            ax1.plot(M_df["Year"], M_df["Total"])
            
        if F_df["Total"].max()>0:
            ax2.plot(F_df["Year"], F_df["Total"])

    plt.savefig(f"imgs/medal_trends_by_sport/{sport}_gloabal_gold.png")
    plt.clf()
        
print(athletes_df.head(30))



