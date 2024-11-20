import streamlit as st

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.answers = [0, 0, 0, 0, 0]

page_title = ['Introduction', 'Basis of optimization', 'Constraints 1', 'Constraints 2', 'Objective function 1', 'Objective function 2']
business_units = ['Beverages', 'Snacks', 'Hygiene', 'Fresh products', 'Other']

st.set_page_config(page_title='Understanding optimization', page_icon='')

# Navigation function
def change_page(delta):
    st.session_state.page = max(0, min(len(page_title) - 1, st.session_state.page + delta))

# Display current page content
current_page = st.session_state.page
if current_page == 0:
    st.title(page_title[current_page])
    st.write(current_page)

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

# Restart if needed
else:
    st.session_state.page = 0