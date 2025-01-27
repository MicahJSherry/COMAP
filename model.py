import pandas as pd
from graphviz import Source
from sklearn import tree
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_cv(olympics_data:pd.DataFrame, model_hyperparams:dict={}, cv_folds=5):
    '''
    Train a regression model on the data

    Multivariate multi-target
    '''

    fold_metrics = {'mae':[], 'mse':[], 'r2':[]}
    fold_models = []
    model = DecisionTreeRegressor(**model_hyperparams)

    tscv = TimeSeriesSplit(n_splits=cv_folds)
    for i, (train_index, test_index) in enumerate(tscv.split(olympics_data['year'])):
        print(f'CV fold: {i}')

        train_data = olympics_data.loc[train_index] # get train rows

        # get input features for training
        # see https://stackoverflow.com/a/20039057/
        X_train_cols = [col for col in train_data.columns if col not in {'country_total_medals','country_golds','country_silvers','country_bronzes'}]
        X_train = olympics_data[X_train_cols]

        # get output targets for training
        y_train_cols = [col for col in train_data.columns if col in {'country_golds','country_silvers','country_bronzes'}]
        y_train = olympics_data[y_train_cols]

        # train the model
        model.fit(X_train, y_train)

        # get input features for testing
        X_test_cols = [col for col in train_data.columns if col not in {'country_total_medals','country_golds','country_silvers','country_bronzes'}]
        X_test = olympics_data[X_test_cols]

        # get output targets for testing
        y_test_cols = [col for col in train_data.columns if col in {'country_golds','country_silvers','country_bronzes'}]
        y_test = olympics_data[y_test_cols]

        # use the trained model to generate predictions
        y_preds = model.predict(X_test)

        # calculate performance metrics
        mae = mean_absolute_error(y_test, y_preds)
        mse = mean_squared_error(y_test, y_preds)
        r2 = r2_score(y_test, y_preds)
        print(f'Metrics:\nMAE: {mae}\nMSE: {mse}\nR^2: {r2}\n{'-'*50}')

        # store performance metrics
        fold_metrics['mae'].append(mae); fold_metrics['mse'].append(mse); fold_metrics['r2'].append(r2)

    return fold_metrics, model

def main():
    olympics_data = pd.read_csv('/home/noahg/competitive_ml/comap/2025/COMAP/preprocessed_data/olympics_data.csv')

    # encode categorical values
    host_country_le = LabelEncoder()
    host_country_le.fit(olympics_data['host_country'])
    olympics_data['host_country'] = host_country_le.transform(olympics_data['host_country'])

    competing_country_le = LabelEncoder()
    competing_country_le.fit(olympics_data['competing_country'])
    olympics_data['competing_country'] = competing_country_le.transform(olympics_data['competing_country'])

    metrics, model = train_cv(olympics_data, cv_folds=3)

if __name__ == '__main__':
    main()



