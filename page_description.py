import streamlit as st
from config import page_title, business_units, available_space, df_bu

def introduction(i):
    #Overall introduction
    if i == 0:
        st.write('A retailer wants to reallocate the macro-space of a store in order to *maximize its sales*')
        st.write(f'The store has {available_space} m² available. The store sells products from {len(business_units)} different Business Units, each with *distinct number of items, margins, dimensions, and space elasticity functions*')
        st.write('Since the assortment is defined by a different team, it is required that every BU has enough space to display at *least one front of its SKUs*')

        st.header('Problem framing', divider='rainbow')
        decision_variables = st.text_input("What are the decision variables of this problem?")
        objetive_function = st.text_input("What is the objective function of this problem?")
        constraints = st.text_input("What are the constraints of this problem?")

        st.header('Answers', divider='rainbow')
        with st.expander('**Click to see answers**'):
            st.markdown('Problem framing')
            st.text_area(label="What are the decision variables of this problem?", value="The decision variables of this problem are the areas allocated to each business unit", height=100)
            st.text_area(label="What is the objective function of this problem?", value="The objective function of this problem is to maximize sales", height=100)
            st.text_area(label="What are the constraints of this problem?", value="The constraints of this problem are: \n- the maximum available space of the store;\n- the need to reserve enough space for each business unit to present at least one unit of each SKU in assortment", height=100)
    
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

    #Linearization exercise
    if i == 3:
        st.write("The space elasticity function, typically does not follow a linear function, it follows a curve similiar to a logarithmic function")
        st.write('Consider the following elasticity (daily sales / space allocated) for different brackets of area allocated [0-100], [100 - 300], [300-800]:')

        st.dataframe(df_bu[['Business Unit', 
            'Linear Space Elasticity (€/m²) - Area in [0,100]',
            'Linear Space Elasticity (€/m²) - Area in [100,300]',
            'Linear Space Elasticity (€/m²) - Area in [300,800]',
            'Minimum Space (m²)']])

        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')

    #Non-linear exercise
    if i >= 4:
        st.write("Now, consider it follows a logarithmic curve instead of linear functions")
        st.write('Consider the following elasticity:')
        
        st.dataframe(df_bu[['Business Unit', 'Log Space Elasticity (€/m²)', 'Minimum Space (m²)']])
        
        st.write('Submit the space you want to allocate to each BU in the left sidebar and analyze your answers below')