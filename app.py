import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Línea de Tiempo de Actividades", layout="wide")

st.title("📅 Línea de Tiempo de Actividades por ID_Cultivo?/Id_Tipo de parcela")

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

# Obtener orden cronológico de actividades y luego invertirlo (para que la primera esté abajo)
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

# Etiquetas con solo la fecha completa
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")
fig.update_traces(
    text=df_filtrado["Etiqueta"],  # Mostrar solo la fecha completa
    textposition="top center",
    textfont_size=10,  # Aumentar tamaño de texto para mejor visibilidad
    mode="markers+text"
)

# Ajustar diseño del eje X para mostrar solo mes y año
fig.update_layout(
    xaxis_title="Mes y Año",
    yaxis_title="Actividad",
    xaxis=dict(
        tickformat="%b %Y",  # Ejemplo: Mar 2024
        tickangle=45,
        dtick="M1"  # Esto asegura que se muestre un mes por tick
    ),
    margin=dict(l=40, r=40, t=80, b=80),  # Mayor espacio en los márgenes
    height=600,  # Aumentar altura
    width=1200,  # Ampliar el ancho del gráfico
    title_font_size=24,  # Aumentar tamaño del título
    font=dict(size=12)  # Tamaño de fuente general
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Espacio entre el gráfico y otros elementos
st.markdown("<br>", unsafe_allow_html=True)

