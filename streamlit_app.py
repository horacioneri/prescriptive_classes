import streamlit as st
page=0
page_title = ['Introduction', 'Basis of optimization', 'Constraints 1', 'Constraints 2', 'Objective function 1', 'Objective function 2']
answers = [0,0,0,0,0]
business_units = ['Beverages', 'Snacks', 'Hygene', 'Fresh products', 'Other']
st.set_page_config(page_title='Understanding optimization', page_icon='')

#This app will have different pages depending on the part of the exercise where the student is in

if page==0:
    st.title(page_title[page])
    with st.expander('Use case'):
        st.markdown('**Introduction to the problem**')
        st.info('Lorem Ipsum...')
    
    left, right = st.columns(2)
    if right.button("Next", use_container_width=True):
        page=page+1
elif page > 0 and page <= 5:
    st.title(page_title[page])
    # Sidebar for accepting input parameters
    with st.sidebar:
        # User can input answers to the problem
        st.header('Your Answer')

        #For each BU, user is allowed to 
        for i in range(0,5,1):
            answers[i] = st.number_imput("Insert the space allocated to " + business_units[i])
            
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True):
        page=page-1
    if right.button("Next", use_container_width=True):
        page=page+1
# Restart
else:
    page=0
