from haystack.nodes import QuestionGenerator


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

    generate_subjective_questions()
    