from data_process import read_excel_with_tabs
from ortools_lp import LP
from distribution import simulate_demands
import numpy as np
from recourse_opt import solve_recourse_opt
from plot import plot_array


def main():
    import json

    # Path to your JSON file
    json_file_path = 'config.json'

    # Read the JSON file
    with open(json_file_path, 'r') as f:
        config = json.load(f)

    # Process the data
    for run_id, entry_data in config.items():
        param1 = entry_data['total_constraint_percentage']
        param2 = entry_data['tau']
        param3 = entry_data['group_lower_bound_percentage']

        print(
            f"Run: {run_id}, total_constraint_percentage: {param1}, tau: {param2}, group_lower_bound_percentage: {param3}")

        call_main_optimization_and_qc(run_id, param1, param2, param3)


def call_main_optimization_and_qc(run_id, total_constraint_percentage, tau, group_lower_bound_percentage):
    file_path = "Input_SUA.xlsx"
    data_dict, substititute_groups, distrubutions_dict = read_excel_with_tabs(file_path)
    lp_model = LP(data_dict, distrubutions_dict, substititute_groups, total_constraint_percentage, tau,
                  group_lower_bound_percentage)
    x_dict, obj_value = lp_model.solve_model()

    num_sims = 60
    sim_dict = {}
    for i in range(0, num_sims):
        sim_demand_dict = simulate_demands(data_dict, distrubutions_dict)
        new_opt = solve_recourse_opt(data_dict, x_dict, sim_demand_dict, substititute_groups)
        sim_dict[i] = new_opt

    dist = np.array(list(sim_dict.values()))

    plot_array(dist, run_id)


if __name__ == '__main__':
    main()
