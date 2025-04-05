import json
from datetime import datetime
from pprint import pprint
import os

from gemini_api_methods import initialize_model, upload_file
from class_recording.metrics import get_dashboard_metrics
from class_recording.prompt_generation_methods import create_analysis_prompt, create_postprocessing_prompt

if __name__ == '__main__':

    # Uncomment the one you want to run
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/hindi.mp3', 4, 'hindi', 'nouns', 'UP', 'UPMSP', 'Bijnor', 'Dhampur')
    # audio_file, grade, subject, topic, state, board, district, block = ('../data/english.mp3', 3, 'english', 'speaking', 'TN', 'TNSB', 'Chennai', 'Adyar')
    audio_file, grade, subject, topic, state, board, district, block = ('../data/economics.mp3', 8, 'economics', 'consumer_literacy', 'DEL', 'CBSE', 'New Delhi', 'Saket')

    output_dir = '../output/{}-{}'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')), subject)
    transcript_filepath = os.path.join(output_dir, 'transcript.txt')
    prompt_filepath = os.path.join(output_dir, 'prompt.txt')
    results_filepath = os.path.join(output_dir, 'results.json')
    os.mkdir(output_dir)

    model = initialize_model(name='gemini-1.5-pro',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    uploaded_file = upload_file(audio_file)

    try:
        result = model.generate_content(contents=['Create a transcript of this audio file in JSON format {"transcript": <transcript text>}',
                                                  uploaded_file])
        transcript_dict = json.loads(result.text)
        transcript = transcript_dict['transcript']
        with open(transcript_filepath, 'w') as f:
            f.write(transcript)

        prompt = create_analysis_prompt(grade=grade,
                                        subject=subject,
                                        topic=topic,
                                        state=state,
                                        board=board,
                                        district=district,
                                        block=block)
        with open(prompt_filepath, 'w') as f:
            f.write(prompt)

        result = model.generate_content(contents=[prompt, transcript, uploaded_file])
        result_dict = json.loads(result.text)
        stats = get_dashboard_metrics(result_dict)
        result_file_content = {'predictions': result_dict, 'metrics': stats}
        suggestions_result = model.generate_content(create_postprocessing_prompt(result_file_content))
        suggestions_dict = json.loads(suggestions_result.text)
        suggestions = suggestions_dict['suggestions']
        result_file_content['suggestions'] = suggestions

        with open(results_filepath, 'w') as f:
            json.dump(result_file_content, f)
        pprint('\n{}\n'.format(result_dict))

    except Exception as e:
        print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))
