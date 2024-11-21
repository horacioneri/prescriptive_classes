import streamlit as st
from config import page_title, business_units, available_space, df_bu

def introduction(i):
    #Overall introduction
    if i == 0:
        st.write('A retailer wants to reallocate the macro-space of a store in order to *maximize its sales*')
        st.write(f'The store has {available_space} m² available. The store sells products from {len(business_units)} different Business Units, each with *distinct number of items, margins, dimensions, and space elasticity functions*')
        st.write('Since the assortment is defined by a different team, it is required that every BU has enough space to display at *least one front of its SKUs*')
    
    #Linear exercise with a single constraint
    if i == 1:
        st.write("For now, consider that each BU has a linear elasticity function and that we don't have to consider the requirement of having enough space to display at least one front of its SKUs")
        st.write('Consider the following elasticity functions (daily sales / space allocated):')
        
        st.dataframe(df_bu[['Business Unit', 'Linear Space Elasticity (€/m²)']])
        
        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')

    #Linear exercise with an additional constraint
    if i == 2:
        st.write("Now, consider the minimum space required for each BU to present one example of each SKU in the assortment")
        st.write('Consider the following minimum spaces:')
        
        st.dataframe(df_bu[['Business Unit', 'Linear Space Elasticity (€/m²)', 'Minimum Space (m²)']])
        
        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')

    #Non-linear exercise
    if i >= 3:
        st.write("The space elasticity function, typically does not follow a linear function, it follows a curve similiar to a logarithmic function")
        st.write('Consider the following elasticity:')
        
        st.dataframe(df_bu[['Business Unit', 'Log Space Elasticity (€/m²)', 'Minimum Space (m²)']])
        
        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')