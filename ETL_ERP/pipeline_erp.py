import os
from dotenv import load_dotenv
from utils.reglas import leer_archivo_csv, eliminar_duplicados, eliminar_espacios, formato_fecha, conversion_mayusculas
from db_utils.update_tienda import cargar_datos_en_db, preparar_datos_para_carga

load_dotenv()

ruta_tienda = os.getenv("RUTA_TIENDA", "csvs/DimTienda_actualizacion.csv")

datos_tienda = leer_archivo_csv(ruta_tienda)

datos_tienda = formato_fecha(datos_tienda, "FechaApertura", "%Y-%m-%d", "%d-%m-%Y")

datos_tienda = conversion_mayusculas(datos_tienda, ["TiendaID"])

datos_tienda = eliminar_espacios(datos_tienda, ["TiendaID"])

datos_tienda = eliminar_duplicados(datos_tienda, ["TiendaID"])

datos_a_cargar = preparar_datos_para_carga(datos_tienda)

actualizados = cargar_datos_en_db(datos_a_cargar)

print(f"Se han actualizado {actualizados} registros en la base de datos.")
