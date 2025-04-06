import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend


def class_analysis(results_filepath: str):

    with open(results_filepath, 'r') as f:
        results = json.load(f)

    school = results['school']
    class_name = results['class']
    date = results['date']
    worksheet_id = results['worksheet_id']
    subject = results['subject']
    scores_dict = results['scores']

    average_class_score = np.mean([x['score'] for x in scores_dict.values()])
    average_class_percent = np.mean([x['percent'] for x in scores_dict.values()])
    percent_scores_by_student = [x['percent'] for i, x in scores_dict.items()]
    scores_by_question = dict()
    for i, student in scores_dict.items():
        for a in student['answers']:
            if a['ques_no'] not in scores_by_question:
                scores_by_question[a['ques_no']] = [1 if a['is_correct'] else 0]
            else:
                scores_by_question[a['ques_no']].append(1 if a['is_correct'] else 0)
    common_mistakes = [(i, 100 - (round(100* sum(x) // len(x)))) for i, x in scores_by_question.items() if sum(x) <= (len(x) * 0.7)]
    students_in_focus = {k: v for k, v in scores_dict.items() if v['percent'] <= 50}


    # Visualize Results

    plt.figure(figsize=(12, 8))
    ax1_1 = plt.subplot(3, 4, 1)
    ax1_2 = plt.subplot(3, 4, 2)
    ax2 = plt.subplot(3, 4, (3, 4))
    pie_ax = {}
    for i in range(0, len(common_mistakes)):
        pie_ax[i] = plt.subplot(3, len(common_mistakes), i + 7)
    ax6 = plt.subplot(3, 1, 3)

    ax1_1.set_axis_off()
    ax1_1.set_title('Avg. Percentage')
    ax1_1.text(0.18, 0.4, '{}%'.format(average_class_percent), fontsize=32)
    ax1_2.set_axis_off()
    ax1_2.set_title('Avg. Score')
    ax1_2.text(0.28, 0.4, '{}'.format(average_class_score), fontsize=28)
    ax1_2.text(x=0.2, y=0.22, s='out of {}'.format(len(scores_by_question.keys())), fontsize=18)
    ax2.hist(percent_scores_by_student, bins=10)
    ax2.set_title('Scores Distribution (%)')
    ax2.set_xlabel('Score (%)')
    ax2.set_ylabel('# Students')
    for i in range(0, len(common_mistakes)):
        unique_values, counts = np.unique(scores_by_question[common_mistakes[i][0]], return_counts=True)
        pie_ax[i].pie(counts,
                      colors=['red', 'green'],
                      autopct='%1.0f%%',
                      startangle=90)
        pie_ax[i].set_title('Question {}'.format(common_mistakes[i][0]))
    ax6.set_axis_off()
    ax6.set_title('Students In Focus')
    student_names = ''
    for x in students_in_focus.values():
        student_names += '{} - {}%\n'.format(x['name'], x['percent'])
    ax6.text(0.4, 0.2, student_names, fontsize=20)


    plt.subplots_adjust(wspace=0.4, hspace=0.5)
    plt.show()
