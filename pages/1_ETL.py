import string
from tokenize import Number
import streamlit as st
import os
import mysql.connector
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import requests
from io import StringIO
import io
from Validator import Validator
from DatabaseConnector import DatabaseConnector

validator = Validator()
db_connector = DatabaseConnector()


def validate_positive_integer(value):
    try:
        # Convirtiendo Valor a un Entero
        integer_value = int(value)

        # Verificar que sea un número positivo
        if integer_value > 0:
            return integer_value
        else:
            st.error("Please enter a positive integer.")
            return None
    except ValueError:
        st.error("Please enter a valid integer.")
        return None


def validateSummaryFile(df, year=2020):
    st.divider()
    delete_columns = ['Country_code', 'WHO_region',
                      'New_cases', 'Cumulative_cases']
    # 1. Eliminar columnas
    df = validator.delete_columns(
        df, delete_columns)

    st.markdown("#### Proceso de Transformación del DataFrame Global")

    st.markdown(
        "1. Eliminación de columnas irrelevantes: 'Country_code', 'WHO_region', 'New_cases', 'Cumulative_cases'")

    # 2. Filtrar por país
    df = validator.filter_by_country(df, 'Country', 'Guatemala')
    st.markdown("2. Filtrado por país: Guatemala")
    st.write(df)

    # 3. Verificar formato de fecha y filtrar por año
    df = validator.check_date_format(df, 'Date_reported', year)
    st.markdown(
        "3. Verificación del formato de fecha y filtrado por año: los datos se filtraron unicamente para el año: " + str(year))
    st.write(df)
    # 4. Eliminar fechas duplicadas
    df = validator.delete_duplicate_dates(df, 'Date_reported')
    st.markdown("4. Eliminación de fechas duplicadas")
    st.write(df)
    # 5. Eliminar duplicados basados en dos columnas
    df = validator.check_repetition(df, 'Date_reported', 'Country')
    st.markdown(
        "5. Eliminación de duplicados basados en dos columnas: Date_reported y Country")
    st.write(df)
    # 6. Verificar y limpiar columna numérica
    df = validator.check_integer(df, 'New_deaths')
    df = validator.check_integer(df, 'Cumulative_deaths')
    st.markdown(
        "6. Verificación y limpieza columnas numéricas: New_deaths y Cumulative_deaths")
    st.write(df)
    # 7. Limpiar datos nulos en una columna específica
    df = validator.clean_data_by_column(df, 'New_deaths')
    df = validator.clean_data_by_column(df, 'Cumulative_deaths')
    st.markdown(
        "7. Limpieza de datos nulos en las columnas: New_deaths y Cumulative_deaths")
    st.write(df)
    # 8. Eliminar valores negativos en una columna
    df = validator.check_negative_values(df, 'New_deaths')
    df = validator.check_negative_values(df, 'Cumulative_deaths')
    st.markdown(
        "8. Limpieza de valores negativos en las columnas: New_deaths y Cumulative_deaths")
    st.write(df)
    return df


def validateLocalFile(df, year=2021):
    st.divider()
    delete_columns = ['codigo_departamento', 'codigo_municipio']
    # 1. Eliminar columnas
    df = validator.delete_columns(
        df, delete_columns)
    st.write(df)
    st.markdown("#### Proceso de Transformación del DataFrame Local")
    st.markdown(
        "1. Eliminación de columnas irrelevantes: 'codigo_departamento', 'codigo_municipio'")
    # 2. Verificar formato de fecha y filtrar por año
    df = validator.validate_and_clean_dates(df, year)
    st.write(df)
    st.markdown(
        "2. Verificación del formato de fecha y filtrado por año: los datos se filtraron unicamente para el año: " + str(year))
    # 3. Eliminar fechas duplicadas
    df = validator.remove_duplicate_dates_in_columns(df)
    st.markdown("3. Eliminación de fechas duplicadas")
    st.write(df)
    # 5. Eliminar duplicados basados en dos columnas
    df = validator.check_repetition(df, 'departamento', 'municipio')
    st.markdown(
        "5. Eliminación de duplicados basados en dos columnas: 'departamento' y 'municipio'")
    st.write(df)
    # 6. Verificar y limpiar los datos numericos
    df = validator.check_numeric_values_column(df)
    st.write(df)
    st.markdown(
        "6. Verificación y limpieza de datos numericos en cada fecha")
    st.markdown(
        "7. Limpieza de datos nulos en cada columna de fecha")
    st.markdown(
        "8. Limpieza de valores negativos en cada columna de fecha")
    st.markdown("9. Convertir Formato de Fecha de mm/dd/yyyy a yyyy-mm-dd")
    df = validator.convert_all_date_columns(df)
    st.write(df)
    return df


