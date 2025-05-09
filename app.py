import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🗓️ Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Convertir a datetime y eliminar nulos
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(
    df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce'
)
df = df[df['Fecha_en_que_se_realizó_la_actividad'].notna()]

# Selección de cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Etiqueta con fecha en texto para mostrar en puntos
df_filtrado["Etiqueta_Fecha"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")

# Ordenar las actividades por fecha de aparición
orden_actividades = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad")["Actividad_realizada"].unique()
df_filtrado["Actividad_realizada"] = pd.Categorical(
    df_filtrado["Actividad_realizada"], categories=orden_actividades, ordered=True
)

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    hover_name="Actividad_realizada",
    text="Etiqueta_Fecha",
    title=f"📌 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#2ca02c"]
)

# Ajustar diseño de etiquetas
fig.update_traces(
    textposition="top center",
    textfont_size=9
)

# Mejorar diseño general
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad realizada (orden cronológico)",
    xaxis_tickformat="%b %Y",
    margin=dict(l=40, r=40, t=80, b=40),
    height=500
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
