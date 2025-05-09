import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("datos_actividades.csv")

# Verificar y limpiar columnas
df.columns = df.columns.str.strip()  # Elimina espacios al inicio/final

# Asegura nombres correctos
col_fecha = "Fecha_en_que_se_realizaron_las_actividades"
col_actividad = "Actividad_realizada"
col_id = "ID_Cultivo"

# Convertir fechas
df[col_fecha] = pd.to_datetime(df[col_fecha])

# Selector de cultivo
id_cultivo = st.selectbox("Selecciona un ID de Cultivo", sorted(df[col_id].unique()))
df_filtrado = df[df[col_id] == id_cultivo].copy()

# Ordenar actividades por fecha
df_filtrado = df_filtrado.sort_values(by=col_fecha)

# Crear una columna con texto personalizado para mostrar
df_filtrado["Etiqueta"] = df_filtrado[col_actividad] + " - " + df_filtrado[col_fecha].dt.strftime("%d %b %Y")

# Para gráfico de Gantt: crear fecha fin (igual a inicio, porque es puntual)
df_filtrado["Fecha_fin"] = df_filtrado[col_fecha] + pd.Timedelta(days=1)

# Crear gráfico tipo timeline
fig = px.timeline(
    df_filtrado,
    x_start=col_fecha,
    x_end="Fecha_fin",
    y=col_actividad,
    color=col_actividad,
    hover_name="Etiqueta",
    title=f"Línea de tiempo de actividades - Cultivo {id_cultivo}"
)

# Mejorar visual
fig.update_yaxes(autorange="reversed")  # Actividades en orden descendente
fig.update_layout(
    margin=dict(l=40, r=40, t=80, b=40),
    xaxis_title="Fecha",
    yaxis_title="Actividad",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
