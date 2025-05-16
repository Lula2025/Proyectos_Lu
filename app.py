import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="Línea de Tiempo de Actividades", layout="wide")
st.title("Actividades por Parcela / ID_Cultivo")

# Cargar el archivo
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")
df['Fecha_en_que_se_realizó_la_actividad'] = pd.to_datetime(df['Fecha_en_que_se_realizó_la_actividad'], errors='coerce')

# Diccionario de emojis
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

# Selección de cultivo
id_cultivo_seleccionado = st.selectbox("✅ Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique())
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()
df_filtrado['Emoji'] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")
df_filtrado = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad").reset_index(drop=True)

# --------- PRIMERA GRÁFICA: Plotly timeline ---------

orden_actividades = df_filtrado["Actividad_realizada"].unique()[::-1]
df_filtrado["Icono_actividad"] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %B %Y")

# Alternar posiciones de texto
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

fig = px.scatter(
    df_filtrado,
    x="Fecha_en_que_se_realizó_la_actividad",
    y="Actividad_realizada",
    category_orders={"Actividad_realizada": orden_actividades},
    title=f"🗓️ Línea de Tiempo de Actividades por Cultivo {id_cultivo_seleccionado}",
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

# --------- SEGUNDA GRÁFICA: Línea de tiempo alterna con tarjetas ---------
st.markdown("---")
st.subheader("🌿 Línea de Tiempo Alterna (Estilo Árbol con Conectores)")

# CSS con línea vertical tronco visible y líneas horizontales conectores
st.markdown("""
<style>
.timeline-wrapper {
    position: relative;
    padding-left: 50px;
    padding-right: 50px;
    margin-bottom: 40px;
}
.timeline-line {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 4px;
    background-color: #FF6347;
    border-radius: 2px;
    transform: translateX(-50%);
    z-index: 0;
}
.timeline-row {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
}
.timeline-left, .timeline-right {
    width: 180px;
    padding: 6px 12px;
    border-radius: 8px;
    background-color: #f0f0f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    font-size: 14px;
    display: flex;
    align-items: center;
}
.timeline-left {
    justify-content: flex-end;
    text-align: right;
    margin-right: 40px;
    position: relative;
}
.timeline-right {
    justify-content: flex-start;
    text-align: left;
    margin-left: 40px;
    position: relative;
}
/* Línea horizontal conectora */
.timeline-left::after, .timeline-right::before {
    content: "";
    position: absolute;
    top: 50%;
    width: 40px;
    height: 2px;
    background-color: #d3d3d3;
    z-index: -1;
}
.timeline-left::after {
    right: -40px;
}
.timeline-right::before {
    left: -40px;
}
.timeline-date {
    font-size: 13px;
    color: #444;
    display: flex;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# Contenedor que incluye línea vertical tronco
st.markdown('<div class="timeline-wrapper"><div class="timeline-line"></div>', unsafe_allow_html=True)

alternar = True
for _, row in df_filtrado.iterrows():
    actividad = f"{row['Icono_actividad']} {row['Actividad_realizada'].title()}"
    fecha = row["Etiqueta"]

    if alternar:
        st.markdown(f"""
        <div class="timeline-row">
            <div class="timeline-left"><strong>{actividad}</strong></div>
            <div class="timeline-right timeline-date">{fecha}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="timeline-row">
            <div class="timeline-left timeline-date">{fecha}</div>
            <div class="timeline-right"><strong>{actividad}</strong></div>
        </div>
        """, unsafe_allow_html=True)
    alternar = not alternar

st.markdown('</div>', unsafe_allow_html=True)

# --------- TERCERA GRÁFICA: Infografía tipo línea de tiempo ---------

colores_actividad = {
    "FERTILIZACION": "#FFB347",  # Naranja claro
    "SIEMBRA": "#8BC34A",        # Verde claro
    "BARBECHO": "#FFA07A",       # Salmón
    "RASTREO": "#FFA07A",        # Salmón
    "SURCOS": "#FFA07A",         # Salmón
    "ESCARDA": "#FFA07A",        # Salmón
    "CONTROL_DE_PLAGAS": "#4CAF50", # Verde oscuro
    "CONTROL_DE_MALEZAS": "#4CAF50",# Verde oscuro
    "TRILLA": "#FFD700",          # Dorado
}


# --------- TERCERA GRÁFICA: Tabla Horizontal por Fecha ---------
st.markdown("---")
st.subheader("📅 Linea de Tiempo")

st.markdown("""
<style>
.timeline-header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 12px;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: #555;
}
.timeline-header .arrow {
    font-size: 22px;
    color: #FF6347;
}
.timeline-header .dot {
    width: 14px;
    height: 14px;
    background-color: #FF6347;
    border-radius: 50%;
}
</style>
<div class="timeline-header">
    <div class="arrow">⬅️</div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="arrow">➡️</div>
</div>
""", unsafe_allow_html=True)


st.markdown("---")
st.subheader("📅 Linea de Tiempo")

# Obtener fechas únicas en orden cronológico
fechas_ordenadas = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dropna().sort_values().unique()
fechas_str = [pd.to_datetime(f).strftime("%d %b %Y") for f in fechas_ordenadas]

# Agrupar actividades por fecha
actividades_por_fecha = {
    pd.to_datetime(fecha).strftime("%d %b %Y"): [
        f"{emoji_actividades.get(row['Actividad_realizada'], '🔄')} {row['Actividad_realizada'].replace('_', ' ').title()}"
        for _, row in df_filtrado[df_filtrado["Fecha_en_que_se_realizó_la_actividad"] == fecha].iterrows()
    ]
    for fecha in fechas_ordenadas
}

# Determinar el número máximo de actividades en un día
max_actividades = max(len(act_list) for act_list in actividades_por_fecha.values())

# Construir estructura de tabla
tabla_datos = {}
for fecha in fechas_str:
    actividades = actividades_por_fecha.get(fecha, [])
    actividades += [""] * (max_actividades - len(actividades))  # rellenar con vacíos
    tabla_datos[fecha] = actividades

df_tabla = pd.DataFrame(tabla_datos)

# Estilo
st.markdown("""
<style>
.infografia-tabla {
    overflow-x: auto;
    border-collapse: collapse;
    margin-top: 20px;
    display: block;
    width: 100%;
}
.infografia-tabla table {
    width: auto;
    border-collapse: collapse;
}
.infografia-tabla th {
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    text-align: center;
    border: 1px solid #ccc;
}
.infografia-tabla td {
    background-color: #f9f9f9;
    padding: 8px;
    border: 1px solid #ddd;
    text-align: center;
    font-size: 14px;
    min-width: 120px;
}
</style>
""", unsafe_allow_html=True)

# Renderizar tabla HTML
html = '<div class="infografia-tabla"><table><thead><tr>'
html += ''.join([f"<th>{fecha}</th>" for fecha in df_tabla.columns])
html += '</tr></thead><tbody>'

for i in range(max_actividades):
    html += '<tr>'
    for col in df_tabla.columns:
        html += f"<td>{df_tabla.loc[i, col]}</td>"
    html += '</tr>'

html += '</tbody></table></div>'

st.markdown(html, unsafe_allow_html=True)

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
# Lista de categorías posibles (ajusta con las tuyas si es necesario)
categorias_colores = {
    "FERTILIZANTE": "#66c2a5",
    "HERBICIDA": "#fc8d62",
    "FUNGICIDA": "#8da0cb",
    "INSECTICIDA": "#e78ac3",
    "ADITIVO": "#a6d854",
    "BACTERICIDA": "#ffd92f",
    "MEJORADOR_DE_SUELO": "#FF6347",
    "Otro": "#e5c494"
}

# Gráfico de pastel por categoría del producto
st.subheader("🛍️ Distribución de Insumos por Categoría")

fig_pie = px.pie(
    df_insumos_filtrado,
    names="Categoría_del_producto",
    values="Cantidad",
    title=" ",
     color="Categoría_del_producto",  # ← ¡!
    color_discrete_map=categorias_colores
)

fig_pie.update_traces(
    textinfo='percent+label',
    pull=0.02,  # Separar levemente las secciones
    marker=dict(line=dict(color='#000000', width=1))  # Borde negro
)

fig_pie.update_layout(
    template="plotly_white",  # Estilo limpio
    height=500,
    margin=dict(t=50, b=50, l=50, r=50),  # Márgenes adicionales
    legend=dict(
        bordercolor="gray",
        borderwidth=1
    )
)

st.plotly_chart(fig_pie, use_container_width=True)

# Separador visual para mayor espacio entre gráficas
st.write("<hr>", unsafe_allow_html=True)

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

st.subheader("📊 Cantidad Total de Insumos Aplicados")

# Obtener las unidades únicas
unidades = df_insumos_filtrado["Unidad_ha"].dropna().unique()

# Crear un gráfico para cada unidad
for unidad in unidades:
    df_unidad = df_insumos_filtrado[df_insumos_filtrado["Unidad_ha"] == unidad]

    # Agrupar por producto y categoría
    df_resumen = (
        df_unidad
        .groupby(["Nombre_del_producto", "Categoría_del_producto"], as_index=False)["Cantidad"]
        .sum()
    )
    
    # Crear etiqueta con cantidad y unidad
    df_resumen["Etiqueta"] = df_resumen["Cantidad"].round(2).astype(str) + f" {unidad}"

    # Ordenar por categoría y luego nombre
    df_resumen = df_resumen.sort_values(by=["Categoría_del_producto", "Nombre_del_producto"])

    # Crear gráfico
    fig = px.bar(
        df_resumen,
        x="Nombre_del_producto",
        y="Cantidad",
        color="Categoría_del_producto",
        color_discrete_map=categorias_colores,  # Colores fijos por categoría
        text="Etiqueta",
        labels={
            "Cantidad": f"Cantidad ({unidad})",
            "Nombre_del_producto": "Producto",
            "Categoría_del_producto": "Categoría"
        },
        title=f"Unidad: {unidad}"
    )

    fig.update_layout(
        template="plotly_white",  # Estilo limpio
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=40, r=40, t=60, b=100),  # Márgenes ajustados
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            bordercolor="gray",
            borderwidth=1
        ),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='gray'
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='gray',
            gridcolor='lightgray'
        )
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=1,
        marker_line_color='black'  # Borde en las barras
    )

    # Añadir un separador visual entre los gráficos
    st.plotly_chart(fig, use_container_width=True)
    st.write("<hr>", unsafe_allow_html=True)
