from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)



template = """
You are an expert resume writer. Using the provided query, generate a tailored and professional resume in valid JSON format.

Query:
-------
{query}
-------

Provide the resume strictly as a JSON object with the following structure:

{{
    "full_name": "full_name",
    "contact": {{
        "phone": "phone_number",
        "email": "email_address",
        "linkedin": "linkedin_profile",
        "github": "github_profile"
    }},
    "education": {{
        "university_name": "university_name",
        "degree": "degree",
        "field_of_study": "field_of_study",
        "expected_graduation": "expected_graduation_date",
        "gpa": "gpa",
        "location": "university_location",
        "relevant_coursework": [
            "course_1",
            "course_2",
            "course_3"
        ]
    }},
    "experience": [
        {{
            "organization": "organization_name",
            "role": "job_title",
            "duration": "job_duration",
            "location": "job_location",
        }}
    ],
    "projects": [
        {{
            "title": "project_title",
            "technologies": [
                "technology_1",
                "technology_2"
            ],
            "description": "project_description",
        }}
    ],
    "technical_skills": {{
        "languages": [
            "programming_language_1",
            "programming_language_2"
        ],
        "technologies": [
            "technology_1",
            "technology_2"
        ],
        "hardware": [
            "hardware_component_1",
            "hardware_component_2"
        ],
        "concepts": [
            "concept_1",
            "concept_2"
        ]
    }},
    "achievements": [
        {{
            "title": "achievement_title",
            "year": "achievement_year",
            "description": "achievement_description"
        }}
    ],
    "social_engagements": [
        {{
            "role": "social_role",
            "organization": "social_organization"
        }}
    ]
}}

Ensure the output is valid JSON with no additional text or explanations.
"""




prompt = PromptTemplate(
    template=template,
    input_variables=["query"] 
)

information_chain = (
    prompt
    | llm
    | JsonOutputParser()
)

