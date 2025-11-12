#!/usr/bin/env python3
"""
Template réutilisable pour générer un CV professionnel à partir d'un fichier CSV

Usage:
    python cv_template.py cv_content.csv output.pdf
    
Le fichier CSV doit contenir les colonnes: section, subsection, type, content, order
"""

import csv
import sys
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak
from reportlab.lib.enums import TA_CENTER

# Configuration des couleurs
DARK_BLUE = colors.HexColor('#1e3a5f')
ACCENT_BLUE = colors.HexColor('#2980b9')
TEXT_GRAY = colors.HexColor('#333333')

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_COLUMN_WIDTH = 7*cm
MARGIN = 1.5*cm


def load_cv_data(csv_file):
    """Charge les données du CV depuis un fichier CSV"""
    data = defaultdict(lambda: defaultdict(list))
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ignorer les lignes de commentaires
            if row['section'].startswith('#'):
                continue
            
            section = row['section'].strip()
            subsection = row['subsection'].strip()
            content_type = row['type'].strip()
            content = row['content'].strip()
            order = int(row['order']) if row['order'].strip() else 0
            
            data[section][subsection].append({
                'type': content_type,
                'content': content,
                'order': order
            })
    
    # Trier par ordre
    for section in data:
        for subsection in data[section]:
            data[section][subsection].sort(key=lambda x: x['order'])
    
    return data


def create_styles():
    """Crée tous les styles nécessaires pour le CV"""
    styles = getSampleStyleSheet()
    
    # Styles pour la sidebar (colonne gauche)
    styles.add(ParagraphStyle(
        name='SidebarName',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.white,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SidebarTitle',
        parent=styles['Normal'],
        fontSize=13,
        textColor=colors.HexColor('#ecf0f1'),
        spaceAfter=12,
        fontName='Helvetica',
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SidebarSection',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        leftIndent=5
    ))
    
    styles.add(ParagraphStyle(
        name='SidebarText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#ecf0f1'),
        spaceAfter=4,
        leading=11,
        fontName='Helvetica',
        leftIndent=5
    ))
    
    styles.add(ParagraphStyle(
        name='SidebarBullet',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#ecf0f1'),
        spaceAfter=3,
        leading=11,
        fontName='Helvetica',
        leftIndent=10,
        bulletIndent=5
    ))
    
    # Styles pour le contenu principal (colonne droite)
    styles.add(ParagraphStyle(
        name='MainSection',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='JobTitle',
        parent=styles['Normal'],
        fontSize=10.5,
        textColor=DARK_BLUE,
        spaceBefore=5,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CompanyDate',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        spaceAfter=3,
        fontName='Helvetica-Oblique'
    ))
    
    styles.add(ParagraphStyle(
        name='MainText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_GRAY,
        spaceAfter=3,
        leading=11,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='MainBullet',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_GRAY,
        leftIndent=12,
        spaceAfter=2,
        leading=11,
        fontName='Helvetica'
    ))
    
    return styles


