import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta  # Solo si lo necesitas para alguna operación específica

# Configuración de la página de Streamlit
st.set_page_config(page_title="Línea de Tiempo de Actividades", layout="wide")

# Título de la aplicación con un emoji de calendario
st.title("📅 Línea de Tiempo de Actividades por Cultivo")

# Cargar el archivo CSV directamente sin necesidad de cargarlo manualmente
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
    "FERTILIZACION": "🛍️",  # Costalito de fertilizante
    "SIEMBRA": "🌱",  # Plantita para la siembra
    "BARBECHO": "🚜",  # Agricultor trabajando el suelo
    "RASTREO": "🚜",  # Agricultor trabajando el suelo
    "SURCOS": "🚜",  # Agricultor trabajando el suelo
    "ESCARDA": "🚜",  # Agricultor trabajando el suelo
    "CONTROL_DE_PLAGAS": "🌿🦗",  # Agricultor trabajando el suelo
    "CONTROL_DE_MALEZAS": "🌿🪓",  # Agricultor trabajando el suelo
    "TRILLA": "🌽"  # Espiga de trigo
}

# Asignar emojis a las actividades solo para el eje Y
df_filtrado["Icono_actividad"] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")  # Emoji por defecto

#####
# Crear la etiqueta de fecha completa
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %B %Y")

# Ordenar por fecha
df_filtrado = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad").reset_index(drop=True)

# Inicializar la columna con posición de texto
df_filtrado["Posición_texto"] = "top center"

# Alternar posición si la fecha está muy cerca (por ejemplo, ≤ 2 días de diferencia)
posiciones = ["top center", "bottom center"]
ultima_fecha = None
posicion_actual = 0

for i, row in df_filtrado.iterrows():
    fecha_actual = row["Fecha_en_que_se_realizó_la_actividad"]

    if ultima_fecha and abs((fecha_actual - ultima_fecha).days) <= 2:
        # Si está muy cerca de la anterior, alternamos posición
        posicion_actual = (posicion_actual + 1) % 2
    else:
        # Si no está cerca, reiniciamos a "top"
        posicion_actual = 0

    df_filtrado.at[i, "Posición_texto"] = posiciones[posicion_actual]
    ultima_fecha = fecha_actual

###

# Crear gráfico de dispersión
fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    category_orders={"Actividad_realizada": orden_actividades},
    title=f"🕒 Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
    labels={"Fecha_en_que_se_realizó_la_actividad": "Fecha"},
    color_discrete_sequence=["#FF6347"],  # Color más vibrante
    hover_data={
        "Actividad_realizada": False,  # No mostrar actividad al pasar el ratón
        "Fecha_en_que_se_realizó_la_actividad": True
    },
)

# Agregar iconos a las actividades solo en el eje Y
fig.update_layout(
    yaxis=dict(
        tickmode="array",  # Mostrar solo las actividades en el eje Y
        tickvals=orden_actividades,  # Definir el orden de las actividades
        ticktext=[f"{emoji_actividades.get(act, '🔄')} {act}" for act in orden_actividades],  # Incluir los iconos en el eje Y
    ),
)

# Agregar las fechas en las etiquetas de los puntos
fig.update_traces(
    text=df_filtrado["Etiqueta"],  # Mostrar solo la fecha
    textposition=df_filtrado["Posición_texto"],
    textfont_size=8,  # Tamaño de fuente pequeño para las fechas
    mode="markers+text",
    marker=dict(size=12, symbol="circle", color="#FF6347")  # Puntos más grandes y coloridos
)

# Mejorar la presentación del gráfico
fig.update_layout(
    xaxis_title="Mes y Año",
    yaxis_title="Actividad",
    xaxis=dict(
        tickformat="%b %Y",  # Mostrar solo mes y año
        tickangle=45,  # Rotar las etiquetas de los meses
        dtick="M1"  # Mostrar un tick cada mes
    ),
    margin=dict(l=40, r=40, t=80, b=80),  # Márgenes más amplios
    height=600,  # Altura más grande
    width=1200,  # Ancho más grande para una mejor visualización
    title_font_size=24,  # Aumentar el tamaño del título
    font=dict(size=12, family="Arial, sans-serif"),  # Usar una fuente más legible
    plot_bgcolor="#F9F9F9"  # Fondo claro para el gráfico
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Espacio entre el gráfico y otros elementos
st.markdown("<br>", unsafe_allow_html=True)






