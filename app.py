# Flask file

# Settimg up flask
from flask import Flask, redirect,request, render_template, url_for
app = Flask(__name__)

from model import summarize

global input_text
input_text = ''

@app.route('/')
def index():
    
    content = ''
    # Pass the content to the HTML template
    return render_template('index.html', content=content)


@app.route('/button-click' , methods=['GET', 'POST'])
def button_click():

    print("Button clicked!")
    
    # Ensuring bith files are free of any previous text
    with open('file.txt', 'w') as file:
        pass
    with open('summary.txt', 'w') as file:
        pass

    if request.method == 'POST':
        # Get the text from the form input
        input_text = request.form['input_text']

        # Write the text to the file
        with open('file.txt', 'w') as file:
            file.write(input_text)

        summarize(input_text) 


    with open('summary.txt','r') as file:
        content = file.read()

    return render_template('index.html',content=content )


        
    # Clearing the 'summary.txt' file
    # with open('summary.txt','w') as new:
    #     pass # The pass keyword will delet all the text in the file
     
    # Summarize text
    # summarize(input_text)

    # Get text from 'summary.txt'
    # with open('summary.txt','r') as file:
    #       content = file.read()

    return render_template('index.html', content=input_text)  # Redirect back to the index page


if __name__ == '__main__':
     app.run(debug=True)
      