from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import numpy as np
import cv2
import base64
from PIL import Image
import io

from formative_assessments.fa_main import get_answer_key
from src.formative_assessments.qr_reader import get_metadata_from_qr
from src.formative_assessments.fa_main import get_prompt_template, initialize_student_data
from src.gemini_api_methods import initialize_model, upload_file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def get_worksheets():
    with open('.data/answer_keys.json', 'r') as f:
        worksheets = json.load(f)
    return worksheets


def grade_worksheet(images: list):
    if not images:
        return jsonify({'error': 'No images provided'}), 400
    try:
        output_dict = dict()
        school_data, class_data, students_data = initialize_student_data('data/database.json')
        model = initialize_model(name='gemini-2.0-flash',
                                 temperature=0,
                                 top_k=5,
                                 top_p=0.5)
        try:
            for image_dict in images:
                image_bytes: bytes = image_dict['binary']
                image_array = np.frombuffer(image_bytes, dtype=np.uint8)
                img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                if img is None:
                    return jsonify({'error': 'Invalid image'}), 400
                metadata = get_metadata_from_qr(img)
                worksheet_id = metadata['worksheet_id']
                student_id = metadata['student_id']
                subject = metadata['subject']
                student_data = [x for x in students_data if x['id'] == student_id][0]
                prompt = get_prompt_template()
                answer_key = get_answer_key(worksheet_id, 'data/answer_keys.json')
                saved_filepath = 'uploaded_images/w{}-s{}-{}.{}'.format(worksheet_id, student_id,
                                                                        datetime.now().strftime('%Y%m%d%H%M'),
                                                                        image_dict['name'].split('.')[-1])
                image_file = Image.open(io.BytesIO(image_bytes))
                image_file.save(saved_filepath)
                uploaded_file = upload_file(saved_filepath)
                result = model.generate_content(contents=[prompt.format(answer_key=answer_key), uploaded_file])
                result_dict = json.loads(result.text)
                student_score = sum([1 for x in result_dict['answers'] if x['is_correct']])
                total = len(result_dict['answers'])
                student_percent = round(100 * student_score / total)
                student_output = {
                    'student_id': student_id,
                    'student_name': student_data['name'],
                    'grade': student_data['grade'],
                    'section': student_data['section'],
                    'subject': subject,
                    'date': datetime.now().isoformat(),
                    'score': student_score,
                    'out_of': total,
                    'percent': student_percent,
                    'answers': result_dict['answers'],
                    'insights': result_dict['insights']
                }
                if worksheet_id not in output_dict:
                    output_dict[worksheet_id] = [student_output]
                else:
                    output_dict[worksheet_id].append(student_output)
        except Exception as e:
            print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))

    except Exception as e:
        print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))
        raise e

    return output_dict


@app.route('/api/worksheets', methods=['GET'])
def get_all_worksheets():
    return get_worksheets()


@app.route('/api/autograde', methods=['POST'])
def autograde_worksheet():
    print("Received request to autograde worksheet")
    if not request.is_json:
        images = request.files.getlist('images')
        if not images:
            return jsonify({'error': 'No images provided'}), 400
        images = [{'name': x.filename, 'type': x.content_type, 'binary': x.read()} for x in images]
    else:
        images_data = request.get_json()['body']['images']
        images = [{'name': x['name'], 'type': x['type'], 'binary': io.BytesIO(base64.b64decode(x['data'])).getvalue()} for x
                  in images_data]
    result = grade_worksheet(images)
    print(result)
    return result


if __name__ == '__main__':
    app.run(debug=True, port=10000)
