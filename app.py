import streamlit as st
import requests
from PIL import Image

# Set Cohere API key directly in the code (temporary approach)
cohere_api_key = "9cXeu16WbLhcKXpfCjJspMsN9WLQY5zEIIaw77BB"  # Replace with your actual Cohere API key

# Function to process image (placeholder for image handling)
def process_image(uploaded_file):
    # Placeholder: Integrate image-processing logic here if needed
    return "Processed image data (details of food items)."

# Function to get response from Cohere using direct HTTP request
def get_cohere_response(prompt):
    url = "https://api.cohere.ai/generate"

    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "command-xlarge-nightly",  # Specify the model
        "prompt": prompt,
        "max_tokens": 300,  # Adjust token limit as needed
        "temperature": 0.7,  # Adjust creativity level
        "stop_sequences": ["\n"]  # Optional stop sequences
    }

    try:
        # Send request to Cohere API
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            # Extract and return the text from response
            generations = response_data.get("generations", [])
            if generations:
                return generations[0].get("text", "No text generated.").strip()
            else:
                return "Error: No generations found in response."
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App Configuration
st.set_page_config(page_title="Cohere Nutrition Analysis", page_icon="🥗")

st.header("Cohere Nutrition Analysis")

# Text input for prompt
input_prompt = st.text_input("Describe what you want analyzed:", key="input")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Analyze Food Nutrition")

# Predefined prompt template
nutrition_prompt_template = """
You are a nutrition expert. Based on the following description, calculate the total calories and provide a breakdown of each food item's calorie count in the format:

1. Item 1 - X calories
2. Item 2 - Y calories
---
Description: {description}
"""

if submit:
    if input_prompt:
        # Handle image processing if an image is uploaded
        processed_image_data = ""
        if uploaded_file:
            processed_image_data = process_image(uploaded_file)

        # Combine text and image information for the prompt
        final_prompt = nutrition_prompt_template.format(
            description=f"{input_prompt}. {processed_image_data}"
        )

        # Get response from Cohere
        response = get_cohere_response(final_prompt)

        # Display the result
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please enter a description or upload an image.")
