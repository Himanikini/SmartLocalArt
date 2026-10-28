import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Set page configuration
st.set_page_config(
    page_title="Painting Price Prediction",
    page_icon="🎨",
    layout="wide"
)

# Title and description
st.title("Painting Price Prediction App")
st.write("Enter the painting details below to get an estimated price")

# Function to load the trained model and related files
@st.cache_resource
def load_model_files():
    try:
        model = joblib.load('model.pkl')
        scaler = joblib.load('scaler.pkl')
        columns = joblib.load('columns.pkl')
        return model, scaler, columns
    except FileNotFoundError as e:
        st.error(f"Error loading model files: {e}")
        return None, None, None

# Load the model, scaler, and columns
model, scaler, columns = load_model_files()

# Main container
main_container = st.container()

with main_container:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Painting Details")
        
        # Create input fields in rows with 2 parameters each
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            painter_options = ["Leonardo", "Van Gogh", "Picasso", "Monet", "Other"]
            painter = st.selectbox("Name of Painter", painter_options)
        with row1_col2:
            subject_options = ["Portrait", "Landscape", "Abstract", "Still Life", "Historical", "Other"]
            subject = st.selectbox("Subject of Painting", subject_options)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            style_options = ["Modern", "Classical", "Impressionist", "Expressionist", "Surrealist", "Contemporary", "Other"]
            style = st.selectbox("Style", style_options)
        with row2_col2:
            medium_options = ["Oil", "Acrylic", "Watercolor", "Mixed Media", "Digital", "Other"]
            medium = st.selectbox("Medium", medium_options)

        row3_col1, row3_col2 = st.columns(2)
        with row3_col1:
            size_options = ["24\"x36\"", "30\"x40\"", "16\"x20\"", "48\"x60\"", "8\"x10\"", "Other"]
            size = st.selectbox("Size", size_options)
        with row3_col2:
            location_options = [
                "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
                "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Surat", "Thane",
                "Vasai-Virar", "Navi Mumbai", "Nagpur", "Indore", "Bhopal",
                "Visakhapatnam", "Patna", "Vadodara", "Ludhiana", "Agra",
                "Nashik", "Kochi", "Chandigarh", "Other"
            ]
            location = st.selectbox("Location", location_options)

        environment_options = ["Home", "Office", "Gallery", "Public Space", "Other"]
        environment = st.selectbox("Recommended Environment", environment_options)
    
    with col2:
        st.subheader("Prediction")
        
        if st.button("Predict Price", type="primary"):
            if model is None or scaler is None or columns is None:
                st.error("Model files not loaded properly")
            else:
                try:
                    new_painting_df = pd.DataFrame(0, index=[0], columns=columns)

                    size_col = f"Size_{size}"
                    if size_col in new_painting_df.columns:
                        new_painting_df[size_col] = 1

                    medium_col = f"Medium_{medium}"
                    if medium_col in new_painting_df.columns:
                        new_painting_df[medium_col] = 1

                    style_col = f"Style_{style}"
                    if style_col in new_painting_df.columns:
                        new_painting_df[style_col] = 1

                    subject_col = f"Subject of Painting_{subject}"
                    if subject_col in new_painting_df.columns:
                        new_painting_df[subject_col] = 1

                    painter_col = f"Name of Painter_{painter}"
                    if painter_col in new_painting_df.columns:
                        new_painting_df[painter_col] = 1

                    location_col = f"Location_{location}"
                    if location_col in new_painting_df.columns:
                        new_painting_df[location_col] = 1

                    environment_col = f"Recommended Environment_{environment}"
                    if environment_col in new_painting_df.columns:
                        new_painting_df[environment_col] = 1
                    
                    # Scale the features using the same scaler
                    new_painting_scaled = scaler.transform(new_painting_df)
                    
                    # Predict the price
                    predicted_price = model.predict(new_painting_scaled)
                    
                    # Display the predicted price
                    st.markdown(f"### Predicted Price:")
                    st.markdown(f"<h2 style='color: green;'>Rs. {predicted_price[0]:.2f}</h2>", unsafe_allow_html=True)
                    
                    # Display image placeholder for the painting
                    # st.image("https://via.placeholder.com/300x200?text=Painting+Preview", 
                    #          caption=f"{painter}'s {subject} in {style} style", 
                    #          width=300)
                    
                except Exception as e:
                    st.error(f"Error making prediction: {e}")
                    st.info("If you selected options that don't exist in the training data, try different selections.")

# Footer
st.markdown("---")
st.markdown("### About This App")
st.write("""
This application uses a machine learning model trained on art price data to predict painting prices. 
The predictions are based on various factors including the artist, style, medium, and other characteristics.
""")