import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📅 Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo local
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Asegurar formato datetime
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(
    df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce'
)

# Selección del ID de cultivo
id_cultivo_seleccionado = st.selectbox(
    "Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique()
)

# Filtrar el DataFrame
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Obtener orden cronológico de actividades y luego invertirlo
orden_actividades = df_filtrado.sort_values(
    "Fecha_en_que_se_realizó_la_actividad"
)["Actividad_realizada"].unique()[::-1]

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    category_orders={"Actividad_realizada": orden_actividades},
    title=f"🕒 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"],
    hover_data={
        "Actividad_realizada": False,
        "Fecha_en_que_se_realizó_la_actividad": True
    },
)

# Añadir etiquetas pequeñas con la fecha
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")
fig.update_traces(
    text=df_filtrado["Etiqueta"],
    textposition="top center",
    textfont_size=9,
    mode="markers+text"
)

# Ajustar diseño con mayor separación entre meses
fig.update_layout(
    xaxis_title="Fecha (mes y año)",
    yaxis_title="Actividad",
    xaxis=dict(
        tickformat="%b %Y",
        tickangle=0,
        dtick="M1"  # Mostrar un tick por mes
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    height=600,
    width=1400  # Mayor ancho para más separación
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=False)
