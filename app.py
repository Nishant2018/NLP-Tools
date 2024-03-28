from flask import Flask, render_template, request
from transformers import pipeline
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static')

def generate_gpt3_text(text):
    generator = pipeline(task='text-generation', model='EleutherAI/gpt-neo-2.7B')
    generated_text = generator(text, max_length=200, num_return_sequences=1, truncation=True)
    return generated_text[0]['generated_text']

def generate_gpt2_text(prompt, max_length):
    generator = pipeline('text-generation', model='gpt2')
    generated_text = generator(prompt, max_length=max_length, num_return_sequences=1, truncation=True)
    return generated_text[0]['generated_text']

def translate_text_t5(prompt):
    translator = pipeline('translation_en_to_fr', model='t5-small')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def translate_text_english_to_hindi(prompt):
    translator = pipeline('translation_en_to_hi', model='Helsinki-NLP/opus-mt-en-hi')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    logging.debug(f'Generated text from GPT-3: {translated_text}')
    print('Translated Text (English to French):', translated_text)
    return translated_text

def translate_text_hindi_to_english(prompt):
    translator = pipeline('translation_hi_to_en', model='Helsinki-NLP/opus-mt-hi-en')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def translate_text_spanish_to_english(prompt):
    translator = pipeline('translation_es_to_en', model='Helsinki-NLP/opus-mt-es-en')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def translate_text_german_to_english(prompt):
    translator = pipeline('translation_de_to_en', model='Helsinki-NLP/opus-mt-de-en')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def translate_text_french_to_english(prompt):
    translator = pipeline('translation_fr_to_en', model='Helsinki-NLP/opus-mt-fr-en')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def translate_text_chinese_to_english(prompt):
    translator = pipeline('translation_zh_to_en', model='Helsinki-NLP/opus-mt-zh-en')
    translated_text = translator(prompt, max_length=100)[0]['translation_text']
    return translated_text

def generate_long_content(input_text):
    summarizer = pipeline('summarization', model='t5-small')
    input_format = "summarize: {}".format(input_text)
    generated_summary = summarizer(input_format, max_length=210, num_return_sequences=1, truncation=True)
    output_summary = generated_summary[0]['summary_text']
    return output_summary

def generate_text_bert(prompt):
    generator = pipeline('fill-mask', model='bert-base-uncased')
    generated_text = generator(prompt)
    generated_sequences = [result['sequence'] for result in generated_text]
    return generated_sequences

@app.route('/', methods=['GET', 'POST'])
def home():
    generated_text = ''
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            model_type = request.form['model_type']

            logging.debug(f'Prompt received: {prompt}')
            logging.debug(f'Model type selected: {model_type}')

            if model_type == 'gpt3':
                generated_text = generate_gpt3_text(prompt)
                logging.debug(f'Generated text from GPT-3: {generated_text}')
            elif model_type == 'gpt2':
                max_length = int(request.form['max_length'])
                generated_text = generate_gpt2_text(prompt, max_length)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_en_to_fr':
                max_length = int(request.form['max_length'])
                generated_text = translate_text_t5(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_en_to_hi':
                generated_text = translate_text_english_to_hindi(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_hi_to_en':
                generated_text = translate_text_hindi_to_english(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_es_to_en':
                generated_text = translate_text_spanish_to_english(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_de_to_en':
                generated_text = translate_text_german_to_english(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_fr_to_en':
                generated_text = translate_text_french_to_english(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'translation_zh_to_en':
                generated_text = translate_text_chinese_to_english(prompt)
                logging.debug(f'Generated text from GPT-2: {generated_text}')
            elif model_type == 'summarization':
                generated_text = generate_long_content(prompt)
                logging.debug(f'Generated text from T5: {generated_text}')
            elif model_type == 'Text_bert':
                generated_text = generate_text_bert(prompt)
                logging.debug(f'Generated text from BERT: {generated_text}')

        except Exception as e:
            logging.error(f'An error occurred: {str(e)}')

        return render_template('index.html', prompt=prompt, generated_text=generated_text)

    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)