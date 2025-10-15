// script.js (JavaScript Frontend Logic)
document.addEventListener('DOMContentLoaded', () => {
    const checkBtn = document.getElementById('check-btn');
    const symptomsTextarea = document.getElementById('symptoms');
    const resultsDiv = document.getElementById('results');
    const conditionsList = document.getElementById('conditions-list');
    const stepsList = document.getElementById('steps-list');
    const disclaimerText = document.getElementById('disclaimer-text');
    const reasoningText = document.getElementById('reasoning-text');
    const loadingDiv = document.getElementById('loading');

    // 💡 IMPORTANT: This URL must match the Flask server's address and port (5000 is default).
    const API_ENDPOINT = 'http://127.0.0.1:5000/check_symptoms'; 

    checkBtn.addEventListener('click', async () => {
        const symptoms = symptomsTextarea.value.trim();

        if (symptoms === "") {
            // Use a custom message box instead of alert()
            displayMessage('Please enter your symptoms to proceed.', 'error');
            return;
        }

        // Show loading state
        resultsDiv.classList.add('hidden');
        loadingDiv.classList.remove('hidden');

        try {
            // Frontend making the API call to the Python Backend
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symptoms: symptoms })
            });

            if (!response.ok) {
                // Read the error message from the backend if available
                const errorData = await response.json().catch(() => ({ error: 'Unknown server error.' }));
                throw new Error(`Server responded with status ${response.status}: ${errorData.error || 'Check server logs.'}`);
            }

            const data = await response.json();
            
            // --- Populate results (Output: Probable conditions + recommended next steps) ---
            
            // Conditions
            conditionsList.innerHTML = '';
            data.probable_conditions.forEach(condition => {
                const li = document.createElement('li');
                li.textContent = condition;
                conditionsList.appendChild(li);
            });

            // Next Steps
            stepsList.innerHTML = '';
            data.recommended_next_steps.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                stepsList.appendChild(li);
            });
            
            // Set safety disclaimers (Evaluation Focus: Safety Disclaimers)
            disclaimerText.innerHTML = data.safety_disclaimer;
            
            // Set LLM reasoning quality (Evaluation Focus: LLM Reasoning Quality)
            reasoningText.textContent = data.reasoning;

            // Show results
            resultsDiv.classList.remove('hidden');

        } catch (error) {
            console.error('Error fetching data:', error);
            displayMessage(`Could not connect to the API or an error occurred: ${error.message}. Please ensure the Python server is running and the API key is set.`, 'fatal');
        } finally {
            // Hide loading state
            loadingDiv.classList.add('hidden');
        }
    });
    
    function displayMessage(message, type) {
        // Simple function to display temporary messages (instead of alert)
        let msgBox = document.getElementById('message-box');
        if (!msgBox) {
            msgBox = document.createElement('div');
            msgBox.id = 'message-box';
            msgBox.style.cssText = `
                position: fixed; top: 10px; left: 50%; transform: translateX(-50%); 
                padding: 10px 20px; border-radius: 8px; z-index: 1000; 
                color: white; font-weight: bold; transition: opacity 0.5s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            `;
            document.body.appendChild(msgBox);
        }
        
        msgBox.textContent = message;
        msgBox.style.opacity = 1;
        
        if (type === 'error' || type === 'fatal') {
            msgBox.style.backgroundColor = '#dc3545';
        } else {
            msgBox.style.backgroundColor = '#007bff';
        }

        setTimeout(() => {
            msgBox.style.opacity = 0;
            setTimeout(() => msgBox.remove(), 500);
        }, 5000);
    }
});
