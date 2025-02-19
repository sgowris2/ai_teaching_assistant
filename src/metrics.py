import json
import matplotlib.pyplot as plt


def get_dashboard_metrics(result_filepath: str):

    with open(result_filepath, 'r') as f:
        results = json.load(f)['predictions']

    pedagogy_score, pedagogy_strengths, pedagogy_areas_of_improvement \
        = _calculate_pedagogy_score(results['pedagogy_metrics'])

    lesson_completion_score, lesson_quality_score, missed_topics \
        = _calculate_lesson_plan_completion(results['lesson_plan_metrics'])

    teaching_guidelines_score, teaching_guidelines_strengths, teaching_guidelines_areas_of_improvement, teaching_guidelines_missed \
        = _calculate_teaching_guidelines_score(results['teaching_guidelines_metrics'])

    metrics = {
        "pedagogy_score": pedagogy_score,
        "pedagogy_strengths": pedagogy_strengths,
        "pedagogy_areas_of_improvements": pedagogy_areas_of_improvement,
        "lesson_completeness": lesson_completion_score,
        "missed_topics": missed_topics,
        "lesson_quality_score": lesson_quality_score,
        "teaching_guidelines_score": teaching_guidelines_score,
        "teaching_guidelines_strengths": teaching_guidelines_strengths,
        "teaching_guidelines_areas_of_improvement": teaching_guidelines_areas_of_improvement,
        "teaching_guidelines_missed": teaching_guidelines_missed,
        "overall_score": round((pedagogy_score + (2 * lesson_quality_score) + teaching_guidelines_score) / 4, 0)
    }

    return metrics


def _calculate_pedagogy_score(metrics: dict):

    engagement_score = metrics['engagement_score']
    explore_score = metrics['explore_score']
    explain_score = metrics['explain_score']
    elaborate_score = metrics['elaborate_score']
    evaluate_score = metrics['evaluate_score']

    all_scores = [engagement_score, explore_score, explain_score, elaborate_score, evaluate_score]

    overall_score = 40 + sum(all_scores) * 4

    strengths = [i for i, j in enumerate(all_scores) if j >= 2]
    improvement_areas = [i for i, j in enumerate(all_scores) if j < 1]

    return overall_score, strengths, improvement_areas


def _calculate_lesson_plan_completion(metrics: dict):

    completeness = round(100 * len(metrics['list_of_topics_covered']) / len(metrics['list_of_all_topics']), 0)
    quality = min(round(100 * ((len(metrics['list_of_excellent_topics']) * 3) +
                                            (len(metrics['list_of_good_topics']) * 2) +
                                            (len(metrics['list_of_poor_topics']))) / (len(metrics['list_of_all_topics']) * 3), 0) + 5, 100)
    missed_topics = [x for x in metrics['list_of_all_topics'] if x not in metrics['list_of_topics_covered']]
    return completeness, quality, missed_topics


def _calculate_teaching_guidelines_score(metrics: dict):
    score = min(round(100 * ((len(metrics['list_of_excellent_guidelines']) * 3) +
                                                 (len(metrics['list_of_good_guidelines']) * 2) +
                                                 (len(metrics['list_of_poor_guidelines']))) / (
                                                  len(metrics['list_of_all_guidelines']) * 3), 0) + 25, 100)
    missed_guidelines = [x for x in metrics['list_of_all_guidelines'] if
                                 x not in metrics['list_of_guidelines_exhibited']]
    strengths = metrics['list_of_excellent_guidelines']
    improvement_areas = metrics['list_of_poor_guidelines']

    return score, strengths, improvement_areas, missed_guidelines



if __name__ == '__main__':

    print(get_dashboard_metrics('../output/19Feb-1215.json'))
