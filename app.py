import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from io import BytesIO
from fpdf import FPDF
from PIL import Image

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube el archivo CSV de actividades", type=["csv"])

if uploaded_file:
    # Leer datos
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Limpia espacios

    # Nombres de columnas
    col_fecha = "Fecha_en_que_se_realizó_la_actividad"
    col_actividad = "Actividad_realizada"
    col_id = "ID_Cultivo"

    # Verifica que las columnas existan
    if not all(col in df.columns for col in [col_fecha, col_actividad, col_id]):
        st.error("El archivo no contiene las columnas necesarias.")
    else:
        # Convertir fechas
        df[col_fecha] = pd.to_datetime(df[col_fecha])

        # Selector de cultivo
        id_cultivo = st.selectbox("Selecciona un ID de Cultivo", sorted(df[col_id].unique()))
        df_filtrado = df[df[col_id] == id_cultivo].copy()

        # Etiqueta personalizada
        df_filtrado["Etiqueta"] = df_filtrado[col_actividad] + " - " + df_filtrado[col_fecha].dt.strftime("%d %b %Y")
        df_filtrado["Fecha_fin"] = df_filtrado[col_fecha] + pd.Timedelta(days=1)

        # Crear línea de tiempo (Gantt)
        fig = px.timeline(
            df_filtrado,
            x_start=col_fecha,
            x_end="Fecha_fin",
            y=col_actividad,
            color=col_actividad,
            hover_name="Etiqueta",
            title=f"Línea de tiempo - Cultivo {id_cultivo}"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(showlegend=False)

        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)

        # Convertir a imagen
        img_bytes = pio.to_image(fig, format="png", width=1000, height=600)

        # Crear PDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        img = Image.open(BytesIO(img_bytes))
        img_path = "/tmp/timeline.png"
        img.save(img_path)
        pdf.image(img_path, x=10, y=20, w=270)

        # Descargar PDF
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Descargar línea de tiempo como PDF",
            data=pdf_buffer,
            file_name=f"Linea_de_tiempo_{id_cultivo}.pdf",
            mime="application/pdf"
        )
else:
    st.info("Por favor, sube un archivo CSV para continuar.")
