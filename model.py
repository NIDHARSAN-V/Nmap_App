from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load T5 model and tokenizer
try:
    tokenizer = T5Tokenizer.from_pretrained('./t5_nmap_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('./t5_nmap_model')
except Exception as e:
    print(f"Error loading tokenizer or model: {e}")
    exit(1)

# Route for generating Nmap commands
@app.route('/generate_command', methods=['POST'])
def generate_command():
    data = request.json
    input_query = data.get('query', '')

    # Check if query is empty
    if not input_query.strip():
        return jsonify({"error": "Empty query provided."}), 400

    try:
        # Generate command from input query
        inputs = tokenizer.encode("translate English to Commands: " + input_query, return_tensors="pt")
        outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
        predicted_command = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the generated command
        return jsonify({
            "input_query": input_query,
            "predicted_command": predicted_command
        })
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": f"Error during processing: {e}"}), 500

# Route for generating Nmap descriptions
@app.route('/nmapdesc', methods=['POST'])
def nmap_desc():
    data = request.json
    nmap_command = data.get('query', '')

    # Check if query is empty
    if not nmap_command.strip():
        return jsonify({"error": "Empty query provided."}), 400

    try:
        # Generate Nmap description using Google Generative AI
        genai.configure(api_key="AIzaSyBgeZPkT58EUUz3fA4LF8-XzvtR_9wcdp0")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Explain the Nmap command: {nmap_command}")
        
        print(response.text)

        # Return the Nmap description
        return jsonify({
            "input_query": nmap_command,
            "nmapdesc": response.text
        })
    except Exception as e:
        print(f"Error during description generation: {e}")
        return jsonify({"error": f"Error during description generation: {e}"}), 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
