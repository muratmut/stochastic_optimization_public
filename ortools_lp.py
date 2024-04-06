from ortools.linear_solver import pywraplp
from distribution import get_pdf, practical_upper_bound
import math


class LP:
    def __init__(self, data_dict, distrubutions_dict, substititute_groups, total_constraint_percentage, tau,
                 group_lower_bound_percentage):
        self._data_dict = data_dict
        self._distributions_dict = distrubutions_dict
        self.substititute_groups = substititute_groups
        self.solver = pywraplp.Solver.CreateSolver("GLOP")
        self.number_of_products = len(self._data_dict.keys())
        self._upper_bounds_dict = self.get_upper_bounds()
        self._tau = tau
        self.group_lower_bound_percentage = group_lower_bound_percentage
        self.total_constraint_percentage = total_constraint_percentage
        self.group_demands = self.get_group_demand()

    def solve_model(self):

        x_vars = []
        for prod_index in range(0, self.number_of_products):
            ub = self._data_dict[prod_index]['Demand'] * (1.0 + self._data_dict[prod_index]['Capacity'])
            if math.isnan(ub):
                ub = self.solver.infinity()
            x_vars.append(self.solver.NumVar(0.0, ub, 'x{}'.format(prod_index)))

        q_vars = [
            self.solver.NumVar(-self.solver.infinity(), self.solver.infinity(), 'q{}'.format(prod_index)) for prod_index
            in range(0, self.number_of_products)]

        demand_vars = [self.solver.NumVar(0.0,
                                          self.solver.infinity(),
                                          'demand{}'.format(prod_index)) for prod_index in
                       range(0, self.number_of_products)]

        slack_vars = [self.solver.NumVar(0.0, 1.0, 's{}'.format(prod_index)) for prod_index in
                      range(0, self.number_of_products)]

        constraints = []

        # constraints for when x_i >= demand_i
        constraints1 = []

        # constraints for when x_i < demand_i
        constraints2 = []

        constraints3 = []  # equality constraints
        constraints4 = []

        for prod_index in range(0, self.number_of_products):
            new_const1 = self.solver.Constraint(-self.solver.infinity(), 0.0)
            new_const1.SetCoefficient(q_vars[prod_index], 1.0)
            new_const1.SetCoefficient(x_vars[prod_index], -self._data_dict[prod_index]['Margin'])
            constraints1.append(new_const1)

            new_const2 = self.solver.Constraint(-self.solver.infinity(), 0.0)
            new_const2.SetCoefficient(q_vars[prod_index], 1.0)
            new_const2.SetCoefficient(demand_vars[prod_index], -1.0 * (
                    self._data_dict[prod_index]['Margin'] + self._data_dict[prod_index]['COGS']))
            new_const2.SetCoefficient(x_vars[prod_index], self._data_dict[prod_index]['COGS'])
            constraints2.append(new_const2)

            new_const3 = self.solver.Constraint(-0.0, 0.0)
            new_const3.SetCoefficient(demand_vars[prod_index], 1.0)
            new_const3.SetCoefficient(slack_vars[prod_index],
                                      -1.0 * (self._data_dict[prod_index]['Demand']) * self._upper_bounds_dict[
                                          self._data_dict[prod_index]['Variance group']])
            constraints3.append(new_const3)

        ub = 500.0 * self._tau
        new_const4 = self.solver.Constraint(0.0, ub)
        for prod_index in range(0, self.number_of_products):
            new_const4.SetCoefficient(slack_vars[prod_index], 1.0)

        total_demand = self.get_total_demand()
        total_x_constraint = self.solver.Constraint(0.0, total_demand * (1.0 + self.total_constraint_percentage))
        for prod_index in range(0, self.number_of_products):
            total_x_constraint.SetCoefficient(x_vars[prod_index], 1.0)

        # set lower bound for total group demands
        for key, value in self.substititute_groups.items():
            group_lb = self.group_demands[key] * self.group_lower_bound_percentage
            if value.size > 1:
                new_const5 = self.solver.Constraint(group_lb, self.solver.infinity())
                for i in value:
                    my_var = self.solver.LookupVariable('x{}'.format(i))
                    new_const5.SetCoefficient(my_var, 1.0)

        objective = self.solver.Objective()
        for prod_index in range(0, self.number_of_products):
            objective.SetCoefficient(q_vars[prod_index], 1.0)
        objective.SetMaximization()
        self.solver.EnableOutput()
        status = self.solver.Solve()
        x_dict = {i: x_vars[i].solution_value() for i in range(0, self.number_of_products)}
        return x_dict, objective.Value()

    def get_upper_bounds(self):
        upper_bound_for_dist_dict = {}
        for key, value in self._distributions_dict.items():
            upper_bound_for_dist_dict[key] = practical_upper_bound(value['c'], value['d'], loc=value['loc'],
                                                                   scale=value['scale'])

        return upper_bound_for_dist_dict

    def get_total_demand(self):
        demand = 0.0
        for key, value in self._data_dict.items():
            demand = value['Demand'] + demand
        return demand

    def get_group_demand(self):

        group_demands_dict = {}
        for key, value in self.substititute_groups.items():

            demand = 0.0
            for index in value:
                demand = demand + self._data_dict[index]['Demand']
            group_demands_dict[key] = demand

        return group_demands_dict
