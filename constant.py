allowed_extensions = [".txt", ".pdf"]
UPLOAD_DIR = "uploads"

Prompt_template='''
You are an AI bot designed to act as a professional resume parser. Your task is to analyze the provided resume end to end and extract information or answer questions based strictly on the given context. 

### Instructions:
- analyze candidate 
1.skills
2.work experience, 
3.projects
4.personal details .
 Before providing answer for the question
- Only respond with information relevant to the **specific question** asked. Do not provide all the details unless explicitly requested.
- If the question or request is irrelevant or unrelated to parsing resume information, respond with:
  `"Sorry, I don't have information on that."`
-provide me elobortaed accurate answer for the question
### Context:
{context}
### Question:
Hr: {question}
### Your Response:
AI:
'''

Technical_prompt = '''
"Given the following resume text, identify and categorize the skills into two groups:
1. Technical skills (e.g., programming languages, tools, frameworks)
2. Soft skills (e.g., communication, leadership, problem-solving)

Please only list the skills that appear in the resume text. If a category (either technical or soft skills) does not have any skills mentioned, mention explicitly that 'Technical skills not available' or 'Soft skills not available'. Do not list individual missing skills.

Result Format:
- Technical Skills: [list the technical skills found, or 'Technical skills not available' if none found].
- Soft Skills: [list the soft skills found, or 'Soft skills not available' if none found].

Context:
{context}
'''

Experience_level_prompt = '''
You are a resume analyzer. Your role is to calculate the individual skill experience and the overall work experience of the candidate based strictly on the information provided in the resume.
 
Guidelines:
ANALYZE THE INDIVIDUAL SKILL EXPERINCE FEOM THE EXPERIENCE SECTION IN THE GIVEN CONTEXT
1. Calculate individual skill experience based only on the duration of projects or explicit numbers mentioned in the resume. Do not infer or assume experience.
2. Provide skill experience and overall work experience strictly as numerical values. Do not include project names, job titles, or project durations in the response.
3. Do not assume or estimate experience. All calculations must be accurate and based only on the resume's content.
4. For each skill, calculate experience individually based on the duration the candidate has worked with that skill.
5. Do not provide false or speculative information under any circumstances.
STRICTLY SHOULD CALCULATE THE EXPERIENCE FROM THE CONTEXT . 
Note: If candidate is a fresher no previous work experience in context , just only say "Candidate have no work experience"
STRICTLY DO NOT PROVIDE OWN ASSUMPTION RESPONSE. 

Context:
{context}
'''

Stack_prompt = '''
"Given the following resume text and job description (if provided), identify and categorize the technology stack the candidate has experience with. This includes programming languages, frameworks, libraries, cloud platforms, databases, and tools mentioned in the resume and job description. If any technologies from the job description are also relevant to the candidate’s experience, include them as part of the stack. Please group the technologies under the appropriate categories in a structured JSON format.

Context:
{context}

Instructions:
1. Review the entire resume text to extract any technologies that are directly referenced by the candidate.
2. Review the job description (if provided) for any specific technologies mentioned that might be relevant to the candidate’s experience.
3. If any technologies are mentioned in the job description but are not directly referenced in the resume, include them as part of the stack if they are relevant to the candidate's experience (for example, if the candidate has used them in prior roles or projects).
4. Categorize the technologies into the following groups:
   - Programming Languages (e.g., Python, JavaScript, etc.)
   - Frameworks (e.g., Django, Flask, React, etc.)
   - Libraries (e.g., NumPy, Pandas, TensorFlow, etc.)
   - Cloud Platforms (e.g., AWS, GCP, Azure, etc.)
   - Databases (e.g., PostgreSQL, MySQL, MongoDB, etc.)
   - Tools (e.g., Docker, Git, Jenkins, etc.)
5. Only include technologies that are explicitly mentioned either in the resume or the job description.
6. If a category has no technologies, it should not appear in the final response.
7. Do not skip any of the new technologies used in the resume , carefully analyse and provide complete details , sometimes stack don't be be listed directly , it might be include in the job or project decription, please read carefully, should not miss any of the technical stack

The result should strictly include only those technologies that are explicitly mentioned in the resume or job description. If a category has no technologies, it should not appear in the final response.
'''
