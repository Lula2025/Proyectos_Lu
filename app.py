    color_discrete_sequence=["#FF6347"],  # Color más vibrante
    hover_data={
        "Actividad_realizada": False,  # No mostrar actividad al pasar el ratón
        "Fecha_en_que_se_realizó_la_actividad": True
    },
)

# Agregar iconos de emojis como texto en las etiquetas
df_filtrado["Etiqueta"] = df_filtrado["Fecha_en_que_se_realizó_la_actividad"].dt.strftime("%d %b %Y")
fig.update_traces(
    text=df_filtrado["Etiqueta"],  # Mostrar solo la fecha completa
    textposition="top center",
    textfont_size=10,  # Tamaño de fuente pequeño para las fechas
    mode="markers+text",
    marker=dict(size=12, symbol="circle", color="#FF6347")  # Puntos más grandes y coloridos
)

# Mejorar la presentación del gráfico
fig.update_layout(
    xaxis_title="Mes y Año",
    yaxis_title="Actividad",
    xaxis=dict(
        tickformat="%b %Y",  # Mostrar solo mes y año
        tickangle=45,  # Rotar las etiquetas de los meses
        dtick="M1"  # Mostrar un tick cada mes
    ),
    margin=dict(l=40, r=40, t=80, b=80),  # Márgenes más amplios
    height=600,  # Altura más grande
    width=1200,  # Ancho más grande para una mejor visualización
    title_font_size=24,  # Aumentar el tamaño del título
    font=dict(size=12, family="Arial, sans-serif"),  # Usar una fuente más legible
    plot_bgcolor="#F9F9F9"  # Fondo claro para el gráfico
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Espacio entre el gráfico y otros elementos
st.markdown("<br>", unsafe_allow_html=True)

