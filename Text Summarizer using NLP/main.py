from flask import Flask, render_template, request
from text_summarizer import preprocess_text, calculate_word_frequencies, calculate_sentence_scores, generate_summary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None

    if request.method == 'POST':
        try:
            if 'text' in request.form:
                text = request.form['text'].strip()
            elif 'fileInput' in request.files:
                file = request.files['fileInput']
                if file.filename.endswith(('.txt', '.doc', '.docx', '.pdf')):
                    text = file.read().decode('utf-8')
                else:
                    error = "Unsupported file format"
            else:
                error = "No text or file provided"

            if not error and text and not text.isspace():
                sentence_list, filtered_words = preprocess_text(text)
                frequency_map = calculate_word_frequencies(filtered_words)
                sent_score = calculate_sentence_scores(sentence_list, frequency_map)
                num_sentences = int(request.form.get('numSentences', 10))
                summary = generate_summary(sent_score, num_sentences=num_sentences)

        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', summary=summary, error=error)


if __name__ == '__main__':
    app.run(debug=True)
