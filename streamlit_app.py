import streamlit as st
import pandas
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
import numpy as np
from config import page_title, business_units, available_space, linear_space_elasticities, min_space, log_space_elasticities, optimized_answers, max_y_axis, linearization_brackets, bracket_space_elasticity, bracket_space_intercept, max_ratio_areas
from page_description import introduction, min_index, max_index

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(business_units)  # Initialize with zeros for all business units

if "expander_open" not in st.session_state:
    st.session_state.expander_open = False  # Track expander state

# Use session state for answers
answers = st.session_state.answers

st.set_page_config(page_title='Understanding optimization', page_icon='', layout = 'wide')

# Navigation function with forced rerun
def change_page(delta):
    st.session_state.page = max(0, min(len(page_title) - 1, st.session_state.page + delta))
    st.session_state.expander_open = False  # Collapse the expander when going to the next page
    st.rerun()  # Force immediate rerun to reflect the updated page state

current_page = st.session_state.page

# Display LTP logo
st.image(image= "images/Asset 6.png", caption = "Powered by", width = 100, use_container_width = False)

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"top_restart_{current_page}"):
        st.session_state.page = 0
        st.rerun()

# Display title of the page
st.title(page_title[current_page], anchor='title')


# Display sidebar when needed
if 0 < current_page <= len(page_title)-1:
    # Sidebar for accepting input parameters
    with st.sidebar:
        st.header('Your Answer')
        for i in range(len(business_units)):
            st.session_state.answers[i] = st.number_input(
                f"Insert the space allocated to {business_units[i]} (m²)",
                #value = answers[i],
                key=f"answer_{i}"
            )


# Display page body
# Display exercise instruction
st.header('Problem description', divider='rainbow')
introduction(current_page)


