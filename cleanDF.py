# Data base web --> https://clickhouse.com/docs/en/getting-started/example-datasets/recipes/

import pandas as pd
import math

df = pd.read_csv('full_dataset_limpio.csv', delimiter=',')

def get_pasos(directions):
    """
    Recibe una receta (str)
    Hace una lista con los pasos de la receta
    Devuelve el número de pasos, es decir, la longitud de la lista
    """
    lista = directions.split("., ") # Lista de los pasos de las instrucciones 
    return len(lista)

def get_tiempo(directions):
    """
    Recibe una receta (str)
    Hace una lista con los pasos de la receta
    Devuelve el número de pasos, es decir, la longitud de la lista
    """
    cadena = directions.split() # Lista de las cadenas de caracteres que hay en las instrucciones 
    num = 0
    tiempo = 10
    for i, n in enumerate(cadena):
        try:
            if 'minute' in n:
                num = int(cadena[i-1])
                if num > 0:
                    tiempo += num
                else:
                    tiempo += abs(num)
                    
            elif 'hour' in n:
                num = int(cadena[i-1])
                if num > 0:
                    tiempo += num*60
                else:
                    tiempo += abs(num)*60
            else:
                pass
        except:
            pass
    return tiempo

def get_ingredientes(ingredientes):
    """
    Recibe una receta (str)
    Hace una lista con los pasos de la receta
    Devuelve el número de pasos, es decir, la longitud de la lista
    """
    lista = ingredientes.split(", ") # Lista de los pasos de las instrucciones 
    return len(lista)

df.loc[df.isnull().any(axis='columns')] # Localiza columnas con al menos un valores nulos
df.dropna(axis='rows', how='any', inplace=True) # Elimina las columnas que les falta un valor


df['Número de pasos'] = df['directions'].map(get_pasos)
df['Tiempo estimado'] = df['directions'].map(get_tiempo)
df['Número de ingredientes'] = df['NER'].map(get_ingredientes)


def dificultad(row):
    """
    PARÁMETROS: 
   
   Tiempo estimado      Nºingredientes      Ing comunes         Número pasos
   < 20 -> 1            < 6 -> 1            > 60% -> 1          1 - 3 -> 1
   20 - 60 -> 2         6 - 10 -> 2         20>% - 60% -> 2     4 - 7 -> 2
   > 60 -> 3            > 10 -> 3           < 20% -> 3          > 7 -> 3
   """

    contador = 0
    tiempo = row['Tiempo estimado']
    if tiempo < 20:
        contador += 1
    elif tiempo >= 20 and tiempo <= 60:
        contador += 2
    else:
        contador += 3
    ingredientes = row['Número de ingredientes']
    if ingredientes < 6:
        contador += 1
    elif ingredientes >= 6 and ingredientes <= 10:
        contador += 2
    else:
        contador += 3
    listaIng = row['NER'].split(", ")
    numComunes = 0
    for ingrediente in listaIng:
        if ingrediente in ingredientesComunes:
            numComunes += 1
    if ingredientes == 0:
        ingredientes += 1
    porcentaje = (numComunes * 100)// ingredientes
    if porcentaje > 60:
        contador += 1
    elif porcentaje >= 20 and porcentaje <= 60:
        contador += 2
    else:
        contador += 3
    numPasos = row['Número de pasos']
    if numPasos == 1 or numPasos == 2 or numPasos == 3:
        contador += 1
    elif numPasos == 4 or numPasos == 5 or numPasos == 6:
        contador += 2
    else:
        contador += 3
    if contador == 4 or contador == 5 or contador == 6:
        return 'Fácil'
    elif contador == 7 or contador == 8 or contador == 9:
        return 'Intermedia'
    else:
        return 'Difícil'
    
df['Dificultad'] = df.apply(dificultad, axis='columns')


def normalizar(ner):
    norm = ner.split(', ')
    for index, ingrediente in enumerate(norm):
        if len(ingrediente.split()) == 1:
            if ingrediente[-1] == "s" and ingrediente[-2] != "e":
                norm[index] = ingrediente[:-1]
            elif ingrediente[-1] == "s" and ingrediente[-2] == "e":
                norm[index] = ingrediente[:-2]
    return norm
    
df['Ingredientes normalizados'] = df['NER'].map(normalizar)


ingredientesComunes = ['sugar', 'brown sugar', 'milk', 'nuts', 'butter', 'beef', 'chicken breasts', 'sour cream', 
                       'cream cheese', 'salt', 'pepper', 'chicken', 'shredded cheese', 'powdered sugar', 'baking potatoes', 
                       'cheddar cheese', 'bacon', 'egg', 'eggs', 'buttermilk', 'flour', 'tomatoes', 'water', 'onions', 
                       'oil', 'pineapple', 'lemons', 'boiling water', 'barbacue sauce', 'ground beef', 'shredded lettuce', 
                       'tomato', 'onion', 'lemon juice', 'strawberries', 'cleaned strawberries', 'mayonnaise', 'vinegar', 
                       'bananas', 'strawberry', 'garlic', 'vainilla', 'olive oil', 'baking powder', 'cinnamon', 'margarine', 
                       'celery', 'baking soda', 'parsley', 'vegetable oil', 'oil', 'carrots', 'soy sauce', 'black pepper', 
                       'mustard', 'chicken broth', 'honey', 'oregano', 'unsalte butter', 'mushrooms']
                       
                       
                    
ing_norm = {}
for index,row in df.iterrows():
    ner = row['NER']
    for i in ner.split(', '): 
        if len(i.split()) == 1:
            if i.lower() not in ing_norm:
                ing_norm[i.lower()] = 1
            else:
                ing_norm[i.lower()] += 1
        else:
            pass

for index,row in df.iterrows():
    ner = row['NER']
    for j in ner.split(', '):
        if len(j.split()) == 1:
            pass
        else:
            for m in j.split():
                if m.lower() in ing_norm:
                    ing_norm[m.lower()] += 1
            
print(ing_norm)                      
        
    
from itertools import combinations
dic = {}
for i in range(len(df)): 
    ing = df.iloc[i]['Ingredientes normalizados']
    comb = combinations(ing, 2)
    for n in list(comb):
        if n in dic:
            dic[n] += 1
        else:
            dic[n] = 1
            
            
claves = []
valores = []
for valor in dic.values():
    valores.append(valor)
for clave in dic.keys():
    claves.append(clave)
elementos = {"combincaciones":claves,"veces":valores}
combDf = pd.DataFrame(elementos)
            
    
    
