import json
import os
from datetime import datetime

from formative_assessments.prompt_engine import get_prompt_template
from formative_assessments.qr_reader import get_metadata_from_qr
from formative_assessments.analysis import class_analysis
from gemini_api_methods import initialize_model, upload_file

RUN_AUTOGRADING = False
SCHOOL_ID = 1
CLASS_ID = 1
WORKSHEET_IMAGES_DIR = '../data/formative_assessments/g3_maths'
WORKSHEET_ID = 1


def initialize_student_data():
    with open('../data/formative_assessments/data.json', 'r') as f:
        data = json.load(f)
    school_data = [x for x in data['schools'] if x['id'] == SCHOOL_ID][0]
    class_data = [x for x in school_data['classes'] if x['id'] == CLASS_ID][0]
    students_data = [x for x in class_data['students']]
    return school_data, class_data, students_data


def get_answer_key(worksheet_id: int):
    with open('../data/formative_assessments/answer_keys.json', 'r') as f:
        answer_keys = json.load(f)
    worksheet_info = [x for x in answer_keys['worksheets'] if x['id'] == worksheet_id][0]
    ak = worksheet_info['answer_key']
    return ak


def run_auto_grading(filepaths, output_filepath):
    school_data, class_data, students_data = initialize_student_data()
    fa_results = {'school': school_data['name'],
                  'class': class_data['name'],
                  'date': datetime.strftime(datetime.now(), format('%d%b-%H%M')),
                  'worksheet_id': WORKSHEET_ID,
                  'subject': 'maths',
                  'scores': {}
                  }
    for filepath in filepaths:
        metadata = get_metadata_from_qr(filepath)
        worksheet_id = metadata['worksheet_id']
        student_id = metadata['student_id']
        subject = metadata['subject']
        student_data = [x for x in students_data if x['id'] == student_id][0]
        answer_key = get_answer_key(worksheet_id)
        uploaded_file = upload_file(filepath)
        prompt = get_prompt_template()
        try:
            result = model.generate_content(contents=[prompt.format(answer_key=answer_key), uploaded_file])
            result_dict = json.loads(result.text)
            student_score = sum([1 for x in result_dict['answers'] if x['is_correct']])
            total = len(result_dict['answers'])
            student_percent = round(100 * student_score / total)
            print('{student_name}: {score}%'.format(student_name=student_data['name'], score=student_percent))
            fa_results['scores'][student_id] = {
                'name': student_data['name'],
                'score': student_score,
                'out_of': total,
                'percent': student_percent,
                'answers': result_dict['answers']
            }
        except Exception as e:
            print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))
    with open(output_filepath, 'w') as f:
        json.dump(fa_results, f)


if __name__ == '__main__':

    results_filepath = '../output/formative_assessment_{}.json'.format(WORKSHEET_ID)

    if RUN_AUTOGRADING:
        worksheet_files = [x for x in os.listdir(WORKSHEET_IMAGES_DIR) if x.endswith('.jpeg')]
        if len(worksheet_files) == 0:
            raise Exception('No files found in worksheet directory')
        worksheet_filepaths = [os.path.join(WORKSHEET_IMAGES_DIR, x) for x in worksheet_files]

        model = initialize_model(name='gemini-2.0-flash',
                                 temperature=0,
                                 top_k=5,
                                 top_p=0.5)
        run_auto_grading(worksheet_filepaths, results_filepath)

    class_analysis(results_filepath)
