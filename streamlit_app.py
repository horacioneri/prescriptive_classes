import streamlit as st
import pandas
import plotly.graph_objects as go
import numpy as np
from config import page_title, business_units, available_space, linear_space_elasticities, min_space, log_space_elasticities, optimized_answers, max_y_axis
from page_description import introduction

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.answers = [0, 0, 0, 0, 0]

st.set_page_config(page_title='Understanding optimization', page_icon='')

# Navigation function with forced rerun
def change_page(delta):
    st.session_state.page = max(0, min(len(page_title) - 1, st.session_state.page + delta))
    st.rerun()  # Force immediate rerun to reflect the updated page state

current_page = st.session_state.page

# Display LTP logo
st.image("images/Asset 6.png", caption = "Powered by", width = 200, use_container_width = False)

# Display title of the page
st.title(page_title[current_page])

# Display sidebar when needed
if 0 < current_page <= len(page_title)-1:
    # Sidebar for accepting input parameters
    with st.sidebar:
        st.header('Your Answer')
        for i in range(len(business_units)):
            st.session_state.answers[i] = st.number_input(
                f"Insert the space allocated to {business_units[i]} (m²)",
                key=f"answer_{i}"
            )

answers = st.session_state.answers

# Display page body
# Display exercise instruction
st.header('Problem description', divider='rainbow')
introduction(current_page)

# Display student answers
if 0 < current_page <= len(page_title)-1:  

    st.header('Elasticity curves', divider='rainbow')
    col = st.columns(len(business_units))
    for i in range(len(business_units)):
        #Create X axis of points to show in graphs, when there is a minimum, create a dashed line
        if current_page <= 1:
            x_cont = np.arange(available_space + 1)
            x_dash = [0]
        else:
            x_cont = [x for x in np.arange(available_space + 1) if x >= min_space[i]]
            x_dash = [x for x in np.arange(available_space + 1) if x < min_space[i]]

        #Calculate the Y values depending on the elasticity function of the problem selected
        if current_page <= 2:
            y_cont = [x * linear_space_elasticities[i] for x in x_cont]
            y_dash = [x * linear_space_elasticities[i] for x in x_dash]
            value = answers[i] * linear_space_elasticities[i]
        else:
            y_cont = [np.log(x+1) * log_space_elasticities[i] for x in x_cont]
            y_dash = [np.log(x+1) * log_space_elasticities[i] for x in x_dash]
            value = np.log(answers[i]+1) * log_space_elasticities[i]

        if i % 2 == 0:
            col = st.columns(2)
        
        with col[i % 2]:
            # Create the elasticity trace
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=x_cont, y=y_cont, mode='lines', name=f'{business_units[i]} (m={linear_space_elasticities[i]})', line=dict(dash='solid')))
            
            fig.add_trace(go.Scatter(x=x_dash, y=y_dash, mode='lines', name=f'{business_units[i]} (m={linear_space_elasticities[i]})', line=dict(dash='dash')))

            # Highlight a specific datapoint
            fig.add_trace(go.Scatter(
                x=[answers[i]],
                y= [value],
                mode='markers',
                marker=dict(size=10, color='red', symbol='circle'),
                name='Your answer'
            ))
            
            # Customize the layout
            fig.update_layout(
                title=f"{business_units[i]} Space Elasticity",
                xaxis_title="Space Allocated (m²)",
                yaxis_title="Sales Impact (€)",
                yaxis=dict(range=[0, max_y_axis]),
                template="ggplot2",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                showlegend=True
            )
            
            # Display the plot in Streamlit
            st.plotly_chart(fig)

    # Summarize the solution found
    st.header('Summary of solution', divider='rainbow')
    area_used = sum(answers)
    st.text_area(label="Area used:", value=area_used, height=68)

    sales_total = sales_total = sum([a * e for a, e in zip(answers, linear_space_elasticities)])
    st.text_area(label="Total expected sales:", value=sales_total, height=68)

    st.header('Optimized solution', divider='rainbow')
    with st.expander('**Click to see optimized solution**'):
        st.markdown('Soluction visualization')
        for i in range(len(business_units)):
            #Create X axis of points to show in graphs, when there is a minimum, create a dashed line
            if current_page <= 1:
                x_cont = np.arange(available_space + 1)
                x_dash = [0]
            else:
                x_cont = [x for x in np.arange(available_space + 1) if x >= min_space[i]]
                x_dash = [x for x in np.arange(available_space + 1) if x < min_space[i]]

            #Calculate the Y values depending on the elasticity function of the problem selected
            if current_page <= 2:
                y_cont = [x * linear_space_elasticities[i] for x in x_cont]
                y_dash = [x * linear_space_elasticities[i] for x in x_dash]
                value = optimized_answers[current_page][i] * linear_space_elasticities[i]
            else:
                y_cont = [np.log(x+1) * log_space_elasticities[i] for x in x_cont]
                y_dash = [np.log(x+1) * log_space_elasticities[i] for x in x_dash]
                value = np.log(optimized_answers[current_page][i]+1) * log_space_elasticities[i]

            if i % 2 == 0:
                col = st.columns(2)
            
            with col[i % 2]:
                # Create the elasticity trace
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(x=x_cont, y=y_cont, mode='lines', name=f'{business_units[i]} (m={linear_space_elasticities[i]})', line=dict(dash='solid')))
                
                fig.add_trace(go.Scatter(x=x_dash, y=y_dash, mode='lines', name=f'{business_units[i]} (m={linear_space_elasticities[i]})', line=dict(dash='dash')))

                # Highlight a specific datapoint
                fig.add_trace(go.Scatter(
                    x=[optimized_answers[current_page][i]],
                    y= [value],
                    mode='markers',
                    marker=dict(size=10, color='red', symbol='circle'),
                    name='Optimal answer'
                ))
                
                # Customize the layout
                fig.update_layout(
                    title=f"{business_units[i]} Space Elasticity",
                    xaxis_title="Space Allocated (m²)",
                    yaxis_title="Sales Impact (€)",
                    yaxis=dict(range=[0, max_y_axis]),
                    template="ggplot2",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True
                )
                
                # Display the plot in Streamlit
                st.plotly_chart(fig)

        # Summarize the solution found
        opt_area_used = sum(optimized_answers[current_page])
        st.text_area(label="Area used:", value=opt_area_used, height=68)

        opt_sales_total = sales_total = sum([a * e for a, e in zip(optimized_answers[current_page], linear_space_elasticities)])
        st.text_area(label="Total expected sales:", value=opt_sales_total, height=68)


    
# Display buttons at the end to navigate between pages
if current_page == 0:
    left, right = st.columns(2)
    if right.button("Next", use_container_width=True, key="next_0"):
        change_page(1)

elif 0 < current_page < len(page_title)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
    if right.button("Next", use_container_width=True, key=f"next_{current_page}"):
        change_page(1)

elif current_page == len(page_title)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)

# Restart if needed
else:
    st.session_state.page = 0