# Display student answers
if 0 < current_page <= len(page_title)-1:  

    st.header('Solution analysis', divider='rainbow')
    col = st.columns(len(business_units))
    values = [0] * len(business_units)
    for i in range(len(business_units)):
        #Create X axis of points to show in graphs, when there is a minimum, create a dashed line
        if current_page <= 1:
            x_cont = np.arange(available_space + 1)
            x_dash = [0]
        else:
            x_cont = [x for x in np.arange(available_space + 1) if x >= min_space[i]]
            x_dash = [x for x in np.arange(available_space + 1) if x < min_space[i]]

        #Calculate the Y values depending on the elasticity function of the problem selected
        if current_page <= 3:
            y_cont = [x * linear_space_elasticities[i] for x in x_cont]
            y_dash = [x * linear_space_elasticities[i] for x in x_dash]
            values[i] = answers[i] * linear_space_elasticities[i]
        elif current_page == 4:
            y_cont = []
            y_dash = []
            for j in range(1, len(linearization_brackets)):
                y_cont += [x * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i] for x in x_cont if linearization_brackets[j-1] < x <= linearization_brackets[j]]
                y_dash += [x * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i] for x in x_dash if linearization_brackets[j-1] < x <= linearization_brackets[j]]
                if linearization_brackets[j-1] <= answers[i] <= linearization_brackets[j]:
                    values[i] = answers[i] * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i] 
                if answers[i] > linearization_brackets[j]:
                    values[i] = answers[i] * bracket_space_elasticity[len(linearization_brackets)-2][i] + bracket_space_intercept[len(linearization_brackets)-2][i]
        else:
            y_cont = [np.log(x+1) * log_space_elasticities[i] for x in x_cont]
            y_dash = [np.log(x+1) * log_space_elasticities[i] for x in x_dash]
            values[i] = np.log(answers[i]+1) * log_space_elasticities[i]

        if i % 2 == 0:
            col = st.columns(2)
        
        with col[i % 2]:
            # Create the elasticity trace
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=x_cont, y=y_cont, mode='lines', name=f'{business_units[i]}', line=dict(dash='solid')))
            
            fig.add_trace(go.Scatter(x=x_dash, y=y_dash, mode='lines', name=f'{business_units[i]}', line=dict(dash='dash'), showlegend=False))

            # Highlight a specific datapoint
            if answers[i] <= available_space:
                fig.add_trace(go.Scatter(
                    x=[answers[i]],
                    y= [values[i]],
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
                template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                showlegend=True,
                legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            # Create a container for the chart
            with st.container():
                # Capture click events using plotly_events but do not render it
                #selected_points = plotly_events(
                #    fig,  # Use the same figure
                #    click_event=True,  # Enable click events
                #    hover_event=False,  # Disable hover events
                #    select_event=False,  # Disable select events
                #    override_height=500,  # Ensure consistent size
                #    override_width="100%"  # Match Streamlit container behavior
                #)

                # Display the chart using Streamlit's optimized layout
                st.plotly_chart(fig, use_container_width=True)

            # Check if the user clicked a point
            #if selected_points:
            #    clicked_x = selected_points[0]["x"]
            #    clicked_y = selected_points[0]["y"]
            #    st.session_state.answers[i] = clicked_x
            #    answers[i] = st.session_state.answers[i]
            #    selected_points = []


    # Summarize the solution found
    st.header('Summary of solution', divider='rainbow')
    area_used = sum(answers)
    st.text_area(label="Area used:", value=str(round(area_used,0)), height=68, key=f"area_{current_page}")

    sales_total = sum(values)
    st.text_area(label="Total expected sales:", value=str(round(sales_total,2)), height=68, key=f"sales_{current_page}")

    st.header('Optimized solution', divider='rainbow')
    with st.expander('**Click to see optimized solution**', expanded=False):
        st.markdown('Soluction visualization')
        optmized_values = [0] * len(business_units)
        for i in range(len(business_units)):
            #Create X axis of points to show in graphs, when there is a minimum, create a dashed line
            if current_page <= 1:
                x_cont = np.arange(available_space + 1)
                x_dash = [0]
            else:
                x_cont = [x for x in np.arange(available_space + 1) if x >= min_space[i]]
                x_dash = [x for x in np.arange(available_space + 1) if x < min_space[i]]

            #Calculate the Y values depending on the elasticity function of the problem selected
            if current_page <= 3:
                y_cont = [x * linear_space_elasticities[i] for x in x_cont]
                y_dash = [x * linear_space_elasticities[i] for x in x_dash]
                optmized_values[i] = optimized_answers[current_page][i] * linear_space_elasticities[i]
            elif current_page == 4:
                y_cont = []
                y_dash = []
                for j in range(1, len(linearization_brackets)):
                    y_cont += [x * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i] for x in x_cont if linearization_brackets[j-1] < x <= linearization_brackets[j]]
                    y_dash += [x * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i] for x in x_dash if linearization_brackets[j-1] < x <= linearization_brackets[j]]
                    if linearization_brackets[j-1] <= optimized_answers[current_page][i] <= linearization_brackets[j]:
                        optmized_values[i] = optimized_answers[current_page][i] * bracket_space_elasticity[j-1][i] + bracket_space_intercept[j-1][i]
            else:
                y_cont = [np.log(x+1) * log_space_elasticities[i] for x in x_cont]
                y_dash = [np.log(x+1) * log_space_elasticities[i] for x in x_dash]
                optmized_values[i] = np.log(optimized_answers[current_page][i]+1) * log_space_elasticities[i]

            if i % 2 == 0:
                col = st.columns(2)
            
            with col[i % 2]:
                # Create the elasticity trace
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(x=x_cont, y=y_cont, mode='lines', name=f'{business_units[i]}', line=dict(dash='solid')))
                
                fig.add_trace(go.Scatter(x=x_dash, y=y_dash, mode='lines', name=f'{business_units[i]}', line=dict(dash='dash'), showlegend=False))

                # Highlight a specific datapoint
                fig.add_trace(go.Scatter(
                    x=[optimized_answers[current_page][i]],
                    y= [optmized_values[i]],
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
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                # Display the plot in Streamlit
                st.plotly_chart(fig)

        # Summarize the solution found
        opt_area_used = sum(optimized_answers[current_page])
        val = str(round(opt_area_used,0))
        if area_used > available_space:
            val = val + '\nYour solution does not respect the available area of the store'
        if current_page >= 2:
            for i in range(len(business_units)):
                if answers[i] < min_space[i]:
                    val = val + f'\nYour answer for {business_units[i]} does not respect the miminum area'
        if current_page >= 3:
            if answers[max_index] >= answers[min_index]*max_ratio_areas:
                val = val + f'\nThe area of {business_units[max_index]} is more than {max_ratio_areas} times larger than the area of {business_units[min_index]}'
        st.text_area(label="Area used:", value=val, height=68, key=f"opt_area_{current_page}")

        opt_sales_total = sum(optmized_values)
        val = str(round(opt_sales_total,2))
        val = val + f'\nYour answer was {100*round((opt_sales_total - sales_total)/opt_sales_total, 4)}% away from the optimal value'
        st.text_area(label="Total expected sales:", value=val, height=68, key=f"opt_sales_{current_page}")


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

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"bot_restart_{current_page}"):
        st.session_state.page = 0
        st.session_state.expander_open = False  # Collapse the expander when going to the next page
        st.rerun()