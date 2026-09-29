import os
from dotenv import load_dotenv
from utils.reglas_producto import leer_archivo_csv, eliminar_duplicados, eliminar_espacios, conversion_mayusculas, validar_precio
from db_utils.update_producto import cargar_datos_en_db, preparar_datos_para_carga

load_dotenv()

ruta_producto = os.getenv("RUTA_PRODUCTO", "csvs/DimProducto_actualizacion.csv")

datos_producto = leer_archivo_csv(ruta_producto)

datos_producto = conversion_mayusculas(datos_producto, ["ProductoID"])

datos_producto = eliminar_espacios(datos_producto, ["ProductoID"])

datos_producto = eliminar_duplicados(datos_producto, ["ProductoID"])

datos_producto = validar_precio(datos_producto, "PrecioListado")

datos_a_cargar = preparar_datos_para_carga(datos_producto)

actualizados = cargar_datos_en_db(datos_a_cargar)

print(f"Se han actualizado {actualizados} registros en la base de datos.")
