import streamlit as st
from config import page_title, business_units, linear_space_elasticities

def introduction(i):
    if i == 1:
        st.write('A retailer wants to reallocate the macro-space of a store in order to *maximize its sales*')
        st.write(f'The store has 800 m² available. The store sells products from {len(business_units)} different Business Units, each with *distinct number of items, margins, dimensions, and space elasticity functions*')
        st.write('Since the assortment is defined by a different team, it is required that every BU has enough space to display at *least one front of its SKUs*')
    
    if i == 2:
        st.write("For now, consider that each BU has a linear elasticity function and that we don't have to consider the requirement of having enough space to display at least one front of its SKUs")
        st.write('Consider the following elasticity functions:"')

        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')