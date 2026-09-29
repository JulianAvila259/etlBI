import pandas as pd
import os

def leer_archivo_csv(ruta_archivo):
    """
    Lee un archivo CSV a partir de su ruta y lo carga en un DataFrame.

    Args:
        ruta_archivo (str): Ruta del archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos del archivo CSV (todas las columnas como texto,
            para que los valores lleguen tal cual están escritos).
    """
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {ruta_archivo}")

    return pd.read_csv(ruta_archivo, dtype=str)

def eliminar_duplicados(df, columnas):
    """
    Elimina filas duplicadas en un DataFrame basado en las columnas especificadas.

    Args:
        df (pd.DataFrame): El DataFrame del cual se eliminarán los duplicados.
        columnas (list): Lista de nombres de columnas para identificar duplicados.

    Returns:
        pd.DataFrame: DataFrame sin filas duplicadas.
    """
    return df.drop_duplicates(subset=columnas)

def formato_fecha(df, columna_fecha, formato="%Y-%m-%d", formato_entrada=None):
    """
    Convierte una columna de fecha en un DataFrame al formato especificado.

    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna de fecha.
        columna_fecha (str): Nombre de la columna que contiene las fechas.
        formato (str): Formato deseado para la fecha (por defecto es "%Y-%m-%d").
        formato_entrada (str): Formato en que vienen las fechas (ej. "%d-%m-%Y"). Si es None, pandas lo infiere.

    Returns:
        pd.DataFrame: DataFrame con la columna de fecha formateada.
    """
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], format=formato_entrada).dt.strftime(formato)
    return df

def renombrar_columnas(df, mapeo_columnas):
    """
    Renombra las columnas de un DataFrame según un mapeo proporcionado.

    Args:
        df (pd.DataFrame): El DataFrame cuyas columnas se renombrarán.
        mapeo_columnas (dict): Diccionario que mapea nombres antiguos a nuevos nombres.

    Returns:
        pd.DataFrame: DataFrame con las columnas renombradas.
    """
    return df.rename(columns=mapeo_columnas)

def conversion_mayusculas(df, columnas):
    """
    Convierte los valores de las columnas especificadas a mayúsculas.

    Args:
        df (pd.DataFrame): El DataFrame que contiene las columnas a convertir.
        columnas (list): Lista de nombres de columnas cuyos valores se convertirán a mayúsculas.

    Returns:
        pd.DataFrame: DataFrame con los valores de las columnas especificadas en mayúsculas.
    """
    for columna in columnas:
        df[columna] = df[columna].str.upper()
    return df

def eliminar_espacios(df, columnas):
    """
    Elimina los espacios en blanco al inicio y al final de los valores en las columnas especificadas.

    Args:
        df (pd.DataFrame): El DataFrame que contiene las columnas a limpiar.
        columnas (list): Lista de nombres de columnas cuyos valores se limpiarán.

    Returns:
        pd.DataFrame: DataFrame con los valores de las columnas especificadas sin espacios en blanco.
    """
    for columna in columnas:
        df[columna] = df[columna].str.strip()
    return df
