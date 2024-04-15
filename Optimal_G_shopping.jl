using Pkg, DataFrames, CSV , JuMP, Gurobi, DelimitedFiles, Pandas


Whole_food_data = CSV.read("Whole_food_clean.csv", DataFrames.DataFrame)
beans_indices_vec = Int.(vec(readdlm("data/beans_indices.txt", ',')))
milk_indices_vec = Int.(vec(readdlm("data/milk_indices.txt", ',')))
flour_indices_vec = Int.(vec(readdlm("data/flour_indices.txt", ',')))
pb_indices_vec = Int.(vec(readdlm("data/pb_indices.txt", ',')))
pasta_indices_vec = Int.(vec(readdlm("data/pasta_indices.txt", ',')))
oats_indices_vec = Int.(vec(readdlm("data/oats_indices.txt", ',')))
bread_indices_vec = Int.(vec(readdlm("data/bread_indices.txt", ',')))


function Optimal_grocery_shopping(#data_set ,
                        calories_intake::Int, 
                        protein_intake;
                        weight_coefficient=0, 
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
                        number_of_bread = 1)
    data_set=Whole_food_data
    n =size(data_set,1)
    model = Model(Gurobi.Optimizer)
    set_optimizer_attribute(model, "OutputFlag", 0)
    @variable(model, x[i=1:n]>=0,Bin)
    @constraint(model, calories_constraints, calories_intake*0.9<= sum(x[i]* data_set[i, "calories"] for i=1:n) <= calories_intake*1.1)
    @constraint(model, proteins_constraints, protein_intake*0.9<= sum(x[i]* data_set[i, "protein"] for i=1:n) <= protein_intake*1.1)
    @constraint(model, cholesterol_constraints, sum(x[i]* data_set[i, "cholesterol"] for i=1:n) <= cholesterol_constraints)
    @constraint(model, fat_constraints,  sum(x[i]* data_set[i, "total_fat_amount"] for i=1:n) <= fat_constraint)
    @constraint(model, saturated_fat_constraints, sum(x[i]* data_set[i, "saturated_fat"] for i=1:n) <= sat_fat_constraint)
    @constraint(model, fiber_constraints, sum(x[i]* data_set[i, "fiber"] for i=1:n) >= fiber_constraint)
    @constraint(model, sodium_constraints, sum(x[i]* data_set[i, "sodium"] for i=1:n) <= sodium_constraint)
    @constraint(model, potassium_constraints, sum(x[i]* data_set[i, "potassium"] for i=1:n) >= potassium_constraint)
    @constraint(model, iron_constraints, sum(x[i]* data_set[i, "iron"] for i=1:n) >= iron_constraint)
    @constraint(model, beans_constraints, sum(x[beans_indices_vec]) <= number_of_beans)
    @constraint(model, milk_constraints, sum(x[milk_indices_vec]) <= number_of_milk)
    @constraint(model, flour_constraints, sum(x[flour_indices_vec]) <= number_of_flour)
    @constraint(model, peanut_butter_constraints, sum(x[pb_indices_vec]) <= number_of_peanut)
    @constraint(model, pasta_constraints, sum(x[pasta_indices_vec]) <= number_of_pasta)
    @constraint(model, oats_constraints, sum(x[oats_indices_vec]) <= number_of_oats)
    @constraint(model, bread_constraints, sum(x[bread_indices_vec]) <= number_of_bread)

    @objective(model, Min, sum(x[i]*data_set[i, "price"] + weight_coefficient *x[i]*data_set[i, "serving_size"] for i=1:n))
    optimize!(model)
    x_true = JuMP.value.(x)
    indices = findall(x -> x >= 1, x_true )
    println("The cost is ", sum(x_true[i]*data_set[i, "price"] for i=1:n))
    println("The weight is ", sum(x_true[i]*data_set[i, "serving_size"] for i=1:n)/1000, " kg")
    return Pandas.DataFrame(data_set[indices,:])
end