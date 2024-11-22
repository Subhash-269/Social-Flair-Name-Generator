import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Set up your OpenAI API key
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tags_with_openai(data):
    """Generate creative tags using OpenAI's Chat Completion API."""
    colors = ", ".join(data.get("color", []))
    celestial_objects = ", ".join(data.get("celestial_object", []))
    zodiac_signs = ", ".join(data.get("zodiac", []))
    star_names = ", ".join(data.get("starname", []))
    moods = ", ".join(data.get("mood", []))
    styles = ", ".join(data.get("style", []))

    # Construct the input message for the chat model
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in generating creative galaxy-themed tags. "
                "Generate 10 unique and creative tags based on the provided inputs. Should be short and concise."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Inputs:\n"
                f"Colors: {colors}\n"
                f"Celestial Objects: {celestial_objects}\n"
                f"Zodiac Signs: {zodiac_signs}\n"
                f"Star Names: {star_names}\n"
                f"Moods: {moods}\n"
                f"Styles: {styles}\n"
                f"Examples: CosmicCrimson, NebulaGlow, VegaTaurusPulse.\n"
                f"Please output the tags as a comma-separated list."
            ),
        },
    ]

    # Call OpenAI Chat Completion API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for better results
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            n=1,
        )
        # Extract the assistant's message
        raw_output = response["choices"][0]["message"]["content"].strip()
        tags = [tag.strip() for tag in raw_output.split(",") if tag.strip()]
        return tags[:10]  # Limit to 10 tags
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate-tags', methods=['POST'])
def generate_tags_api():
    """Generate tags based on user input."""
    data = request.json

    # Ensure required fields are present
    if not data.get("color") or not data.get("celestial_object"):
        return jsonify({"error": "Colors and Celestial Objects are required fields"}), 400

    # Generate tags using OpenAI
    tags = generate_tags_with_openai(data)
    return jsonify({"tags": tags})

if __name__ == '__main__':
    app.run(debug=True)
