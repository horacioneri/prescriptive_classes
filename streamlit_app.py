import streamlit as st
import matplotlib.pyplot as plt
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

# Display current page content
current_page = st.session_state.page
if current_page == 0:
    st.title(page_title[current_page])
    st.write('Intro to the exercise')

    left, right = st.columns(2)
    if right.button("Next", use_container_width=True, key="next_0"):
        change_page(1)

elif 0 < current_page <= 5:
    st.title(page_title[current_page])

    # Sidebar for accepting input parameters
    with st.sidebar:
        st.header('Your Answer')
        for i in range(len(business_units)):
            st.session_state.answers[i] = st.number_input(
                f"Insert the space allocated to {business_units[i]}",
                key=f"answer_{i}"
            )

    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
    if right.button("Next", use_container_width=True, key=f"next_{current_page}"):
        change_page(1)

    st.header('Elasticity curves', divider='rainbow')
    col = st.columns(len(business_units))
    for i in range(len(business_units)):
        with col[i]:
            x = range(0,500,1)
            y = x * linear_space_elasticities[i]

            # Plot the function
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, y, label=f"{business_units[i]} (m={linear_space_elasticities[i]})")
            ax.set_title(f"{business_units[i]} Space Elasticity")
            ax.set_xlabel("Space Allocated")
            ax.set_ylabel("Elasticity (Sales Impact)")
            ax.grid(True)
            ax.legend()
            
            # Render the plot in Streamlit
            st.pyplot(fig)

# Restart if needed
else:
    st.session_state.page = 0
