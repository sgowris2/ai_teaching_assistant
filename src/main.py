import json
from datetime import datetime

from gemini_api_methods import initialize_model, upload_all_files, upload_file
from prompt_generation_methods import create_prompt

if __name__ == '__main__':

    output_filepath = '../output/{}.json'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')))
    results = []

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    upload_file('../data/hindi.mp3')

    try:
        prompt = create_prompt(grade=4,
                               subject='hindi',
                               topic='nouns',
                               state='KA',
                               board='karnataka_state',
                               district='BLRURBAN',
                               block='BLRURBAN-NORTH')

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
