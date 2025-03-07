from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)



template = """
You are an expert resume writer. Using the provided query, generate a professional resume in LaTeX format.and fill the missing values with None.

Query:
-------
{query}
-------

Provide the resume strictly as a LaTeX document using the following structure:

```latex
\\documentclass"resume"  % Use a standard resume class
\\begin"document"

% Personal Information
\\name"FULL_NAME"
\\contactinfo"EMAIL","PHONE","LINKEDIN","GITHUB"

 Education Section
\\section"Education"
\\educationentry{DEGREE, FIELD_OF_STUDY}{UNIVERSITY_NAME, LOCATION}{EXPECTED_GRADUATION}{GPA}
Relevant Coursework: COURSE_1, COURSE_2, COURSE_3

 Experience Section
\\section{Experience}
\\workentry{ROLE at ORGANIZATION}{DURATION, LOCATION}
\\begin{itemize}
    \\item Describe key responsibility or achievement.
    \\item Another achievement or contribution.
\\end{itemize}

% Projects Section
\\section{Projects}
\\projectentry{PROJECT_TITLE}{TECHNOLOGY_1, TECHNOLOGY_2}
\\begin{itemize}
    \\item PROJECT_DESCRIPTION
\\end{itemize}

% Technical Skills
\\section{Technical Skills}
Languages: PROGRAMMING_LANGUAGE_1, PROGRAMMING_LANGUAGE_2 \\\\
Technologies: TECHNOLOGY_1, TECHNOLOGY_2 \\\\
Hardware: HARDWARE_COMPONENT_1, HARDWARE_COMPONENT_2 \\\\
Concepts: CONCEPT_1, CONCEPT_2

% Achievements
\\section{Achievements}
\\achievemententry{ACHIEVEMENT_TITLE (YEAR)}{ACHIEVEMENT_DESCRIPTION}

% Social Engagements
\\section{Social Engagements}
\\socialentry{ROLE at ORGANIZATION}

\\end{document}
"""




prompt = PromptTemplate(
    template=template,
    input_variables=["query"] 
)

Latex_chain = (
    prompt
    | llm
    | StrOutputParser()
)

