import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

RUTA_DB = os.getenv("RUTA_DB", "instance")

conn = sqlite3.connect(f'{RUTA_DB}/datacaos_estrella.db')
"""
def _siguiente_numero_venta(con):
    actual = con.execute(
        "SELECT MAX(CAST(SUBSTR(VentaID, 2) AS INTEGER)) FROM VentasFact"
    ).fetchone()[0]
    return actual or 0
"""


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
    """
    # Genera los consecutivos de VentaID basados en el último número en la base de datos
    siguiente = _siguiente_numero_venta(conn)
    df["VentaID"] = [f"V{str(siguiente + i + 1).zfill(6)}" for i in range(len(df))]
    """
    df = df[["TiendaID", "NombreTienda", "Ciudad", "Region", "FechaApertura"]]

    return df


def cargar_datos_en_db(df):
    """
    Actualiza los datos de DimTienda en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a actualizar.

    Returns:
        int: Cantidad de tiendas actualizadas.
    """
    sql = """
        UPDATE DimTienda
        SET NombreTienda  = ?,
            Ciudad        = ?,
            Region        = ?,
            FechaApertura = ?
        WHERE TiendaID = ?
    """
    filas = df[["NombreTienda", "Ciudad", "Region", "FechaApertura", "TiendaID"]]
    cur = conn.cursor()
    actualizados = 0
    for fila in filas.itertuples(index=False, name=None):
        cur.execute(sql, fila)
        if cur.rowcount == 0:
            print(f"Aviso: el ID {fila[-1]} no existe en DimTienda, se omitió.")
        actualizados += cur.rowcount
    conn.commit()
    return actualizados
