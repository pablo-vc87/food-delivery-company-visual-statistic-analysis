import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Lista con los nombres de los DataFrames del proyecto
def filas_dup(lista_df, nombres):
    """
    Función que recibe una lista de dataframes y una lista de nombres para cada dataframe
    Arroja la cantidad de filas duplicadas de cada Dataframe
    Ejemplo: 
    Lista de nombres de los dataframes:
    lista_df= [
    df_insta_orders,
    df_products, 
    df_order_products,
    df_aisles, 
    df_departments
    ]
    Lista de nombres para mostrar en pantalla
    nombres = [
    "insta_orders",
    "products",
    "order_products",
    "aisles",
    "departments"
    ]
    filas_dup(lista_df, nombres)
    """
    for nombre, df in zip(nombres, lista_df):
        print(f"{nombre}: {df.duplicated().sum()} filas duplicadas")
    print("-"*50)
#====================================================================
def mostrar_nan(df, columna=None, num_filas=10):
    """
    Imprime la cantidad de valores Nan por columna del DataFrame
    Muestra las filas completas que contienen valores NaN
    
    Parámetros:
    df: DataFrame a analizar
    columna: nombre de columna específica (opcional)
    num_filas: cuántas filas mostrar (por defecto 10)
    """
    name = str(df)
    lista= df.columns
    print(f"\nEl dataframe tiene {df.duplicated().sum()} filas repetidas")
    print('-'*50)
    #Para una sola columna:
    if columna:  
        filas_nan = df[df[columna].isna()] #crea DF de puros valores NaN
        print(f"\nFilas con NaN en '{columna}': {len(filas_nan)} encontradas") # imprime nombre de la columna y cantidad de NaN
        if not filas_nan.empty: # Si el DF filas_nan tiene algo adentro
                print("\nPrimeras", min(num_filas, len(filas_nan)), "filas completas conteniendo NaN para: ", "'",columna,"'")
                print(filas_nan.head(num_filas))
                print('-'*50) #separador visual
    else:        
        for column in lista:
            filas_nan =df[df[column].isna()]
            print(f"\nFilas con NaN en '{column}': {len(filas_nan)} encontradas") #hace lo mismo que el del if anterior para cada columna de un dF
            if not filas_nan.empty:
                print("\nPrimeras", min(num_filas, len(filas_nan)), "filas completas conteniendo NaN para: ", "'",column,"'")
                print(filas_nan.head(num_filas))
                print('-'*50) #separador visual
    return filas_nan
#=========================================================
def mostrar_dupli(df, columna=None, num_filas=10):
    """
    Imprime la cantidad de filas duplicadas del DataFrame
    Muestra las filas completas que están duplicadas
    
    Parámetros:
    df: DataFrame a analizar
    columna: nombre de columna específica para buscar duplicados (opcional)
    num_filas: cuántas filas mostrar (por defecto 10)
    """
    
    print(f"\nEl dataframe tiene {df.duplicated().sum()} filas completamente duplicadas")
    print('-'*50)
    if columna:
        # Para una sola columna:  
        filas_duplicadas = df[df.duplicated(subset=[columna], keep=False)]
        print(f"\nFilas con valores duplicados en '{columna}': {len(filas_duplicadas)} encontradas")
        print('-'*50)
        if not filas_duplicadas.empty:
            print(f"\nPrimeras {min(num_filas, len(filas_duplicadas))} filas completas con duplicados en: '{columna}'")
            print(filas_duplicadas.head(num_filas))
            print('-'*50)
    else:        
        # Para duplicados completos (todas las columnas)
        filas_duplicadas = df[df.duplicated(keep=False)]
        print(f"\nFilas completamente duplicadas: {len(filas_duplicadas)} encontradas")
        print('-'*50)
        if not filas_duplicadas.empty:
            print(f"\nPrimeras {min(num_filas, len(filas_duplicadas))} filas completamente duplicadas:")
            print(filas_duplicadas.sort_values('user_id').head(num_filas))
            print('-'*50)
    return filas_duplicadas
