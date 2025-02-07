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

class ModelRunner:
    def __init__(self, player_name, target_stat, money_line):
        self.player_name = player_name

        last_five_games_stats = LeagueDashPlayerStats(
            season=Season.default,
            last_n_games=last_n_games,
            per_mode_detailed='PerGame'
        )
        input_data = last_five_games_stats.get_dict()

        self.player_id = -1
        input_headers = input_data['resultSets'][0]['headers']
        input_df = pd.DataFrame(columns=input_headers)
        for i in range(len(input_data['resultSets'][0]['rowSet'])):
            if input_data['resultSets'][0]['rowSet'][i][1].upper() == player_name:
                self.player_id = input_data['resultSets'][0]['rowSet'][i][0]
                break
                
        self.target_stat = target_stat
        self.money_line = money_line
    
    def get_player_recent_stats(self):
        last_five_games_stats = LeagueDashPlayerStats(
            season=Season.default,
            last_n_games=last_n_games,
            per_mode_detailed='PerGame'
        )
        input_data = last_five_games_stats.get_dict()

        input_headers = input_data['resultSets'][0]['headers']
        input_df = pd.DataFrame(columns=input_headers)
        for i in range(len(input_data['resultSets'][0]['rowSet'])):
            if input_data['resultSets'][0]['rowSet'][i][1].upper() == self.player_name:
                input_df.loc[i] = input_data['resultSets'][0]['rowSet'][i]
                break
        
        input_df.drop([col for col in input_headers if col not in keep_headers], axis=1, inplace=True)
        input_df = input_df[list(keep_headers)]

        return input_df

    def get_player_game_log(self):
        def update_training_data(df, season_stats):
            all_game_data = season_stats.get_dict()
            for game_data in all_game_data['resultSets'][0]['rowSet']:
                df.loc[len(df.index)] = game_data

        this_season_stats = PlayerGameLog(self.player_id, season=Season.current_season)
        this_season_game_data = this_season_stats.get_dict()
        training_headers = this_season_game_data['resultSets'][0]['headers']
        training_df = pd.DataFrame(columns=training_headers)

        update_training_data(training_df, this_season_stats)
        for i in range(1, max_seasons_of_data):
            season = '{}-{}'.format(Season.current_season_year - i, str(Season.current_season_year - i + 1)[2:])
            season_stats = PlayerGameLog(self.player_id, season=season)
            update_training_data(training_df, season_stats)
        
        training_df.drop([col for col in training_headers if col not in keep_headers], axis=1, inplace=True)
        training_df = training_df[list(keep_headers)]

        return training_df

    def train_model(self, training_df, target_stat, money_line):
        X = training_df.drop(columns=target_stat)
        y = training_df[target_stat]
        for i in range(len(y)):
            y[i] = 1 if y[i] > money_line else 0
        
        if sum(y) == 0:
            return '-4'
        elif sum(y) == len(y):
            return '-5'
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = LogisticRegression(random_state=0, C=0.7, fit_intercept=True).fit(X_train_scaled, y_train)
        
        return (model, X_test_scaled, y_test, X_train_scaled, y_train, scaler)

    def test_model(self, model, X_test_scaled, y_test, X_train_scaled, y_train):
        print(model.score(X_train_scaled, y_train))
        print(model.score(X_test_scaled, y_test))

    def run_model(self):
        
        if self.player_id == -1:
            return '-1'
        if self.target_stat not in keep_headers:
            return '-2'
        try:
            if not self.money_line.endswith('.5'):
                return '-3'
            self.money_line = float(self.money_line)
        except:
            return '-3'

        input_df = self.get_player_recent_stats()
        training_df = self.get_player_game_log()

        model_result = self.train_model(training_df, self.target_stat, self.money_line)
        if model_result == '-4' or model_result == '-5':
            return model_result

        model, X_test_scaled, y_test, X_train_scaled, y_train, scaler = model_result
        
        X_input = input_df.drop(columns=self.target_stat)
        X_input_scaled = scaler.transform(X_input)

        prediction = model.predict(X_input_scaled)
        prediction_prob = model.predict_proba(X_input_scaled)

        result = f'You should probably take the {'over' if prediction[0] == 1 else 'under'}: {prediction_prob[0][prediction[0]] * 100}%'
        return result
