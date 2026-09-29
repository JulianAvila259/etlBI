import pandas as pd
import os
import re

def leer_archivo_csv(ruta_archivo):
    """
    Lee un archivo CSV a partir de su ruta y lo carga en un DataFrame.

    Args:
        ruta_archivo (str): Ruta del archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos del archivo CSV (todas las columnas como texto,
            para que el precio llegue tal cual está escrito y se valide después con validar_precio).
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

def validar_precio(df, columna):
    """
    Valida que los valores de una columna de precio respeten el formato DECIMAL(12,2) de la base de datos:
    solo dígitos con punto decimal, máximo 2 decimales y máximo 10 dígitos enteros. No admite valores vacíos.

    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna de precio.
        columna (str): Nombre de la columna de precio.

    Returns:
        pd.DataFrame: DataFrame con la columna de precio convertida a número.

    Raises:
        ValueError: Si algún valor no respeta el formato. El mensaje lista todos los valores inválidos.
    """
    df = df.copy()
    errores = []

    for indice, valor in df[columna].items():
        fila = indice + 2  # la fila 1 del CSV es el encabezado
        if pd.isna(valor) or str(valor).strip() == "":
            errores.append(f"Fila {fila} | {columna} | vacío | el precio no puede estar vacío")
            continue

        numero = re.fullmatch(r"(\d+)(?:\.(\d+))?", str(valor).strip())
        if not numero:
            errores.append(f"Fila {fila} | {columna} | '{valor}' | no es un número válido (solo dígitos y punto decimal)")
        elif len(numero.group(2) or "") > 2:
            errores.append(f"Fila {fila} | {columna} | '{valor}' | tiene más de 2 decimales, DECIMAL(12,2)")
        elif len(numero.group(1)) > 10:
            errores.append(f"Fila {fila} | {columna} | '{valor}' | supera los 10 dígitos enteros de DECIMAL(12,2)")

    if errores:
        raise ValueError("Precios que no respetan el formato de la base de datos:\n  " + "\n  ".join(errores))

    df[columna] = df[columna].astype(float)
    return df
