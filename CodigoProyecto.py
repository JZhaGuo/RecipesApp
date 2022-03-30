import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

########################
# Configurar la página #
########################

st.set_page_config(layout="wide", page_title="CookClick", 
                   initial_sidebar_state="expanded", )  
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

###################
# Leer data frame #
###################

st.title('Recetas')

# df = pd.read_csv("/Users/jinhaozhangguo/Desktop/Proyi/RecetasReducido.csv")
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

receta = pd.read_cs("RecetasReducido.csv")

selection = aggrid_interactive_table(df=receta)

if selection:
    st.write("You selected:")
    st.json(selection["selected_rows"])

#################
# Barra lateral #
#################

st.sidebar.text("")
st.sidebar.text("")
provincia = st.sidebar.selectbox("Seleccione una categoría", ("Lleva más preparación", "Platos rápidos", "Postres",
                                                            "(Próximamente)")) 




