import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="🌳 Línea de Tiempo de Actividades", layout="wide")
st.title("🌱 Actividades por Parcela / ID_Cultivo")

# Cargar archivo
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

# Filtro
id_cultivo_seleccionado = st.selectbox("✅ Selecciona un ID de Cultivo", df['ID_Cultivo'].dropna().unique())
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado].copy()
df_filtrado = df_filtrado.sort_values("Fecha_en_que_se_realizó_la_actividad").reset_index(drop=True)
df_filtrado["Emoji"] = df_filtrado["Actividad_realizada"].map(emoji_actividades).fillna("🔄")
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %B %Y")

# ----------- CSS personalizado bonito ----------
st.markdown("""
<style>
/* Estructura general */
.timeline-container {
    position: relative;
    margin: 50px auto;
    width: 90%;
}
.timeline-trunk {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 5px;
    background: linear-gradient(to bottom, #FF6347, #ffa07a);
    box-shadow: 0 0 10px rgba(255,99,71,0.3);
    z-index: 0;
}

/* Fila de evento */
.timeline-event {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 50px 0;
    position: relative;
    z-index: 1;
    animation: fadeIn 0.8s ease-in;
}

/* Tarjetas de actividad y fecha */
.timeline-box {
    background: linear-gradient(135deg, #fff7f0, #fefefe);
    padding: 16px 20px;
    border-radius: 16px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    font-size: 16px;
    max-width: 240px;
    transition: transform 0.3s ease;
}
.timeline-box:hover {
    transform: scale(1.02);
}
.timeline-actividad {
    font-weight: bold;
    font-size: 18px;
}
.timeline-fecha {
    font-style: italic;
    color: #666;
    font-size: 14px;
}

/* Línea conectora */
.timeline-connector {
    flex: 1;
    height: 2px;
    background-color: #ccc;
    margin: 0 10px;
    z-index: 0;
}

/* Animación */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ----------- Timeline HTML dinámico bonito ----------
st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
st.markdown('<div class="timeline-trunk"></div>', unsafe_allow_html=True)

for i, row in df_filtrado.iterrows():
    actividad = f"<span class='timeline-actividad'>{row['Emoji']} {row['Actividad_realizada']}</span>"
    fecha = f"<span class='timeline-fecha'>{row['Etiqueta']}</span>"
    lado = "left" if i % 2 == 0 else "right"

    if lado == "left":
        html = f"""
        <div class="timeline-event">
            <div class="timeline-box">{actividad}</div>
            <div class="timeline-connector"></div>
            <div class="timeline-box">{fecha}</div>
        </div>
        """
    else:
        html = f"""
        <div class="timeline-event">
            <div class="timeline-box">{fecha}</div>
            <div class="timeline-connector"></div>
            <div class="timeline-box">{actividad}</div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
