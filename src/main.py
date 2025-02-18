import json
from datetime import datetime

from gemini_api_methods import initialize_model, upload_files
from prompt_generation_methods import create_prompt

if __name__ == '__main__':

    output_filepath = '../output/{}.json'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')))
    results = []

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0,
                             top_k=5,
                             top_p=0.5)
    upload_files()

    result_file_content = {
        'prompt_template': '',
        'curriculum_context': '',
        'pedagogy_context': '',
        'training_context': '',
        'predictions': []
    }

    try:
        prompt = create_prompt(grade=7,
                               subject='science',
                               topic='magnetism',
                               state='KA',
                               board='karnataka_state',
                               district='BLRURBAN',
                               block='BLRURBAN-NORTH')

        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)
        results.append(result_dict)
        result_file_content['predictions'] = results
        print('\n{}\n'.format(result_dict))
        with open(output_filepath, 'w') as f:
            json.dump(result_file_content, f)
    except Exception as e:
        print('****************\nException:\n{}\n***************'.format(e, e.__traceback__))
