import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("datos_actividades.csv")

# Verificar columnas
st.write("Columnas disponibles:", df.columns.tolist())

# Asegurarse que la fecha está bien nombrada
col_fecha = "Fecha_en_que_se_realizaron_las_actividades"  # Cambia si tiene otro nombre
col_actividad = "Actividad_realizada"
col_id = "ID_Cultivo"

# Convertir a datetime
df[col_fecha] = pd.to_datetime(df[col_fecha])

# Extraer mes (formato nombre de mes)
df["Mes"] = df[col_fecha].dt.strftime("%B")
df["Mes_Num"] = df[col_fecha].dt.month  # Para ordenar correctamente

# Crear etiqueta combinada: actividad + fecha
df["Etiqueta"] = df[col_actividad] + " - " + df[col_fecha].dt.strftime("%d-%b")

# Selector de cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df[col_id].unique())

# Filtrar DataFrame
df_filtrado = df[df[col_id] == id_cultivo_seleccionado]

# Ordenar por mes
df_filtrado = df_filtrado.sort_values("Mes_Num")

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="Mes",
    y=[col_actividad],
    text="Etiqueta",
    title=f"Actividades por mes - Cultivo {id_cultivo_seleccionado}",
    labels={"Mes": "Mes", col_actividad: "Actividad"},
    color_discrete_sequence=["#1f77b4"]
)

fig.update_traces(mode="markers+text", textposition="top center")
fig.update_layout(
    yaxis=dict(showticklabels=False),  # Oculta etiquetas repetidas
    margin=dict(l=40, r=40, t=60, b=40),
    xaxis_categoryorder="array",
    xaxis_categoryarray=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
)

st.plotly_chart(fig, use_container_width=True)
