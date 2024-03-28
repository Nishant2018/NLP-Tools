---

### Description

This Flask web application includes a new feature to generate text using the BERT model. The `generate_text_bert` function utilizes the Hugging Face Transformers library to perform masked language modeling, generating text based on a provided prompt.

### How to Use

1. **Integration Steps:**
   - Import the necessary libraries, including Flask and Transformers, into your Python environment.
   - Define the `generate_text_bert` function within your Flask app or Python script.
   - Call the `generate_text_bert` function with a prompt to generate text using the BERT model.

2. **Flask App Integration:**
   - Ensure that your Flask app includes the `generate_text_bert` function.
   - Modify your Flask routes to handle POST requests for BERT text generation.
   - Create a form in your HTML template to capture the user's prompt input and model type selection.
   - Display the generated text on the frontend using the appropriate template variables.

3. **Example Code Snippet:**
   ```python
   from flask import Flask, render_template, request
   from transformers import pipeline

   app = Flask(__name__)

   # Function to generate text using BERT
   def generate_text_bert(prompt):
       generator = pipeline('fill-mask', model='bert-base-uncased')
       generated_text = generator(prompt)
       generated_sequences = [result['sequence'] for result in generated_text]
       return generated_sequences

   @app.route('/', methods=['GET', 'POST'])
   def home():
       generated_text = ''
       if request.method == 'POST':
           prompt = request.form['prompt']
           model_type = request.form['model_type']
           if model_type == 'BERT Text Generation':
               generated_text = generate_text_bert(prompt)
               return render_template('index.html', prompt=prompt, generated_text=generated_text)
       return render_template('index.html', generated_text=generated_text)

   if __name__ == '__main__':
       app.run(debug=True)
   ```

4. **Dependencies:**
   - Python 3.x
   - Flask
   - Hugging Face Transformers

5. **Usage Example:**
   - Launch the Flask app locally.
   - Access the web interface, enter a prompt, and select 'BERT Text Generation' to generate text using the BERT model.

---
