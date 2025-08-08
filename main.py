import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

# Streamlit app configuration
st.set_page_config(page_title="Resume Builder", layout="wide")
st.title("Resume Builder")

# Initialize session state for form data
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        'personal': {},
        'objective': '',
        'education': [],
        'experience': [],
        'projects': [],
        'skills': [],
        'certifications': [],
        'achievements': []
    }

# Function to add education entry
def add_education():
    st.session_state.resume_data['education'].append({
        'degree': '',
        'college': '',
        'location': '',
        'duration': '',
        'cgpa': ''
    })

# Function to add experience entry
def add_experience():
    st.session_state.resume_data['experience'].append({
        'position': '',
        'company': '',
        'duration': '',
        'location': '',
        'contributions': []
    })

# Function to add project entry
def add_project():
    st.session_state.resume_data['projects'].append({
        'name': '',
        'tech': '',
        'description': [],
        'link': ''
    })

# Function to add certification entry
def add_certification():
    st.session_state.resume_data['certifications'].append({
        'title': '',
        'platform': '',
        'date': ''
    })

# Function to add achievement entry
def add_achievement():
    st.session_state.resume_data['achievements'].append({
        'competition': '',
        'result': '',
        'organization': '',
        'date': ''
    })

# Personal Details
st.header("1. Personal Details")
with st.form(key='personal_form'):
    st.session_state.resume_data['personal']['full_name'] = st.text_input("Full Name *", placeholder="Rajan Singh")
    st.session_state.resume_data['personal']['phone'] = st.text_input("Phone Number *", placeholder="+91 9876543210")
    st.session_state.resume_data['personal']['email'] = st.text_input("Email Address *", placeholder="rajan.singh.dev@gmail.com")
    st.session_state.resume_data['personal']['linkedin'] = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/rajansingh")
    st.session_state.resume_data['personal']['portfolio'] = st.text_input("Portfolio/GitHub URL (optional)", placeholder="https://github.com/rajansingh")
    st.session_state.resume_data['personal']['address'] = st.text_input("Address (optional)", placeholder="Jaipur, Rajasthan")
    submit_personal = st.form_submit_button("Save Personal Details")

# Career Objective
st.header("2. Career Objective / Summary")
st.session_state.resume_data['objective'] = st.text_area("Career Objective (2-3 lines)", placeholder="A motivated B.Tech graduate seeking to leverage expertise in Python and React to build innovative solutions.")

# Education
st.header("3. Education")
if st.button("Add Education"):
    add_education()
for i, edu in enumerate(st.session_state.resume_data['education']):
    with st.form(key=f'education_form_{i}'):
        st.subheader(f"Education {i+1}")
        edu['degree'] = st.text_input(f"Degree Name *", key=f"degree_{i}", placeholder="B.Tech in Computer Science")
        edu['college'] = st.text_input(f"College/University Name *", key=f"college_{i}", placeholder="IIT Jaipur")
        edu['location'] = st.text_input(f"Location", key=f"location_edu_{i}", placeholder="Jaipur, Rajasthan")
        edu['duration'] = st.text_input(f"Duration *", key=f"duration_{i}", placeholder="Aug 2019 - May 2023")
        edu['cgpa'] = st.text_input(f"CGPA/Percentage", key=f"cgpa_{i}", placeholder="8.5")
        submit_edu = st.form_submit_button(f"Save Education {i+1}")

# Work Experience
st.header("4. Work Experience / Internships")
if st.button("Add Experience"):
    add_experience()
for i, exp in enumerate(st.session_state.resume_data['experience']):
    with st.form(key=f'experience_form_{i}'):
        st.subheader(f"Experience {i+1}")
        exp['position'] = st.text_input(f"Position Title *", key=f"position_{i}", placeholder="Software Engineer Intern")
        exp['company'] = st.text_input(f"Company Name *", key=f"company_{i}", placeholder="TechCorp")
        exp['duration'] = st.text_input(f"Duration *", key=f"duration_exp_{i}", placeholder="June 2022 - Aug 2022")
        exp['location'] = st.text_input(f"Location", key=f"location_exp_{i}", placeholder="Bangalore, Karnataka")
        contributions = st.text_area(f"Contributions (one per line)", key=f"contributions_{i}", placeholder="Developed a feature\nOptimized codebase")
        exp['contributions'] = contributions.split('\n') if contributions else []
        submit_exp = st.form_submit_button(f"Save Experience {i+1}")

# Projects
st.header("5. Projects")
if st.button("Add Project"):
    add_project()
for i, proj in enumerate(st.session_state.resume_data['projects']):
    with st.form(key=f'project_form_{i}'):
        st.subheader(f"Project {i+1}")
        proj['name'] = st.text_input(f"Project Name *", key=f"project_name_{i}", placeholder="E-commerce Platform")
        proj['tech'] = st.text_input(f"Tools/Tech Used *", key=f"tech_{i}", placeholder="React, Node.js, MongoDB")
        description = st.text_area(f"Description (one per line)", key=f"description_{i}", placeholder="Built a full-stack application\nIntegrated payment gateway")
        proj['description'] = description.split('\n') if description else []
        proj['link'] = st.text_input(f"GitHub/Live Link", key=f"link_{i}", placeholder="https://github.com/rajansingh/project")
        submit_proj = st.form_submit_button(f"Save Project {i+1}")

