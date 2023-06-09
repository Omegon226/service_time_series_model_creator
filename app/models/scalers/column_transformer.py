import pandas as pd

from app.models.data_models.time_series_df import TimeSeriesDF
from app.scripts.http_error import http_error
import dill
import os


class ColumnTransformer:
    def __init__(self, data: TimeSeriesDF):
        self.sequence_of_creating_new_params = data.sequence_of_creating_new_params
        self.sequence_of_columns = list(data.df_work.columns.values)
        self.data_columns = data.data_params
        self.already_exists_new_columns = False
        self.main_parameter = data.main_parameter[0]

    def save(self, path: str = "app/resources/testing_column_transformers", name: str = "column_transformer"):
        with open(os.path.join(path, name+".dill"), 'wb+') as file:
            dill.dump(self, file)

    @staticmethod
    def load(path: str = "app/resources/testing_column_transformers", name: str = "column_transformer"):
        with open(os.path.join(path, name+".dill"), 'rb+') as file:
            return dill.load(file)

    def check_for_needed_columns(self, time_series_df: TimeSeriesDF | pd.DataFrame):
        if type(time_series_df) is TimeSeriesDF:
            all_columns_is_in = set(self.sequence_of_columns).issubset(set(list(time_series_df.df_work.columns.values)))
        else:
            all_columns_is_in = set(self.sequence_of_columns).issubset(set(list(time_series_df.columns.values)))

        return all_columns_is_in

    def return_needed_columns(self, time_series_df: TimeSeriesDF | pd.DataFrame):
        if type(time_series_df) is TimeSeriesDF:
            return list(set(self.sequence_of_columns) - set(list(time_series_df.df_work.columns.values)))
        else:
            return list(set(self.sequence_of_columns) - set(list(time_series_df.columns.values)))

    # Переименовать
    def sort_columns_in_needed_sequence(self, time_series_df: TimeSeriesDF | pd.DataFrame):
        if type(time_series_df) is TimeSeriesDF:
            return time_series_df.df_work[self.sequence_of_columns]
        else:
            return time_series_df[self.sequence_of_columns]

    def create_new_columns(self, time_series_df: TimeSeriesDF | pd.DataFrame):
        try:
            for new_param in self.sequence_of_creating_new_params:

                if new_param["param"] == "mean":
                    time_series_df = ColumnTransformer._add_mean(time_series_df, new_param["param_name"],
                                                                 new_param["data_params"])
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "median":
                    time_series_df = ColumnTransformer._add_median(time_series_df, new_param["param_name"],
                                                                   new_param["data_params"])
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "range":
                    time_series_df = ColumnTransformer._add_range(time_series_df, new_param["param_name"],
                                                                  new_param["data_params"])
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "std":
                    time_series_df = ColumnTransformer._add_std(time_series_df, new_param["param_name"],
                                                                new_param["data_params"])
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "rolling mean":
                    time_series_df = ColumnTransformer._add_rolling_mean(time_series_df, new_param["param_name"],
                                                                         new_param["data_params"],
                                                                         new_param["window_size"],
                                                                         self.main_parameter)
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "rolling median":
                    time_series_df = ColumnTransformer._add_rolling_median(time_series_df, new_param["param_name"],
                                                                           new_param["data_params"],
                                                                           new_param["window_size"],
                                                                           self.main_parameter)
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "rolling range":
                    time_series_df = ColumnTransformer._add_rolling_range(time_series_df, new_param["param_name"],
                                                                          new_param["data_params"],
                                                                          new_param["window_size"],
                                                                          self.main_parameter)
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                elif new_param["param"] == "rolling std":
                    time_series_df = ColumnTransformer._add_rolling_std(time_series_df, new_param["param_name"],
                                                                        new_param["data_params"],
                                                                        new_param["window_size"],
                                                                        self.main_parameter)
                    if not self.already_exists_new_columns:
                        self.sequence_of_columns += [new_param["param_name"]]

                else:
                    error_message = f"Переданный тип параметра ({new_param['param']}) для создания нового параметра " \
                                    f"не существует или не реализован в ColumnTransformer"
                    raise Exception(error_message)

            self.already_exists_new_columns = True
            return time_series_df

        except Exception as error:
            error_message = f"Произошла ошибка при создании новых параметров в объекте ColumnTransformer"
            http_error(error_message, error)

    @staticmethod
    def _add_mean(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = "Mean"
        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].mean(axis=1)
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].mean(axis=1)

        return time_series_df

    @staticmethod
    def _add_median(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = "Median"
        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].median(axis=1)
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].median(axis=1)

        return time_series_df

    @staticmethod
    def _add_range(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = "Range"
        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].max(axis=1) - \
                                                        time_series_df.df_work[data_params].min(axis=1)
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].max(axis=1) - \
                                                time_series_df[data_params].min(axis=1)

        return time_series_df

    @staticmethod
    def _add_std(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = "STD"
        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].std(axis=1)
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].std(axis=1)

        return time_series_df

    @staticmethod
    def _add_rolling_mean(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list,
                          window_size: int, main_parameter: str | None):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = f"Rolling Mean {time_series_df.main_parameter}"
        if window_size is None:
            error_message = "Не было указан размер окна для добавления новых данных"
            raise Exception(error_message)
        if main_parameter is None:
            error_message = "Для создания такого параметра нужно знать главный параметр"
            raise Exception(error_message)

        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].rolling(
                window=window_size).mean()
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].rolling(
                window=window_size).mean()

        return time_series_df

    @staticmethod
    def _add_rolling_median(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list,
                            window_size: int, main_parameter: str):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = f"Rolling Median {time_series_df.main_parameter}"
        if window_size is None:
            error_message = "Не было указан размер окна для добавления новых данных"
            raise Exception(error_message)
        if main_parameter is None:
            error_message = "Для создания такого параметра нужно знать главный параметр"
            raise Exception(error_message)

        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].rolling(
                    window=window_size).median()
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].rolling(
                window=window_size).median()

        return time_series_df

    @staticmethod
    def _add_rolling_range(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list,
                           window_size: int, main_parameter: str):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = f"Rolling Range {time_series_df.main_parameter}"
        if window_size is None:
            error_message = "Не было указан размер окна для добавления новых данных"
            raise Exception(error_message)
        if main_parameter is None:
            error_message = "Для создания такого параметра нужно знать главный параметр"
            raise Exception(error_message)

        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = \
                time_series_df.df_work[data_params].rolling(window=window_size).max() - \
                time_series_df.df_work[data_params].rolling(window=window_size).min()
        else:
            time_series_df[name_of_new_param] = \
                time_series_df[data_params].rolling(window=window_size).max() - \
                time_series_df[data_params].rolling(window=window_size).min()

        return time_series_df

    @staticmethod
    def _add_rolling_std(time_series_df: TimeSeriesDF | pd.DataFrame, name_of_new_param: str | None, data_params: list,
                         window_size: int, main_parameter: str):
        if name_of_new_param is None or name_of_new_param == "string":
            name_of_new_param = f"Rolling STD {time_series_df.main_parameter}"
        if window_size is None:
            error_message = "Не было указан размер окна для добавления новых данных"
            raise Exception(error_message)
        if main_parameter is None:
            error_message = "Для создания такого параметра нужно знать главный параметр"
            raise Exception(error_message)
        if type(time_series_df) is TimeSeriesDF:
            time_series_df.df_work[name_of_new_param] = time_series_df.df_work[data_params].rolling(
                    window=window_size).std()
        else:
            time_series_df[name_of_new_param] = time_series_df[data_params].rolling(
                window=window_size).std()

        return time_series_df
