import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta  # Solo si lo necesitas para alguna operación específica

# Configuración de la página de Streamlit
st.set_page_config(page_title="Línea de Tiempo de Actividades", layout="wide")

# Título de la aplicación con un emoji de calendario
st.title("📅 Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo CSV de actividades
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")

# Asegurar formato datetime para las fechas
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce')

# Selección del ID de cultivo con un selectbox
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique())

# Filtrar los datos por el ID de cultivo seleccionado
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()

# Ordenar las actividades cronológicamente y luego invertirlas para que las más antiguas estén abajo
orden_actividades = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad")["Actividad_realizada"].unique()[::-1]

# Diccionario de emojis según la actividad
emoji_actividades = {
    "FERTILIZACION": "🛍️",
    "SIEMBRA": "🌱",
    "BARBECHO": "🚜",
    "RASTREO": "🚜",
    "SURCOS": "🚜",
    "ESCARDA": "🚜",
    "CONTROL_DE_PLAGAS": "🌿🦗",
    "CONTROL_DE_MALEZAS": "🌿🪓",
    "TRILLA": "🌽"
}

# Asignar emojis a las actividades
df_filtrado["Icono_actividad"] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")

# Crear la etiqueta de fecha
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %B %Y")

# Ordenar por fecha
df_filtrado = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad").reset_index(drop=True)

# Alternar posiciones para etiquetas
df_filtrado["Posición_texto"] = "top center"
posiciones = ["top center", "bottom center"]
ultima_fecha = None
posicion_actual = 0

for i, row in df_filtrado.iterrows():
    fecha_actual = row["Fecha_en_que_se_realizó_la_actividad"]
    if ultima_fecha and abs((fecha_actual - ultima_fecha).days) <= 2:
        posicion_actual = (posicion_actual + 1) % 2
    else:
        posicion_actual = 0
    df_filtrado.at[i, "Posición_texto"] = posiciones[posicion_actual]
    ultima_fecha = fecha_actual

# Crear gráfico de dispersión
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    category_orders={"Actividad_realizada": orden_actividades},
    title=f"🕒 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#FF6347"],
    hover_data={"Actividad_realizada": False, "Fecha_en_que_se_realizó_la_actividad": True},
)

fig.update_layout(
    yaxis=dict(
        tickmode="array",
        tickvals=orden_actividades,
        ticktext=[f"{emoji_actividades.get(act, '🔄')} {act}" for act in orden_actividades],
    ),
    xaxis_title="Mes y Año",
    yaxis_title="Actividad",
    xaxis=dict(
        tickformat="%b %Y",
        tickangle=45,
        dtick="M1"
    ),
    margin=dict(l=40, r=40, t=80, b=80),
    height=600,
    width=1200,
    title_font_size=24,
    font=dict(size=12, family="Arial, sans-serif"),
    plot_bgcolor="#F9F9F9"
)

fig.update_traces(
    text=df_filtrado["Etiqueta"],
    textposition=df_filtrado["Posición_texto"],
    textfont_size=8,
    mode="markers+text",
    marker=dict(size=8, symbol="circle", color="#FF6347")
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------
# TABLA DE INSUMOS
# ----------------------------

# Cargar archivo de insumos
df_insumos = pd.read_csv("Insumos_2023_2024_a_marzo_2025.csv")

# Mostrar columnas para verificar nombres
st.write(df_insumos.columns)

# Convertir fechas a datetime
df_insumos['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(
    df_insumos['Fecha_en_que_se_realizó_la_actividad'], errors='coerce'
)

# Filtrar por cultivo seleccionado
df_insumos_filtrado = df_insumos[df_insumos["ID_Cultivo"] == id_cultivo_seleccionado].copy()

# Columnas a mostrar
columnas_deseadas = [
    "ID_Cultivo",
    "Fecha_en_que_se_realizó_la_actividad",
    "Categoría_del_producto",
    "Nombre_del_producto",
    "Cantidad",
    "Unidad_ha",
    "Lugar_de_aplicación"
]

df_insumos_filtrado = df_insumos_filtrado[columnas_deseadas]

# Redondear la cantidad a 2 decimales
df_insumos_filtrado["Cantidad"] = df_insumos_filtrado["Cantidad"].round(2)

# Formatear la fecha para quitar los segundos
df_insumos_filtrado["Fecha_en_que_se_realizó_la_actividad"] = df_insumos_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%Y-%m-%d %H:%M")

# Mostrar la tabla ordenada
st.subheader("📋 Aplicación de Insumos por Fecha")
st.dataframe(df_insumos_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad"))