st.title("Transformación de Datos")
st.write("""
ETL es un acrónimo que hace referencia a las tres fases clave de la preparación de datos: Extracción (Extraction), Transformación (Transformation) y Carga (Loading).""")
st.write("Donde: ")
st.write("- **Extracción (Extraction):** la fase de extracción se refiere a la recopilación de datos desde diversas fuentes. Estas fuentes pueden ser bases de datos, archivos, servicios web, aplicaciones, y más. Durante esta etapa, los datos se extraen de su fuente original para su procesamiento posterior.")
st.write("- **Transformación (Transformation):** en la fase de transformación, los datos extraídos se someten a diversas operaciones para limpiar, estructurar y prepararlos para su análisis. Las transformaciones pueden incluir la eliminación de datos duplicados, la corrección de errores, la conversión de formatos y la agregación de información. El objetivo es garantizar que los datos sean coherentes y útiles para el análisis.")
st.write("- **Carga (Loading):** la fase de carga implica la inserción de los datos transformados en el sistema de destino, que puede ser un almacén de datos, una base de datos relacional, un data lake o cualquier otro repositorio de datos. Durante esta etapa, los datos se organizan y almacenan de manera que sean accesibles para análisis futuros.")
st.divider()
st.subheader("Carga del Archivo")
st.write("""
Para realizar el ETL, es necesario cargar un archivo de datos y otro mediante una URL, con un formato específico. Este debe ser un formato csv.
""")
# urlFile = st.text_input("Ingrese la URL del archivo Global a Analizar", "https://seminario2.blob.core.windows.net/fase1/global.csv?sp=r&st=2023-12-06T03:45:26Z&se=2024-01-04T11:45:26Z&sv=2022-11-02&sr=b&sig=xdx7LdUOekGyBvGL%2FNE55ZZj9SBvCC%2FWegxtpSsKjJg%3D",placeholder="Debe ser un archivo en formato csv")
# uploadFile = st.file_uploader("Elija un archivo", type=['csv', 'xls', 'xlsx', 'json'])

# Obtiene la ruta del directorio actual (donde se encuentra app.py)
directorio_actual = os.path.dirname(__file__)

# Combina la ruta del directorio actual con la ubicación del archivo CSV
uploadFile = os.path.join(directorio_actual, "municipio-calificacion.csv")
uploadFile2 = os.path.join(directorio_actual, "global-calificacion.csv")


if (uploadFile is not None and uploadFile2 is not None):

    # Descargar el archivo CSV desde la URL
    # response = requests.get(urlFile)
    # if response.status_code == 200:
    #     summaryFile = StringIO(response.content.decode('utf-8'))
    #     df_summary = pd.read_csv(summaryFile)
    # else:
    #     st.error("Error al descargar el archivo")
    #     st.stop()

    # splitNameLocal = os.path.splitext(uploadFile.name)

    # fileNameLocal = splitNameLocal[0]
    # fileExtensionLocal = splitNameLocal[1]

    # Verificamos la extension del Archivo, para su lectura correspondiente
    # if (fileExtensionLocal == ".csv" and fileExtensionGlobal == ".csv"):
    df_local = pd.read_csv(uploadFile)
    df_summary = pd.read_csv(uploadFile2)

    # Imprimimos el contenido de la tabla
    st.subheader("Extracción de Datos")
    st.markdown("##### Archivo Local")
    st.dataframe(df_local)

    st.markdown("##### Archivo Descargado vía URL")
    st.dataframe(df_summary)

    st.subheader("Parametrización")
    st.write("""
        Elija las variables que se utilizarán para el proceso de ETL """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Año de Análisis")
        var_year = st.selectbox("Por favor elija un año de la pandemia",
                                ["2020", "2021", "2022"], key="year", )

    with col2:
        st.markdown("##### Cantidad de Datos a Insertar")
        batch_size = st.text_input("Por favor ingrese un número entero",
                                   key="batch_size", type="default", value=50)
        batch_size = validate_positive_integer(batch_size)

    if st.button('Transformar e Insertar Datos', type='primary'):
        if batch_size is None:
            st.warning(
                "La cantidad de datos a insertar debe ser un número entero positivo")
            st.stop()
        df_summary_transform = validateSummaryFile(
            df_summary, int(var_year))

        df_local_transform = validateLocalFile(df_local, int(var_year))
        st.divider()
        st.subheader("Inserción a la Base de Datos")
        with st.spinner('Cargando...'):
            db_connector.insert_data_in_blocks(
                df_local_transform, df_summary_transform, batch_size)
        st.success("Inserción de datos finalizada.")

else:
    st.warning("Debe Cargar un Archivo Previamente")


st.sidebar.title("Bienvenidos")

st.sidebar.markdown("""
## Ingenieria USAC
### Laboratorio de Seminario de Sistemas 2
Aux. Erick 
""")

st.sidebar.markdown("""
## Estudiante:
- Eriksson José Hernández López
- 2927191591415
- 201830459
""")

st.sidebar.markdown("@ErikssonHerlo on " +
                    '<a href="https://github.com/ErikssonHerlo/DataScience" target="_blank">GitHub</a>', unsafe_allow_html=True)
