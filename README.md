# Optimal Grocery Shopping

## Problem Summary
The project entails the development of an optimal dietary plan that leverages linear optimization techniques to minimize costs while satisfying specific nutritional, caloric, and taste constraints. We are using data from the Whole Foods website. The core objective is to construct a cost-effective dietary regimen that is practically acceptable, i.e. could be used realistically by a graduate student to reduce its cost but without compromising on dietary needs or the taste of the food. This balancing act will be achieved through the formulation of a linear optimization model that intricately aligns the cost minimization goal with the stipulated dietary requirements and taste preferences, presenting a solution that is both economically and nutritionally optimized.

## Dataset
To tackle this challenge, we have collected a Dataset scraped from [Whole Food market](https://www.wholefoodsmarket.com/product/pete-and-gerrys-organic-large-eggs-12-eggs-b00f0znk8e) which contains data for most grocery products and includes for each of them: the price, Macro- and Micro- nutrient data.

## Methods
Mostly Linear Optimization Methods to model the objective and the linear constraints such as the nutritional requirements. Furthermore, leveraging MIO methods to add constraints to make the solution more interesting from a cooking point of view. Lastly, adding Mixed Integer Constraints to make sure that we don't suggest products that need others to complement them, such as flour without yeast or eggs.

