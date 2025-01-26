'''
Dataset Feature Engineering

Year - year of olympics
Host_Country - country hosting olympics
Competing_Country - name of country competing per year/game
Country_Total_Athletes - total number of athletes representing a country at olympics
Country_Total_Medals - total gold, silver, bronze medals earned by a country at olympics
Country_Golds - total gold medals country earned at olympics
Country_Silvers - total silver medals country earned at olympics
Country_Bronzes - total bronze medals country earned at olympics
Country_Rank - final place country ended in based on medal counts
Country_Delta_Total_Medals - change in country's total medals between this and previous olympics
Country_Delta_Rank - change in country's final place between this and previous olympics
Country_Delta_Golds - change in country's gold medals
Country_Delta_Silvers - change in country's silver medals
Country_Delta_Bronzes - change in country's bronze medals
Country_Total_Appearances - running total of number of olympics country competed in
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

def init_basics():
    hosts = pd.read_csv("/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_hosts_cleaned.csv")
    medal_counts = pd.read_csv("/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_medal_counts.csv")
    all_ioc = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/all_ioc.csv').set_index('Nation')['Code'] # load 3-letter country codes
    athletes_data = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_athletes.csv')
    programs_data = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/summerOly_programs_cleaned.csv')

    host_years = hosts["Year"]

    game_host_countries = {} # maps an olympic year to its host country
    game_participating_countries = {} # maps an olympic year to a set of countries competing in it
    for year in host_years:
        if year > 2024:
            # no data for programs/athletes/medals for beyond 2024, so don't include this info
            continue

        curr_year_data = medal_counts.loc[(medal_counts['Year'] == year)] # slice dataframe so only rows where Year = current year are included
        game_participating_countries[year] = sorted(set(curr_year_data['NOC'])) # sort the competing countries alphabetically

        curr_year_data = hosts.loc[(hosts['Year'] == year)] # slice dataframe so only rows where Year = current year are 
        curr_year_location = curr_year_data['Host'].values[0] # get the Host column, convert it to a list of its values, then get the 1st value (a string)
        location_parts = curr_year_location.split(',') # separate the city and the country (we only want the country)
        game_host_countries[year] = location_parts[1] # map the olympic year to the host country

    print(f'1896 host country: {game_host_countries[1896]}')
    print(f'1896 competing countries: {game_participating_countries[1896]}')

    return hosts, medal_counts, all_ioc, athletes_data, game_host_countries, game_participating_countries, programs_data

def init_df(game_participating_countries:dict, game_host_countries:dict):    
    print('Initializing olympics data dataframe...')

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

    olympics_df = pd.DataFrame.from_dict(init_df_dict)
    print(f'Initial dataframe:\n{olympics_df.head(n=25)}')

    return olympics_df

def country_total_athletes(olympics_df:pd.DataFrame, game_participating_countries:dict, all_ioc:pd.DataFrame, athletes_data:pd.DataFrame):
    '''
    total number of athletes representing a country at olympics
    '''

    print('Engineering country_total_athletes feature...')

    total_athletes = []

    for year in game_participating_countries:
        print(f'Processing athletes for every country in {year} olympics...')
        for country in game_participating_countries[year]:
            curr_year_data = athletes_data.loc[(athletes_data['Year'] == year) & (athletes_data['NOC'] == all_ioc[country])]
            athlete_names = curr_year_data['Name'].unique()
            total_athletes.append(len(athlete_names))

    olympics_df['country_total_athletes'] = total_athletes
    print(f'Updated dataframe:\n{olympics_df.head(n=25)}')
    return olympics_df

def country_total_medals(olympics_df:pd.DataFrame, medal_counts:pd.DataFrame, game_participating_countries:dict):
    '''
    total gold, silver, bronze medals earned by a country at olympics
    '''

    print('Engineering country_total_medals feature...')

    total_medals = []

    for year in game_participating_countries:
        print(f'Processing medal counts for every country in {year} olympics...')
        for country in game_participating_countries[year]:
            curr_year_data = medal_counts.loc[(medal_counts['Year'] == year) & (medal_counts['NOC'] == country)]
            total_medals.append(curr_year_data['Total'].values[0])
    
    olympics_df['country_total_medals'] = total_medals
    print(f'Updated dataframe:\n{olympics_df.head(n=25)}')
    return olympics_df

def country_total_appearances(olympics_df:pd.DataFrame):
    '''
    running total of number of olympics country competed in
    '''

    print('Engineering country_total_appearances...')
    olympics_df['country_total_appearances'] = olympics_df.groupby(['competing_country'], sort=False, observed=True).cumcount() + 1
    return olympics_df

def game_sport_events(olympics_df:pd.DataFrame, programs_data:pd.DataFrame, game_participating_countries:dict):
    '''
    Adds columns for number of events for a sport and its disciplines at olympics
    '''

    print('Engineering game_<sport>_events feature...')

    sports = sorted(programs_data['Sport'].unique()) # get all sports
    temp_dfs = []
    for sport in sports:
        temp_df_dict = {f'game_{sport.lower()}_events': []}
        curr_sport_data = programs_data.loc[(programs_data['Sport'] == sport)]
        for year in game_participating_countries:
            num_participating_countries = len(game_participating_countries[year])
            temp_df_dict[f'game_{sport.lower()}_events'].extend(curr_sport_data[str(year)].sum().astype('int') for _ in range(num_participating_countries))
        temp_df = pd.DataFrame.from_dict(temp_df_dict)
        temp_dfs.append(temp_df)
    merged_df = pd.concat(temp_dfs, axis=1)
    
    olympics_df = pd.concat([olympics_df, merged_df], axis=1)
    print(f'Updated dataframe:\n{olympics_df.head(n=25)}')
    return olympics_df

def country_golds(olympics_df:pd.DataFrame, medal_counts:pd.DataFrame, game_participating_countries:dict):
    golds_per_country = []

    print('Engineering country_golds feature...')

    for year in game_participating_countries:
        countries = game_participating_countries[year]
        for country in countries:
            curr_games_data = medal_counts.loc[(medal_counts['Year'] == year) & (medal_counts['NOC'] == country)]
            golds_per_country.append(curr_games_data['Gold'].values[0])

    olympics_df['country_golds'] = golds_per_country
    print(f'Updated dataframe:\n{olympics_df.head(n=25)}')
    return olympics_df

def country_silvers(olympics_df:pd.DataFrame, medal_counts:pd.DataFrame, game_participating_countries:dict):
    silvers_per_country = []

    print('Engineering country_silvers feature...')

    for year in game_participating_countries:
        countries = game_participating_countries[year]
        for country in countries:
            curr_games_data = medal_counts.loc[(medal_counts['Year'] == year) & (medal_counts['NOC'] == country)]
            silvers_per_country.append(curr_games_data['Silver'].values[0])
    olympics_df['country_silvers'] = silvers_per_country
    
    return olympics_df

def country_bronzes(olympics_df:pd.DataFrame, medal_counts:pd.DataFrame, game_participating_countries:dict):
    bronzes_per_country = []

    print('Engineering country_bronzes feature...')

    for year in game_participating_countries:
        countries = game_participating_countries[year]
        for country in countries:
            curr_games_data = medal_counts.loc[(medal_counts['Year'] == year) & (medal_counts['NOC'] == country)]
            bronzes_per_country.append(curr_games_data['Bronze'].values[0])
    olympics_df['country_bronzes'] = bronzes_per_country

    return olympics_df

def country_rank(olympics_df:pd.DataFrame, medal_counts:pd.DataFrame, game_participating_countries:dict):
    rank_per_country = []

    for year in game_participating_countries:
        countries = game_participating_countries[year]
        for country in countries:
            curr_game_data = medal_counts.loc[(medal_counts['Year'] == year) & (medal_counts['NOC'] == country)]
            rank_per_country.append(curr_game_data['Rank'].values[0])
    olympics_df["country_ranking"] = rank_per_country

    return olympics_df

def main():    
    hosts, medal_counts, all_ioc, athletes_data, game_host_countries, game_participating_countries, programs_data = init_basics()

    # initialize dataframe if empty (so we haven't done any feature engineering before)
    try:
        olympics_df = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/olympics_data.csv')
    except pd.errors.EmptyDataError as e:
        olympics_df = init_df(game_participating_countries, game_host_countries)

    # create country_total_athletes column
    if 'country_total_athletes' not in olympics_df:
        olympics_df = country_total_athletes(olympics_df, game_participating_countries, all_ioc, athletes_data)

    # create country_total_medals column
    if 'country_total_medals' not in olympics_df:
        olympics_df = country_total_medals(olympics_df, medal_counts, game_participating_countries)

    # create country_total_appearances
    if 'country_total_appearances' not in olympics_df:
        country_total_appearances(olympics_df)

    if 'country_golds' not in olympics_df:
        olympics_df = country_golds(olympics_df, medal_counts, game_participating_countries)

    if 'country_silvers' not in olympics_df:
        olympics_df = country_silvers(olympics_df, medal_counts, game_participating_countries)

    if 'country_bronzes' not in olympics_df:
        olympics_df = country_bronzes(olympics_df, medal_counts, game_participating_countries)

    if 'country_ranking' not in olympics_df:
        olympics_df = country_rank(olympics_df, medal_counts, game_participating_countries)

    # create game_<sport>_events columns
    sports = programs_data['Sport'].unique()
    for sport in sports:
        if f'game_{sport.lower()}_events' not in olympics_df:
            olympics_df = game_sport_events(olympics_df, programs_data, game_participating_countries)
            break

    olympics_df.to_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/olympics_data.csv', index=False)

if __name__ == '__main__':
    main()
