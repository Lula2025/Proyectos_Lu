import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta  # Solo si lo necesitas para alguna operación específica

# Configuración de la página de Streamlit
st.set_page_config(page_title="Línea de Tiempo de Actividades", layout="wide")

# Título de la aplicación con un emoji de calendario
st.title("Actividades por Cultivo")

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
    title=f"🕒 Línea de Tiempo de Actividades por Cultivo {id_cultivo_seleccionado}",
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

# Formatear la fecha y renombrar la columna
df_insumos_filtrado["Fecha_en_que_se_realizó_la_actividad"] = df_insumos_filtrado[
    "Fecha_en_que_se_realizó_la_actividad"
].dt.strftime("%Y-%m-%d")

# Renombrar la columna de fecha
df_insumos_filtrado = df_insumos_filtrado.rename(columns={
    "Fecha_en_que_se_realizó_la_actividad": "Fecha_de_aplicación"
})

# Ocultar las columnas "ID_Cultivo" y "Categoría_del_producto"
columnas_a_mostrar = [
    "Fecha_de_aplicación",
    "Nombre_del_producto",
    "Cantidad",
    "Unidad_ha",
    "Lugar_de_aplicación"
]

# Resetear el índice para evitar que se muestre como columna
df_insumos_filtrado = df_insumos_filtrado.reset_index(drop=True)

# Mostrar la tabla ordenada sin el índice original
st.subheader("📋 Detalle de Aplicación de Insumos")
st.dataframe(
    df_insumos_filtrado.sort_values("Fecha_de_aplicación"),
    use_container_width=True
)


######################
# Gráfico de pastel por categoría del producto
st.subheader("🛍️ Distribución de Insumos por Categoría")

fig_pie = px.pie(
    df_insumos_filtrado,
    names="Categoría_del_producto",
    values="Cantidad",
    title=" ",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_pie.update_traces(textinfo='percent+label')
fig_pie.update_layout(title_font_size=18)

st.plotly_chart(fig_pie, use_container_width=True)

######################################
# Agrupar por producto y unidad, y sumar la cantidad
df_resumen = (
    df_insumos_filtrado
    .groupby(["Nombre_del_producto", "Unidad_ha"], as_index=False)["Cantidad"]
    .sum()
)

# Crear columna de etiquetas con cantidad + unidad
df_resumen["Etiqueta"] = df_resumen["Cantidad"].round(2).astype(str) + " " + df_resumen["Unidad_ha"]

# Ordenar por cantidad
df_resumen = df_resumen.sort_values(by="Cantidad", ascending=False)

# Crear gráfico de barras
import plotly.express as px

st.subheader("📊 Cantidad Total de Insumo Aplicado por Producto y Unidad")

# Obtener las unidades únicas
unidades = df_insumos_filtrado["Unidad_ha"].dropna().unique()

# Para cada unidad, crear un gráfico separado
for unidad in unidades:
    df_unidad = df_insumos_filtrado[df_insumos_filtrado["Unidad_ha"] == unidad]

    # Agrupar por producto
    df_resumen = (
        df_unidad
        .groupby("Nombre_del_producto", as_index=False)["Cantidad"]
        .sum()
    )
    
    # Crear etiquetas con la cantidad redondeada y unidad
    df_resumen["Etiqueta"] = df_resumen["Cantidad"].round(2).astype(str) + f" {unidad}"
    
    # Ordenar por cantidad
    df_resumen = df_resumen.sort_values(by="Cantidad", ascending=False)

    # Crear gráfico
    fig = px.bar(
        df_resumen,
        x="Nombre_del_producto",
        y="Cantidad",
        title=f"Unidad: {unidad}",
        labels={"Cantidad": f"Cantidad ({unidad})", "Nombre_del_producto": "Producto"},
        color="Cantidad",
        color_continuous_scale="Blues",
        text="Etiqueta"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=450,
        margin=dict(l=20, r=20, t=60, b=100)
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)
