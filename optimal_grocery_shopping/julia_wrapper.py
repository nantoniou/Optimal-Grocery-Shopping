from julia import Julia
import pandas as pd

class JuliaWrapper:
    
    def __init__(self):
        jl = Julia(runtime="C:\\Users\\Nick\\AppData\\Local\\Programs\\Julia-1.9.2\\bin\\julia.exe")
        jl.eval('include("Optimal_G_shopping.jl")')
        
        self.jl = jl

    def run_opt(self,
        calories_intake, 
        protein_intake,
        weight_coefficient=0.1, 
        cholesterol_constraints=4200, 
        fat_constraint = 840, 
        sat_fat_constraint=70, 
        fiber_constraint= 490, 
        sodium_constraint = 14000, 
        potassium_constraint= 65800, 
        iron_constraint = 252, 
        number_of_beans = 1,
        number_of_milk = 1, 
        number_of_flour = 0, 
        number_of_peanut = 1, 
        number_of_pasta=1, 
        number_of_oats = 1, 
        number_of_bread = 1
    ):

        jl = Julia(runtime="C:\\Users\\Nick\\AppData\\Local\\Programs\\Julia-1.9.2\\bin\\julia.exe")
        jl.eval('include("Optimal_G_shopping.jl")')
        res_df = jl.eval('Optimal_grocery_shopping(' +
                    str(calories_intake) + ',' +
                    str(protein_intake) + ';' +
                    'weight_coefficient = ' + str(weight_coefficient) + ',' +
                    'cholesterol_constraints = ' + str(cholesterol_constraints) + ',' +
                    'fat_constraint = ' + str(fat_constraint) + ',' +
                    'sat_fat_constraint = ' + str(sat_fat_constraint) + ',' +
                    'fiber_constraint = ' + str(fiber_constraint) + ',' +
                    'sodium_constraint = ' + str(sodium_constraint) + ',' +
                    'potassium_constraint = ' + str(potassium_constraint) + ',' +
                    'iron_constraint = ' + str(iron_constraint) + ',' +
                    'number_of_beans = ' + str(number_of_beans) + ',' +
                    'number_of_milk = ' + str(number_of_milk) + ',' +
                    'number_of_flour = ' + str(number_of_flour) + ',' +
                    'number_of_peanut = ' + str(number_of_peanut) + ',' +
                    'number_of_pasta = ' + str(number_of_pasta) + ',' +
                    'number_of_oats = ' + str(number_of_oats) + ',' +
                    'number_of_bread = ' + str(number_of_bread) + ')'
        )
        return res_df
    

