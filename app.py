import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Set up your OpenAI API key
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

def generate_tags_with_openai(data):
    """Generate creative tags using OpenAI's Chat Completion API."""
    theme = data.get("theme", "custom")
    colors = ", ".join(data.get("color", []))
    moods = ", ".join(data.get("mood", []))
    hobbies = ", ".join(data.get("hobbies", []))
    adjectives = ", ".join(data.get("adjectives", []))
    food_drinks = ", ".join(data.get("food_drinks", []))
    fantasy_mythology = ", ".join(data.get("fantasy_mythology", []))

    print("Debug - Input Data for OpenAI:")
    print(f"Theme: {theme}, Colors: {colors}, Moods: {moods}, Hobbies: {hobbies}, Adjectives: {adjectives}, Food/Drinks: {food_drinks}, Fantasy/Mythology: {fantasy_mythology}")

    # Construct the input message for the chat model
    messages = [
        {
            "role": "system",
            "content": (
                f"You are an expert in generating creative '{theme}'-themed tags. "
                "Generate 10 unique and creative tags based on the provided inputs. Should be short and concise."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Inputs:\n"
                f"Colors: {colors}\n"
                f"Moods: {moods}\n"
                f"Hobbies: {hobbies}\n"
                f"Adjectives: {adjectives}\n"
                f"Food/Drinks: {food_drinks}\n"
                f"Fantasy/Mythology: {fantasy_mythology}\n"
                f"Examples: SuperCoder, MysticVoyager, StarryLatte.\n"
                f"Please output the tags as a comma-separated list."
            ),
        },
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            n=1,
        )
        raw_output = response["choices"][0]["message"]["content"].strip()
        tags = [tag.strip() for tag in raw_output.split(",") if tag.strip()]
        return tags[:10]  # Limit to 10 tags
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return [f"Error: {str(e)}"]


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate-tags', methods=['POST'])
def generate_tags_api():
    """Generate tags based on user input."""
    data = request.json
    print("Received data from frontend:", data)

    # Ensure at least one attribute is present
    if not any([data.get("color"), data.get("mood"), data.get("hobbies"),
                data.get("adjectives"), data.get("food_drinks"), data.get("fantasy_mythology")]):
        return jsonify({"error": "At least one attribute must be provided"}), 400

    # Generate tags using OpenAI
    tags = generate_tags_with_openai(data)
    print("Generated Tags:", tags)
    return jsonify({"tags": tags})


if __name__ == '__main__':
    print(openai.api_key)
    app.run(debug=True)
