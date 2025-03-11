import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os


st.title("CalcMate Unit Converter")

conversion_factors = {
    "Length": {
        "Meters": 1,
        "Kilometers": 1000,
        "Feet": 0.3048,
        "Inches": 0.0254,
        "Centimeters": 0.01,  
        "Millimeters": 0.001,
        "Yards": 0.9144,
        "Miles": 1609.34
    },
    "Weight": {
        "Kilograms": 1,
        "Pounds": 0.453592,
        "Grams": 0.001,
        "Ounces": 0.0283495,
        "Milligrams": 0.000001,
        "Tons (Metric)": 1000,
        "Tons (US)": 907.184
    },
    "Time": {
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400,
        "Weeks": 604800,   # 7 days
        "Months": 2628000,  # Approx. 30.44 days
        "Years": 31536000  # 365 days
    },
    "Speed": {
        "Meters per second": 1,
        "Kilometers per hour": 3.6,
        "Miles per hour": 2.23694,
        "Feet per second": 3.28084
    },
    "Volume": {
        "Liters": 1,
        "Milliliters": 0.001,
        "Cubic Meters": 1000,
        "Cubic Feet": 28.3168,
        "Gallons (US)": 3.78541,
        "Gallons (UK)": 4.54609
    }
}


category = st.selectbox("Category", list(conversion_factors.keys()))
input_value = st.number_input("Enter value", min_value=0.0, format="%.1f")  
input_unit = st.selectbox("From", list(conversion_factors[category].keys()))
output_unit = st.selectbox("To", list(conversion_factors[category].keys()))


def conversion_function(input_value, input_unit, output_unit, category):
    if input_value > 0:
        factor_from = conversion_factors[category][input_unit]  # Convert to base unit
        factor_to = conversion_factors[category][output_unit]  # Convert from base unit

        if factor_from and factor_to:
            # Convert input to base unit first, then to the output unit
            base_value = input_value * factor_from  # Convert to base unit
            output_value = base_value / factor_to  # Convert to target unit
            st.success(f"The converted value is: {output_value:.4f}")
        else:
            st.error("Conversion factors not found. Please check your inputs.")
    else:
        st.warning("Enter a value greater than zero to convert.")


if input_value > 0:
    conversion_function(input_value, input_unit, output_unit, category)


# Set up Gemini API key
# Load environment variables from .env file
load_dotenv()

# Initialize Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))  # Assuming GEMINI_API_KEY is the variable name in your .env file


# Streamlit UI
st.divider()
st.subheader("Chat with CalcMate 🤖")

# User input field
user_input = st.text_input("Ask me anything about conversions!",placeholder="100 meters to kilometers...")

# Process the request
if user_input:
    model = genai.GenerativeModel("gemini-2.0-flash")  # Load the model
    response = model.generate_content(contents=[{"parts": [{"text": user_input}]}])

    # Extract and display AI response
    if response and response.candidates:
        answer = response.candidates[0].content.parts[0].text
        st.text_area("CalcMate 🤖:", answer)
    else:
        st.text_area("CalcMate 🤖:", "Sorry, I couldn't generate a response.")

  
