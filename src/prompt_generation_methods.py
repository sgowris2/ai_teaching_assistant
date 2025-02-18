def create_prompt(grade: int, subject: str, topic: str, state: str, board: str, district: str, block: str):

    template = '''
    You are a teacher's helpful assistant that listens to a teacher delivering a lesson to a classroom through an audio 
    recording and gives helpful suggestions of how the teacher has performed in the lesson based on the requirements of 
    pedagogy, curriculum, other guidelines given to the teacher during training.
    
    For the given audio recording from a grade {grade} classroom where the teacher is teaching a {subject} lesson on 
    the topic of {topic}, analyze the audio and return structured output in JSON. The structure of the JSON is given 
    below.
    
    Curriculum: 
    {curriculum}
    
    Pedagogy: 
    {pedagogy}
    
    Training Guidelines: 
    {training_guidelines}
    
    Output JSON Structure:
    {{
        "pedagogy_score": <percent as integer of pedagogy guidelines followed>,
        "pedagogy_specifics": [list of strings where each is a bullet point with specific performance of the teacher on each pedagogy guideline],
        "curriculum_coverage_score": <percent as integer of curriculum topics covered>,
        "curriculum_specifics": [list of strings with bullet points with specific topics that were not covered in the lesson that are part of the curriculum],
        "training_guidelines_score": <percent as integer of training guidelines followed by the teacher>,
        "training_guidelines_specifics": [list of strings with bullet points with specific training guidelines that were not used by the teacher in the lesson],
        "positive_aspects": [list of strings with bullet points with specific things that were done well by the teacher in the lesson with examples from the audio],
        "areas_of_improvement": [list of strings with bullet points with specific things that could be improved by the teacher with examples from the audio],
        "suggestions_for_next_lesson": [list of string with suggestions on what the teacher can do in the next lesson on the same topic]
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
    return '''
    1. What is a Sangjna?
    2. What are examples of Sagjna?
    3. Identify Sangja in a sentence.
    4. Construct sentences using one or more Sangja that are given to the student.
    '''


def _get_pedagogy(state: str, board: str):
    # TODO Get from database of pedagogy guidelines per state and board
    return '''
    The 5E's instructional model is a research-based framework designed to facilitate inquiry-based learning and promote a deeper understanding of mathematical concepts. Each phase of the model—Engage, Explore, Explain, Elaborate, and Evaluate—plays a vital role in the teaching and learning process.
    1. Engage: The engage phase aims to capture students' attention and generate interest in the topic. It involves activities or discussions that activate prior knowledge, stimulate curiosity, and create a connection between the students' experiences and the new concepts being taught.
    2. Explore: In the explore phase, students actively participate in hands-on activities, investigations, and experiments. They explore the mathematical concepts, make observations, ask questions, and collect data. This phase encourages students to develop critical thinking skills, engage in problem-solving, and discover patterns and relationships.
    3. Explain: The explain phase focuses on providing explanations, clarifying concepts, and developing a deeper understanding. Teachers facilitate discussions, present mathematical principles, and guide students in making connections between their observations and the underlying mathematical concepts.
    4. Elaborate: In the elaborate phase, students apply their understanding of the concepts in real-life contexts. They engage in extended activities, solve complex problems, and work on projects that require higher-order thinking skills. This phase encourages students to explore mathematics beyond the classroom and strengthens their problem-solving abilities.
    5. Evaluate: The evaluate phase involves assessing students' learning outcomes and understanding. Various assessment strategies, including formative and summative assessments, are used to measure students' progress and provide feedback for further improvement.
    '''


def _get_training_guidelines(state: str, district: str, block: str):
    # TODO Get from database of training guidelines
    return '''
    1. Make sure to slow down and repeat important concepts so that all students understand.
    2. Ask questions to multiple children in the class.
    3. Give more than one example for each important concept.
    '''
