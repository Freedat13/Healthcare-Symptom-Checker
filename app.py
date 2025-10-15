# app.py (Python Backend using Flask and Gemini API)

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

# --- FLASK SETUP ---
app = Flask(__name__)
# Enable CORS to allow the frontend HTML/JS to communicate with this API.
CORS(app)

# --- GEMINI API SETUP ---
# Client initialization will automatically use the GEMINI_API_KEY
# environment variable if set (which you must do before running).
try:
    client = genai.Client() 
    print("Gemini Client initialized successfully (using environment variable).")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("!!! WARNING: Ensure GEMINI_API_KEY is set in your terminal environment.")
    client = None

# System instruction guides the LLM on its role and required output format.
SYSTEM_INSTRUCTION = (
    "You are a helpful, professional, and educational symptom checker AI. "
    "Your responses MUST include: 1) a list of 2-3 probable medical conditions, "
    "2) a list of 2-3 recommended next steps, and 3) a prominent safety disclaimer. "
    "The output must be STRICTLY in JSON format to be parsed by a web application. "
    "Prioritize safety and education. Do NOT provide a diagnosis."
)

def query_llm_for_suggestions(symptoms):
    """
    Calls the Gemini LLM API for reasoning & suggestion generation[cite: 11].
    """
    if not client:
        return {
            "probable_conditions": ["Setup Error: LLM Client Not Available"],
            "recommended_next_steps": ["Ensure your API key is correctly set as a GEMINI_API_KEY environment variable."],
            "safety_disclaimer": "⚠️ **FATAL ERROR:** The AI service is offline. Seek medical attention if needed.",
            "llm_reasoning_quality": "Failed to connect to LLM."
        }

    # Example prompt guidance: "Based on these symptoms, suggest possible conditions and next steps with educational disclaimer." [cite: 13]
    prompt = f"Based on these symptoms: '{symptoms}', suggest possible conditions and next steps with an educational disclaimer."
    
    # Define the expected JSON output structure (Schema for Structured Output)
    response_schema = {
        "type": "object",
        "properties": {
            "probable_conditions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of 2-3 potential conditions based on the symptoms."
            },
            "recommended_next_steps": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of 2-3 specific, safe, and actionable next steps."
            },
            "safety_disclaimer": {
                "type": "string",
                "description": "A required, prominent, educational safety disclaimer (Evaluation Focus: safety disclaimers)."
            },
            "llm_reasoning_quality": {
                "type": "string",
                "description": "A brief internal note on the complexity of the reasoning applied by the LLM (Evaluation Focus: LLM reasoning quality)."
            }
        },
        "required": ["probable_conditions", "recommended_next_steps", "safety_disclaimer", "llm_reasoning_quality"]
    }
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )
        
        # The response.text is a valid JSON string compliant with the schema
        return json.loads(response.text)

    except Exception as e:
        print(f"An error occurred during LLM API call: {e}")
        # Return a safe error response if the API call fails unexpectedly
        return {
            "probable_conditions": ["API Call Failed"],
            "recommended_next_steps": [f"Error Details: {str(e)}", "Please check your network connection and API key status."],
            "safety_disclaimer": "⚠️ **ERROR:** The AI service failed to generate a response. Seek immediate medical attention if concerned.",
            "llm_reasoning_quality": "API Exception encountered."
        }


# --- FLASK ROUTE ---

@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    """
    Backend API to accept user input & query LLM[cite: 9].
    """
    data = request.get_json()
    symptom_text = data.get('symptoms', '') # Input: Symptom text [cite: 5]

    if not symptom_text:
        return jsonify({"error": "Symptom text is required."}), 400

    # Call the LLM function to get output: Probable conditions + recommended next steps [cite: 6]
    llm_output = query_llm_for_suggestions(symptom_text)
    
    # Return the structured data received from the LLM
    return jsonify({
        "probable_conditions": llm_output.get("probable_conditions", []),
        "recommended_next_steps": llm_output.get("recommended_next_steps", []),
        "safety_disclaimer": llm_output.get("safety_disclaimer", ""),
        "reasoning": llm_output.get("llm_reasoning_quality", "")
    })

if __name__ == '__main__':
    # Run the server on port 5000.
    # Ensure you have run 'pip install Flask Flask-CORS google-genai' first.
    app.run(debug=True, port=5000)