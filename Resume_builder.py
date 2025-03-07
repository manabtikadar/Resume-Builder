import streamlit as st
import json
import os
import warnings
from build_graph import app
from build_pdf import generate_resume
import pprint

warnings.filterwarnings("ignore")

# Streamlit Web App Title
st.title("📄 AI-Powered Resume Builder")

# Job Role Selection
st.header("👔 Select Job Role")
job_roles = ["Data Scientist", "Product Manager", "Content Writer", "General Engineering", "Custom"]
selected_role = st.selectbox("Choose your desired job role", job_roles)

# Input LinkedIn Profile if "Custom" is selected
linkedin_profile = ""
custom_question = ""
if selected_role == "Custom":
    linkedin_profile = st.text_input("Enter your LinkedIn profile URL")
    custom_question = st.text_input("Enter the job role")

# User Input Form
st.header("📝 Enter Resume Details")
user_name = st.text_input("Enter your name")
query = st.text_area("Enter your resume details in plain text", height=250)

output_dir = "C:\\Users\\manab\\OneDrive\\Desktop\\Resume_Builder\\store"

if st.button("Generate Resume"):
    if not query.strip() and not linkedin_profile.strip():
        st.warning("Please enter resume details or provide a LinkedIn profile!")
    elif not user_name.strip():
        st.warning("Please enter your name!")
    else:
        output_pdf_path = os.path.join(output_dir, f"{user_name}_Resume.pdf")

        selected_question = custom_question if selected_role == "Custom" else selected_role

        inputs = {"question": selected_question, "query": query, "linkedin_link": linkedin_profile.strip()}
        json_output = None

        with st.spinner("Generating your resume... ✨"):
            for output in app.stream(inputs):
                for key, value in output.items():
                    pprint.pprint(f"Node '{key}': {value}")
                    if "json_output" in value:
                        json_output = value["json_output"]

        # if json_output:
        #     # Display JSON Output
        #     st.subheader("📜 JSON Resume Output")
        #     st.json(json_output)

            # Save JSON file
            json_filename = os.path.join(output_dir, f"{user_name}_resume.json")
            with open(json_filename, "w", encoding="utf-8") as json_file:
                json.dump(json_output, json_file, indent=4, ensure_ascii=False)

            st.success(f"✅ JSON Resume saved as `{json_filename}`")

            # Generate PDF
            pdf_filename = os.path.join(output_dir, f"{user_name}_Resume.pdf")
            generate_resume(json_output, output_filename=pdf_filename)

            st.success(f"✅ PDF Resume saved as `{pdf_filename}`")

            # Download Buttons
            with open(json_filename, "rb") as file:
                st.download_button("📥 Download JSON Resume", file, file_name=f"{user_name}_resume.json", mime="application/json")

            with open(pdf_filename, "rb") as file:
                st.download_button("📥 Download PDF Resume", file, file_name=f"{user_name}_Resume.pdf", mime="application/pdf")

st.sidebar.header("ℹ️ About This App")
st.sidebar.write(
    """
    This AI-powered resume builder generates professional resumes using a 
    Retrieval-Augmented Generation (RAG) pipeline. Select a job role or enter a 
    LinkedIn profile to automatically extract resume details.
    """
)
