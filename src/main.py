import json
from datetime import datetime

from gemini_api_methods import initialize_model, upload_all_files, upload_file
from prompt_generation_methods import create_analysis_prompt

if __name__ == '__main__':

    # Uncomment the one you want to run
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/hindi.mp3', 4, 'hindi', 'nouns', 'UP', 'UPMSP', 'Bijnor', 'Dhampur')
    audio_file, grade, subject, topic, state, board, district, block = ('../data/english.mp3', 3, 'english', 'speaking', 'TN', 'TNSB', 'Chennai', 'Adyar')
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/economics.mp3', 8, 'economics', 'consumer_literacy', 'DEL', 'CBSE', 'New Delhi', 'Saket')

    output_filepath = '../output/{}.json'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')))
    results = []

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    upload_file(audio_file)

    try:
        prompt = create_analysis_prompt(grade=grade,
                                        subject=subject,
                                        topic=topic,
                                        state=state,
                                        board=board,
                                        district=district,
                                        block=block)

        result_file_content = {
            'prompt': prompt,
            'predictions': []
        }
        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)
        results.append(result_dict)
        result_file_content['predictions'] = results
        print('\n{}\n'.format(result_dict))
        with open(output_filepath, 'w') as f:
            json.dump(result_file_content, f)
    except Exception as e:
        print('****************\nException:\n{}\n***************'.format(e, e.__traceback__))
