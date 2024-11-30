import streamlit as st
import pandas as pd
from io import BytesIO

# Ruta del archivo CSV
file_path = "base_examen.csv"

# Carga de datos
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error("No se encontró el archivo en la ruta: " + path)
        return None

# Convertir DataFrame a archivo Excel
@st.cache_data
def convert_to_excel(df):
    # Eliminar la columna "Grupo" antes de guardar el archivo
    df = df.drop(columns=["Grupo"])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Datos Filtrados")
    processed_data = output.getvalue()
    return processed_data

# Cargar datos
data = load_data(file_path)

if data is not None:
    st.title("Base de datos para el Quizz 2")

    # Crear lista de grupos únicos con "Selecciona un grupo" como primera opción
    grupos = ["Selecciona un grupo"] + sorted(data['Grupo'].dropna().unique().tolist())

    # Selector de grupo
    selected_group = st.selectbox("Selecciona tu grupo:", grupos)

    # Verifica que se haya seleccionado un grupo válido
    if selected_group != "Selecciona un grupo":
        # Filtrar datos
        filtered_data = data[data["Grupo"] == selected_group]

        # Botón para descargar los datos filtrados
        excel_data = convert_to_excel(filtered_data)
        st.download_button(
            label="Descargar datos para morir en el quiz",
            data=excel_data,
            file_name=f"¡Mucho éxito equipo {selected_group}!.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("Selecciona un grupo para habilitar la descarga de datos.")
