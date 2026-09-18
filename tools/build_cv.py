"""Build the public two-page CV. Requires reportlab; uses installed Arial fonts."""
from pathlib import Path
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(os.environ.get('CV_FONT_DIR', 'C:/Windows/Fonts'))
for name, file in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial', boldItalic='Arial-Bold')

styles = {
    'name': ParagraphStyle('Name', fontName='Arial-Bold', fontSize=27, leading=31, spaceAfter=6, textColor=black),
    'tagline': ParagraphStyle('Tagline', fontName='Arial', fontSize=11.2, leading=15, spaceAfter=9),
    'contact': ParagraphStyle('Contact', fontName='Arial', fontSize=9.2, leading=13, spaceAfter=3),
    'section': ParagraphStyle('Section', fontName='Arial-Bold', fontSize=10, leading=13, spaceBefore=13, spaceAfter=7, keepWithNext=True),
    'body': ParagraphStyle('Body', fontName='Arial', fontSize=10, leading=13.5, spaceAfter=6),
    'role': ParagraphStyle('Role', fontName='Arial-Bold', fontSize=10.6, leading=14, spaceBefore=8, spaceAfter=3, keepWithNext=True),
    'meta': ParagraphStyle('Meta', fontName='Arial', fontSize=9.1, leading=12.5, spaceAfter=5, keepWithNext=True),
    'bullet': ParagraphStyle('Bullet', fontName='Arial', fontSize=10, leading=13.3, leftIndent=11, firstLineIndent=-10, spaceAfter=3),
    'small': ParagraphStyle('Small', fontName='Arial', fontSize=9.4, leading=13.1, spaceAfter=6),
}

story = []
def p(text, style='body'):
    return Paragraph(text, styles[style])
def add(text, style='body'):
    story.append(p(text, style))
def section(title):
    add(title.upper(), 'section')
def role(title, organisation, dates, location, bullets):
    block = [p(title + ' | ' + organisation, 'role'), p(dates + ' | ' + location, 'meta')]
    block += [p('- ' + text, 'bullet') for text in bullets]
    story.append(KeepTogether(block))
def link(url, label):
    return f'<link href="{url}" color="#000000"><u>{label}</u></link>'

add('RIFAT ISLAM RUPOK', 'name')
add('Research &amp; Analytics | Grants &amp; Programme Development', 'tagline')
add('Winnipeg, Manitoba | ' + link('https://rupokri.ca', 'rupokri.ca') + ' | ' + link('https://linkedin.com/in/rifat-rupok', 'linkedin.com/in/rifat-rupok'), 'contact')
add(link('mailto:contact@rupokri.ca', 'contact@rupokri.ca') + ' | Backup: ' + link('mailto:rifatislamrupok02@gmail.com', 'rifatislamrupok02@gmail.com'), 'contact')

section('Professional profile')
add('Research, analytics, and development professional with experience across Canada and Bangladesh. Coordinate a $17M+ grant portfolio at Siloam Mission, connecting funding requirements, programme evidence, and stakeholder relationships. Combine social science research, practical data skills, and team leadership to produce clear reports, funding cases, and actionable recommendations.')

section('Core capabilities')
add('Grant writing and compliance | Policy and mixed-methods research | Data analysis and visualisation | Programme reporting and evaluation | Stakeholder engagement | Project coordination | Team leadership', 'body')
add('Technical tools: Python, SQL, Excel, Power BI, Tableau, R, and DonorPerfect.', 'small')

section('Professional experience')
role('Development Coordinator', 'Siloam Mission', 'June 2023 - Present', 'Winnipeg, MB', [
    'Coordinate a $17M+ portfolio across 23+ funding agreements, spanning applications, financial tracking, compliance requirements, and funder reporting.',
    'Work across Finance, Programs, and Development to assemble evidence, clarify deliverables, and coordinate reporting and funding activities.',
    'Prepare grant applications, cases for support, and donor impact reports that connect programme needs with funder priorities.',
    'Apply donor and programme analytics to support planning, stewardship, and evidence-based decisions; maintain relationships with institutional funders and government partners.',
])
role('Research Analyst', 'Manitoba Métis Federation', 'April 2023 - May 2023', 'Winnipeg, MB', [
    'Conducted policy and data analysis supporting Métis community initiatives, translating findings into research reports and recommendations for stakeholders.',
    'Delivered short-cycle research assignments under tight timelines, combining evidence synthesis with attention to community context.',
])
role('Managing Partner', 'Beyond Peace', 'October 2020 - April 2023', 'Dhaka, Bangladesh', [
    'Led partnerships, strategic planning, resource allocation, and operations for peacebuilding and community research initiatives.',
    'Supervised six research assistants and coordinated community field research on education technology access in Dhaka\'s Korail community.',
    'Developed collaborations with local and international partners and facilitated workshops on conflict resolution and community engagement.',
])

