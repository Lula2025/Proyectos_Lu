import streamlit as st
import pandas as pd
import plotly.express as px

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube el archivo CSV de actividades", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Nombres de columnas
    col_fecha = "Fecha_en_que_se_realizó_la_actividad"
    col_actividad = "Actividad_realizada"
    col_id = "ID_Cultivo"

    # Validación de columnas
    if not all(col in df.columns for col in [col_fecha, col_actividad, col_id]):
        st.error("El archivo no contiene las columnas necesarias.")
    else:
        # Convertir fecha
        df[col_fecha] = pd.to_datetime(df[col_fecha])
        df["Mes"] = df[col_fecha].dt.month
        df["Nombre_mes"] = df[col_fecha].dt.strftime("%B")
        df["Etiqueta"] = df[col_actividad] + " - " + df[col_fecha].dt.strftime("%d %b %Y")

        # Seleccionar cultivo
        id_cultivo = st.selectbox("Selecciona un ID de Cultivo", sorted(df[col_id].unique()))
        df_filtrado = df[df[col_id] == id_cultivo].copy()

        # Ordenar meses manualmente (en español)
        meses_ordenados = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        df_filtrado["Nombre_mes"] = df_filtrado[col_fecha].dt.strftime("%B").str.lower()
        df_filtrado["Nombre_mes"] = pd.Categorical(df_filtrado["Nombre_mes"], categories=meses_ordenados, ordered=True)

        # Crear gráfico con etiquetas visibles
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
else:
    st.info("Por favor, sube un archivo CSV para continuar.")
