from datetime import datetime
import pandas as pd
import os


class Validator:
    def __init__(self):
        pass

    def delete_duplicate_dates(self, df, column_name):
        df = df.drop_duplicates(subset=[column_name])
        return df

    def check_date_format(self, df, column_name, year):
        df[column_name] = pd.to_datetime(
            df[column_name], format='%m/%d/%Y', errors='coerce')
        df.dropna(subset=[column_name], inplace=True)
        # # Extraer la parte de la fecha y asignarla a la columna
        df[column_name] = df[column_name].dt.date

        # Filtrar por año
        df = df[df[column_name].apply(lambda x: x.year) == year]
        return df

    def check_repetition(self, df, column_name_1, column_name_2):
        df = df.drop_duplicates(subset=[column_name_1, column_name_2])
        return df

    def check_integer(self, df, column_name):
        # Verificar si la columna existe en el DataFrame
        if column_name not in df.columns:
            print(f"La columna {column_name} no existe en el DataFrame.")
            return None
        try:
            df[column_name] = pd.to_numeric(
                df[column_name], errors='coerce', downcast='integer')
        except ValueError:
            print(f"La columna {column_name} no es numérica.")
            return None
        df.dropna(subset=[column_name], inplace=True)
        return df

    def clean_data_by_column(self, df, column_name):
        # Convert null values to 0 in the specified column
        df[column_name] = df[column_name].fillna(0)
        return df

    def filter_by_country(self, df, column_name, country):
        df = df[df[column_name] == country]
        return df

    def check_negative_values(self, df, column_name):
        df = df[df[column_name] >= 0]
        return df

    def delete_columns(self, df, column_list):
        df = df.drop(columns=column_list, errors='ignore')
        return df

    def validate_and_clean_dates(self, df, year):
        """
        Filter DataFrame columns for a specific year and convert dates to date type.

        Parameters:
        - df (pd.DataFrame): Input DataFrame.
        - year (int): Year to filter.

        Returns:
        - pd.DataFrame: DataFrame with filtered columns and converted dates.
        """

        # List to store columns to be deleted
        columns_to_delete = []

        for column in df.columns[3:]:
            try:
                # Attempt to validate the date format
                datetime.strptime(column, '%m/%d/%Y')

                # Filter by year (skip if it's not a valid date column)
                if df[column].dtype == 'int64' and column != 'year' and pd.to_datetime(column).year != year:
                    columns_to_delete.append(column)
            except ValueError:
                # If validation fails, add the column to the deletion list
                columns_to_delete.append(column)

        # Drop columns with incorrect date formats
        df = df.drop(columns=columns_to_delete)

        return df

    def remove_duplicate_dates_in_columns(self, df):
        """
        Remove duplicate dates in DataFrame columns, keeping only the first instance.

        Parameters:
        - df (pd.DataFrame): Input DataFrame.

        Returns:
        - pd.DataFrame: DataFrame with duplicate dates removed.
        """

        # Extract date columns for validation
        date_columns = df.columns[3:]

        # Transpose DataFrame and drop duplicates
        transposed_df = df.set_index(['departamento', 'municipio']).transpose()
        transposed_df = transposed_df[~transposed_df.index.duplicated(
            keep='first')]

        # Transpose back to original format
        df = transposed_df.transpose().reset_index()

        return df

    def check_numeric_values_column(self, df):
        """
        Check if all values in date columns are numeric, and remove columns with non-numeric values.

        Parameters:
        - df (pd.DataFrame): Input DataFrame.

        Returns:
        - pd.DataFrame: DataFrame with non-numeric columns removed.
        """

        # Extract date columns for validation
        date_columns = df.columns[3:]

        # Convert non-integer values to zero
        for col in date_columns:
            try:
                df[col] = pd.to_numeric(
                    df[col], errors='coerce').fillna(0).astype(int)
            except ValueError:
                df[col] = 0

            # Convert negative values to zero
            df.loc[df[col] < 0, col] = 0

        return df

    def convert_all_date_columns(self, df):
        """
        Convierte todas las columnas de fecha al formato %Y-%m-%d.

        Parameters:
        - df (pd.DataFrame): DataFrame de entrada.

        Returns:
        - pd.DataFrame: DataFrame con las fechas convertidas.
        """
        # Extract date columns for validation
        date_columns = df.columns[3:]

        # Convertir todas las columnas de fecha al formato %Y-%m-%d
        for col in date_columns:
            try:
                # Convierte el nombre de la columna a formato datetime
                date = pd.to_datetime(col, format='%m/%d/%Y')

                # Cambia el formato del nombre de la columna
                new_format = date.strftime('%Y-%m-%d')

                # Renombra la columna en el DataFrame
                df.rename(columns={col: new_format}, inplace=True)
            except ValueError:
                print(f"Error al convertir las fechas en la columna {col}.")

        return df
