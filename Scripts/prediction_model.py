import pandas as pd
import numpy as np
from nba_api.stats.library.parameters import Season
from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static.players import get_active_players
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import sys

last_n_games = '10'
keep_headers = {'MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 
                'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PTS', 'PLUS_MINUS'}
max_seasons_of_data = 3


def get_player_recent_stats(player_name):
    last_five_games_stats = LeagueDashPlayerStats(
        season=Season.default,
        last_n_games=last_n_games,
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


def train_model(training_df, target_stat, money_line):
    X = training_df.drop(columns=target_stat)
    y = training_df[target_stat]
    for i in range(len(y)):
        y[i] = 1 if y[i] > money_line else 0
    
    if sum(y) == 0:
        return -4
    elif sum(y) == len(y):
        return -5
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(random_state=0, C=0.7, fit_intercept=True).fit(X_train_scaled, y_train)
    
    return (model, X_test_scaled, y_test, X_train_scaled, y_train, scaler)


def test_model(model, X_test_scaled, y_test, X_train_scaled, y_train):
    print(model.score(X_train_scaled, y_train))
    print(model.score(X_test_scaled, y_test))


def verify_inputs(player_name, target_stat, money_line):
    players_list = get_active_players()
    found = False
    for player in players_list:
        if player['full_name'] == player_name:
            found = True
            break
    if not found:
        return -1
    
    if target_stat not in keep_headers:
        return -2
    
    try:
        if money_line[len(money_line) - 2:] != '.5':
            return -3
        money_line = float(money_line)
    except:
        return -3
    
    return 0


def main():

    player_name = sys.argv[1] + ' ' + sys.argv[2]
    target_stat = sys.argv[3]
    money_line = sys.argv[4]

    valid = verify_inputs(player_name, target_stat, money_line)
    if valid != 0:
        return valid
    money_line = float(money_line)

    input_df, player_id = get_player_recent_stats(player_name)
    training_df = get_player_game_log(player_id)

    model_result = train_model(training_df, target_stat, money_line)
    if model_result == -4 or model_result == -5:
        return model_result

    model, X_test_scaled, y_test, X_train_scaled, y_train, scaler = model_result
    
    X_input = input_df.drop(columns=target_stat)
    X_input_scaled = scaler.transform(X_input)

    prediction = model.predict(X_input_scaled)
    prediction_prob = model.predict_proba(X_input_scaled)

    result = f'You should probably take the {'over' if prediction[0] == 1 else 'under'}: {prediction_prob[0][prediction[0]] * 100}%'
    return result

print(main())