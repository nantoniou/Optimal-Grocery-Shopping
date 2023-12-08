import sys
sys.path.append( '..' )

from optimise_basket import optimal_grocery_shopping

import streamlit as st
import streamlit.components.v1 as html
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Optimal Groceries Shopping', page_icon=':shopping_trolley:', layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


data_filepath = '../data/'
days = 14


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
    col1, col2 = st.columns( [3, 2])
    with col1:     
        st.markdown(style1, unsafe_allow_html=True)
        st.markdown('<p class="font">Build your optimal grocery shopping list!</p>', unsafe_allow_html=True)    
        st.markdown("Welcome to our app!")
        st.markdown("This app that allows you to build your Whole Foods shopping list, leveraging linear optimization techniques to minimize costs while satisfying specific nutritional, caloric, and taste constraints.")


elif choose == "Optimal Shopper":
    
    
    st.markdown(style1, unsafe_allow_html=True)
    st.markdown('<p class="font">Optimise my groceries!</p>', unsafe_allow_html=True)
    
    with st.form("user_prefs"):
        tab1, tab2 = st.tabs(["Know your Macros?", "What are Macros?"])
        
        with tab1:
            st.write("Insert your daily macro-nutrient intake & preferences, and we'll create your optimal basket")
            col11, col21, col31 = st.columns( [1, 1, 1])
            with col11:
                tdee = st.number_input("Calories",1000,5000,2000) * days
                carbs_g = st.number_input("Carbs",100,500,250) * days
                chol_g = st.number_input("Cholesterol (mg)",0,500,300) * days
                
            with col21:
                protein_g = st.number_input("Protein",30,400,100) * days
                fat_g = st.number_input("Fat",20,100,60) * days
                sodium_mg = st.number_input("Sodium (mg)",300,3000,1500) * days
                
            with col31:
                satfat_g = st.number_input("Saturated Fat",10,50,20) * days
                fiber_g = st.number_input("Fiber",5,100,25) * days
                potas_mg = st.number_input("Potassium (mg)",1000,8000,4000) * days
                
            col12, col22 = st.columns( [1, 2])
            with col12:
                iron_mg = st.number_input("Iron (mg)",0,50,15) * days

                
            
        with tab2:
            col13, col23, col33 = st.columns( [1, 1, 1])
            with col13:
                age_val = st.number_input("Age",0,100,0)
                gender = st.radio("Gender", ["Male :man:", "Female :woman:", "Other"], horizontal=True)
                
            with col23:
                weight_val = st.number_input("Weight (kg)",0,300,80)

            with col33:
                height_val = st.number_input("Height (cm)",0,250,180)
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
                    ], horizontal=True
            )
            
        col14, col24 = st.columns( [1, 1])
        with col14:
            weight = st.slider('How much do you care about the weight of the basket?', 0, 100, 25) * 0.00005
        with col24:
            prefs = st.multiselect(
                    'Which food products do you like?',
                    ['Beans', 'Milk', 'Peanuts', 'Pasta', 'Flour', 'Oats', 'Bread']
            )
            if not prefs: prefs=[]
            
        submitted = st.form_submit_button("Submit")
        
        
    if submitted and age_val != 0:


        if gender == 'Male :man:':
            bmr = 88.362 + (13.397 * weight_val) + (4.799 * height_val) - (5.677 * age_val)
        else:
            bmr = 447.593 + (9.247 * weight_val) + (3.098 * height_val) - (4.330 * age_val)

        tdee = bmr * activity_lvl_map.get(activity_lvl, 1.2)
        tdee *= days

        protein_cal = tdee * 0.2
        protein_g = protein_cal / 4

        fat_cal = tdee * 0.3
        fat_g = fat_cal / 9
        
        satfat_cal = tdee * 0.06
        satfat_g = satfat_cal / 9

        carbs_cal = tdee - protein_cal - fat_cal
        carbs_g = carbs_cal / 4
        
        fiber_g = tdee * 0.014
        
        chol_g = 200 * days

        sodium_mg = tdee
        potas_mg = 4000 * days
        iron_mg = 15 * days

        
        
    if submitted:
        #st.write(tdee, protein_g, weight, chol_g, fat_g, satfat_g, fiber_g, sodium_mg, potas_mg, iron_mg)
        
        cost, df = optimal_grocery_shopping(
            calories_intake = tdee,
            protein_intake = protein_g,
            weight_coefficient = weight,
            cholesterol_constraint = chol_g,
            fat_constraint = fat_g,
            sat_fat_constraint = satfat_g,
            fiber_constraint = fiber_g,
            sodium_constraint = sodium_mg,
            potassium_constraint = potas_mg,
            iron_constraint = iron_mg,
            number_of_beans = int("Beans" in prefs),
            number_of_milk = int("Milk" in prefs),
            number_of_flour = int("Flour" in prefs),
            number_of_peanut = int("Peanuts" in prefs),
            number_of_pasta = int("Pasta" in prefs),
            number_of_oats = int("Oats" in prefs),
            number_of_bread = int("Bread" in prefs)
        )
        
        if cost is None: st.write("### Cannot find a basket for the provided information!")
        else:
            cost = str(round(cost,2))
            st.text("")
            st.markdown(f"#### The cost of your optimised shopping basket is *${cost}*!")
            st.divider()
            st.write("#### Your selected products:")
            st.dataframe(df)#, hide_index=True)
            st.text("")

            col15, col25, col35 = st.columns( [1, 3, 1])
            with col25:
                brand_counts = df.product_brand.value_counts()
                plt.style.use('ggplot')
                fig, ax = plt.subplots(figsize=(7,4))
                brand_counts.plot(kind='barh', legend = False, ax=ax, grid=False)
                ax.set_xlabel('Products in basket')
                ax.tick_params(axis='x', colors='lightgray')
                ax.tick_params(axis='y', colors='lightgray')
                ax.xaxis.label.set_color('lightgray')
                #ax.set_ylabel('Brand')
                st.pyplot(fig, transparent=True)
















