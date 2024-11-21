import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.answers = [0, 0, 0, 0, 0]

page_title = ['Introduction', 'Basis of optimization', 'Constraints 1', 'Constraints 2', 'Objective function 1', 'Objective function 2']
business_units = ['Beverages', 'Snacks', 'Hygiene', 'Fresh products', 'Other']
linear_space_elasticities = [5, 1, 2, 4, 0.5]

st.set_page_config(page_title='Understanding optimization', page_icon='')

# Navigation function with forced rerun
def change_page(delta):
    st.session_state.page = max(0, min(len(page_title) - 1, st.session_state.page + delta))
    st.rerun()  # Force immediate rerun to reflect the updated page state

current_page = st.session_state.page

# Display title of the page
st.title(page_title[current_page])

# Display sidebar when needed
if 0 < current_page <= len(page_title)-1:
    # Sidebar for accepting input parameters
    with st.sidebar:
        st.header('Your Answer')
        for i in range(len(business_units)):
            st.session_state.answers[i] = st.number_input(
                f"Insert the space allocated to {business_units[i]}",
                key=f"answer_{i}"
            )


# Display page body
if current_page == 0:
    
    st.write('Intro to the exercise')

elif 0 < current_page <= len(page_title)-1:  

    st.header('Elasticity curves', divider='rainbow')
    col = st.columns(len(business_units))
    for i in range(len(business_units)):
        if i % 2 == 0:
            col = st.columns(2)
        
        with col[i % 2]:
            x = np.arange(501)
            y = x * linear_space_elasticities[i]

            # Create a Plotly figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'{business_units[i]} (m={linear_space_elasticities[i]})'))
            
            # Customize the layout
            fig.update_layout(
                title=f"{business_units[i]} Space Elasticity",
                xaxis_title="Space Allocated",
                yaxis_title="Elasticity (Sales Impact)",
                template="ggplot2",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                showlegend=True
            )
            
            # Display the plot in Streamlit
            st.plotly_chart(fig)

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