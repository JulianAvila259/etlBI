import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

RUTA_DB = os.getenv("RUTA_DB", "instance")

conn = sqlite3.connect(f'{RUTA_DB}/datacaos_estrella.db')

def preparar_datos_para_carga(df):
    """
    Prepara los datos para la carga en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a preparar.

    Returns:
        pd.DataFrame: DataFrame preparado para la carga.
    """
    # Aquí puedes agregar cualquier transformación adicional que necesites
    df = df.copy()
    
    df = df[["ClienteID", "NombreCliente", "Genero", "RangoEdad", "Ciudad", "SegmentoCliente"]]

    return df


def cargar_datos_en_db(df):
    """
    Actualiza los datos de DimCliente en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a actualizar.

    Returns:
        int: Cantidad de clientes actualizados.
    """
    sql = """
        UPDATE DimCliente
        SET NombreCliente   = ?,
            Genero          = ?,
            RangoEdad       = ?,
            Ciudad          = ?,
            SegmentoCliente = ?
        WHERE ClienteID = ?
    """
    filas = df[["NombreCliente", "Genero", "RangoEdad", "Ciudad", "SegmentoCliente", "ClienteID"]]
    cur = conn.cursor()
    actualizados = 0
    for fila in filas.itertuples(index=False, name=None):
        cur.execute(sql, fila)
        if cur.rowcount == 0:
            print(f"Aviso: el ID {fila[-1]} no existe en DimCliente, se omitió.")
        actualizados += cur.rowcount
    conn.commit()
    return actualizados
