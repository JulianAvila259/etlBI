import os
from dotenv import load_dotenv
from utils.reglas_cliente import leer_archivo_csv, eliminar_duplicados, eliminar_espacios, conversion_mayusculas, normalizar_valores
from db_utils.update_cliente import cargar_datos_en_db, preparar_datos_para_carga

load_dotenv()

ruta_cliente = os.getenv("RUTA_CLIENTE", "csvs/DimCliente_actualizacion.csv")

datos_cliente = leer_archivo_csv(ruta_cliente)

datos_cliente = conversion_mayusculas(datos_cliente, ["ClienteID"])

datos_cliente = eliminar_espacios(datos_cliente, ["ClienteID"])

datos_cliente = eliminar_duplicados(datos_cliente, ["ClienteID"])

equivalencias_genero = {
    "F": "F",
    "FEMENINO": "F",
    "M": "M",
    "MASCULINO": "M"
}

datos_cliente = normalizar_valores(datos_cliente, "Genero", equivalencias_genero)

datos_a_cargar = preparar_datos_para_carga(datos_cliente)

actualizados = cargar_datos_en_db(datos_a_cargar)

print(f"Se han actualizado {actualizados} registros en la base de datos.")
