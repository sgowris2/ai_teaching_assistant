# Shikshasaathi
### MVP Definition

1. Multi-school System

	- Each school has its own "tenant".
	- School has static properties.
	- Teachers are users associated with a school.
	- School has its own pedagogy database:
		- Pedagogy can be different by subject and grade.
	- School has its own curriculum database:
		- Curriculum is organized by grade, subject, and topic.
		- Standard curriculum is loaded into the database.
		- School is allowed to make modifications to the curriculum.
	- School has its own lesson plans database:
		- Lesson plans are organized by grade, subject, and topic.
		- Existing lesson plans are loaded into the database.
		- Newly generated lesson plans are added into the database.
		- Lesson plans can have rating by different teachers.
	- School has its own question bank database:
		- Question bank is organized by grade, subject, and topic.
		- Existing question bank is loaded into the database.
		- Newly generated questions are added into the question bank if approved by teachers.
		- Questions can be rated by teachers.

2. Pre-lesson:
	- Generate lesson plan (enriched teacher notes)
		- View popular lesson plans from other teachers.
		- Generate a new plan based on all data available in database + creativity.
		- View plan on a small mobile device easily.
		- Listen to the lesson plan instead of reading it.
		- Add / remove / edit steps of the lesson plan as needed.
		- Save a modified lesson plan.
		- Like a lesson plan.
		- Dislike a lesson plan and re-generate.
		- Create lesson plan from scratch.
		- Generate Interactive Activity as part of the lesson plan.
			- View popular activities from other teachers.
			- Generate new activity based on data available in database + creativity.
			- View activity on small mobile devices easily in steps.
			- Listen to the activity instead of reading it.
			- Add / edit / remove steps of the activity.
			- Like / dislike activity. 
			- Regenerate a new activity using a prompt.
	- Generate Quiz / HW assignment
		- View popular quizzes from other teachers.
		- Generate quiz using questions from the question bank only.
		- Generate new quiz with new questions.
		- View quiz on small mobile devices easily.
		- Add / remove questions in the quiz.
		- Save a modified quiz.
		- Like / dislike questions in the quiz.
		- Regenerate individual questions in the quiz.
		- Regenerate entire quiz.
		- Use prompt to generate question on a specific topic.

3. During Lesson:
	- Record lesson.
	- Real-time tracking of lesson plan completion and status shown to teacher.
	- Access lesson plan and questions.
	- Generate new questions.

4. Post-lesson:
	- Listen to lesson again.
	- View detailed report of the lesson.
		- Show topics covered, topics not covered. Teacher can manually update if any mistake.
		- Mark uncovered topics as "to be covered in next lesson".
		- Generate HW assignment.
			- Same options as pre-lesson quiz generation.
	- Share lesson report with others through link.
	- Delete lesson recording and report (if school allows this policy)
