import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo CSV directamente
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")
df.columns = df.columns.str.strip()

# Nombres de las columnas
col_fecha = "Fecha_en_que_se_realizó_la_actividad"
col_actividad = "Actividad_realizada"
col_id = "ID_Cultivo"

# Validación de las columnas
if not all(col in df.columns for col in [col_fecha, col_actividad, col_id]):
    st.error("El archivo no contiene las columnas necesarias.")
else:
    # Convertir la columna de fecha al formato adecuado (mes/día/año)
    df[col_fecha] = pd.to_datetime(df[col_fecha], format="%m/%d/%Y", errors="coerce")

    # Verificar si hay fechas no válidas
    st.write("Fechas no válidas:", df[df[col_fecha].isna()])

    # Agregar columnas para Mes, Día y Etiqueta
    df["Mes"] = df[col_fecha].dt.month
    df["Día"] = df[col_fecha].dt.day
    df["Nombre_mes"] = df[col_fecha].dt.strftime("%B")
    df["Etiqueta"] = df[col_actividad] + " - " + df[col_fecha].dt.strftime("%d %b %Y")

    # Selección por ID de Cultivo
    id_cultivo = st.selectbox("Selecciona un ID de Cultivo", sorted(df[col_id].dropna().unique()))
    df_filtrado = df[df[col_id] == id_cultivo].copy()

    # Ordenar meses (en español)
    meses_ordenados = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    df_filtrado["Nombre_mes"] = df_filtrado[col_fecha].dt.strftime("%B").str.lower()
    df_filtrado["Nombre_mes"] = pd.Categorical(df_filtrado["Nombre_mes"], categories=meses_ordenados, ordered=True)

    # Crear gráfico de dispersión (scatter plot)
    fig = px.scatter(
        df_filtrado,
        x=col_fecha,  # Usamos la fecha exacta en el eje X
        y=col_actividad,  # Las actividades en el eje Y
        color=col_actividad,  # Colores por actividad
        text="Etiqueta",  # Mostrar la etiqueta (nombre actividad + fecha)
        title=f"Actividades realizadas por mes - Cultivo {id_cultivo}",
    )

    # Ajustar el formato del gráfico
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Actividad realizada",
        showlegend=False,
        height=600,
        xaxis=dict(
            tickmode="array",
            tickvals=pd.date_range(df_filtrado[col_fecha].min(), df_filtrado[col_fecha].max(), freq="5D"),  # Muestra cada 5 días
            ticktext=[f"{x.strftime('%d %b')}" for x in pd.date_range(df_filtrado[col_fecha].min(), df_filtrado[col_fecha].max(), freq="5D")]
        )
    )

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)
