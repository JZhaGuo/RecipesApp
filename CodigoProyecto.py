import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import smtplib
from email.mime.text import MIMEText
from PIL import Image

########################
# Configurar la página #
########################

img = Image.open("logoweb.png")
st.set_page_config(layout="wide",page_title="Cooklick", page_icon=img,
                   initial_sidebar_state="expanded", )  # configuramos la página
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
image = Image.open('logoweb.png')
st.image(image, width=600)

###################
# Leer data frame #
###################

st.title('Recetas')

# df = pd.read_csv("/Users/jinhaozhangguo/Desktop/Proyi/RecetasReducido2.csv")
# st.dataframe(df)

#########################
# Seleccionar cada fila #
#########################

def aggrid_interactive_table(df: pd.DataFrame):

    options = GridOptionsBuilder.from_dataframe(
        receta, enableRowGroup=True, enableValue=True, enablePivot=True)

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="dark",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True)

    return selection

receta = pd.read_csv("/Users/jinhaozhangguo/Desktop/Proyi/RecetasReducido2.csv")

selection = aggrid_interactive_table(df=receta)

if selection:
    st.write("You selected:")
    st.json(selection["selected_rows"])

#################
# Barra lateral #
#################

st.sidebar.text("")
st.sidebar.text("")
recetas = st.sidebar.selectbox("Seleccione una categoría", ("Lleva más preparación", "Platos rápidos", "Postres",
                                                            "(Próximamente)"))


def enviar(email, recetas):
    """
    Suscribe a los emails en el newsletter
    """
    text_type = "plain"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(usuario, contra)
    texto = f"Le damos la bienvenida al newsletter de CookCLick sobre {recetas}. Cada vez que actualicemos la página recibirá un email con un resumen.\n\nUn saludo,\n\nel equipo de CookClick."
    msg = MIMEText(texto, text_type, 'utf-8')
    msg['Subject'] = "Bienvenido"
    msg['From'] = usuario
    msg['To'] = email
    server.sendmail(usuario, usuario, f"Subject:Suscripcion {recetas} {email}")
    server.send_message(msg)
    server.quit()

email = st.sidebar.text_input(f"Reciba un email una vez a la semana con información relevante para {recetas}.",
                              'ejemplo@mail.com')
a = st.sidebar.button("Suscribirme")
usuario = "Usuario EMAIL"
contra = "Contraseña EMAIL"

if a:
    email1 = email.split("@")
    if email == "ejemplo@mail.com":
        st.sidebar.text("Escriba su email")
        a = False
    elif len(email1) == 2:
        email2 = email1[1].split(".")
        if len(email2) >= 2:
            enviar(email, provincia)
            st.sidebar.text("¡Ya se ha suscrito!")
        else:
            a = False
            st.sidebar.text("Email incorrecto, inténtelo de nuevo.")
    else:
        a = False
        st.sidebar.text("Email incorrecto, inténtelo de nuevo.")









