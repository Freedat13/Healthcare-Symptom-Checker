### 🏥 Healthcare Symptom Checker (LLM-Powered)
This project implements a web-based Healthcare Symptom Checker, fulfilling the assignment objective of creating an application that takes symptom text input and outputs probable conditions and recommended next steps using a Large Language Model (LLM) for dynamic reasoning.

### 🎯 Project Objective
The primary goal is to demonstrate the integration of an LLM as a backend API service to provide educational, non-diagnostic health information based on user-provided symptoms. The system prioritizes safety, correctness, and high-quality LLM reasoning.

### ✨ Features
Dynamic LLM Analysis: Uses the Gemini API (gemini-2.5-flash) for sophisticated, context-aware analysis of symptom text, providing unique responses for every input.

Structured Output: The Python backend uses the Gemini API's JSON Schema capability to ensure the LLM output is consistently structured (probable_conditions, recommended_next_steps), making it easy for the frontend to parse and display.

Safety Focus: Includes a prominent, LLM-generated safety disclaimer in every response, emphasizing that the output is for educational purposes only.

Decoupled Architecture: Clean separation between the Python Flask backend (API) and the HTML/CSS/JavaScript frontend.

LLM Reasoning Trace: Displays a note on the LLM's reasoning quality/complexity for evaluation.

## 💻 Technical Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | Python, Flask, Google GenAI SDK, `python-dotenv` | Handles API requests, communicates with the Gemini LLM, and enforces structured JSON output. |
| **Frontend** | HTML5, CSS3, JavaScript | User interface for input, displays structured LLM output, handles AJAX communication. |
| **LLM Service** | Google Gemini API (`gemini-2.5-flash`) | The core reasoning engine that generates health suggestions and disclaimers. |


### ⚙️ Setup and Execution
### 1. Project Structure
Ensure your project directory contains these files:

symptom_checker/
├── main.py       # Python Backend (Flask + Gemini API, loads .env)

├── index.html    # HTML Frontend

├── style.css     # CSS Styling

├── script.js     # JavaScript Logic

├── .env          # Stores your secret API key (MUST be ignored by Git)

└── .gitignore    # Configured to ignore the .env file


### 2. Install Dependencies
Open your terminal or command prompt, navigate to the project directory, and install the required Python libraries.

pip install Flask Flask-CORS google-genai python-dotenv

### 3. Configure API Key (CRUCIAL STEP)
The Python backend securely loads your API key from a local file named .env.

Create a file named .env in your project root directory.

Add your Google AI API key to this file in the following format:

GEMINI_API_KEY='YOUR_API_KEY_HERE'

ex: GEMINI_API_KEY='AIzaSy...your-placeholder...XXX'

⚠️ CRITICAL: The example above uses a placeholder. Never commit your actual key to a public repository. The included .gitignore file prevents this by ignoring .env.

### ▶️ Execution
1. Run the Python Backend (Terminal 1)
Open your first terminal window, navigate to the project directory, and start the Flask server. This runs your API on port 5000.

python main.py
Keep this terminal window open and running.

2. Run the HTML Frontend (Browser)
Open the index.html file in your web browser.

start index.html
(or simply double-click the file in your file explorer)

3. Test the Application
Enter your symptoms (e.g., "Sharp headache behind the eyes and sensitivity to light").

Click the "Check Symptoms" button.

The JavaScript will send the request to the running Python API, the LLM will generate a structured response, and the results will populate the lists on the web page.



