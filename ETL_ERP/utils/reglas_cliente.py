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

def normalizar_valores(df, columna, equivalencias):
    """
    Reemplaza los valores de una columna según un diccionario de equivalencias, sin distinguir
    mayúsculas de minúsculas ni espacios al inicio o al final.

    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna.
        columna (str): Nombre de la columna a normalizar.
        equivalencias (dict): Diccionario {valor_en_mayusculas: valor_final}, ej. {"FEMENINO": "F"}.

    Returns:
        pd.DataFrame: DataFrame con la columna normalizada. Los valores vacíos se dejan como están.

    Raises:
        ValueError: Si algún valor no tiene equivalencia. El mensaje lista los valores no reconocidos.
    """
    df = df.copy()
    normalizado = df[columna].str.strip().str.upper().map(equivalencias)
    no_reconocidos = df[columna].notna() & normalizado.isna()

    if no_reconocidos.any():
        permitidos = ", ".join(dict.fromkeys(equivalencias.values()))
        errores = [f"Fila {indice + 2} | {columna} | '{valor}' | no es un valor reconocido (debe ser {permitidos})"
                   for indice, valor in df.loc[no_reconocidos, columna].items()]
        raise ValueError("Valores que no se pueden normalizar:\n  " + "\n  ".join(errores))

    df[columna] = normalizado
    return df
