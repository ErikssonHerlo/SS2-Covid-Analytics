import mysql.connector
import pandas as pd
import streamlit as st
import io
import os
from datetime import datetime


class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.connect()  # Llama a la función connect al inicializar

    def connect(self):
        mysql_config = {
            'HOST': os.environ.get('HOST'),
            'USER': os.environ.get('USER'),
            'PASS': '201830459',
            'DATABASE': os.environ.get('DATABASE')
        }

        db_config = {
            'host': mysql_config['HOST'],
            'user': mysql_config['USER'],
            'password': mysql_config['PASS'],
            'database': mysql_config['DATABASE'],
            'raise_on_warnings': True
        }

        try:
            # Intentar establecer la conexión
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                print('Conexión exitosa a MySQL')
        except mysql.connector.Error as err:
            print(f'Error al conectar a MySQL: {err}')

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def insert_data_in_blocks(self, df_local, df_summary, batch_size=50):
        successful_blocks = 0
        failed_blocks = 0
        total_records_inserted = 0  # Nuevo contador
        try:
            # Verificar si la conexión está abierta
            if not self.connection or not self.connection.is_connected():
                print('La conexión no está abierta.')
                self.connect()  # Intentar reconectar

            # Crear cursor
            print('Creando cursor...')
            cursor = self.connection.cursor()

            # Iterar sobre las columnas de fecha y generar bloques de inserción
            print('Iterando sobre columnas de fecha...')
            date_columns = df_local.columns[2:]
            print(f'Recorriendo Columnas de fecha')
            for date_column in date_columns:
                try:
                    # # Obtener bloques de datos para la columna de fecha actual
                    # print(f'Obteniendo bloques de datos para {date_column}')
                    data_block = df_local[['departamento',
                                           'municipio', date_column]]
                    # data_block['date'] = pd.to_datetime(data_block[date_column], errors='coerce').dt.date
                    # data_block['date'] = pd.to_datetime(data_block['date'], format='%Y-%m-%d').dt.date

                    data_block['date'] = datetime.strptime(
                        date_column, '%Y-%m-%d').date()
                    data_block['new_deaths'] = df_local[date_column]
                    data_block = data_block.dropna()

                    # Cambiar el nombre de las columnas para que coincidan con la estructura esperada
                    data_block = data_block.rename(
                        columns={'departamento': 'departament', 'municipio': 'municipality'})

                    print(
                        f'Insertando {len(data_block)} registros para la fecha {date_column}.')

                    # Fijar los valores constantes
                    data_block['country'] = 'Guatemala'
                    data_block['cumulative_deaths'] = 0
                    data_block['register_type'] = 2

                    print("Generando Data Fake para completar la tabla")
                    # Reorganizar las columnas para que coincidan con el orden en la consulta SQL
                    data_block = data_block[[
                        'country', 'cumulative_deaths', 'register_type', 'date', 'departament', 'municipality', 'new_deaths']]

                    # Agregar el segundo dataframe y rellenar los valores faltantes
                    summary_block = df_summary.rename(columns={
                        'Date_reported': 'date', 'Country': 'country', 'New_deaths': 'new_deaths', 'Cumulative_deaths': 'cumulative_deaths'})
                    # Fijar los valores constantes
                    summary_block['departament'] = 'TOTAL'
                    summary_block['municipality'] = 'TOTAL'
                    summary_block['register_type'] = 1

                    summary_block = summary_block[[
                        'country', 'cumulative_deaths', 'register_type', 'date', 'departament', 'municipality', 'new_deaths']]
                    print(summary_block)
                    data_block = pd.concat(
                        [data_block, summary_block], ignore_index=True)

                    # Ordenar en base a la fecha
                    data_block = data_block.sort_values(
                        by=['date']).reset_index(drop=True)
                    # Generar el SQL para la inserción del bloque
                    sql = """
                        INSERT INTO dataset.death
                        (country, cumulative_deaths, register_type, date, departament, municipality, new_deaths)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    # Iniciar transacción
                    cursor.execute("START TRANSACTION;")
                    print('Transacción iniciada.')
                    # Iterar sobre bloques de tamaño batch_size
                    for i in range(0, len(data_block), batch_size):
                        print(f'Insertando bloque {i}...')
                        batch_data = data_block[i:i + batch_size]
                        print(batch_data)
                        print(batch_data.values.tolist())
                        # Ejecutar la inserción del bloque
                        cursor.executemany(sql, batch_data.values.tolist())
                        print(
                            f'Insertados {len(batch_data)} registros con éxito para la fecha {date_column}.')
                        successful_blocks += 1
                        # Actualizar el contador total
                        total_records_inserted += len(data_block)

                        # if i == 1:
                        #     raise mysql.connector.Error(
                        #         "Error provocado para simular falla en la transacción")
                    # Confirmar la transacción al finalizar
                    cursor.execute("COMMIT;")
                    print('Transacción completada con éxito.')

                except mysql.connector.Error as err:
                    print(f'Error en la transacción: {err}')
                    # Revertir la transacción en caso de error
                    cursor.execute("ROLLBACK;")
                    failed_blocks += 1
                    # Si hay un error, intentar nuevamente solo una vez
                    try:
                        # Ejecutar la inserción del bloque nuevamente
                        cursor.executemany(sql, data_block.values)
                        print(
                            f'Reintentando inserción del bloque para la fecha {date_column}.')
                        successful_blocks += 1
                        total_records_inserted += len(data_block)
                        # Actualizar el contador total
                        total_records_inserted += len(data_block)
                    except mysql.connector.Error as retry_err:
                        print(
                            f'Error en el reintento de la transacción: {retry_err}')
                        self.connection.rollback()
                        failed_blocks += 1
        except mysql.connector.Error as err:
            print(f'Error al manejar la transacción: {err}')

        finally:
            # Cerrar el cursor
            if cursor:
                cursor.close()
        # Mostrar el informe al final de la carga
        st.markdown(
            "### Informe de carga:")
        # Mostrar el reporte en Streamlit con st.markdown
        st.markdown(
            f'**Bloques insertados correctamente:** {successful_blocks}')
        st.markdown(f'**Bloques fallidos:** {failed_blocks}')
        st.markdown(
            f'**Total de registros insertados:** {total_records_inserted}')
        print(
            f'\nInforme de carga:\nBloques insertados con éxito: {successful_blocks}\nBloques fallidos: {failed_blocks}')

    def insert_sample_data(self):
        try:
            if not self.connection or not self.connection.is_connected():
                print('La conexión no está abierta.')
                self.connect()

            # Habilitar el modo de autocommit
            self.connection.autocommit = True

            # Crear cursor
            cursor = self.connection.cursor()

            # Restablecer el modo de autocommit a False
            self.connection.autocommit = False

            # Datos de ejemplo
            sample_data = [
                ('Guatemala', 0, 1, '2023-01-01', 'Guatemala', 'Ciudad', 10),
                ('Guatemala', 0, 1, '2023-01-02', 'Guatemala', 'Pueblo', 5),
                ('Guatemala', 0, 1, '2023-01-03', 'Guatemala', 'Aldea', 3)
            ]

            # SQL para la inserción
            sql = """
                INSERT INTO dataset.death
                (country, cumulative_deaths, register_type, date, departament, municipality, new_deaths)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Ejecutar la inserción
            cursor.executemany(sql, sample_data)

            # Confirmar la transacción
            self.connection.commit()
            print('Transacción completada con éxito.')

        except mysql.connector.Error as err:
            print(f'Error al manejar la transacción: {err}')

        finally:
            # Cerrar el cursor
            if cursor:
                cursor.close()
