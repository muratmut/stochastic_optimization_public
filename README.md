# stochastic_opt


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

