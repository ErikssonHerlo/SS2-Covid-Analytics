# SS2-Covid-Analytics
### Ingenieria USAC
**Laboratorio de Seminario de Sistemas 2**

Aux. Erick José André Villatoro Revolorio

# Transformación de Datos

## ETL (Extracción, Transformación, Carga)

ETL es un acrónimo que hace referencia a las tres fases clave de la preparación de datos: Extracción (Extraction), Transformación (Transformation) y Carga (Loading).

**Extracción (Extraction):** La fase de extracción se refiere a la recopilación de datos desde diversas fuentes. Estas fuentes pueden ser bases de datos, archivos, servicios web, aplicaciones, y más. Durante esta etapa, los datos se extraen de su fuente original para su procesamiento posterior.

**Transformación (Transformation):** En la fase de transformación, los datos extraídos se someten a diversas operaciones para limpiar, estructurar y prepararlos para su análisis. Las transformaciones pueden incluir la eliminación de datos duplicados, la corrección de errores, la conversión de formatos y la agregación de información. El objetivo es garantizar que los datos sean coherentes y útiles para el análisis.

**Carga (Loading):** La fase de carga implica la inserción de los datos transformados en el sistema de destino, que puede ser un almacén de datos, una base de datos relacional, un data lake o cualquier otro repositorio de datos. Durante esta etapa, los datos se organizan y almacenan de manera que sean accesibles para análisis futuros.

---

# Limpieza de Datos

## Transformación del Archivo Global

1. **Eliminación de columnas irrelevantes:** 'Country_code', 'WHO_region', 'New_cases', 'Cumulative_cases'
   - En esta etapa, se eliminan del conjunto de datos las columnas mencionadas, consideradas irrelevantes para el análisis.

2. **Filtrado por país:** Guatemala
   - Se realiza un filtrado específico para incluir solo los datos relacionados con el país Guatemala.

3. **Verificación del formato de fecha y filtrado por año:** Los datos se filtraron únicamente para un año de la pandemia
   - Se verifica que el formato de fecha en la columna 'Date_reported' sea correcto y se filtran los datos para incluir solo registros correspondientes a un año específico.

4. **Eliminación de fechas duplicadas**
   - Se identifican y eliminan las filas que contienen fechas duplicadas en la columna 'Date_reported'.

5. **Eliminación de duplicados basados en dos columnas:** Date_reported y Country
   - Se eliminan las filas duplicadas basadas en dos columnas específicas: 'Date_reported' y 'Country'.

6. **Verificación y limpieza columnas numéricas:** New_deaths y Cumulative_deaths
   - Verificación y limpieza de las columnas numéricas 'New_deaths' y 'Cumulative_deaths'.

7. **Limpieza de datos nulos en las columnas:** New_deaths y Cumulative_deaths
   - Limpieza de datos nulos en las columnas 'New_deaths' y 'Cumulative_deaths'.

8. **Limpieza de valores negativos en las columnas:** New_deaths y Cumulative_deaths
   - Limpieza de valores negativos en las columnas 'New_deaths' y 'Cumulative_deaths'.

## Transformación del Archivo Local

1. **Eliminación de columnas irrelevantes:** 'codigo_departamento', 'codigo_municipio', 'poblacion'
   - En esta etapa, se eliminan del conjunto de datos las columnas mencionadas, consideradas irrelevantes para el análisis.

2. **Verificación del formato de fecha y filtrado por año:** Los datos se filtraron únicamente para un año específico de la pandemia
   - Verificación del formato de fecha y filtrado de datos para incluir solo registros de un año específico.

3. **Eliminación de fechas duplicadas**
   - Identificación y eliminación de filas que contienen fechas duplicadas.

5. **Eliminación de duplicados basados en dos columnas:** 'departamento' y 'municipio'
   - Eliminación de filas duplicadas basadas en dos columnas específicas: 'departamento' y 'municipio'.

6. **Verificar y limpiar los datos numéricos**
   - Verificación y limpieza de las columnas numéricas en el conjunto de datos.

