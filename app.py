import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Línea de Tiempo de Actividades por Cultivo")

# --- Cargar datos ---
try:
    df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")  # Asegúrate de que este archivo esté en el mismo directorio
except FileNotFoundError:
    st.error("❌ Archivo '6_2023_2024_a_marzo_2025.csv' no encontrado.")
    st.stop()

# --- Convertir fechas a formato datetime ---
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce')

# --- Selección interactiva de ID de cultivo ---
ids_disponibles = df['ID_Cultivo'].dropna().unique()
id_cultivo_seleccionado = st.selectbox("🔍 Selecciona un ID de Cultivo", ids_disponibles)

# --- Filtrar datos por ID seleccionado ---
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado]

# --- Crear gráfico tipo línea de tiempo ---
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y=["Actividad_realizada"],
    text="Actividad_realizada",
    title=f"🗓️ Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# --- Configurar presentación de texto ---
fig.update_traces(mode="markers+text", textposition="top center")

# --- Mejorar diseño del gráfico ---
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad",
    yaxis=dict(showticklabels=False),  # Oculta etiquetas repetitivas
    margin=dict(l=40, r=40, t=80, b=40)
)

# --- Mostrar gráfico ---
st.plotly_chart(fig, use_container_width=True)
