'''
Dataset Features

Year - year of olympics
Host_Country - country hosting olympics
Country - name of country competing
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