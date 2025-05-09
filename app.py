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

# Filtrar fechas válidas
df = df[df['Fecha_en_que_se_realizó_la_actividad'].notna()]

# Selección del cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

# Filtrar por el ID seleccionado
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Etiqueta como fecha en texto (formato legible)
df_filtrado["Etiqueta_Fecha"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")

# Crear gráfico sin mostrar nombre de actividad como texto
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    hover_name="Actividad_realizada",  # nombre completo visible al pasar el cursor
    text="Etiqueta_Fecha",  # etiqueta visible pequeña
    title=f"📌 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# Ajustar diseño de etiquetas pequeñas
fig.update_traces(
    textposition="top center",
    textfont_size=9
)

# Mejorar layout
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad realizada",
    xaxis_tickformat="%b %Y",  # abreviatura de mes
    margin=dict(l=40, r=40, t=80, b=40),
    height=500
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
