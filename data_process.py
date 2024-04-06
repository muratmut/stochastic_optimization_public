import pandas as pd


def read_excel_with_tabs(file_path):
    distrubutions_pd = pd.read_excel(file_path, sheet_name='Demand Variance')
    distrubutions_pd['Demand Var Group'] = distrubutions_pd['Demand Var Group'].astype(int)
    distrubutions_pd = distrubutions_pd.rename(columns={'Demand Var Group': 'Variance group'})
    distrubutions_pd['loc'] = distrubutions_pd['loc'].astype(float)
    distrubutions_pd['scale'] = distrubutions_pd['scale'].astype(float)

    data_pd = pd.read_excel(file_path, sheet_name='Demand', skiprows=1)

    data_pd = data_pd.T.reset_index(names=None)
    data_pd.columns = data_pd.iloc[0]
    data_pd = data_pd.drop(0)
    data_pd.reset_index(inplace=True)
    data_pd = data_pd.drop(columns=['index'], axis=1)
    data_pd['Demand'] = data_pd['Demand'].astype(float)
    data_pd['Substitutability group'] = data_pd['Substitutability group'].astype(int)
    data_pd['Variance group'] = data_pd['Variance group'].astype(int)
    data_dict = data_pd.to_dict(orient='index')

    substititute_groups = data_pd.groupby(by=['Substitutability group']).groups
    distrubutions_dict = distrubutions_pd.to_dict(orient='index')

    return data_dict, substititute_groups, distrubutions_dict

    print('Data reading done')
