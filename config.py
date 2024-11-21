import pandas as pd
import numpy as np

available_space = 800
page_title = ['Introduction', 'Basics of optimization', 'Constraints', 'Objective function', 'Non-linear problem']
business_units = ['Beverages', 'Snacks', 'Hygiene', 'Fresh products', 'Other']
linear_space_elasticities = [5, 1, 2, 4, 0.5]
min_space = [70, 70, 70, 70, 70]

linearization_brackets = [0, 100, 300, 800]

log_space_elasticities = [round((300 * x) / np.log(301),2) for x in linear_space_elasticities] 

bracket_space_elasticity = np.zeros((len(linearization_brackets)-1, len(log_space_elasticities)))
bracket_space_intercept = np.zeros((len(linearization_brackets)-1, len(log_space_elasticities)))

for i in range(len(log_space_elasticities)):
    for j in range(1, len(linearization_brackets)):
        bracket_space_elasticity[j-1][i] = (log_space_elasticities[i] * np.log(linearization_brackets[j]+1) - log_space_elasticities[i] * np.log(linearization_brackets[j-1]+1))/(linearization_brackets[j] - linearization_brackets[j-1])
        bracket_space_intercept[j-1][i] = (log_space_elasticities[i] * np.log(linearization_brackets[j]+1)) - bracket_space_elasticity[j-1][i]*linearization_brackets[j]

df_bu = pd.DataFrame({
    'Business Unit': business_units,
    'Linear Space Elasticity (€/m²)': linear_space_elasticities,
    'Minimum Space (m²)': min_space,
    'Log Space Elasticity (€/m²)': log_space_elasticities,
    'Linear Space Elasticity (€/m²) - Area in [0,100]': bracket_space_elasticity[0],
    'Linear Space Elasticity (€/m²) - Area in [100,300]': bracket_space_elasticity[1],
    'Linear Space Elasticity (€/m²) - Area in [300,800]': bracket_space_elasticity[2],
    'Linear Space Intercept - Area in [0,100]': bracket_space_intercept[0],
    'Linear Space Intercept - Area in [100,300]': bracket_space_intercept[1],
    'Linear Space Intercept - Area in [300,800]': bracket_space_intercept[2],
})

optimized_answers = [[0,0,0,0,0],[800,0,0,0,0],[520,70,70,70,70],[300,100,100,200,100],[300.37,70.0,119.54,240.09,70.0]]
max_y_axis = max(linear_space_elasticities)*available_space + 1

#df_bu.to_excel('dataframe.xlsx')

#js = ''' <a target="_self" href="#title"></a>'''