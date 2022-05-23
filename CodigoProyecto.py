import streamlit as st
import pandas as pd
import numpy as np
import ast


def busquedaReceta(ingredientes):
    busqueda = []
    for index, row in df.iterrows():
        ingReceta = row['Ingredientes normalizados']
        mostrar = True
        for ing in ingredientes:
            if ing not in ingReceta:
                mostrar = False
        if mostrar == True:
            busqueda.append(index)
    return busqueda


########################
# Configurar la página #
########################

#img = Image.open("logoweb.png")
st.set_page_config(layout="wide",page_title="Cooklick",
                   initial_sidebar_state="expanded" )  # configuramos la página
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
#image = Image.open('logoweb.png')
#st.image(image, width=600)

###################
# Web #
###################

df = pd.read_csv("./data.csv", delimiter=',') #.sample(n=4000, random_state=1)

st.title('Recetas')

options = st.multiselect('Seleccione los ingredientes', ['sugar', 'brown sugar', 'milk', 'nuts', 'butter', 'beef', 'chicken breasts', 'sour cream', 
                       'cream cheese', 'salt', 'pepper', 'chicken', 'shredded cheese', 'powdered sugar', 'baking potatoes', 
                       'cheddar cheese', 'bacon', 'egg', 'eggs', 'buttermilk', 'flour', 'tomatoes', 'water', 'onions', 
                       'oil', 'pineapple', 'lemons', 'boiling water', 'barbacue sauce', 'ground beef', 'shredded lettuce', 
                       'tomato', 'onion', 'lemon juice', 'strawberries', 'cleaned strawberries', 'mayonnaise', 'vinegar', 
                       'bananas', 'strawberry', 'garlic', 'vainilla', 'olive oil', 'baking powder', 'cinnamon', 'margarine', 
                       'celery', 'baking soda', 'parsley', 'vegetable oil', 'oil', 'carrots', 'soy sauce', 'black pepper', 
                       'mustard', 'chicken broth', 'honey', 'oregano', 'unsalte butter', 'mushrooms'])


cool1, cool2 = st.columns(2)
    
    
filtros = cool1.selectbox('Ordenar por: ', ['Menor tiempo', 'Mayor tiempo', 'Menor número de pasos', 'Mayor número de pasos', 'Menor número de ingredientes', 'Mayor número de ingredientes'])

dif = cool2.selectbox('Elige dificultad: ',['Intermedia', 'Difícil', 'Fácil'])


if len(options) != 0:
    with st.spinner("Buscando las recetas"):
        df = df.iloc[busquedaReceta(options)]

    df = df.loc[df["Dificultad"]==dif]
       
    if filtros == 'Menor tiempo':
        df.sort_values(by=['Tiempo estimado'], ascending=True, inplace=True)
    elif filtros == 'Mayor tiempo':
        df.sort_values(by=['Tiempo estimado'], ascending=False, inplace=True)
    elif filtros == 'Menor número de pasos':
        df.sort_values(by=['Numero de pasos'], ascending=True, inplace=True)
    elif filtros == 'Mayor número de pasos':
        df.sort_values(by=['Numero de pasos'], ascending=False, inplace=True)
    elif filtros == 'Menor número de ingredientes':
        df.sort_values(by=['Lista Ingredientes'], ascending=True, inplace=True)
    elif filtros == 'Mayor número de ingredientes':
        df.sort_values(by=['Lista Ingredientes'], ascending=False, inplace=True)
        
    col1, col2 = st.columns(2)
    ing = df.iloc[:25]
    res = col1.radio("Elige una receta para obtener más detalles", ing["title"])
    ing2 = ing.loc[ing["title"] == res]
    lista_ing= ", ".join(ast.literal_eval(list(ing2['ingredients2'])[0]))
    lista_pasos= " ".join(ast.literal_eval(list(ing2['directions2'])[0]))
    col2.markdown(f"#### Ingredientes\n{lista_ing}\n#### Instrucciones\n{lista_pasos}\n")
