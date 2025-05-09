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

# Filtrar solo filas con fechas válidas
df = df[df['Fecha_en_que_se_realizó_la_actividad'].notna()]

# Selección interactiva del ID de Cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

# Filtrar por el ID seleccionado y ordenar
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].sort_values(by="Fecha_en_que_se_realizó_la_actividad")

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y=[0] * len(df_filtrado),  # valor constante para ocultar eje Y
    text="Actividad_realizada",
    title=f"📌 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# Configuración del gráfico
fig.update_traces(mode="markers+text", textposition="top center")
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title=None,
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    xaxis_tickformat="%b %Y",
    margin=dict(l=40, r=40, t=80, b=40),
    height=400
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)
