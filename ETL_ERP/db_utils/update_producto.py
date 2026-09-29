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
    
    df = df[["ProductoID", "NombreProducto", "MarcaProducto", "NombreCategoria", "NombreProveedor", "PaisProveedor", "PrecioListado"]]

    return df


def cargar_datos_en_db(df):
    """
    Actualiza los datos de DimProducto en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a actualizar.

    Returns:
        int: Cantidad de productos actualizados.
    """
    sql = """
        UPDATE DimProducto
        SET NombreProducto  = ?,
            MarcaProducto   = ?,
            NombreCategoria = ?,
            NombreProveedor = ?,
            PaisProveedor   = ?,
            PrecioListado   = ?
        WHERE ProductoID = ?
    """
    filas = df[["NombreProducto", "MarcaProducto", "NombreCategoria", "NombreProveedor", "PaisProveedor", "PrecioListado", "ProductoID"]]
    cur = conn.cursor()
    actualizados = 0
    for fila in filas.itertuples(index=False, name=None):
        cur.execute(sql, fila)
        if cur.rowcount == 0:
            print(f"Aviso: el ID {fila[-1]} no existe en DimProducto, se omitió.")
        actualizados += cur.rowcount
    conn.commit()
    return actualizados
