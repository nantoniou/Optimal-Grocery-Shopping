import sys
sys.path.append( '..' )

import streamlit as st
import streamlit.components.v1 as html
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from plots_package import plot_maker
import collections
import string
from  PIL import Image
import requests
from pathlib import Path

from io import BytesIO
import collections
import urllib.request

import nltk 
st.set_page_config(page_title='Optimal Groceries Shopping', page_icon=':shopping_trolley:', layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


data_filepath = '../data/'

sns.set_style("whitegrid", {'axes.grid' : False})

activity_lvl_map = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725,
    "Extra active": 1.9
}


with st.sidebar:
    choose = option_menu("Main Menu", ["About", "Optimal Shopper"],
                         icons=['house',
                                'cart'],
                         menu_icon="list", default_index=0,
                         styles={"container": {"padding": "5!important", 
                                               "background-color": "#fffff"},
                                 "icon": {"color": "#530958", 
                                          "font-size": "25px"}, 
                                 "nav-link": {"font-size": "16px", 
                                              "text-align": "left", 
                                              "margin":"0px", 
                                              "--hover-color": "#4b1919"},
                                 "nav-link-selected": {"background-color": "#321111"},
                                }
                        )
    style1 = """ <style> .font {
                font-size:35px ; font-family: 'Cooper Black'; color: #056dcb;} 
                </style> """
    
if choose == "About":
    col1, col2 = st.columns( [3, 1])
    with col1:     
        st.markdown(style1, unsafe_allow_html=True)
        st.markdown('<p class="font">Build your optimal grocery shopping list!</p>', unsafe_allow_html=True)    
        st.write("App that allows you to build your Whole Foods shopping list, leveraging linear optimization techniques to minimize costs while satisfying specific nutritional, caloric, and taste constraints.")


elif choose == "Optimal Shopper":
    
    
    st.markdown(style1, unsafe_allow_html=True)
    st.markdown('<p class="font">Optimise my groceries!</p>', unsafe_allow_html=True)
    
    with st.form("user_prefs"):
        tab1, tab2 = st.tabs(["Know your Macros?", "What are Macros?"])
        
        with tab1:
            st.write("Insert your weekly macro-nutrient intake & preferences, and we'll create your optimal basket")
            col1, col2, col3 = st.columns( [1, 1, 1])
            with col1:
                protein_val = st.number_input("Protein",1995,2040)
                carbs_val = st.number_input("Carbs",1995,2040)
                #avoid = st.text_input(label='I really don\'t like:')
                #slider_val = st.slider("Form slider")
                #variety_bool = st.checkbox("I want variety!")

            with col2:
                my_year = st.number_input("Year",1995,2040)
                fat_val = st.number_input("Fat",1995,2040)
        with tab2:
            col12, col22, col32 = st.columns( [1, 1, 1])
            with col12:
                age_val = st.number_input("Age",0,100)
                gender = st.radio("Gender", ["Male :man:", "Female :woman:", "Other"], horizontal=True)
                
            with col22:
                weight_val = st.number_input("Weight (kg)",0,300)

            with col32:
                height_val = st.number_input("Height (cm)",0,250)
            activity_lvl = st.radio(
                    "Activity Level",
                    options = [
                        "Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"
                    ],
                    captions = [
                        'limited exercise',
                        'light exercise (< 3 days per week)',
                        'moderate exercise (most days of the week)',
                        'hard exercise (every day)',
                        'strenuous exercise (>=2 times per day)'
                    ],
                    horizontal=True
                )
            

        avoid = st.text_input(label='I really don\'t like:')
        variety_bool = st.checkbox("I want variety!")
        submitted = st.form_submit_button("Submit")
        
        
    if submitted and age_val != 0:
        st.write("Age", age_val, "Weight", weight_val)
        st.write("Multiplier:", activity_lvl_map[activity_lvl])


        if gender == 'Male :man:':
            bmr = 88.362 + (13.397 * weight_val) + (4.799 * height_val) - (5.677 * age_val)
        else:
            bmr = 447.593 + (9.247 * weight_val) + (3.098 * height_val) - (4.330 * age_val)

        tdee = bmr * activity_lvl_map.get(activity_lvl, 1.2)

        protein_cal = tdee * 0.2
        protein_g = protein_cal / 4

        fat_cal = tdee * 0.3
        fat_g = fat_cal / 9

        carbs_cal = tdee - protein_cal - fat_cal
        carbs_g = carbs_cal / 4


        st.write(tdee, protein_g, fat_g, carbs_g)

    elif submitted:
        st.write("Protein", protein_val, "Carbs", carbs_val)

    st.write("Outside the form")



































