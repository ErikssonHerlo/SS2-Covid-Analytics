# Importar las librerias necesarias

import streamlit as st
from PIL import Image

st.title("Transformación de Datos")
st.write("""
ETL es un acrónimo que hace referencia a las tres fases clave de la preparación de datos: Extracción (Extraction), Transformación (Transformation) y Carga (Loading).""")
st.write("Donde: ")
st.write("- **Extracción (Extraction):** la fase de extracción se refiere a la recopilación de datos desde diversas fuentes. Estas fuentes pueden ser bases de datos, archivos, servicios web, aplicaciones, y más. Durante esta etapa, los datos se extraen de su fuente original para su procesamiento posterior.")
st.write("- **Transformación (Transformation):** en la fase de transformación, los datos extraídos se someten a diversas operaciones para limpiar, estructurar y prepararlos para su análisis. Las transformaciones pueden incluir la eliminación de datos duplicados, la corrección de errores, la conversión de formatos y la agregación de información. El objetivo es garantizar que los datos sean coherentes y útiles para el análisis.")
st.write("- **Carga (Loading):** la fase de carga implica la inserción de los datos transformados en el sistema de destino, que puede ser un almacén de datos, una base de datos relacional, un data lake o cualquier otro repositorio de datos. Durante esta etapa, los datos se organizan y almacenan de manera que sean accesibles para análisis futuros.")
st.divider()

st.title("Limpieza de Datos")
st.subheader("Transformación del Archivo Global")

st.markdown("1. **Eliminación de columnas irrelevantes:** 'Country_code', 'WHO_region', 'New_cases', 'Cumulative_cases'")
st.markdown(
    "   - En esta etapa, se eliminan del conjunto de datos las columnas 'Country_code', 'WHO_region', 'New_cases' y 'Cumulative_cases'."
    " Estas columnas se consideran irrelevantes para el análisis, lo que simplifica el conjunto de datos y enfoca la atención en la información esencial."
)

st.markdown("2. **Filtrado por país:** Guatemala")
st.markdown(
    "   - Se realiza un filtrado específico para incluir solo los datos relacionados con el país Guatemala. Esto ayuda a aislar y analizar los datos específicos de un país."
)

st.markdown("3. **Verificación del formato de fecha y filtrado por año:** Los datos se filtraron únicamente para un año de la pandemia")
st.markdown(
    "   - Se verifica que el formato de fecha en la columna 'Date_reported' sea correcto. Además, se filtran los datos para incluir únicamente registros correspondientes a un año específico de la pandemia."
)

st.markdown("4. **Eliminación de fechas duplicadas**")
st.markdown(
    "   - En esta etapa, se identifican y eliminan las filas que contienen fechas duplicadas en la columna 'Date_reported'. La eliminación de duplicados es crucial para mantener la integridad de los datos."
)

st.markdown(
    "5. **Eliminación de duplicados basados en dos columnas:** Date_reported y Country")
st.markdown(
    "   - Se eliminan las filas duplicadas basadas en dos columnas específicas: 'Date_reported' y 'Country'. Esto asegura que cada combinación de fecha y país sea única en el conjunto de datos."
)

st.markdown(
    "6. **Verificación y limpieza columnas numéricas:** New_deaths y Cumulative_deaths")
st.markdown(
    "   - Se realiza una verificación y limpieza de las columnas numéricas 'New_deaths' y 'Cumulative_deaths'. Esto garantiza que los datos en estas columnas sean coherentes y estén en formato numérico."
)

st.markdown(
    "7. **Limpieza de datos nulos en las columnas:** New_deaths y Cumulative_deaths")
st.markdown(
    "   - Se lleva a cabo la limpieza de datos nulos en las columnas 'New_deaths' y 'Cumulative_deaths'. Esto es esencial para asegurar que no haya valores faltantes que puedan afectar el análisis."
)

st.markdown(
    "8. **Limpieza de valores negativos en las columnas:** New_deaths y Cumulative_deaths")
st.markdown(
    "   - Se realiza la limpieza de valores negativos en las columnas 'New_deaths' y 'Cumulative_deaths'. La presencia de valores negativos podría distorsionar los resultados del análisis, por lo que es necesario eliminarlos."
)


st.subheader("Transformación del Archivo Local")
# 1. Eliminación de columnas irrelevantes
st.markdown(
    "1. **Eliminación de columnas irrelevantes:** 'codigo_departamento', 'codigo_municipio', 'poblacion'")
st.markdown(
    "   - En esta etapa, se eliminan del conjunto de datos las columnas 'codigo_departamento', 'codigo_municipio' y 'poblacion'."
    " Estas columnas no son relevantes para el análisis, permitiendo simplificar y concentrarse en los datos cruciales."
)

# 2. Verificar formato de fecha y filtrar por año
st.markdown("2. **Verificación del formato de fecha y filtrado por año:** los datos se filtraron únicamente para un año especifico de la pandemia")
st.markdown(
    "   - Se realiza una verificación del formato de fecha en la columna correspondiente ('fecha' o similar) para asegurarse de que"
    " todos los datos estén representados de manera coherente. Luego, se filtran los datos para incluir únicamente aquellos"
    " correspondientes al año especificado, ayudando a reducir el conjunto de datos a una escala temporal específica."
)

# 3. Eliminar fechas duplicadas
st.markdown("3. **Eliminación de fechas duplicadas**")
st.markdown(
    "   - En esta etapa, se identifican y eliminan las filas que contienen fechas duplicadas. Esto es esencial para mantener la integridad"
    " de los datos y evitar problemas durante el análisis, ya que cada fecha debe tener una representación única en el conjunto de datos."
)