7. **Limpieza de datos nulos en cada columna de fecha**
   - Limpieza de valores nulos en cada columna de fecha.

8. **Limpieza de valores negativos en cada columna de fecha**
   - Eliminación de valores negativos en las columnas de fecha.

9. **Convertir Formato de Fecha de mm/dd/yyyy a yyyy-mm-dd**
   - Conversión del formato de fecha de mm/dd/yyyy a yyyy-mm-dd.

---

# Modelo de Datos

## Modelo de Datos

Se eligió el siguiente modelo de datos para representar la información relacionada con las defunciones:

```sql
CREATE DATABASE IF NOT EXISTS `dataset`
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `dataset`.`death` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `country` VARCHAR(45) NULL,
  `departament` VARCHAR(45) NULL,
  `municipality` VARCHAR(45) NULL,
  `population` INT NULL,
  `new_deaths` INT NULL,
  `cumulative_deaths` INT NULL,
  `register_type` ENUM('summary', 'municipality') NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
```
Este modelo de datos se diseñó considerando varios aspectos clave para representar la información de defunciones de manera efectiva:

- **Tablas:** Se utiliza una tabla llamada `death` dentro de la base de datos `dataset`.
- **Atributos:** Cada columna en la tabla representa un atributo específico relacionado con las defunciones, como la fecha (`date`), país (`country`), departamento (`departament`), municipio (`municipality`), nuevas defunciones (`new_deaths`), defunciones acumulativas (`cumulative_deaths`), y el tipo de registro (`register_type`).
- **Claves Primarias:** La columna `id` se designa como la clave primaria, lo que garantiza la unicidad de cada registro en la tabla.
- **Tipos de Datos y Restricciones:** Se utilizan tipos de datos apropiados, como `DATE` para la fecha, `VARCHAR` para texto y `INT` para valores numéricos. Además, se utiliza un tipo enumerado (`ENUM`) para la columna `register_type` que solo puede tomar valores 'summary' o 'municipality'.
- **Autoincremento:** La columna `id` se configura como autoincremental, simplificando la asignación de identificadores únicos a cada registro.
- **Motor de Almacenamiento:** Se utiliza el motor de almacenamiento InnoDB para mejorar la integridad referencial y las transacciones.

Este diseño proporciona una estructura ordenada y eficiente para almacenar información sobre las diferentes fuentes de datos de defunciones, permitiendo consultas y análisis de datos de manera efectiva.

### Manejo de Integridad Referencial y Transacciones

Para garantizar la integridad referencial y mantener la consistencia de los datos, se implementa el manejo de transacciones, commits y rollbacks. Esto se logra mediante el uso del motor de almacenamiento InnoDB, que es compatible con transacciones en MySQL.

A continuación, se describe cómo se manejan las transacciones en el contexto del modelo de datos proporcionado:

- **Inicio de Transacción:** Antes de realizar un conjunto de operaciones (como inserciones, actualizaciones o eliminaciones) que deben ejecutarse de manera atómica, se inicia una transacción.

- **Commit:** Una vez que todas las operaciones dentro de la transacción se han ejecutado con éxito y no ha habido problemas, se emite un commit. Esto confirma permanentemente los cambios y los hace permanentes en la base de datos.

- **Rollback:** Si en algún punto dentro de la transacción surge un problema o error, se puede emitir un rollback. Esto deshace todas las operaciones realizadas desde el inicio de la transacción, devolviendo la base de datos a su estado original antes de la transacción.

El manejo adecuado de transacciones, commits y rollbacks es fundamental para garantizar la integridad referencial y la consistencia de los datos en situaciones donde múltiples operaciones deben ejecutarse de manera coherente.

## Herramientas Utilizadas
- Python _Version 3.12.1_
- Pandas _Version 2.1.4_
- Numpy _Version 1.26.2_
- Streamlit _Version 1.29.0_
- MySQL Connector _Version 2.2.9_
- MySQL _Version 8.0.35_

## Estudiante:
- Eriksson José Hernández López
- 2927191591415
- 201830459
