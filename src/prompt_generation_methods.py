def create_prompt(grade: int, subject: str, topic: str, state: str, board: str, district: str, block: str):

    template = '''
    You are a teacher's helpful assistant that listens to a teacher delivering a lesson to a classroom through an audio 
    recording and gives helpful suggestions of how the teacher has performed in the lesson based on the requirements of 
    pedagogy, curriculum, other guidelines given to the teacher during training.
    
    For the given audio recording from a grade {grade} classroom where the teacher is teaching a {subject} lesson on 
    the topic of {topic}, analyze the audio and return structured output in JSON. The structure of the JSON is given 
    below.
    
    Curriculum: {curriculum}
    
    Pedagogy: {pedagogy}
    
    Training Guidelines: {training_guidelines}
    
    Output JSON Structure:
    {{
        "positive_aspects": <bullet points with specific things that were done well by the teacher in the lesson with examples from the audio>,
        "areas_of_improvement": <bullet points with specific things that could be improved by the teacher with examples from the audio>
    }}        
    '''

    curriculum_context = _get_curriculum(state=state, board=board, grade=grade, subject=subject, topic=topic),
    pedagogy_context = _get_pedagogy(state=state, board=board),
    training_context = _get_training_guidelines(state=state, district=district, block=block)

    prompt = template.format(grade=grade,
                             subject=subject,
                             topic=topic,
                             curriculum=curriculum_context,
                             pedagogy=pedagogy_context,
                             training_guidelines=training_context)

    return prompt


def _get_curriculum(state: str, board: str, grade: int, subject: str, topic: str):
    # TODO Get from database of curriculums based on grade, state, board, topic
    return ''


def _get_pedagogy(state: str, board: str):
    # TODO Get from database of pedagogy guidelines per state and board
    return ''


def _get_training_guidelines(state: str, district: str, block: str):
    # TODO Get from database of training guidelines
    return ''
