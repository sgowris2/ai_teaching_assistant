import json
from datetime import datetime
from pprint import pprint
import os
import cv2

from gemini_api_methods import initialize_model, upload_file

def get_metadata_from_qr(image_filepath):

    image = cv2.imread(image_filepath)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is not None:
        print("QRCode data:")
        print(data)
    else:
        print("There was some error")
    metadata = json.loads(data)
    return metadata

if __name__ == '__main__':

    worksheet_filename = 'g3_maths_5.jpeg'

    #######################################################################################
    # System code below this #
    #######################################################################################

    with open('../data/formative_assessments/data.json', 'r') as f:
        data = json.load(f)

    with open('../data/formative_assessments/answer_keys.json', 'r') as f:
        answer_keys = json.load(f)

    worksheet_filepath = '../data/formative_assessments/{}'.format(worksheet_filename)

    metadata = get_metadata_from_qr(worksheet_filepath)

    worksheet_id = metadata['worksheet_id']
    student_id = metadata['student_id']
    subject = metadata['subject']
    worksheet_info = [x for x in answer_keys['worksheets'] if x['id'] == worksheet_id][0]
    answer_key = worksheet_info['answer_key']

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0,
                             top_k=5,
                             top_p=0.5)

    uploaded_file = upload_file(worksheet_filepath)

    prompt = '''
    
    You are a grader of worksheets. Provided is an image of a worksheet that has been filled by a student
    Grade the worksheet and provide output in the following JSON format: '
    {{
        "answers": [
                        {{
                            "ques_no": <string that uniquely identifies the question number like 1, 2a, etc.>, 
                            "answer": <string that shows the student's answer for that particular question exactly like it is if it is written by the student, if it is a multiple choice question, just show the options circled or ticked by the student>, 
                            "is_correct": <bool>,
                            "explanation": <string - if answer is wrong, give feedback on how to solve the problem and briefly explain the concept that is used to solve the problem>
                        }}, 
                        {{..}}
                    ]
    }}
    
    Use the following answer key that is in JSON format to say whether an answer is correct or not. 
    The field "q" refers to the question number, and the field "a" is the answer to that question. 
    Here is the answer key: 
    {answer_key}
    
    Rules for grading the worksheet:
    - Ignore minor spelling mistakes when scoring questions that have word answers written by students.
    - Grade answers that are in the "Answer:" field on the worksheet, or in the blanks "____" in the fill in the blanks questions, or for multiple choice questions, look for the child circling the options or putting a tick against them.
    - For multiple choice questions, the "ans" field in the output JSON should show the options selected by the student i.e. a or be or c
    - If a student leaves a question blank, then mark that as incorrect and provide an explanation on how to solve that problem.
    - The answers that are written in words may not match exactly with the answer key but it should have the 
    same meaning.
                                                  
    '''

    try:
        result = model.generate_content(contents=[prompt.format(answer_key=answer_key),
                                                  uploaded_file])
        result_dict = json.loads(result.text)
        student_score = sum([1 for x in result_dict['answers'] if x['is_correct']])
        total = len(result_dict['answers'])

        print('\nScore: {score}%\n\nAnswers:'.format(score=round(100*student_score/total)))
        pprint(result_dict)

    except Exception as e:
        print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))
