# from transformers import T5Tokenizer, T5ForConditionalGeneration
# from transformers import BartTokenizer, BartForConditionalGeneration
from haystack.nodes import QuestionGenerator # type: ignore
import random
import nltk
from nltk.tokenize import word_tokenize
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering



# Function to generate fill-in-the-blank questions from a given text
def generate_fill_in_the_blank(text, num_blanks_per_question=1, num_questions=2):
    # """
    # Generate multiple fill-in-the-blank questions from a given text by replacing key information with blanks.

    # Parameters:
    # - text (str): The input text from which to generate the fill-in-the-blank questions.
    # - num_blanks_per_question (int): The number of blanks to create in each question. Default is 1.
    # - num_questions (int): The number of different fill-in-the-blank questions to generate. Default is 3.

    # Returns:
    # - list[str]: A list of generated fill-in-the-blank questions.
    # """
    words = word_tokenize(text)
    fill_in_the_blank_questions = []
    
    for _ in range(num_questions):
        # Create a copy of the words to work with for each question
        words_copy = words.copy()
        blanks = random.sample(words_copy, num_blanks_per_question)
        
        fill_in_the_blank_text = text
        for blank in blanks:
            # Replace the selected word with a blank
            fill_in_the_blank_text = fill_in_the_blank_text.replace(blank, '_____')
        
        fill_in_the_blank_questions.append(fill_in_the_blank_text)
    
    return fill_in_the_blank_questions



def generate_subjective_questions(text, num_questions = 5):

    

    # Initialize the Haystack Question Generator
    generator = QuestionGenerator(model_name_or_path="valhalla/t5-small-qg-hl")

    def generate_questions(text: str):
        try:
            # Generate questions from the input text
            questions = generator.generate(text)
            return questions
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []


    ques = generate_questions(text)   
    return ques




if __name__ == "__main__":
    
    generate_fill_in_the_blank()
    generate_subjective_questions()
    