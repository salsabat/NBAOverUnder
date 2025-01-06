import pandas as pd
import numpy as np
from nba_api.stats.library.parameters import Season
from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.endpoints import PlayerGameLog
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import sys

keep_headers = {'MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 
                'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PTS', 'PLUS_MINUS'}
max_seasons_of_data = 4

def get_player_recent_stats(player_name):
    last_five_games_stats = LeagueDashPlayerStats(
        season=Season.default,
        last_n_games='5',
        per_mode_detailed='PerGame'
    )
    input_data = last_five_games_stats.get_dict()

    input_headers = input_data['resultSets'][0]['headers']
    input_df = pd.DataFrame(columns=input_headers)
    for i in range(len(input_data['resultSets'][0]['rowSet'])):
        if input_data['resultSets'][0]['rowSet'][i][1] == player_name:
            player_id = input_data['resultSets'][0]['rowSet'][i][0]
            input_df.loc[i] = input_data['resultSets'][0]['rowSet'][i]
            break
    
    input_df.drop([col for col in input_headers if col not in keep_headers], axis=1, inplace=True)
    input_df = input_df[list(keep_headers)]

    return (input_df, player_id)

def get_player_game_log(player_id):
    def update_training_data(df, season_stats):
        all_game_data = season_stats.get_dict()
        for game_data in all_game_data['resultSets'][0]['rowSet']:
            df.loc[len(df.index)] = game_data

    this_season_stats = PlayerGameLog(player_id, season=Season.current_season)
    this_season_game_data = this_season_stats.get_dict()
    training_headers = this_season_game_data['resultSets'][0]['headers']
    training_df = pd.DataFrame(columns=training_headers)

    update_training_data(training_df, this_season_stats)
    for i in range(1, max_seasons_of_data):
        season = '{}-{}'.format(Season.current_season_year - i, str(Season.current_season_year - i + 1)[2:])
        season_stats = PlayerGameLog(player_id, season=season)
        update_training_data(training_df, season_stats)
    
    training_df.drop([col for col in training_headers if col not in keep_headers], axis=1, inplace=True)
    training_df = training_df[list(keep_headers)]

    return training_df


if __name__ == '__main__':
    input_df, player_id = get_player_recent_stats('Kevin Durant')
    training_df = get_player_game_log(player_id)
    print(input_df)
    print(training_df)