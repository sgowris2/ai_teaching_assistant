# Formative Assessments
## MVP Definition

### Overview
A system that allows teachers across contexts implement formative assessments (FAs) in their classes with minimal extra effort.
The purpose of the FAs is to ensure that no student is left behind and any lag is identified promptly and addressed by the teacher.

### High-level Guidelines
1. The system should work for various contexts including low-resource settings, remote areas, vernacular instruction, public schools, and affordable private schools.
2. The system should seamlessly fit into the existing ecosystem of schools with minimal additional infrastructure requirements.
3. The system should emphasise conceptual understanding and constructive feedback, not rote learning nor peer-to-peer competition. 
4. The system should be compatible and ideally enable other suggestions from the NEP 2020 such as peer-group learning, cohort-based learning, personalized/independent learning journeys, etc.

### Why Formative Assessments?
1. Formative assessments (FAs) have been regarded by decades of research as an effective way to ensure learning objectives are met at various levels of education.
2. The NEP 2020 has also suggested that schools move in the direction of implementing formative assessments rather than summative assessments. 
3. However, implementing formative assessments is challenging because of the extra bandwidth it requires to design, run, and grade assessments, and also analyze the feedback and adjust lesson plans accordingly. This is even harder when a large fraction of schools in India (and other parts of the world) are under-resourced and are responsible for much more than just learning outcomes.
4. Therefore, FA looks to be a good area in which technology can provide automation and intelligence to reduce the human resources required. Also, the same technology can be used to reduce the existing human resources used in grading tasks. 
5. In addition, the latest large-language models (LLMs) are making big strides in understanding language in multiple modes (text, voice, images) that greatly helps with the promise of an intuitive and adaptive user interface for educators that does not further burden them in their everyday routine.

### How It Would Work
1. FA Generation
   - Based on the grade, subject, language of instruction, topic, and learning objectives, the system would be able to generate an FA.
   - A teacher can modify the FA with an intuitive user interface (could be voice enabled also) and get it finalized.
   - Then, the teacher prints the FA on pieces of paper that also get a unique QR code to identify each student.
   - The teacher would distribute the printed FA worksheets to the class making sure that each student gets the worksheet with their name (QR code) on it.
2. FA Auto-grading
   - Once the FA worksheets have been filled by the students, the teacher collects all of them and scans the worksheets. This can be done using an existing phone or by using an auto-feed scanner device.
   - The scanned worksheets are uploaded to the central AI system that grades the worksheets automatically.
   - The results are stored in a secure database and is ready for analysis.
   - *Side-note*: This system can also be adapted for use in auto-grading existing worksheets that are given to students through their textbooks or teacher's/school's worksheet database. This can reduce the burden of grading and help teachers devote more time towards ensuring that no student is getting left behind in their classes.
3. FA Analysis
   - The analysis module of the system continuously analyses the results of the FAs and creates a number of dashboards and insights for the teacher.
   - This includes the following analyses for each subject:
     - Student analysis - Each student's conceptual understanding and progress is tracked. Common mistakes and suggested interventions for the student are highlighted.
     - Class analysis - Analytics on how students are generally understanding the material and suggestions for how subsequent lesson plans could be adjusted to help the class as a whole.

### Future Expansion
1. Cohort/Peer-group Learning
   - A popular way of running cohort-based or peer-group learning methods in classrooms involves giving activities or worksheets to groups of students to solve together.
   - The FA system can be extended to automatically generate the required materials to engage cohorts such that the teacher can give more attention to students who need it most.
   - The system can also automatically create the cohorts based on the FA results if needed.
2. Independent Learning Journeys
   - The FA system has information about each student's progress. Therefore, it can also create personalised worksheets for each student so that they can practice in the areas that need the most attention.
   - The same system can also be implemented via a chatbot interface that can help with familiarizing students with how to use computers and also with other learning techniques such as Socratic Questioning.
