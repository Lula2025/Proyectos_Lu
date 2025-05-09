import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📅 Línea de Tiempo de Actividades por Cultivo")

# Cargar archivo directamente desde la misma carpeta
try:
    df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo '6_2023_2024_a_marzo_2025.csv'. Asegúrate de que esté en la misma carpeta que este script.")
    st.stop()

# Convertir la columna de fecha al tipo datetime
df['Fecha_en_que_se_realizaron_las_actividades'] = pd.to_datetime(
    df['Fecha_en_que_se_realizaron_las_actividades'], errors='coerce')

# Selector de ID de cultivo
id_cultivo_seleccionado = st.selectbox("🌾 Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique())

# Filtrar el DataFrame por el ID seleccionado
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado]

# Crear el gráfico de línea de tiempo
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizaron_las_actividades",
    y=["Actividad_realizada"],
    text="Actividad_realizada",
    title=f"🛠️ Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizaron_las_actividades": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

fig.update_traces(mode="markers+text", textposition="top center")

# Ajustar diseño
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad",
    yaxis=dict(showticklabels=False),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
