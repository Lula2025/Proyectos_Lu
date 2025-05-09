import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Línea de Tiempo de Actividades")

# Leer el archivo directamente desde la misma carpeta
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Convertir a datetime
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(
    df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce'
)

# Extraer el mes con nombre (abreviado o completo)
df['Mes'] = df['Fecha_en_que_se_realizó_la_actividad'].dt.strftime('%b')  # %B para nombre completo

# Selección del cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

# Filtrar datos
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado]

# Ordenar por fecha para mejor visualización
df_filtrado = df_filtrado.sort_values(by="Fecha_en_que_se_realizó_la_actividad")

# Gráfico tipo scatter con nombres de mes en el eje X
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y=["Actividad_realizada"],
    text="Actividad_realizada",
    title=f"Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# Mostrar etiquetas y configurar diseño
fig.update_traces(mode="markers+text", textposition="top center")

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad",
    yaxis=dict(showticklabels=False),
    xaxis_tickformat="%b %Y",  # Mostrar nombre del mes y año
    margin=dict(l=40, r=40, t=80, b=40)
)

st.plotly_chart(fig, use_container_width=True)
