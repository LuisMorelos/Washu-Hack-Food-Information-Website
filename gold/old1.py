
from openai import OpenAI
import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import random
import json
from datetime import datetime

# Load environment variables
load_dotenv()
food_components = []
date = datetime.today()
os.environ["OPENAI_API_KEY"] = 
# Function to generate food nutritional data using ChatGPT
def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        value = '0'
        return value
    

# Access API keys
API_KEY = 'LkbenMqO.G4m7CrnF9M6UUElgAwTL1Zy8U2ws5I9g'
SERPAPI_API_KEY = '5312ce5c5c97a3ff70fe04fcf1e49d7e38039018892ceec45dbb0798c200137a'

if not API_KEY:
    st.error("FOODVISOR_API_KEY environment variable not set.")
    st.stop()
if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

# File uploader for the user to upload an image
uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image file
    image_bytes = uploaded_file.read()

    # Determine the MIME type
    filename = uploaded_file.name
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        mime_type = 'image/jpeg'
    elif filename.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        st.error("Unsupported file type. Please upload a JPG or PNG image.")
        st.stop()

    # Display the uploaded image
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption='Uploaded Food Image', use_column_width=True)

    # Prepare and send the request to the Foodvisor API
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": "Api-Key " + API_KEY}
    files = {
        "image": (filename, image_bytes, mime_type)
    }

    with st.spinner('Analyzing image...'):
        response = requests.post(url, headers=headers, files=files)
        try:
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.write(response.text)
            st.stop()
        except Exception as err:
            st.error(f"An error occurred: {err}")
            st.stop()

    # Check if any items were detected
    items = data.get('items')
    if not items:
        st.error("No food items detected in the image.")
        st.stop()

    st.success('Analysis complete!')
# Function 1: Allow the user to choose between detected food items
def display_and_choose_food_option(item, i):
    food_options = [food['food_info']['display_name'] for food in item['food']]
    
    # Let the user choose the correct food if multiple options are available
    if len(food_options) > 1:
        selected_option = st.selectbox(f"Multiple items detected for Ingredient {i+1}: Please select the correct food item", food_options)
        food_components.pop(food_options[0])
        # Find the selected food's information
        selected_food = next(food for food in item['food'] if food['food_info']['display_name'] == selected_option)
    else:
        # If only one option is available, select it automatically
        selected_food = item['food'][0]
        
    # Extract and display the nutritional data for the selected food
    food_info = selected_food['food_info']
    nutrition = food_info['nutrition']

    st.markdown(f"**Ingredient {i+1}: {food_info['display_name']}**")
    with st.expander("Nutritional Information"):
        st.write(f"**Serving Size:** {food_info.get('g_per_serving', 'Unknown')} g")
        st.write(f"**Calories:** {format_number((nutrition.get('calories_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} kcal")
        st.write(f"**Total Fat:** {format_number((nutrition.get('fat_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} g")
        st.write(f"**Cholesterol:** {format_number((nutrition.get('cholesterol_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} mg")
        st.write(f"**Sodium:** {format_number((nutrition.get('sodium_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} mg")
        st.write(f"**Total Carbohydrates:** {format_number((nutrition.get('carbs_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} g")
        st.write(f"  - **Dietary Fiber:** {format_number((nutrition.get('fibers_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} g")
        st.write(f"  - **Sugars:** {format_number((nutrition.get('sugars_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} g")
        st.write(f"**Protein:** {format_number((nutrition.get('proteins_100g', 0) / 100 * food_info.get('g_per_serving', 0)))} g")

    return food_info
def chatgpt_meal_name():
    food_components_str = ", ".join(food_components)
    # Step 3: Make the API request
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "ou are a helpful assistant that creates meal names."},
            {
                "role": "user",
                "content": f"Based on these ingredients: {food_components_str}, what would you name the dish?"
            }
        ]
    )
    # Print the generated dish name
    dish_name = response['choices'][0]['message']['content']
    return dish_name

def make_data_list(dish_name, date):
    food_journal = {}
    dish_name
    meal_entry = {
        "name": dish_name,
        "calories": calorie_sum,
        "fat": fat_sum,
        "cholesterol": cholesterol_sum,
        "sodium": sodium_sum,
        "carbs": carbs_sum,
        "fiber": fiber_sum,
        "sugars": sugars_sum,
        "protein": protein_sum,
        "vitamin_a": vitamin_a_sum,
        "vitamin_c": vitamin_c_sum,
        "vitamin_d": vitamin_d_sum,
        "vitamin_b12": vitamin_b12_sum,
        "calcium": calcium_sum,
        "iron": iron_sum,
        "potassium": potassium_sum
    }
    date_str = date.strftime("%Y-%m-%d")

    # Add the meal entry under the selected date
    food_journal[date_str] = {
        "meal": meal_entry
    }

    # Write the food journal to a JSON file
    with open("user.json", "w") as json_file:
        json.dump(food_journal, json_file, indent=4)
