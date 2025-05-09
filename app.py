import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la app
st.title("📅 Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo local
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Asegurarse de que la fecha esté en formato datetime
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce')

# Selección del ID de cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique())

# Filtrar el DataFrame por el ID de cultivo
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Ordenar actividades por fecha (más antigua primero)
orden_actividades = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad")["Actividad_realizada"].unique()[::-1]

# Crear gráfico de línea de tiempo
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

# Personalizar el texto de cada punto (pequeño, solo la fecha)
df_filtrado["TextoEtiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")
fig.update_traces(text=df_filtrado["TextoEtiqueta"], textposition="top center", textfont_size=9, mode="markers+text")

# Mejorar diseño del gráfico
fig.update_layout(
    xaxis_title="Fecha (por mes)",
    yaxis_title="Actividad",
    xaxis=dict(tickformat="%b %Y"),
    yaxis=dict(categoryorder='array', categoryarray=orden_actividades),
    margin=dict(l=40, r=40, t=80, b=40),
    height=600
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)
