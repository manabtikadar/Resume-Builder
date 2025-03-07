from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import json
from question_answer import information_chain

def generate_resume(resume, output_filename="resume.pdf"):
    
    
    pdf = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    title_style = styles['Title']
    content.append(Paragraph(resume["full_name"], title_style))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"📧 {resume['contact']['email']} | 📞 {resume['contact']['phone']} | "
                             f"<a href='{resume['contact']['linkedin']}'>LinkedIn</a> | "
                             f"<a href='{resume['contact']['github']}'>GitHub</a>", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Education</b>", styles['Heading2']))
    content.append(Paragraph(f"{resume['education']['degree']} in {resume['education']['field_of_study']} - "
                             f"{resume['education']['university_name']} ({resume['education']['expected_graduation']})", styles['Normal']))
    content.append(Paragraph(f"GPA: {resume['education']['gpa']}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Experience</b>", styles['Heading2']))
    for exp in resume['experience']:
        content.append(Paragraph(f"<b>{exp['role']}</b> at {exp['organization']} ({exp['duration']})", styles['Normal']))
        content.append(Spacer(1, 6))


    content.append(Paragraph("<b>Projects</b>", styles['Heading2']))
    for project in resume['projects']:
        content.append(Paragraph(f"<b>{project['title']}</b>", styles['Normal']))
        content.append(Paragraph(f"Technologies: {', '.join(project['technologies'])}", styles['Normal']))
        content.append(Paragraph(f"Description: {project['description']}", styles['Normal']))
        content.append(Spacer(1, 6))

    
    content.append(Paragraph("<b>Technical Skills</b>", styles['Heading2']))
    content.append(Paragraph(f"Languages: {', '.join(resume['technical_skills']['languages'])}", styles['Normal']))
    content.append(Paragraph(f"Technologies: {', '.join(resume['technical_skills']['technologies'])}", styles['Normal']))
    content.append(Paragraph(f"Hardware: {', '.join(resume['technical_skills']['hardware'])}", styles['Normal']))
    content.append(Paragraph(f"Concepts: {', '.join(resume['technical_skills']['concepts'])}", styles['Normal']))
    content.append(Spacer(1, 12))

    
    content.append(Paragraph("<b>Achievements</b>", styles['Heading2']))
    for achievement in resume['achievements']:
        content.append(Paragraph(f"• {achievement['title']} ({achievement['year']}): {achievement['description']}", styles['Normal']))
    content.append(Spacer(1, 12))

    
    content.append(Paragraph("<b>Social Engagements</b>", styles['Heading2']))
    for social in resume['social_engagements']:
        content.append(Paragraph(f"• {social['role']} at {social['organization']}", styles['Normal']))

    
    pdf.build(content)
    print(f"Resume saved as {output_filename}")

