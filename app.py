from flask import Flask, request, render_template
app = Flask(__name__)

from model import summarize
from qgen import generate_fill_in_the_blank, generate_subjective_questions

@app.route('/')
def index():
    content = ''
    return render_template('index.html', content=content)

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['input_text']
    action = request.form['action']

    if action == 'generate_summary':
        # Clear previous summary and questions
        with open('file.txt', 'w') as new:
            pass
        with open('summary.txt', 'w') as file:
            pass

        # Write the text to the file
        with open('file.txt', 'w') as file:
            file.write(input_text)

        summarize(input_text)

        with open('summary.txt', 'r') as file:
            content = file.read()
        return render_template('index.html', content=content)

    elif action == 'generate_questions':
        with open('questions.txt', 'w') as file:
            pass
        # Generate subjective questions and fill-in-the-blank questions
        subjective_questions = (generate_subjective_questions(input_text))
        # fill_ups = generate_fill_in_the_blank(input_text)
        
        # Step 1: Join the list into a single string
        joined_string = ''.join(subjective_questions)

        # Step 2: Split the string by '?'
        sentences = joined_string.split('?')        

        # Step 3: Add '?' back to each sentence and trim whitespace
        sentences = [sentence.rstrip(',').strip() + '?' for sentence in sentences if sentence.strip()]
        
        # Write the generated questions to a file
        i = 1
        for ques in sentences:

            with open('questions.txt', 'a') as new:
                # new.write(questions_content)
                new.write(f'Ques {i}. {ques}\n')
                i+=1

        generated_ques= ''
        with open('questions.txt','r') as file:
            generated_ques = file.read()

        # return render_template('index.html', content=questions_content)
        return render_template('index.html', content=generated_ques)

    # If no valid action was provided, return an error or redirect
    return "Invalid action", 400  # Returning a 400 Bad Request response if the action is invalid

if __name__ == '__main__':
    app.run(debug=True)