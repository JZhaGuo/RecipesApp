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

df = pd.read_csv("data.csv", delimiter=',') #.sample(n=4000, random_state=1)

st.title('Find what to cook')

options = st.multiselect('Select one or more ingredients:', ['sugar', 'brown sugar', 'milk', 'nuts', 'butter', 'beef', 'chicken breasts', 'sour cream', 
                       'cream cheese', 'salt', 'pepper', 'chicken', 'shredded cheese', 'powdered sugar', 'baking potatoes', 
                       'cheddar cheese', 'bacon', 'egg', 'eggs', 'buttermilk', 'flour', 'tomatoes', 'water', 'onions', 
                       'oil', 'pineapple', 'lemons', 'boiling water', 'barbacue sauce', 'ground beef', 'shredded lettuce', 
                       'tomato', 'onion', 'lemon juice', 'strawberries', 'cleaned strawberries', 'mayonnaise', 'vinegar', 
                       'bananas', 'strawberry', 'garlic', 'vainilla', 'olive oil', 'baking powder', 'cinnamon', 'margarine', 
                       'celery', 'baking soda', 'parsley', 'vegetable oil', 'oil', 'carrots', 'soy sauce', 'black pepper', 
                       'mustard', 'chicken broth', 'honey', 'oregano', 'unsalte butter', 'mushrooms'])


cool1, cool2 = st.columns(2)
    
    
filtros = cool1.selectbox('Select one filter: ', ['Less preparation time', 'More preparation time', 'Less steps', 'More steps', 'Less number of ingredients', 'More number of ingredients'])

dif = cool2.selectbox('Select hardness: ',['Easy', 'Medium', 'Hard'])

dificultad = {"Medium":'Intermedia', "Hard":'Difícil', "Easy":'Fácil'}

if len(options) != 0:
    with st.spinner("Searching recipes"):
        df = df.iloc[busquedaReceta(options)]

    df = df.loc[df["Dificultad"]==dificultad[dif]]

    if filtros == 'Less preparation time':
        df.sort_values(by=['Tiempo estimado'], ascending=True, inplace=True)
    elif filtros == 'More preparation time':
        df.sort_values(by=['Tiempo estimado'], ascending=False, inplace=True)
    elif filtros == 'Less steps':
        df.sort_values(by=['Número de pasos'], ascending=True, inplace=True)
    elif filtros == 'More steps':
        df.sort_values(by=['Número de pasos'], ascending=False, inplace=True)
    elif filtros == 'Less number of ingredients':
        df.sort_values(by=['Número de ingredientes'], ascending=True, inplace=True)
    elif filtros == 'More number of ingredients':
        df.sort_values(by=['Número de ingredientes'], ascending=False, inplace=True)
        
    col1, col2 = st.columns(2)
    ing = df.iloc[:25]
    res = col1.radio("Select a recipe for more information", ing["title"])
    ing2 = ing.loc[ing["title"] == res]
    if True:
        lista_ing= ", ".join(ast.literal_eval(list(ing2['ingredients2'])[0]))
        lista_pasos= " ".join(ast.literal_eval(list(ing2['directions2'])[0]))
        col2.markdown(f"#### Ingredients\n{lista_ing}\n#### Instructions\n{lista_pasos}\n\n##### Time: {int(ing2['Tiempo estimado'])} minutes")


    
    
    
    
    
