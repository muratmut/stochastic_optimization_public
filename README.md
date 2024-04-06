# stochastic_opt



# Stochastic Optimization for Profit Maximization

Welcome to our project repository! This project focuses on solving a stochastic optimization problem aimed at maximizing profit margins within a production plan. Our primary objective is to determine the optimal surplus quantity to be added to the demand forecast for each product. 

## Problem Description
For each product, we have access to data including:
- Estimated demand and its variability distribution.
- Margin per unit, calculated as net price minus cost.
- Cost of goods sold (COGS), representing production costs.
- Capacity constraints, defining the maximum percentage of demand that can be added as surplus.
- Substitutability group numbers indicating product substitutability.

**The details of the problem description is in ProblemStatement.pdf**



## Goal
The goal is to develop an efficient solution that identifies the ideal surplus quantity for each product, considering all the aforementioned factors. By doing so, we aim to enhance profit margins while adhering to capacity limitations and product substitutability constraints.

## Repository Contents
- **Documentation**: Detailed explanation of the problem statement, methodology, and solution approach.
- **Codebase**: Implementation of the stochastic optimization algorithm tailored to this problem.
- **Results**: Output and analysis of optimized surplus quantities for various scenarios.




### Installation

```bash
pip install -r requirements.txt

```

### Run
python start.py



### Code flow

1. The main function in start.py reads the config file and for each hyperparameter combination, it solves the main stochastic optimization as an LP, which finds amount $x_i$ to be produced for product $i$. 

   1a. The config file has 3 parameters, total_constraint_percentage, tau(controlling the slack variables $s_i's$ determining how close the demand variables in the optimization are to the historical demand ) , and group_lower_bound_percentage. group_lower_bound_percentage is a lower bound percentage that controls the total product produced within a specific group. 

2. Once the main optimization is solved, $x_i's$ are available. To evaluate the performance of those variables, demands are simulated. For each simulated value of demands, a 2nd stage optimization is solved. This stage takes advantage of the ability of substitution within a product group. 

3. The resulting objective from the 2nd stage is recorded and simulation of demands is repeated k times. A histogram distribution of the objectives is produced.

   

The details of the models are in the pdf file.

