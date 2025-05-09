import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🗓️ Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo desde la carpeta local
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Convertir a fecha y limpiar errores
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(
    df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce'
)

# Filtrar solo fechas válidas
df = df[df['Fecha_en_que_se_realizó_la_actividad'].notna()]

# Selección de cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

# Filtrar por ID de cultivo
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Limitar longitud de etiquetas largas (opcional)
df_filtrado["Etiqueta_Actividad"] = df_filtrado["Actividad_realizada"].str.slice(0, 50)

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    text="Etiqueta_Actividad",
    title=f"📌 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# Mejorar presentación
fig.update_traces(mode="markers+text", textposition="top center")
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad realizada",
    xaxis_tickformat="%b %Y",  # nombre del mes
    margin=dict(l=40, r=40, t=80, b=40),
    height=500
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