story.append(PageBreak())
add('RESEARCH, EDUCATION & SELECTED WORK', 'section')
role('Research Data Analyst', 'Centre for Genocide Studies, University of Dhaka', 'December 2020 - December 2021', 'Dhaka, Bangladesh', [
    'Analysed human rights and conflict datasets and produced reports and visualisations to inform policy and advocacy.',
    'Maintained ethical data protocols and trained junior analysts in research methodology and responsible data handling.',
])
role('Research Assistant', 'NETZ', 'January 2020 - November 2020', 'Dhaka, Bangladesh', [
    'Supported development and justice research through literature reviews, field data collection, and stakeholder presentations.',
])
role('Administrative Assistant', 'Community Development Federation', 'January 2018 - December 2019', 'Dhaka, Bangladesh', [
    'Supported community programmes through event coordination, funding applications, record management, and compliance documentation.',
])

section('Education')
add('Master of Social Science, Peace and Conflict Studies | University of Dhaka | 2019', 'small')
add('Bachelor of Social Science, Peace and Conflict Studies | University of Dhaka | 2015 - 2018', 'small')

section('Certifications & professional development')
add('Google Data Analytics | Google, 2023<br/>Fundraising and Development Foundations | UC Davis, 2023<br/>Python for Data Science, AI &amp; Development | IBM, 2023<br/>Fundamentals of Predictive Project Management | PMI, 2024<br/>Six Sigma White Belt | Educate360, 2025', 'small')

section('Selected publications')
add('Recent Developments in India-Bangladesh Relations: A Comprehensive Analysis. SSRN working paper, 2025. ' + link('https://doi.org/10.2139/ssrn.5230684', 'doi.org/10.2139/ssrn.5230684'), 'small')
add('Geopolitical Chess in South and Southeast Asia: US-China Rivalry and the Cost of Regional Instability. SSRN working paper, 2025. ' + link('https://doi.org/10.2139/ssrn.5557040', 'doi.org/10.2139/ssrn.5557040'), 'small')
add('Integration of Technology in Education for Marginalized Children in the Korail Slum of Dhaka during the COVID-19 Pandemic. EdTech Hub / Beyond Peace, 2021. ' + link('https://doi.org/10.53832/edtechhub.0063', 'doi.org/10.53832/edtechhub.0063'), 'small')
add('Public commentary: letters on housing, addiction, and urban policy in the Winnipeg Free Press, 2024-2025.', 'small')

section('Independent project')
add('Flowly | ' + link('https://flowly.today', 'flowly.today') + '<br/>Build and maintain a minimalist RSS news reader, exploring product design and a calmer approach to following the news. Public beta.', 'small')

def page_frame(c, doc):
    c.saveState()
    c.setStrokeColor(black)
    c.setLineWidth(.6)
    c.line(45, 751, 567, 751)
    c.setLineWidth(.35)
    c.line(45, 37, 567, 37)
    c.setFont('Arial', 8)
    c.drawString(45, 24, 'RIFAT ISLAM RUPOK  |  rupokri.ca')
    c.drawRightString(567, 24, f'{doc.page} / 2')
    c.restoreState()

doc = SimpleDocTemplate(str(ROOT / 'Rifat_Rupok_CV.pdf'), pagesize=letter,
    rightMargin=45, leftMargin=45, topMargin=53, bottomMargin=48,
    title='Rifat Islam Rupok | Research, Analytics & Development',
    author='Rifat Islam Rupok', subject='Professional resume',
    pageCompression=1)
doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
print('Created', ROOT / 'Rifat_Rupok_CV.pdf')