def build_sidebar(data, styles):
    """Construit le contenu de la colonne latérale"""
    story = []
    
    # Nom et titre
    story.append(Spacer(1, 1*cm))
    if 'header' in data:
        if 'nom' in data['header']:
            nom = data['header']['nom'][0]['content']
            story.append(Paragraph(nom, styles['SidebarName']))
        
        if 'titre' in data['header']:
            titre = data['header']['titre'][0]['content']
            story.append(Paragraph(titre, styles['SidebarTitle']))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Contact
    story.append(Paragraph("📧 Contact", styles['SidebarSection']))
    if 'header' in data:
        for key in ['email', 'telephone', 'localisation', 'remote']:
            if key in data['header']:
                content = data['header'][key][0]['content']
                story.append(Paragraph(content, styles['SidebarText']))
    story.append(Spacer(1, 0.3*cm))
    
    # Réseaux sociaux
    if 'header' in data and ('twitter' in data['header'] or 'linkedin' in data['header']):
        story.append(Paragraph("🌐 Réseaux sociaux", styles['SidebarSection']))
        for key in ['twitter', 'linkedin']:
            if key in data['header']:
                content = data['header'][key][0]['content']
                story.append(Paragraph(content, styles['SidebarText']))
        story.append(Spacer(1, 0.3*cm))
    
    # Langues
    if 'langues' in data:
        story.append(Paragraph("🌍 Langues", styles['SidebarSection']))
        for lang_key in sorted(data['langues'].keys()):
            for item in data['langues'][lang_key]:
                story.append(Paragraph(item['content'], styles['SidebarText']))
        story.append(Spacer(1, 0.3*cm))
    
    # Compétences clés
    if 'competences_cles' in data:
        story.append(Paragraph("💡 Compétences clés", styles['SidebarSection']))
        for comp_key in sorted(data['competences_cles'].keys()):
            for item in data['competences_cles'][comp_key]:
                story.append(Paragraph(f"• {item['content']}", styles['SidebarBullet']))
                story.append(Spacer(1, 0.2*cm))
        story.append(Spacer(1, 0.3*cm))
    
    # Centres d'intérêt
    if 'centres_interet' in data:
        story.append(Paragraph("🎨 Centres d'intérêt", styles['SidebarSection']))
        for interet_key in sorted(data['centres_interet'].keys()):
            for item in data['centres_interet'][interet_key]:
                story.append(Paragraph(item['content'], styles['SidebarText']))
    
    return story


def build_main_content(data, styles):
    """Construit le contenu principal"""
    story = []
    
    story.append(Spacer(1, 0.5*cm))
    
    # Profil
    if 'profil' in data:
        story.append(Paragraph("PROFIL", styles['MainSection']))
        if 'description' in data['profil']:
            profil_text = data['profil']['description'][0]['content']
            story.append(Paragraph(profil_text, styles['MainText']))
        story.append(Spacer(1, 0.3*cm))
    
    # Expériences professionnelles
    if 'experience' in data:
        story.append(Paragraph("EXPÉRIENCES PROFESSIONNELLES", styles['MainSection']))
        
        # Grouper les expériences par préfixe (iafluence_, appuy_, etc.)
        experiences = defaultdict(dict)
        for key in data['experience']:
            # Extraire le préfixe (avant le _)
            if '_' in key:
                prefix, suffix = key.split('_', 1)
                if suffix not in experiences[prefix]:
                    experiences[prefix][suffix] = []
                experiences[prefix][suffix].extend(data['experience'][key])
        
        # Trier les expériences par ordre
        sorted_experiences = []
        for prefix in experiences:
            if 'titre' in experiences[prefix]:
                order = experiences[prefix]['titre'][0]['order']
                sorted_experiences.append((order, prefix, experiences[prefix]))
        
        sorted_experiences.sort(key=lambda x: x[0])
        
        # Afficher chaque expérience
        for _, prefix, exp_data in sorted_experiences:
            if 'titre' in exp_data:
                titre = exp_data['titre'][0]['content']
                story.append(Paragraph(titre, styles['JobTitle']))
            
            if 'periode' in exp_data:
                periode = exp_data['periode'][0]['content']
                story.append(Paragraph(periode, styles['CompanyDate']))
            
            # Bullets
            bullets = []
            for key in exp_data:
                if key.startswith('bullet'):
                    bullets.extend(exp_data[key])
            
            bullets.sort(key=lambda x: x['order'])
            for bullet in bullets:
                story.append(Paragraph(f"• {bullet['content']}", styles['MainBullet']))
            
            story.append(Spacer(1, 0.2*cm))
    
    # Formations
    if 'formation' in data:
        story.append(Paragraph("DIPLÔMES ET FORMATIONS", styles['MainSection']))
        
        # Grouper les formations par préfixe
        formations = defaultdict(dict)
        for key in data['formation']:
            if '_' in key:
                prefix, suffix = key.split('_', 1)
                if suffix not in formations[prefix]:
                    formations[prefix][suffix] = []
                formations[prefix][suffix].extend(data['formation'][key])
        
        # Trier par ordre
        sorted_formations = []
        for prefix in formations:
            if 'titre' in formations[prefix]:
                order = formations[prefix]['titre'][0]['order']
                sorted_formations.append((order, prefix, formations[prefix]))
        
        sorted_formations.sort(key=lambda x: x[0])
        
        # Afficher chaque formation
        for _, prefix, form_data in sorted_formations:
            if 'titre' in form_data:
                titre = form_data['titre'][0]['content']
                story.append(Paragraph(titre, styles['JobTitle']))
            
            if 'periode' in form_data:
                periode = form_data['periode'][0]['content']
                story.append(Paragraph(periode, styles['CompanyDate']))
            
            if 'description' in form_data:
                description = form_data['description'][0]['content']
                story.append(Paragraph(description, styles['MainText']))
            
            story.append(Spacer(1, 0.15*cm))
    
    # Compétences techniques (optionnel - page 2)
    if 'competences_tech' in data:
        story.append(Paragraph("COMPÉTENCES TECHNIQUES", styles['MainSection']))
        for comp_key in sorted(data['competences_tech'].keys()):
            for item in data['competences_tech'][comp_key]:
                story.append(Paragraph(f"• {item['content']}", styles['MainBullet']))
        story.append(Spacer(1, 0.2*cm))
    
    return story


