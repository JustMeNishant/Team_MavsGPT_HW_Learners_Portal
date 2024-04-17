import os
import re
import json
from docx import Document

def extract_info_from_resume(resume_text):
    # Regular expressions to extract name, email, and experience
    name_pattern = r"Name:\s*(.+)"
    email_pattern = r"Email:\s*([^\s@]+@[^\s@]+\.[^\s@]+)"
    experience_pattern = r"Experience:\s*(\d+)\s*years?"

    # Extract name, email, and experience using regular expressions
    name_match = re.search(name_pattern, resume_text)
    email_match = re.search(email_pattern, resume_text)
    experience_match = re.search(experience_pattern, resume_text)

    name = name_match.group(1) if name_match else ''
    email = email_match.group(1) if email_match else ''
    exp_start_index = resume_text.find("Experience in Technology:") 
    # print(exp_start_index)
    exp_end_index = resume_text.find("ExperienceEnd")
    # print(exp_end_index)
    experience_text=resume_text[exp_start_index:exp_end_index].strip()
    # Extract skills and current job role using text processing
    experience = [experience.strip() for experience in experience_text.split("\n") if experience.strip()]
    skills_start_index = resume_text.find("Skills:") 
    # print(skills_start_index)
    skills_end_index = resume_text.find("Experience in Technology:")
    # print(skills_end_index)
    skills_text = resume_text[skills_start_index:skills_end_index].strip()
    # print(skills_text)
    skills = [skill.strip() for skill in skills_text.split("\n") if skill.strip()]
    current_job_role_start_index = resume_text.find("Current Job Role:") 
    current_job_role_end_index = resume_text.find("EndofFile")
    job_role_text=resume_text[current_job_role_start_index+18:current_job_role_end_index].strip()
    print(job_role_text)
    # print(current_job_role_end_index)
    current_job_role = [current_job_role.strip() for current_job_role in job_role_text.split("\n") if current_job_role.strip()]

    return name, email, skills, current_job_role, experience

def process_resumes_in_folder(folder_path):
    all_resumes_info = []

    for filename in os.listdir(folder_path):
        if not filename.startswith('~$') and (filename.endswith(".txt") or filename.endswith(".docx")):
            resume_path = os.path.join(folder_path, filename)
            if filename.endswith(".txt"):
                with open(resume_path, 'r', encoding='utf-8') as file:
                    resume_text = file.read()
            elif filename.endswith(".docx"):
                try:
                    document = Document(resume_path)
                    resume_text = "\n".join([p.text for p in document.paragraphs])
                except Exception as e:
                    print(f"Error processing {resume_path}: {e}")
                    continue

            name, email, skills, current_job_role, experience = extract_info_from_resume(resume_text)

            resume_info = {
                "Name": name,
                "Email": email,
                "Skills": skills,
                "Current Job Role": current_job_role,
                "Experience": experience
            }
            all_resumes_info.append(resume_info)

    output_json_path = "resumes_info.json"
    with open(output_json_path, "w") as json_file:
        json.dump(all_resumes_info, json_file, indent=4)

    print(f"Extracted information from {len(all_resumes_info)} resumes saved to {output_json_path}")
    # print(all_resumes_info)

folder_path = r"D:\Virtual_ENV\resumes"
process_resumes_in_folder(folder_path)
