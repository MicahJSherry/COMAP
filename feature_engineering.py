'''
Dataset Features

Year - year of olympics
Host_Country - country hosting olympics
Competing_Country - name of country competing per year/game
Country_Total_Athletes - total number of athletes representing a country at olympics
Country_Total_Medals - total gold, silver, bronze medals earned by a country
Country_Golds - total gold medals
Country_Silvers - total silver medals
Country_Bronzes - total bronze medals
Country_Rank - final place country ended in based on medal counts
Country_Delta_Total_Medals - change in country's total medals between this and previous olympics
Country_Delta_Rank - change in country's final place between this and previous olympics
Country_Delta_Golds - change in country's gold medals
Country_Delta_Silvers - change in country's silver medals
Country_Delta_Bronzes - change in country's bronze medals
Games_Competed_In - running total of number of olympics country competed in
Game_Events - number of events at olympics
Country_Total_Events - number of events country had athletes compete in
Game_<Sport>_Events - number of events for a sport and its disciplines at olympics
Country_<Sport>_Enrollment - number of athletes representing a country for a sport and its disciplines
Country_Athlete_Turnover - percentage of debuting athletes for a country compared to past olympics across all sports
Country_Female_Athletes - number of female athletes representing a country
Country_Male_Athletes - number of male athletes representing a country
Game_Mens_Events - number of men's events at olympics
Game_Womens_Events - number of women's events at olympics
Game_Mixed_Events - number of mixed events at olympics
Country_Mens_Events_Enrollment - number of athletes representing a country in men's events
Country_Womens_Events_Enrollment - number of athletes representing a country in women's events
Country_Mixed_Events_Enrollment - number of athletes representing a country in mixed events
'''

import pandas as pd

def country_total_athletes(comap_df):
    all_ioc = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/all_ioc.csv').set_index('Nation')['Code'] # load 3-letter country codes
    print(f'Country codes:\n{all_ioc.head(n=15)}')
    athletes_data = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_athletes.csv')

    total_athletes = []
    for year in game_participating_countries:
        print(f'Processing athletes for every country in {year} olympics...')
        for country in game_participating_countries[year]:
            curr_year_data = athletes_data.loc[(athletes_data['Year'] == year) & (athletes_data['NOC'] == all_ioc[country])]
            athlete_names = curr_year_data['Name'].unique()
            total_athletes.append(len(athlete_names))

    comap_df['country_total_athletes'] = total_athletes
    print(f'Updated dataframe:\n{comap_df.head(n=25)}')
    return comap_df

hosts = pd.read_csv("/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_hosts_cleaned.csv")
medal_count = pd.read_csv("/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_medal_counts.csv")

host_years = hosts["Year"]
host_locations = hosts["Host"]

game_host_countries = {} # maps an olympic year to its host country
game_participating_countries = {} # maps an olympic year to a set of countries competing in it
for year in host_years:
    curr_year_data = medal_count.loc[(medal_count['Year'] == year)] # slice dataframe so only rows where Year = current year are included
    game_participating_countries[year] = sorted(set(curr_year_data['NOC'])) # sort the competing countries alphabetically

    curr_year_data = hosts.loc[(hosts['Year'] == year)] # slice dataframe so only rows where Year = current year are 
    curr_year_location = curr_year_data['Host'].values[0] # get the Host column, convert it to a list of its values, then get the 1st value (a string)
    location_parts = curr_year_location.split(',') # separate the city and the country (we only want the country)
    game_host_countries[year] = location_parts[1] # map the olympic year to the host country

print(f'1896 host country: {game_host_countries[1896]}')
print(f'1896 competing countries: {game_participating_countries[1896]}')
    
init_df_dict = {'year':[], 'host_country':[], 'competing_country':[]} # dict to initialize the new dataframe from
for year in game_participating_countries:
    competing_countries = game_participating_countries[year]
    num_competing_counties = len(competing_countries) # get the number of countries competing in current year's olympics
    
    # add countries to dataframe dict (each gets its own row)
    for country in competing_countries:
        init_df_dict['competing_country'].append(country)

    # add year and host country to dataframe dict
    for i in range(num_competing_counties):
        init_df_dict['year'].append(year)
        init_df_dict['host_country'].append(game_host_countries[year])
comap_df = pd.DataFrame.from_dict(init_df_dict)
print(f'Initial dataframe:\n{comap_df.head(n=25)}')

# create country_total_athletes column
comap_df = country_total_athletes(comap_df)
comap_df.to_csv('foo.csv')


