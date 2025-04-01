
# **Optimal Grocery Shopping 🛒**  
_An intelligent shopping optimization tool, allowing you to lower your costs (and the weight of your basket), automate your product selection, while adhering to your nutritional needs._  

## **Overview**
This project helps users **optimize their grocery shopping** by finding the most cost-effective way to buy items on WholeFoods, ensuring a light-weight basket for easy transportation, while adhering to nutrational constraints. Those constraints include calories, macro-nutrients (e.g. protein), and micro-nutrients (e.g. iron). It is carried out with binary integer linear programming optimisation modeling, through a module that is called by the Streamlit app.

The module contains two working versions of the optimisation module, a Python and a Julia one. Streamlit uses the latter, since there are no significant runtime differences, but Julia and its wrapper are kept for future developments.


## **Dataset**
To tackle this challenge, we have collected a Dataset scraped from [Whole Food market](https://www.wholefoodsmarket.com/) which contains data for most grocery products and includes for each of them: the price, weight, Macro- and Micro- nutrient data.


## **Modeling**
### Variables
Let $x_i$ be a binary variable, where $i = 1, \dots, 4925$, indicating the selection of the specific product.

### Objective Function

```math
min\sum_{i=1}^{n} x_i \cdot \text{price}_i + \lambda \cdot \sum_{i=1}^{n} x_i \cdot \text{weight}_i
```
### Macro-nutrient Constraints

```math
\text{calories\_intake} \cdot 0.9 \leq \sum_{i=1}^{n} x_i \cdot \text{calories}_i \leq \text{calories\_intake} \cdot 1.2
```
```math
\text{protein\_intake} \leq \sum_{i=1}^{n} x_i \cdot \text{protein}_i \leq \text{protein\_intake} \cdot 1.3
```
```math
\sum_{i=1}^{n} x_i \cdot \text{total\_fat\_amount}_i \leq \text{fat\_constraint}
```

### Preferences Constraints

```math
\sum_{\text{beans\_indices\_vec}} x_i \leq \text{max\_number\_of\_beans}
```
```math
\sum_{\text{milk\_indices\_vec}} x_i \leq \text{max\_number\_of\_milk}
```
```math
\sum_{\text{flour\_indices\_vec}} x_i \leq \text{max\_number\_of\_flour}
```
```math
\sum_{\text{pb\_indices\_vec}} x_i \leq \text{max\_number\_of\_peanut}
```
```math
\sum_{\text{pasta\_indices\_vec}} x_i \leq \text{max\_number\_of\_pasta}
```
```math
\sum_{\text{oats\_indices\_vec}} x_i \leq \text{max\_number\_of\_oats}
```
```math
\sum_{\text{bread\_indices\_vec}} x_i \leq \text{max\_number\_of\_bread}
```

### Micro-nutrient Constraints

```math
\sum_{i=1}^{n} x_i \cdot \text{cholesterol}_i \leq \text{cholesterol\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{total\_fat\_amount}_i \leq \text{fat\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{saturated\_fat}_i \leq \text{sat\_fat\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{fiber}_i \geq \text{fiber\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{sodium}_i \leq \text{sodium\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{potassium}_i \geq \text{potassium\_constraint}
```
```math
\sum_{i=1}^{n} x_i \cdot \text{iron}_i \geq \text{iron\_constraint}
```


## **⚡ Features**  
✔️ Automatically finds the cheapest and lightest product selection, using MILP optimisation<br>
✔️ Handles different nutritional requirements and food preferences<br>
✔️ Allows the automatic selection of the nutritional requirements<br>
✔️ Easy-to-use interface with Streamlit

## **Streamlit Example Usage**  

![Demo](media/demo.gif)

## **🛠️ Installation & Setup**  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/nantoniou/optimal-grocery-shopping.git
   cd optimal-grocery-shopping
   ```
2. **Create & activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```


## **🚀 Future Improvements**  
🔹 Create an LLM agent, by wrapping the engine with an LLM.

## **Contributing**  
Contributions are welcome! Feel free to open an issue or submit a pull request.  

## **🐝 License**  
This project is licensed under the GNU General Public License v3.0.  
