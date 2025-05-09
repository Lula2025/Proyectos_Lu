import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("Hoja 6 2023-2024 a marzo 2025.csv")  # Reemplaza con tu archivo

# Asegurarse que las fechas estén en formato datetime
df['Fecha_en_que_se_realizaron_las_actividades'] = pd.to_datetime(df['Fecha_en_que_se_realizaron_las_actividades'])

# Selección interactiva del ID de cultivo
id_cultivo_seleccionado = st.selectbox("Selecciona un ID de Cultivo", df['ID_Cultivo'].unique())

# Filtrar por el ID seleccionado
df_filtrado = df[df['ID_Cultivo'] == id_cultivo_seleccionado]

# Crear la línea de tiempo
fig = px.scatter(df_filtrado, 
                 x="Fecha_en_que_se_realizaron_las_actividades", 
                 y=["Actividad_realizada"], 
                 text="Actividad_realizada",
                 title=f"Actividades realizadas en el cultivo {id_cultivo_seleccionado}",
                 labels={"Fecha_en_que_se_realizaron_las_actividades": "Fecha"},
                 color_discrete_sequence=["#2ca02c"])

# Mostrar etiquetas
fig.update_traces(mode="markers+text", textposition="top center")

# Mejorar el diseño
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Actividad",
    yaxis=dict(showticklabels=False),  # Para no repetir etiquetas
    margin=dict(l=40, r=40, t=80, b=40)
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app.run (debug=True, port=8051)
