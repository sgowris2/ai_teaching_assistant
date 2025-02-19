import json
from datetime import datetime
from pprint import pprint

from gemini_api_methods import initialize_model, upload_file
from metrics import get_dashboard_metrics
from prompt_generation_methods import create_analysis_prompt, create_postprocessing_prompt

if __name__ == '__main__':

    # Uncomment the one you want to run
    audio_file, grade, subject, topic, state, board, district, block = ('../data/hindi.mp3', 4, 'hindi', 'nouns', 'UP', 'UPMSP', 'Bijnor', 'Dhampur')
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/english.mp3', 3, 'english', 'speaking', 'TN', 'TNSB', 'Chennai', 'Adyar')
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/economics.mp3', 8, 'economics', 'consumer_literacy', 'DEL', 'CBSE', 'New Delhi', 'Saket')

    output_filepath = '../output/{}-{}.json'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')), subject)

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
            'predictions': {},
            'metrics': {}
        }
        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)
        result_file_content['predictions'] = result_dict
        stats = get_dashboard_metrics(result_file_content)
        result_file_content['metrics'] = stats

        suggestions_result = model.generate_content(create_postprocessing_prompt(result_file_content))
        suggestions_dict = json.loads(suggestions_result.text)
        suggestions = suggestions_dict['suggestions']
        result_file_content['suggestions'] = suggestions

        with open(output_filepath, 'w') as f:
            json.dump(result_file_content, f)
        pprint('\n{}\n'.format(result_dict))

    except Exception as e:
        print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))
