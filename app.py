import streamlit as st
import pandas as pd
import plotly.express as px

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
    "FERTILIZACION": "💼",  # Costalito de fertilizante
    "SIEMBRA": "🌱",  # Plantita para la siembra
    "BARBECHO": "🧑‍🌾",  # Agricultor trabajando el suelo
    "TRILLA": "🌾",  # Espiga de trigo
    # Puedes agregar más actividades e iconos según necesites
}

# Asignar emojis a las actividades solo para el eje Y
df_filtrado["Icono_actividad"] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")  # Emoji por defecto

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

# Agregar las fechas en las etiquetas de los puntos, pero sin iconos
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")
fig.update_traces(
    text=df_filtrado["Etiqueta"],  # Mostrar solo la fecha
    textposition="top center",
    textfont_size=10,  # Tamaño de fuente pequeño para las fechas
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
