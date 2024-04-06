from scipy.stats import burr12


def get_pdf(c, d, loc=0.0, scale=1.0):
    rv = burr12(c, d, scale=scale)
    return rv


def simulate_value(c, d, loc=0.0, scale=1.0):
    rv = burr12(c, d, scale=scale)
    val = rv.rvs() + loc
    # val = rv.rvs(random_state=rng) + loc
    return val


def practical_upper_bound(c, d, loc=0.0, scale=1.0):
    rv = burr12(c, d, scale=scale)
    max = rv.ppf(0.999999)
    return max + loc


def simulate_demands(data_dict, distrubutions_dict):
    sim_dict = {}
    for key, val in data_dict.items():
        c = distrubutions_dict[val['Variance group']]['c']
        d = distrubutions_dict[val['Variance group']]['d']
        loc = distrubutions_dict[val['Variance group']]['loc']
        scale = distrubutions_dict[val['Variance group']]['scale']
        # rng = np.random.default_rng(seed=key)
        sim_val = simulate_value(c, d, loc, scale)
        sim_dict[key] = sim_val * val['Demand']

    return sim_dict
