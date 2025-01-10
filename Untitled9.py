import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Page configuration
st.set_page_config(page_title="Local Cuisines - Explore the Flavors of the World", layout="wide")

# Function to load data from Excel
@st.cache_data
def load_cuisine_data(file_path):
    try:
        data = pd.read_excel(file_path, engine='openpyxl')
        if data.empty:
            st.error("The Excel file is empty.")
            st.stop()
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        st.stop()

# Local path to your uploaded file
file_path = 'local_cuisines_data.xlsx'

# Load the cuisines data
cuisines_data = load_cuisine_data(file_path)

# Ensure necessary columns are present
required_columns = ['Cuisine Name', 'Region', 'Ingredients', 'Price Range', 'Star Rating', 'Specialty', 'Image URL']
missing_columns = [col for col in required_columns if col not in cuisines_data.columns]
if missing_columns:
    st.error(f"The following required columns are missing from the Excel file: {', '.join(missing_columns)}")
    st.stop()

# App title and description
st.title('🍲 Local Cuisines')
st.subheader('Explore the Flavors of the World')
st.write('Discover local dishes and their specialties from various regions.')
st.write('---')
st.write('Guided by Dr. PRANJALI GAJBHIYE')

# Sidebar filters
st.sidebar.header('Filter Cuisines')

# Region Filter
region_filter = st.sidebar.multiselect('Region', options=sorted(cuisines_data['Region'].dropna().unique()), default=sorted(cuisines_data['Region'].dropna().unique()))

# Price Range Filter
price_filter = st.sidebar.slider('Price Range (₹)', 
                                  min_value=int(cuisines_data['Price Range'].min()), 
                                  max_value=int(cuisines_data['Price Range'].max()), 
                                  value=(int(cuisines_data['Price Range'].min()), int(cuisines_data['Price Range'].max())))

# Star Rating Filter
star_rating = st.sidebar.selectbox('Minimum Star Rating', options=[1, 2, 3, 4, 5], index=4)

# Specialty Filter
specialty_filter = st.sidebar.text_input('Search Specialty', '')

# Sort options
sort_by = st.sidebar.selectbox('Sort by', ['Price Range', 'Star Rating', 'Cuisine Name'])

# Apply Filters button
apply_filters = st.sidebar.button('Apply Filters')

# Save Wish List in session state
if 'wish_list' not in st.session_state:
    st.session_state.wish_list = []

# Function to add cuisine to wish list
def add_to_wish_list(cuisine_name):
    if cuisine_name not in st.session_state.wish_list:
        st.session_state.wish_list.append(cuisine_name)
        st.success(f"{cuisine_name} added to your Wish List!")

# Apply filters and sorting once the button is clicked
if apply_filters:
    # Filter data based on selections
    filtered_data = cuisines_data[
        (cuisines_data['Region'].isin(region_filter)) &
        (cuisines_data['Price Range'].between(price_filter[0], price_filter[1])) &
        (cuisines_data['Star Rating'] >= star_rating) &
        (cuisines_data['Specialty'].str.contains(specialty_filter, case=False, na=False))
    ].sort_values(by=sort_by, ascending=True)

    # Display filtered results
    if filtered_data.empty:
        st.write("No cuisines match your criteria.")
    else:
        st.subheader('Filtered Cuisines')

        # Display each filtered cuisine with details
        for index, row in filtered_data.iterrows():
            st.write('---')
            col1, col2 = st.columns([2, 1])  # Create two columns (left for info, right for image)

            # Left column for cuisine information
            with col1:
                st.markdown(f"### {row['Cuisine Name']}")
                st.markdown(f"**Region:** {row['Region']}")
                st.markdown(f"**Ingredients:** {row['Ingredients']}")
                st.markdown(f"**Price Range:** ₹{row['Price Range']}")
                st.markdown(f"**Star Rating:** {row['Star Rating']} stars")
                st.markdown(f"**Specialty:** {row['Specialty']}")

                # Add to Wish List button
                if st.button(f"Add {row['Cuisine Name']} to Wish List", key=index):
                    add_to_wish_list(row['Cuisine Name'])

                # Book your experience
                st.markdown("[👆 Book a Tasting Experience](https://forms.office.com/)", unsafe_allow_html=True)

                # Add a review button with form link
                st.markdown(f"[📝 Add a Review](https://forms.office.com/)", unsafe_allow_html=True)

            # Right column for image
            with col2:
                if pd.notna(row['Image URL']):
                    st.image(row['Image URL'], caption=f"{row['Cuisine Name']}", use_container_width=True)

        st.write('---')

# Footer
st.write('---')
st.markdown('<div style="text-align: center; font-size: small;">© 2024 Local Cuisines. All rights reserved.</div>', unsafe_allow_html=True)
