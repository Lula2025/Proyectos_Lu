import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Línea de Tiempo de Actividades")

archivo = st.file_uploader("Sube el archivo CSV", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)

    df['Fecha_en_que_se_realizaron_las_actividades'] = pd.to_datetime(
        df['Fecha_en_que_se_realizaron_las_actividades'])

    id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

    df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado]

    fig = px.scatter(df_filtrado, 
                     x="Fecha_en_que_se_realizaron_las_actividades", 
                     y=["Actividad_realizada"], 
                     text="Actividad_realizada",
                     title=f"Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
                     labels={"Fecha_en_que_se_realizaron_las_actividades": "Fecha"},
                     color_discrete_sequence=["#2ca02c"])

    fig.update_traces(mode="markers+text", textposition="top center")

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Actividad",
        yaxis=dict(showticklabels=False),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

