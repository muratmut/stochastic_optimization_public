from ortools.linear_solver import pywraplp


def solve_recourse_opt(data_dict, x_dict, sim_demand_dict, substititute_groups):
    total_opt = 0.0
    for group in substititute_groups:
        x_dict_subset = {key: value for key, value in x_dict.items() if key in substititute_groups[group]}
        sim_dict_subset = {key: value for key, value in sim_demand_dict.items() if key in substititute_groups[group]}
        data_dict_subset = {key: value for key, value in data_dict.items() if key in substititute_groups[group]}
        opt_val = solve_single_group_recourse(x_dict_subset, sim_dict_subset, data_dict_subset)
        total_opt = total_opt + opt_val

    return total_opt


def solve_single_group_recourse(x_dict_subset, sim_dict_subset, data_dict_subset):
    solver = pywraplp.Solver.CreateSolver("GLOP")
    from itertools import product
    m = len(x_dict_subset)
    cartesian_product = list(product(x_dict_subset.keys(), x_dict_subset.keys()))
    for tuple in cartesian_product:
        solver.NumVar(0.0, solver.infinity(), 'y_{}_{}'.format(tuple[0], tuple[1]))

    for tuple in cartesian_product:
        i = tuple[0]
        j = tuple[1]
        new_constr = solver.Constraint(-solver.infinity(), x_dict_subset[i])
        var_name = 'y_{}_{}'.format(i, j)
        my_var = solver.LookupVariable(var_name)
        new_constr.SetCoefficient(my_var, 1.0)

    for tuple in cartesian_product:
        j = tuple[0]
        i = tuple[1]
        new_constr = solver.Constraint(-solver.infinity(), sim_dict_subset[i])
        var_name = 'y_{}_{}'.format(i, j)
        my_var = solver.LookupVariable(var_name)
        new_constr.SetCoefficient(my_var, 1.0)

    objective = solver.Objective()
    for tuple in cartesian_product:
        i = tuple[0]
        j = tuple[1]
        var_name = 'y_{}_{}'.format(i, j)
        my_var = solver.LookupVariable(var_name)
        # the cost of substituting j by i is m(i,j) = margin[j] + cogs[j] - cogs[i]
        coeff = data_dict_subset[j]['Margin'] + data_dict_subset[j]['COGS'] - data_dict_subset[i]['COGS']
        objective.SetCoefficient(my_var, coeff)

    objective.SetMaximization()
    solver.EnableOutput()
    status = solver.Solve()
    optimal_value = objective.Value()

    return optimal_value
