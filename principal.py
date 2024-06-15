import streamlit as st

st.set_page_config(page_title="Estudio enfermedades respiratorias y calidad del aire", page_icon="📊", layout="wide")

st.title("Visualización de datos de enfermedades respiratorias y calidad del aire")


st.write("## Explicación de los datos")

st.subheader("Datos de cáncer")
st.write("Número de casos de cáncer por estado y año")
st.markdown("[Enlace a la base de datos de cáncer](https://ephtracking.cdc.gov/qrd/61)")

st.subheader("Datos de asma")
st.write("Número de visitas a emergencia por asma por estado y año")
st.markdown("[Enlace a la base de datos de asma](https://ephtracking.cdc.gov/qrd/87)")

st.subheader("Datos de calidad del aire")
st.write("Medición de PM2.5 por estado y año.")
st.write("PM2.5: Concentración de partículas en el aire que tienen un diámetro de 2.5 micrómetros o menos")
st.markdown("[Enlace a la base de datos de calidad del aire](https://ephtracking.cdc.gov/qrd/434)")

