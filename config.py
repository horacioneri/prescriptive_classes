print("Loaded config.py")

import pandas as pd
import numpy as np

available_space = 800
page_title = ['Introduction', 'Basics of optimization', 'Constraints', 'Objective function', 'Non-linear problem']
business_units = ['Beverages', 'Snacks', 'Hygiene', 'Fresh products', 'Other']
linear_space_elasticities = [5, 1, 2, 4, 0.5]
min_space = [100, 100, 100, 100, 100]

linearization_brackets = [0, 100, 300, available_space]

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
})

optimized_answers = [[0,0,0,0,0],[800,0,0,0,0],[400,100,100,100,100],[300,133,133,133,101],[300,133,133,133,101]]
max_y_axis = max(linear_space_elasticities)*available_space + 1

