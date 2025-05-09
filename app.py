import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar archivo directamente
df = pd.read_csv("6_2023_2024_a_marzo_2025.csv")
df.columns = df.columns.str.strip()

# Nombres de columnas
col_fecha = "Fecha_en_que_se_realizó_la_actividad"
col_actividad = "Actividad_realizada"
col_id = "ID_Cultivo"

# Validación de columnas
if not all(col in df.columns for col in [col_fecha, col_actividad, col_id]):
    st.error("El archivo no contiene las columnas necesarias.")
else:
    # Convertir fecha con el formato mes/día/año
    df[col_fecha] = pd.to_datetime(df[col_fecha], format="%m/%d/%Y", errors="coerce")
    
    # Verificar si hay fechas no válidas
    st.write("Fechas no válidas:", df[df[col_fecha].isna()])

    # Agregar columnas para Mes y Etiqueta
    df["Mes"] = df[col_fecha].dt.month
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

    # Crear gráfico
    fig = px.scatter(
        df_filtrado,
        x="Nombre_mes",
        y=col_actividad,
        color=col_actividad,
        text="Etiqueta",
        title=f"Actividades realizadas por mes - Cultivo {id_cultivo}",
    )

    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Actividad realizada",
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
