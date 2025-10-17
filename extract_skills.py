import os
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv

# --- Step 1: Read .env file for API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Step 2: Get file name from command line ---
if len(sys.argv) < 2:
    print("❌ Please provide a text file name as an argument.")
    print("Example: python extract_skills.py resume_cleaned.txt")
    sys.exit(1)

file_name = sys.argv[1]

# --- Step 3: Read the input file ---
try:
    with open(file_name, "r", encoding="utf-8") as f:
        resume_text = f.read()
except FileNotFoundError:
    print(f"❌ File '{file_name}' not found.")
    sys.exit(1)

# --- Step 4: Create prompt ---
prompt = f"""
You are an expert résumé parser.
Extract all skills from the resume text below and classify them into:
- ProgrammingLanguages
- FrameworksLibraries
- ToolsPlatforms
- SoftSkills

Output must be STRICT JSON only in this format:
{{
  "skills": {{
    "ProgrammingLanguages": ["Python", "SQL"],
    "FrameworksLibraries": ["React", "scikit-learn"],
    "ToolsPlatforms": ["Git", "Docker"],
    "SoftSkills": ["Teamwork", "Communication"]
  }}
}}

Resume:
{resume_text}
"""

# --- Step 5: Call GPT-5 Mini ---
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    response_format={"type": "json_object"}
)

# --- Step 6: Handle response safely ---
raw = response.choices[0].message.content

try:
    skills_data = json.loads(raw)
    print(json.dumps(skills_data, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("⚠️ JSON decoding failed, raw response:")
    print(raw)