# 5. Eliminar duplicados basados en dos columnas
st.markdown(
    "5. **Eliminación de duplicados basados en dos columnas:** 'departamento' y 'municipio'")
st.markdown(
    "   - Aquí se eliminan las filas duplicadas basadas en dos columnas específicas: 'departamento' y 'municipio'. Esto es útil cuando"
    " se espera que estas dos columnas juntas deberían ser únicas en el conjunto de datos, y la presencia de duplicados podría afectar"
    " la validez del análisis."
)

# 6. Verificar y limpiar los datos numéricos
st.markdown("6. **Verificación y limpieza de datos numéricos en cada fecha**")
st.markdown(
    "   - Esta etapa se enfoca en verificar y limpiar las columnas numéricas en el conjunto de datos. Se realiza una verificación para"
    " asegurarse de que los valores sean de tipo numérico y, en caso necesario, se realiza una limpieza para corregir cualquier"
    " discrepancia o formato incorrecto."
)

st.markdown("7. **Limpieza de datos nulos en cada columna de fecha**")
st.markdown(
    "   - Aquí se aborda la limpieza de valores nulos en cada columna de fecha. La presencia de datos faltantes puede afectar la"
    " calidad del análisis, por lo que esta etapa garantiza que los datos estén completos y preparados para su análisis."
)

st.markdown("8. **Limpieza de valores negativos en cada columna de fecha**")
st.markdown(
    "   - Se realiza una limpieza específica para eliminar cualquier valor negativo que pueda estar presente en las columnas de fecha."
    " Esto es importante según el contexto del análisis, ya que los valores negativos pueden distorsionar la interpretación de los datos."
)

st.markdown("9. **Convertir Formato de Fecha de mm/dd/yyyy a yyyy-mm-dd**")
st.markdown(
    "   - En esta etapa, se lleva a cabo la conversión del formato de fecha de mm/dd/yyyy a yyyy-mm-dd. Esto asegura que todas las fechas"
    " en el conjunto de datos sigan un formato consistente, facilitando operaciones futuras y garantizando la coherencia en el análisis."
)


st.title("Modelo de Datos")

st.markdown("### Modelo de Datos")

st.markdown("Se eligió el siguiente modelo de datos para representar la información relacionada con las defunciones:")

st.code("""
CREATE DATABASE IF NOT EXISTS `dataset`
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `dataset`.`death` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `country` VARCHAR(45) NULL,
  `departament` VARCHAR(45) NULL,
  `municipality` VARCHAR(45) NULL,
  `new_deaths` INT NULL,
  `cumulative_deaths` INT NULL,
  `register_type` ENUM('summary', 'municipality') NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
""", language='sql')

st.markdown(
    "Este modelo de datos se diseñó considerando varios aspectos clave para representar la información de defunciones de manera efectiva:\n"
    "- **Tablas:** Se utiliza una tabla llamada `death` dentro de la base de datos `dataset`.\n"
    "- **Atributos:** Cada columna en la tabla representa un atributo específico relacionado con las defunciones, como la fecha (`date`), país (`country`), departamento (`departament`), municipio (`municipality`), nuevas defunciones (`new_deaths`), defunciones acumulativas (`cumulative_deaths`), y el tipo de registro (`register_type`).\n"
    "- **Claves Primarias:** La columna `id` se designa como la clave primaria, lo que garantiza la unicidad de cada registro en la tabla.\n"
    "- **Tipos de Datos y Restricciones:** Se utilizan tipos de datos apropiados, como `DATE` para la fecha, `VARCHAR` para texto y `INT` para valores numéricos. Además, se utiliza un tipo enumerado (`ENUM`) para la columna `register_type` que solo puede tomar valores 'summary' o 'municipality'.\n"
    "- **Autoincremento:** La columna `id` se configura como autoincremental, simplificando la asignación de identificadores únicos a cada registro.\n"
    "- **Motor de Almacenamiento:** Se utiliza el motor de almacenamiento InnoDB para mejorar la integridad referencial y las transacciones."
)

st.markdown(
    "Este diseño proporciona una estructura ordenada y eficiente para almacenar información sobre las diferentes fuentes de datos de defunciones, permitiendo consultas y análisis de datos de manera efectiva."
)

st.markdown("### Manejo de Integridad Referencial y Transacciones")

st.markdown(
    "Para garantizar la integridad referencial y mantener la consistencia de los datos, se implementa el manejo de transacciones,"
    " commits y rollbacks. Esto se logra mediante el uso del motor de almacenamiento InnoDB, que es compatible con transacciones en MySQL."
)

st.markdown(
    "A continuación, se describe cómo se manejan las transacciones en el contexto del modelo de datos proporcionado:\n"
    "- **Inicio de Transacción:** Antes de realizar un conjunto de operaciones (como inserciones, actualizaciones o eliminaciones) que deben ejecutarse de manera atómica, se inicia una transacción."
)

st.markdown(
    "- **Commit:** Una vez que todas las operaciones dentro de la transacción se han ejecutado con éxito y no ha habido problemas, se emite un commit. Esto confirma permanentemente los cambios y los hace permanentes en la base de datos."
)

st.markdown(
    "- **Rollback:** Si en algún punto dentro de la transacción surge un problema o error, se puede emitir un rollback. Esto deshace todas las operaciones realizadas desde el inicio de la transacción, devolviendo la base de datos a su estado original antes de la transacción."
)

st.markdown(
    "El manejo adecuado de transacciones, commits y rollbacks es fundamental para garantizar la integridad referencial y la consistencia de los datos en situaciones donde múltiples operaciones deben ejecutarse de manera coherente."
)


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