# Initialize the nutritional sum variables
calorie_sum = 0
fat_sum = 0
cholesterol_sum = 0
sodium_sum = 0
carbs_sum = 0
fiber_sum = 0
sugars_sum = 0
protein_sum = 0
vitamin_a_sum = 0
vitamin_c_sum = 0
vitamin_d_sum = 0
vitamin_b12_sum = 0
calcium_sum = 0
iron_sum = 0
potassium_sum = 0


# Loop through each detected item and allow the user to choose the correct one
if uploaded_file is not None:   
    for i, item in enumerate(items):
        food_info = display_and_choose_food_option(item, i)  # Let the user choose the correct food
        display_name = food_info['display_name']
        nutrition = food_info['nutrition']
        food_components.append(display_name)
        # Accumulate nutritional values
        calorie_sum += (nutrition.get('calories_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('calories_100g') is not None else 0
        fat_sum += (nutrition.get('fat_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fat_100g') is not None else 0
        cholesterol_sum += (nutrition.get('cholesterol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('cholesterol_100g') is not None else 0
        sodium_sum += (nutrition.get('sodium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sodium_100g') is not None else 0
        carbs_sum += (nutrition.get('carbs_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('carbs_100g') is not None else 0
        fiber_sum += (nutrition.get('fibers_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fibers_100g') is not None else 0
        sugars_sum += (nutrition.get('sugars_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sugars_100g') is not None else 0
        protein_sum += (nutrition.get('proteins_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('proteins_100g') is not None else 0

        vitamin_a_sum += (nutrition.get('vitamin_a_retinol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_a_retinol_100g') is not None else 0
        vitamin_c_sum += (nutrition.get('vitamin_c_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_c_100g') is not None else 0
        vitamin_d_sum += (nutrition.get('vitamin_d_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_d_100g') is not None else 0
        vitamin_b12_sum += (nutrition.get('vitamin_b12_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_b12_100g') is not None else 0

        calcium_sum += (nutrition.get('calcium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('calcium_100g') is not None else 0
        iron_sum += (nutrition.get('iron_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('iron_100g') is not None else 0
        potassium_sum += (nutrition.get('potassium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('potassium_100g') is not None else 0

    st.markdown('<span style="font-size: 24px;">Total Nutritional Information for Meal</span>', unsafe_allow_html=True)
    # Display the detailed nutritional information in an expandable section
    # Function to add manual food using ChatGPT API to fetch nutritional data
def total_sum_expander():
        with st.expander("Nutritional Information"):
            st.write(f"**Total Calories:** {format_number(calorie_sum)} kcal")
            st.write(f"**Total Fat:** {format_number(fat_sum)} g")
            st.write(f"**Total Cholesterol:** {format_number(cholesterol_sum)} mg")
            st.write(f"**Total Sodium:** {format_number(sodium_sum)} mg")
            st.write(f"**Total Carbohydrates:** {format_number(carbs_sum)} g")
            st.write(f"**Total Dietary Fiber:** {format_number(fiber_sum)} g")
            st.write(f"**Total Sugars:** {format_number(sugars_sum)} g")
            st.write(f"**Total Protein:** {format_number(protein_sum)} g")
            st.write(f"**Total Vitamin A:** {format_number(vitamin_a_sum)} µg")
            st.write(f"**Total Vitamin C:** {format_number(vitamin_c_sum)} mg")
            st.write(f"**Total Vitamin D:** {format_number(vitamin_d_sum)} µg")
            st.write(f"**Total Vitamin B12:** {format_number(vitamin_b12_sum)} µg")
            st.write(f"**Total Calcium:** {format_number(calcium_sum)} mg")
            st.write(f"**Total Iron:** {format_number(iron_sum)} mg")
            st.write(f"**Total Potassium:** {format_number(potassium_sum)} mg")
import random

# Simulated API (ChatGPT) to generate nutritional data for a given food
def generate_nutritional_data(food_name):
    # Simulating nutrition data generation (random realistic values)
    return {
        "calories_100g": random.uniform(50, 400),  # kcal per 100g
        "fat_100g": random.uniform(0, 30),         # g per 100g
        "proteins_100g": random.uniform(1, 30),    # g per 100g
        "carbs_100g": random.uniform(1, 100),      # g per 100g
        "fibers_100g": random.uniform(0, 15),      # g per 100g
        "sugars_100g": random.uniform(0, 50),      # g per 100g
        "cholesterol_100g": random.uniform(0, 150),# mg per 100g
        "sodium_100g": random.uniform(0, 1000),    # mg per 100g
        "vitamin_a_retinol_100g": random.uniform(0, 500), # µg per 100g
        "vitamin_c_100g": random.uniform(0, 100),  # mg per 100g
        "vitamin_d_100g": random.uniform(0, 10),   # µg per 100g
        "vitamin_b12_100g": random.uniform(0, 5),  # µg per 100g
        "calcium_100g": random.uniform(0, 500),    # mg per 100g
        "iron_100g": random.uniform(0, 10),        # mg per 100g
        "potassium_100g": random.uniform(0, 1000)  # mg per 100g
    }

# Function to manually add food and decide whether to sum it with the total nutritional data
def add_manual_food_optional():
    st.markdown("<span style='font-size: 24px;'>Add Food Manually</span>", unsafe_allow_html=True)
    
    # Checkbox for whether the user needs to add food manually
    manual_food_needed = st.checkbox("I need to manually add food")
    
    if manual_food_needed:
        manual_food_name = st.text_input("Enter the food name:")
        
        if manual_food_name is not None:
            # Call the ChatGPT simulated API to get food data
            food_nutrition = generate_nutritional_data(manual_food_name)

            serving_size = st.number_input(f"Enter serving size for {manual_food_name} (g)", min_value=0)

            if serving_size > 0:
                # Calculate the nutritional values based on serving size
                calories = (food_nutrition['calories_100g'] / 100) * serving_size
                fat = (food_nutrition['fat_100g'] / 100) * serving_size
                protein = (food_nutrition['proteins_100g'] / 100) * serving_size
                carbs = (food_nutrition['carbs_100g'] / 100) * serving_size
                fiber = (food_nutrition['fibers_100g'] / 100) * serving_size
                sugars = (food_nutrition['sugars_100g'] / 100) * serving_size
                cholesterol = (food_nutrition['cholesterol_100g'] / 100) * serving_size
                sodium = (food_nutrition['sodium_100g'] / 100) * serving_size

                # Display the generated nutritional data for this food
                st.markdown(f"**Manually Added Food: {manual_food_name}**")
                with st.expander("Nutritional Information"):
                    st.write(f"**Serving Size:** {serving_size} g")
                    st.write(f"**Calories:** {format_number(calories)} kcal")
                    st.write(f"**Total Fat:** {format_number(fat)} g")
                    st.write(f"**Protein:** {format_number(protein)} g")
                    st.write(f"**Total Carbohydrates:** {format_number(carbs)} g")
                    st.write(f"  - **Dietary Fiber:** {format_number(fiber)} g")
                    st.write(f"  - **Sugars:** {format_number(sugars)} g")
                    st.write(f"**Cholesterol:** {format_number(cholesterol)} mg")
                    st.write(f"**Sodium:** {format_number(sodium)} mg")

                # Option to add this food to the total sum
                include_in_total = st.checkbox(f"Include {manual_food_name} in total nutritional data")

                if include_in_total:
                    food_components.append(manual_food_name)
                    # Update the global nutritional totals
                    global calorie_sum, fat_sum, protein_sum, carbs_sum, fiber_sum, sugars_sum, cholesterol_sum, sodium_sum
                    calorie_sum += calories
                    fat_sum += fat
                    protein_sum += protein
                    carbs_sum += carbs
                    fiber_sum += fiber
                    sugars_sum += sugars
                    cholesterol_sum += cholesterol
                    sodium_sum += sodium

                    # Re-display the total nutritional information for the entire meal
                    total_sum_expander()

# Call the function to manually add food (optional)
add_manual_food_optional()
# Call the function to manually add food and sum up the nutritional values
total_sum_expander()
# Function to search for more information about the selected food using SerpAPI
def search_user_input():
    st.markdown("<span style='font-size: 24px;'>Search for More Information</span>", unsafe_allow_html=True)
    user_input = st.text_input("What would you like to know about this food?", "")

    if user_input:
        query = display_name + " " + user_input

        params = {
            "q": query,
            "location": "United States",
            "hl": "en",
            "gl": "us",
            "api_key": SERPAPI_API_KEY
        }

        response = requests.get('https://serpapi.com/search', params=params)
        try:
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.write(response.text)
            return
        except Exception as err:
            st.error(f"An error occurred: {err}")
            return

        if "organic_results" in results:
            st.markdown("<h3>Search Results</h3>", unsafe_allow_html=True)
            for result in results["organic_results"]:
                title = result.get("title")
                link = result.get("link")
                if title and link:
                    st.markdown(f"[{title}]({link})")
        else:
            st.write("No results found.")

# Display the option to search for more information about the selected food
search_user_input()
meal_name = chatgpt_meal_name()
# Final nutritional totals and manual addition functionality has already been included in Part 3
if st.button("Add Meal to Journal"):
    # Prompt for date input
    if st.button("Today"):
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        date = st.date_input("Select the date you ate this food", datetime.today())

    # Save the meal to user.json when the date is selected
    if date:
        make_data_list(meal_name,date)
        st.success("Meal added to food journal!")
