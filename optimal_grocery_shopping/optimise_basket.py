import pandas as pd
import numpy as np
import csv
from gurobipy import Model, GRB, quicksum

# Load data
whole_food_data = pd.read_csv("Whole_food_clean.csv")

# Load index data from files
def load_indices(file_path):
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        return [int(row[0]) for row in reader]

beans_indices_vec = load_indices("data/beans_indices.txt")
milk_indices_vec = load_indices("data/milk_indices.txt")
flour_indices_vec = load_indices("data/flour_indices.txt")
pb_indices_vec = load_indices("data/pb_indices.txt")
pasta_indices_vec = load_indices("data/pasta_indices.txt")
oats_indices_vec = load_indices("data/oats_indices.txt")
bread_indices_vec = load_indices("data/bread_indices.txt")

def optimal_grocery_shopping(calories_intake, protein_intake, weight_coefficient=0, 
                             cholesterol_constraint=4200, fat_constraint=840, 
                             sat_fat_constraint=70, fiber_constraint=490, 
                             sodium_constraint=14000, potassium_constraint=65800, 
                             iron_constraint=252, number_of_beans=1, number_of_milk=1, 
                             number_of_flour=0, number_of_peanut=1, number_of_pasta=1, 
                             number_of_oats=1, number_of_bread=1):
    data_set = whole_food_data
    n = data_set.shape[0]

    # Create a new model
    model = Model('OptimalGroceryShopping')

    # Variables
    x = model.addVars(n, vtype=GRB.BINARY, name="x")

    # Objective
    model.setObjective(quicksum(x[i] * data_set.loc[i, "price"] + weight_coefficient * x[i] * data_set.loc[i, "serving_size"] for i in range(n)), GRB.MINIMIZE)

    # Nutritional Constraints
    model.addConstr(quicksum(x[i] * data_set.loc[i, "calories"] for i in range(n)) >= calories_intake * 0.9, "CaloriesMin")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "calories"] for i in range(n)) <= calories_intake * 1.2, "CaloriesMax")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "protein"] for i in range(n)) >= protein_intake * 1, "ProteinMin")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "protein"] for i in range(n)) <= protein_intake * 1.3, "ProteinMax")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "cholesterol"] for i in range(n)) <= cholesterol_constraint, "Cholesterol")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "total_fat_amount"] for i in range(n)) <= fat_constraint, "Fat")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "saturated_fat"] for i in range(n)) <= sat_fat_constraint, "SaturatedFat")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "fiber"] for i in range(n)) >= fiber_constraint, "FiberMin")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "sodium"] for i in range(n)) <= sodium_constraint, "Sodium")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "potassium"] for i in range(n)) >= potassium_constraint, "PotassiumMin")
    model.addConstr(quicksum(x[i] * data_set.loc[i, "iron"] for i in range(n)) >= iron_constraint, "IronMin")

    # Category Constraints
    model.addConstr(quicksum(x[i] for i in beans_indices_vec) <= number_of_beans, "Beans")
    model.addConstr(quicksum(x[i] for i in milk_indices_vec) <= number_of_milk, "Milk")
    model.addConstr(quicksum(x[i] for i in flour_indices_vec) <= number_of_flour, "Flour")
    model.addConstr(quicksum(x[i] for i in pb_indices_vec) <= number_of_peanut, "PeanutButter")
    model.addConstr(quicksum(x[i] for i in pasta_indices_vec) <= number_of_pasta, "Pasta")
    model.addConstr(quicksum(x[i] for i in oats_indices_vec) <= number_of_oats, "Oats")
    model.addConstr(quicksum(x[i] for i in bread_indices_vec) <= number_of_bread, "Bread")

    # Solve
    model.optimize()

    if model.status == GRB.OPTIMAL:
        solution = model.getAttr('x', x)
        selected_items = [i for i in solution if solution[i] > 0.5]
        cost_ = model.objVal - sum([weight_coefficient * solution[i] * data_set.loc[i, "serving_size"] for i in range(n)])
        return (model.objVal, data_set.iloc[selected_items, :])

    else:
        print("No optimal solution found")
        return (None, None)