def generate_cv(csv_file, output_file):
    """Génère le CV PDF à partir du fichier CSV"""
    
    # Charger les données
    print(f"📖 Chargement des données depuis {csv_file}...")
    data = load_cv_data(csv_file)
    
    # Créer les styles
    styles = create_styles()
    
    # Créer le document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=0,
        rightMargin=0,
        topMargin=0,
        bottomMargin=0
    )
    
    # Définir les frames (colonnes)
    sidebar_frame = Frame(
        0, 0, LEFT_COLUMN_WIDTH, PAGE_HEIGHT,
        leftPadding=10, rightPadding=10, topPadding=10, bottomPadding=10,
        showBoundary=0
    )
    
    main_frame = Frame(
        LEFT_COLUMN_WIDTH, 0, PAGE_WIDTH - LEFT_COLUMN_WIDTH, PAGE_HEIGHT,
        leftPadding=MARGIN, rightPadding=MARGIN, topPadding=MARGIN, bottomPadding=MARGIN,
        showBoundary=0
    )
    
    # Fonction pour dessiner le fond de la sidebar
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, LEFT_COLUMN_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        canvas.restoreState()
    
    # Créer le template de page
    page_template = PageTemplate(
        id='TwoColumn',
        frames=[sidebar_frame, main_frame],
        onPage=on_page
    )
    
    doc.addPageTemplates([page_template])
    
    # Construire le contenu
    print("🔨 Construction du CV...")
    story = []
    
    # Contenu de la sidebar
    story.extend(build_sidebar(data, styles))
    
    # Passage au frame principal
    story.append(FrameBreak())
    
    # Contenu principal
    story.extend(build_main_content(data, styles))
    
    # Générer le PDF
    print(f"📄 Génération du PDF: {output_file}...")
    doc.build(story)
    
    print(f"✅ CV généré avec succès: {output_file}")


if __name__ == "__main__":
    # Arguments par défaut
    csv_file = "cv_content.csv"
    output_file = "cv_output.pdf"
    
    # Lire les arguments en ligne de commande
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        generate_cv(csv_file, output_file)
    except FileNotFoundError:
        print(f"❌ Erreur: Le fichier {csv_file} n'existe pas")
        print(f"\nUsage: python {sys.argv[0]} [fichier_csv] [fichier_pdf_sortie]")
        print(f"Exemple: python {sys.argv[0]} cv_content.csv mon_cv.pdf")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la génération du CV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