# Skills
st.header("6. Skills")
skills_input = st.text_area("Skills (one per line)", placeholder="Python\nReact\nAWS\nCommunication")
st.session_state.resume_data['skills'] = skills_input.split('\n') if skills_input else []

# Certifications
st.header("7. Certifications")
if st.button("Add Certification"):
    add_certification()
for i, cert in enumerate(st.session_state.resume_data['certifications']):
    with st.form(key=f'certification_form_{i}'):
        st.subheader(f"Certification {i+1}")
        cert['title'] = st.text_input(f"Certificate Title *", key=f"cert_title_{i}", placeholder="Python for Data Science")
        cert['platform'] = st.text_input(f"Platform/Institute *", key=f"platform_{i}", placeholder="Coursera")
        cert['date'] = st.text_input(f"Completion Date *", key=f"cert_date_{i}", placeholder="May 2023")
        submit_cert = st.form_submit_button(f"Save Certification {i+1}")

# Achievements
st.header("8. Achievements / Awards / Hackathons")
if st.button("Add Achievement"):
    add_achievement()
for i, ach in enumerate(st.session_state.resume_data['achievements']):
    with st.form(key=f'achievement_form_{i}'):
        st.subheader(f"Achievement {i+1}")
        ach['competition'] = st.text_input(f"Competition Name *", key=f"comp_{i}", placeholder="CodeJam")
        ach['result'] = st.text_input(f"Rank/Result *", key=f"result_{i}", placeholder="1st Place")
        ach['organization'] = st.text_input(f"Organization *", key=f"org_{i}", placeholder="Google")
        ach['date'] = st.text_input(f"Date *", key=f"ach_date_{i}", placeholder="Apr 2022")
        submit_ach = st.form_submit_button(f"Save Achievement {i+1}")

# PDF Generation
def generate_pdf(resume_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=20, spaceAfter=12, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SubHeader', fontSize=12, leading=14, spaceAfter=8, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalBold', fontSize=10, leading=12, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Normal', fontSize=10, leading=12, fontName='Helvetica'))

    # Personal Details
    story.append(Paragraph(resume_data['personal'].get('full_name', ''), styles['Header']))
    if resume_data['personal'].get('email'):
        story.append(Paragraph(resume_data['personal']['email'], styles['Normal']))
    if resume_data['personal'].get('phone'):
        story.append(Paragraph(resume_data['personal']['phone'], styles['Normal']))
    if resume_data['personal'].get('linkedin'):
        story.append(Paragraph(resume_data['personal']['linkedin'], styles['Normal']))
    if resume_data['personal'].get('portfolio'):
        story.append(Paragraph(resume_data['personal']['portfolio'], styles['Normal']))
    if resume_data['personal'].get('address'):
        story.append(Paragraph(resume_data['personal']['address'], styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Career Objective
    if resume_data['objective']:
        story.append(Paragraph("Career Objective", styles['SubHeader']))
        story.append(Paragraph(resume_data['objective'], styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    # Education
    if resume_data['education']:
        story.append(Paragraph("Education", styles['SubHeader']))
        for edu in resume_data['education']:
            text = f"{edu['degree']}, {edu['college']}, {edu['location']}<br/>{edu['duration']}"
            if edu['cgpa']:
                text += f" | {edu['cgpa']}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    # Work Experience
    if resume_data['experience']:
        story.append(Paragraph("Work Experience", styles['SubHeader']))
        for exp in resume_data['experience']:
            text = f"{exp['position']}, {exp['company']}, {exp['duration']}"
            if exp['location']:
                text += f", {exp['location']}"
            story.append(Paragraph(text, styles['NormalBold']))
            if exp['contributions']:
                contributions = [ListItem(Paragraph(c, styles['Normal'])) for c in exp['contributions'] if c]
                story.append(ListFlowable(contributions, bulletType='bullet'))
            story.append(Spacer(1, 0.1*inch))

    # Projects
    if resume_data['projects']:
        story.append(Paragraph("Projects", styles['SubHeader']))
        for proj in resume_data['projects']:
            text = f"{proj['name']} | {proj['tech']}"
            story.append(Paragraph(text, styles['NormalBold']))
            if proj['description']:
                descriptions = [ListItem(Paragraph(d, styles['Normal'])) for d in proj['description'] if d]
                story.append(ListFlowable(descriptions, bulletType='bullet'))
            if proj['link']:
                story.append(Paragraph(proj['link'], styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    # Skills
    if resume_data['skills']:
        story.append(Paragraph("Skills", styles['SubHeader']))
        skills_text = ", ".join([s for s in resume_data['skills'] if s])
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    # Certifications
    if resume_data['certifications']:
        story.append(Paragraph("Certifications", styles['SubHeader']))
        for cert in resume_data['certifications']:
            text = f"{cert['title']}, {cert['platform']}, {cert['date']}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    # Achievements
    if resume_data['achievements']:
        story.append(Paragraph("Achievements", styles['SubHeader']))
        for ach in resume_data['achievements']:
            text = f"{ach['competition']}, {ach['result']}, {ach['organization']}, {ach['date']}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Download PDF button
if st.button("Generate and Download Resume PDF"):
    pdf_buffer = generate_pdf(st.session_state.resume_data)
    st.download_button(
        label="Download Resume PDF",
        data=pdf_buffer,
        file_name="resume.pdf",
        mime="application/pdf"
    )
