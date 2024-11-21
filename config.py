print("Loaded config.py")

import pandas as pd

available_space = 800
page_title = ['Introduction', 'Basis of optimization', 'Constraints 1', 'Constraints 2', 'Objective function 1', 'Objective function 2']
business_units = ['Beverages', 'Snacks', 'Hygiene', 'Fresh products', 'Other']
linear_space_elasticities = [5, 1, 2, 4, 0.5]
min_space = [100, 100, 100, 100, 100]
df_bu = pd.DataFrame({
    'Business Unit': business_units,
    'Linear Space Elasticity (€/m²)': linear_space_elasticities,
    'Minimum Space (m²)': min_space
})