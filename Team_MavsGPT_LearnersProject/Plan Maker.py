import google.generativeai as genai
import json

# Read input from JSON file
with open('resumes_info.json', 'r') as file:
    input_data = json.load(file)
# Configure the GEMINI LLM
genai.configure(api_key='AIzaSyByPYpRrOF9JB7YMoo5TnqbPS9OirU4B9Y')
model = genai.GenerativeModel('gemini-pro')
responses=[]
# Basic generation
def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text

def format_prompt(prompt_text, name, email, skills, experience, current_job_role, task, format):
    # Use f-string to format the prompt
    prompt = f"{prompt_text}\nExperience: {', '.join(experience)}\nName: {name}\nEmail: {email}\nSkills: {', '.join(skills)}\nCurrent Job Role: {current_job_role}\n\nSuggest: {', '.join(task)}\n\nFormat: {', '.join(format)}\n\n"
    return prompt

# Example data
prompt_text = "Here's some information about me:"
task= ["suggest some courses, certifications and a roadmap for me along with some tips and tricks"]
format=["return the result in JSON Format"]
# Example data
concatenated_prompt = "Here's some information about few people:"
task= ["suggest some courses(from where), certifications(from where) and a roadmap(timeline and order) for them along with some tips and tricks"]
format=["return the result in JSON Format"]
def concat_prompt(input_data, prompt_text, task, format):
    concatenated_prompt = f"{prompt_text}\n\n"
    for person in input_data:
        name = person.get('Name', '')
        email = person.get('Email', '')
        skills = person.get('Skills', [])
        experience = person.get('Experience', [])
        current_job_role = person.get('Current Job Role', '')
        
        # Concatenate person's information to the prompt string
        concatenated_prompt += f"Name: {name}\n"
        concatenated_prompt += f"Email: {email}\n"
        concatenated_prompt += f"Skills: {', '.join(skills)}\n"
        concatenated_prompt += f"Experience: {', '.join(experience)}\n"
        concatenated_prompt += f"Current Job Role: {current_job_role}\n"
        concatenated_prompt += f"Task: {', '.join(task)}\n"
        concatenated_prompt += f"Format: {', '.join(format)}\n\n"

    return concatenated_prompt



# Call the function with the input data
concatenated_prompt = concat_prompt(input_data, prompt_text, task, format)

# Print the concatenated prompt
print(concatenated_prompt)

    # Generate the response
answer = generate_text(concatenated_prompt)
print(answer)
responses.append(answer)

with open('Roadmap.json', 'w') as file:
    json.dump(responses, file)