import streamlit as st
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
import io

st.set_page_config(page_title="Professional Resume Builder", layout="wide")
st.title("🎯 Professional Resume Builder")
st.markdown("---")

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
        'guide': '',
        'contributions': []
    })

# Function to add project entry
def add_project():
    st.session_state.resume_data['projects'].append({
        'name': '',
        'tech': '',
        'description': [],
        'link': '',
        'users': '',
        'date': '',
        'guide': ''
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

# Enhanced PDF Generation with Professional Styling
def generate_professional_pdf(resume_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom professional styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=2*mm,
        alignment=TA_CENTER,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=1*mm,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=3*mm,
        spaceBefore=5*mm,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.black,
        borderPadding=2,
        backColor=colors.lightgrey
    )
    
    content_style = ParagraphStyle(
        'ContentText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=2*mm,
        textColor=colors.black,
        alignment=TA_JUSTIFY
    )
    
    bold_content_style = ParagraphStyle(
        'BoldContent',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=2*mm,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Header Section with Name
    if resume_data['personal'].get('full_name'):
        story.append(Paragraph(resume_data['personal']['full_name'], title_style))
        
        # Contact Information in a more organized way
        contact_info = []
        if resume_data['personal'].get('phone'):
            contact_info.append(f"Ph No: {resume_data['personal']['phone']}")
        if resume_data['personal'].get('field'):
            story.append(Paragraph(resume_data['personal']['field'], contact_style))
        if resume_data['personal'].get('college'):
            story.append(Paragraph(resume_data['personal']['college'], contact_style))
            
        # Create contact table for better layout
        contact_data = []
        row1, row2 = [], []
        
        if resume_data['personal'].get('email'):
            row1.append(f"Email ID: {resume_data['personal']['email']}")
        if resume_data['personal'].get('linkedin'):
            row2.append(f"Linkedin: LinkedIn")  # Simplified as in original
            
        if row1 or row2:
            if row1:
                contact_data.append(row1)
            if row2:
                contact_data.append(row2)
                
            if contact_data:
                contact_table = Table(contact_data, colWidths=[90*mm, 90*mm])
                contact_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(contact_table)
        
        story.append(Spacer(1, 5*mm))
    
    # Career Objective
    if resume_data.get('objective'):
        story.append(Paragraph("CAREER OBJECTIVE", section_header_style))
        story.append(Paragraph(resume_data['objective'], content_style))
    
    # Education Section
    if resume_data['education']:
        story.append(Paragraph("EDUCATION", section_header_style))
        
        # Create education table
        edu_data = [['Education', 'University', 'Institute', 'Year', 'CGPA']]
        for edu in resume_data['education']:
            edu_data.append([
                edu.get('degree', ''),
                edu.get('location', ''),  # Using location as university
                edu.get('college', ''),
                edu.get('duration', ''),
                edu.get('cgpa', '')
            ])
        
        edu_table = Table(edu_data, colWidths=[40*mm, 25*mm, 40*mm, 25*mm, 20*mm])
        edu_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(edu_table)
        story.append(Spacer(1, 3*mm))
    
    # Experience Section
    if resume_data['experience']:
        story.append(Paragraph("EXPERIENCE", section_header_style))
        for i, exp in enumerate(resume_data['experience']):
            # Experience header
            exp_header = f"• {exp.get('position', '')} – {exp.get('company', '')} ({exp.get('duration', '')})"
            story.append(Paragraph(exp_header, bold_content_style))
            
            # Guide/Location info
            if exp.get('location') or exp.get('guide'):
                guide_info = f"({exp.get('location', '')}"
                if exp.get('guide'):
                    guide_info += f" / {exp.get('guide')}"
                guide_info += ")"
                story.append(Paragraph(guide_info, content_style))
            
            # Contributions
            if exp.get('contributions'):
                for contrib in exp['contributions']:
                    if contrib.strip():
                        story.append(Paragraph(f"◦ {contrib.strip()}", content_style))
            story.append(Spacer(1, 2*mm))
    
    # Projects Section
    if resume_data['projects']:
        story.append(Paragraph("PROJECTS", section_header_style))
        for proj in resume_data['projects']:
            # Project header with users count and date
            proj_header = f"• {proj.get('name', '')}"
            if proj.get('users'):
                proj_header += f" (Active Users – {proj.get('users')})"
            if proj.get('date'):
                proj_header += f" ({proj.get('date')})"
            story.append(Paragraph(proj_header, bold_content_style))
            
            # Guide info
            if proj.get('guide'):
                story.append(Paragraph(f"( Guide: {proj.get('guide')} )", content_style))
            
            # Project description
            if proj.get('description'):
                for desc in proj['description']:
                    if desc.strip():
                        story.append(Paragraph(f"◦ {desc.strip()}", content_style))
            story.append(Spacer(1, 2*mm))
    
    # Technical Skills
    if resume_data['skills']:
        story.append(Paragraph("TECHNICAL SKILLS", section_header_style))
        # Group skills by category
        tools_langs = [s for s in resume_data['skills'] if any(keyword in s.lower() for keyword in ['c++', 'c', 'python', 'javascript', 'dart', 'flutter', 'sql', 'git', 'node', 'mongo'])]
        technologies = [s for s in resume_data['skills'] if s not in tools_langs]
        
        if tools_langs:
            story.append(Paragraph(f"• Tools & Languages: {', '.join(tools_langs)}", content_style))
        if technologies:
            story.append(Paragraph(f"• Technologies: {', '.join(technologies)}", content_style))
        story.append(Spacer(1, 3*mm))
    
    # Achievements
    if resume_data['achievements']:
        story.append(Paragraph("ACHIEVEMENTS & POSITIONS OF RESPONSIBILITY", section_header_style))
        for ach in resume_data['achievements']:
            ach_text = f"• {ach.get('result', '')} in {ach.get('competition', '')} | {ach.get('organization', '')}"
            if ach.get('date'):
                ach_text += f" ({ach.get('date', '')})"
            story.append(Paragraph(ach_text, content_style))
        story.append(Spacer(1, 3*mm))
    
    # Certifications
    if resume_data['certifications']:
        story.append(Paragraph("CERTIFICATIONS", section_header_style))
        for cert in resume_data['certifications']:
            cert_text = f"• {cert.get('title', '')} - {cert.get('platform', '')}"
            if cert.get('date'):
                cert_text += f" ({cert.get('date', '')})"
            story.append(Paragraph(cert_text, content_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Sidebar for navigation
st.sidebar.title("📋 Resume Sections")
sections = ["Personal Details", "Career Objective", "Education", "Experience", "Projects", "Skills", "Certifications", "Achievements", "Generate PDF"]
selected_section = st.sidebar.selectbox("Choose Section", sections)

# Personal Details
if selected_section == "Personal Details":
    st.header("👤 Personal Details")
    with st.form(key='personal_form'):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.resume_data['personal']['full_name'] = st.text_input("Full Name *", 
                value=st.session_state.resume_data['personal'].get('full_name', ''),
                placeholder="Rajan Kumar Singh")
            st.session_state.resume_data['personal']['phone'] = st.text_input("Phone Number *", 
                value=st.session_state.resume_data['personal'].get('phone', ''),
                placeholder="+91 8409568399")
            st.session_state.resume_data['personal']['email'] = st.text_input("Email Address *", 
                value=st.session_state.resume_data['personal'].get('email', ''),
                placeholder="rr791337@gmail.com")
        with col2:
            st.session_state.resume_data['personal']['linkedin'] = st.text_input("LinkedIn Profile URL", 
                value=st.session_state.resume_data['personal'].get('linkedin', ''),
                placeholder="https://linkedin.com/in/username")
            st.session_state.resume_data['personal']['portfolio'] = st.text_input("Portfolio/GitHub URL", 
                value=st.session_state.resume_data['personal'].get('portfolio', ''),
                placeholder="https://github.com/username")
            st.session_state.resume_data['personal']['field'] = st.text_input("Field of Study", 
                value=st.session_state.resume_data['personal'].get('field', ''),
                placeholder="Computer Science & Engineering")
            st.session_state.resume_data['personal']['college'] = st.text_input("Current Institution", 
                value=st.session_state.resume_data['personal'].get('college', ''),
                placeholder="Global Institute of Technology Jaipur")
        submit_personal = st.form_submit_button("💾 Save Personal Details", use_container_width=True)

# Career Objective
elif selected_section == "Career Objective":
    st.header("🎯 Career Objective / Summary")
    st.session_state.resume_data['objective'] = st.text_area("Career Objective (2-3 lines)", 
        value=st.session_state.resume_data.get('objective', ''),
        placeholder="A motivated B.Tech graduate seeking to leverage expertise in Python and React to build innovative solutions.",
        height=100)

# Education
elif selected_section == "Education":
    st.header("🎓 Education")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Education", use_container_width=True):
            add_education()
    
    for i, edu in enumerate(st.session_state.resume_data['education']):
        with st.expander(f"🎓 Education {i+1}", expanded=True):
            with st.form(key=f'education_form_{i}'):
                col1, col2 = st.columns(2)
                with col1:
                    edu['degree'] = st.text_input(f"Degree Name *", 
                        value=edu.get('degree', ''),
                        key=f"degree_{i}", 
                        placeholder="B.Tech In Computer Science")
                    edu['college'] = st.text_input(f"College/University *", 
                        value=edu.get('college', ''),
                        key=f"college_{i}", 
                        placeholder="GIT Jaipur")
                    edu['location'] = st.text_input(f"Location", 
                        value=edu.get('location', ''),
                        key=f"location_edu_{i}", 
                        placeholder="Jaipur, Rajasthan")
                with col2:
                    edu['duration'] = st.text_input(f"Duration *", 
                        value=edu.get('duration', ''),
                        key=f"duration_{i}", 
                        placeholder="2023–2027")
                    edu['cgpa'] = st.text_input(f"CGPA/Percentage", 
                        value=edu.get('cgpa', ''),
                        key=f"cgpa_{i}", 
                        placeholder="8.81")
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit_edu = st.form_submit_button(f"💾 Save", use_container_width=True)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Education {i+1}", use_container_width=True):
                        st.session_state.resume_data['education'].pop(i)
                        st.rerun()

# Work Experience
elif selected_section == "Experience":
    st.header("💼 Work Experience / Internships")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Experience", use_container_width=True):
            add_experience()
    
    for i, exp in enumerate(st.session_state.resume_data['experience']):
        with st.expander(f"💼 Experience {i+1}", expanded=True):
            with st.form(key=f'experience_form_{i}'):
                col1, col2 = st.columns(2)
                with col1:
                    exp['position'] = st.text_input(f"Position Title *", 
                        value=exp.get('position', ''),
                        key=f"position_{i}", 
                        placeholder="Research Intern")
                    exp['company'] = st.text_input(f"Company/Organization *", 
                        value=exp.get('company', ''),
                        key=f"company_{i}", 
                        placeholder="Indian Institute of Technology, Jammu")
                    exp['duration'] = st.text_input(f"Duration *", 
                        value=exp.get('duration', ''),
                        key=f"duration_exp_{i}", 
                        placeholder="May '25 – Jul'25")
                with col2:
                    exp['location'] = st.text_input(f"Location/Type", 
                        value=exp.get('location', ''),
                        key=f"location_exp_{i}", 
                        placeholder="On-site in IIT Jammu campus")
                    exp['guide'] = st.text_input(f"Guide/Supervisor", 
                        value=exp.get('guide', ''),
                        key=f"guide_{i}", 
                        placeholder="Prof. Parmaveer Nandal")
                
                contributions = st.text_area(f"Key Contributions (one per line)", 
                    value='\n'.join(exp.get('contributions', [])),
                    key=f"contributions_{i}", 
                    placeholder="Developed a real-time anomaly detection system\nBuilt predictive models using LSTM neural networks\nIntegrated Apache Kafka for streaming sensor data",
                    height=120)
                exp['contributions'] = [c.strip() for c in contributions.split('\n') if c.strip()]
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit_exp = st.form_submit_button(f"💾 Save", use_container_width=True)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Experience {i+1}", use_container_width=True):
                        st.session_state.resume_data['experience'].pop(i)
                        st.rerun()

# Projects
elif selected_section == "Projects":
    st.header("🚀 Projects")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Project", use_container_width=True):
            add_project()
    
    for i, proj in enumerate(st.session_state.resume_data['projects']):
        with st.expander(f"🚀 Project {i+1}", expanded=True):
            with st.form(key=f'project_form_{i}'):
                col1, col2 = st.columns(2)
                with col1:
                    proj['name'] = st.text_input(f"Project Name *", 
                        value=proj.get('name', ''),
                        key=f"project_name_{i}", 
                        placeholder="Text-to-Text Generator Transformer")
                    proj['tech'] = st.text_input(f"Tools/Tech Used *", 
                        value=proj.get('tech', ''),
                        key=f"tech_{i}", 
                        placeholder="GPT-2, Transformers, Python, Streamlit")
                    proj['users'] = st.text_input(f"Active Users (if applicable)", 
                        value=proj.get('users', ''),
                        key=f"users_{i}", 
                        placeholder="60")
                with col2:
                    proj['date'] = st.text_input(f"Project Date", 
                        value=proj.get('date', ''),
                        key=f"date_{i}", 
                        placeholder="Jul 2025")
                    proj['guide'] = st.text_input(f"Guide/Mentor", 
                        value=proj.get('guide', ''),
                        key=f"guide_{i}", 
                        placeholder="Prof. Navneet Kumar, IIT Jammu")
                    proj['link'] = st.text_input(f"GitHub/Live Link", 
                        value=proj.get('link', ''),
                        key=f"link_{i}", 
                        placeholder="https://github.com/username/project")
                
                description = st.text_area(f"Description (one point per line)", 
                    value='\n'.join(proj.get('description', [])),
                    key=f"description_{i}", 
                    placeholder="Built a transformer using gpt-2 as base model with 124 million parameters\nDeployed this model on Hugging Face\nCreated interactive space using streamlit",
                    height=100)
                proj['description'] = [d.strip() for d in description.split('\n') if d.strip()]
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit_proj = st.form_submit_button(f"💾 Save", use_container_width=True)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Project {i+1}", use_container_width=True):
                        st.session_state.resume_data['projects'].pop(i)
                        st.rerun()

# Skills
elif selected_section == "Skills":
    st.header("🛠️ Technical Skills")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Programming Languages & Tools")
        languages_input = st.text_area("Languages & Tools (comma separated)", 
            placeholder="C, C++, Python, Dart, Flutter, JavaScript, Bash, SQL, Git, Node.js, MongoDB",
            height=100)
    with col2:
        st.subheader("Technologies & Platforms")
        technologies_input = st.text_area("Technologies (comma separated)", 
            placeholder="Google Cloud Engine, Firebase, Docker, Kubernetes, Google Colab",
            height=100)
    
    # Combine both inputs
    all_skills = []
    if languages_input:
        all_skills.extend([s.strip() for s in languages_input.split(',') if s.strip()])
    if technologies_input:
        all_skills.extend([s.strip() for s in technologies_input.split(',') if s.strip()])
    
    st.session_state.resume_data['skills'] = all_skills

# Certifications
elif selected_section == "Certifications":
    st.header("🏆 Certifications")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Certification", use_container_width=True):
            add_certification()
    
    for i, cert in enumerate(st.session_state.resume_data['certifications']):
        with st.expander(f"🏆 Certification {i+1}", expanded=True):
            with st.form(key=f'certification_form_{i}'):
                col1, col2 = st.columns(2)
                with col1:
                    cert['title'] = st.text_input(f"Certificate Title *", 
                        value=cert.get('title', ''),
                        key=f"cert_title_{i}", 
                        placeholder="AI/ML Certification")
                    cert['platform'] = st.text_input(f"Platform/Institute *", 
                        value=cert.get('platform', ''),
                        key=f"platform_{i}", 
                        placeholder="Coursera")
                with col2:
                    cert['date'] = st.text_input(f"Completion Date *", 
                        value=cert.get('date', ''),
                        key=f"cert_date_{i}", 
                        placeholder="May 2023")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit_cert = st.form_submit_button(f"💾 Save", use_container_width=True)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Certification {i+1}", use_container_width=True):
                        st.session_state.resume_data['certifications'].pop(i)
                        st.rerun()

# Achievements
elif selected_section == "Achievements":
    st.header("🏅 Achievements & Awards")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Achievement", use_container_width=True):
            add_achievement()
    
    for i, ach in enumerate(st.session_state.resume_data['achievements']):
        with st.expander(f"🏅 Achievement {i+1}", expanded=True):
            with st.form(key=f'achievement_form_{i}'):
                col1, col2 = st.columns(2)
                with col1:
                    ach['competition'] = st.text_input(f"Competition/Event *", 
                        value=ach.get('competition', ''),
                        key=f"comp_{i}", 
                        placeholder="Technovate for India Hackathon")
                    ach['result'] = st.text_input(f"Position/Result *", 
                        value=ach.get('result', ''),
                        key=f"result_{i}", 
                        placeholder="1st runner up")
                with col2:
                    ach['organization'] = st.text_input(f"Organization *", 
                        value=ach.get('organization', ''),
                        key=f"org_{i}", 
                        placeholder="The Times of India")
                    ach['date'] = st.text_input(f"Date", 
                        value=ach.get('date', ''),
                        key=f"ach_date_{i}", 
                        placeholder="Apr 2025")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit_ach = st.form_submit_button(f"💾 Save", use_container_width=True)
                with col2:
                    if st.form_submit_button(f"🗑️ Delete Achievement {i+1}", use_container_width=True):
                        st.session_state.resume_data['achievements'].pop(i)
                        st.rerun()

# Generate PDF Section
elif selected_section == "Generate PDF":
    st.header("📄 Generate Professional Resume")
    
    # Preview section
    st.subheader("📋 Resume Preview")
    
    # Display current data summary
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Personal Details", "✅" if st.session_state.resume_data['personal'].get('full_name') else "❌")
        st.metric("Education Entries", len(st.session_state.resume_data['education']))
        st.metric("Experience Entries", len(st.session_state.resume_data['experience']))
        st.metric("Project Entries", len(st.session_state.resume_data['projects']))
    
    with col2:
        st.metric("Skills Added", len(st.session_state.resume_data['skills']))
        st.metric("Certifications", len(st.session_state.resume_data['certifications']))
        st.metric("Achievements", len(st.session_state.resume_data['achievements']))
        st.metric("Objective", "✅" if st.session_state.resume_data.get('objective') else "❌")
    
    st.markdown("---")
    
    # Generate PDF button with validation
    if st.session_state.resume_data['personal'].get('full_name'):
        if st.button("🚀 Generate Professional Resume PDF", use_container_width=True, type="primary"):
            with st.spinner('Generating your professional resume...'):
                try:
                    pdf_buffer = generate_professional_pdf(st.session_state.resume_data)
                    
                    st.success("✅ Resume generated successfully!")
                    
                    # Create download button
                    st.download_button(
                        label="📥 Download Professional Resume PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"{st.session_state.resume_data['personal']['full_name'].replace(' ', '_')}_Resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
    else:
        st.warning("⚠️ Please fill in at least your name in Personal Details before generating the PDF.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎯 Professional Resume Builder | Built with Streamlit & ReportLab</p>
    </div>
    """, 
    unsafe_allow_html=True
)
