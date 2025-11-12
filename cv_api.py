#!/usr/bin/env python3
"""
API Flask pour générer des CV à partir de CSV
Compatible avec Custom GPT OpenAPI 3.1.0
"""

from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import csv
import uuid
from datetime import datetime
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak
from reportlab.lib.enums import TA_CENTER
import io
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = '/tmp/cv_uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/cv_outputs'

# Créer les dossiers s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Configuration des couleurs
DARK_BLUE = colors.HexColor('#1e3a5f')
ACCENT_BLUE = colors.HexColor('#2980b9')
TEXT_GRAY = colors.HexColor('#333333')

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_COLUMN_WIDTH = 7*cm
MARGIN = 1.5*cm


def create_styles():
    """Crée tous les styles nécessaires pour le CV"""
    styles = getSampleStyleSheet()
    
    # Styles sidebar
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
    
    # Styles main content
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


def parse_csv_content(csv_content):
    """Parse le contenu CSV"""
    data = defaultdict(lambda: defaultdict(list))
    
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    for row in csv_reader:
        if row['section'].startswith('#') or not row['section'].strip():
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


def build_sidebar(data, styles):
    """Construit le contenu de la colonne latérale"""
    story = []
    
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
        
        experiences = defaultdict(dict)
        for key in data['experience']:
            if '_' in key:
                prefix, suffix = key.split('_', 1)
                if suffix not in experiences[prefix]:
                    experiences[prefix][suffix] = []
                experiences[prefix][suffix].extend(data['experience'][key])
        
        sorted_experiences = []
        for prefix in experiences:
            if 'titre' in experiences[prefix]:
                order = experiences[prefix]['titre'][0]['order']
                sorted_experiences.append((order, prefix, experiences[prefix]))
        
        sorted_experiences.sort(key=lambda x: x[0])
        
        for _, prefix, exp_data in sorted_experiences:
            if 'titre' in exp_data:
                titre = exp_data['titre'][0]['content']
                story.append(Paragraph(titre, styles['JobTitle']))
            
            if 'periode' in exp_data:
                periode = exp_data['periode'][0]['content']
                story.append(Paragraph(periode, styles['CompanyDate']))
            
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
        
        formations = defaultdict(dict)
        for key in data['formation']:
            if '_' in key:
                prefix, suffix = key.split('_', 1)
                if suffix not in formations[prefix]:
                    formations[prefix][suffix] = []
                formations[prefix][suffix].extend(data['formation'][key])
        
        sorted_formations = []
        for prefix in formations:
            if 'titre' in formations[prefix]:
                order = formations[prefix]['titre'][0]['order']
                sorted_formations.append((order, prefix, formations[prefix]))
        
        sorted_formations.sort(key=lambda x: x[0])
        
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
    
    # Compétences techniques
    if 'competences_tech' in data:
        story.append(Paragraph("COMPÉTENCES TECHNIQUES", styles['MainSection']))
        for comp_key in sorted(data['competences_tech'].keys()):
            for item in data['competences_tech'][comp_key]:
                story.append(Paragraph(f"• {item['content']}", styles['MainBullet']))
        story.append(Spacer(1, 0.2*cm))
    
    return story


def generate_cv_from_csv(csv_content, output_path):
    """Génère le CV PDF à partir du contenu CSV"""
    
    # Parser les données
    data = parse_csv_content(csv_content)
    
    # Créer les styles
    styles = create_styles()
    
    # Créer le document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=0,
        rightMargin=0,
        topMargin=0,
        bottomMargin=0
    )
    
    # Frames
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
    
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, LEFT_COLUMN_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        canvas.restoreState()
    
    page_template = PageTemplate(
        id='TwoColumn',
        frames=[sidebar_frame, main_frame],
        onPage=on_page
    )
    
    doc.addPageTemplates([page_template])
    
    # Construire le contenu
    story = []
    story.extend(build_sidebar(data, styles))
    story.append(FrameBreak())
    story.extend(build_main_content(data, styles))
    
    # Générer le PDF
    doc.build(story)


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/generate-cv', methods=['POST'])
def generate_cv():
    """
    Génère un CV à partir d'un contenu CSV
    
    Body (JSON):
    {
        "csv_content": "section,subsection,type,content,order\\nheader,nom,text,John Doe,1\\n..."
    }
    
    Ou (multipart/form-data):
    - csv_file: fichier CSV uploadé
    
    Response:
    {
        "success": true,
        "cv_id": "uuid",
        "download_url": "/download-cv/uuid",
        "message": "CV généré avec succès"
    }
    """
    try:
        csv_content = None
        
        # Vérifier si c'est du JSON avec csv_content
        if request.is_json:
            data = request.get_json()
            csv_content = data.get('csv_content')
            
            if not csv_content:
                return jsonify({
                    "success": False,
                    "error": "Le champ 'csv_content' est requis"
                }), 400
        
        # Vérifier si c'est un fichier uploadé
        elif 'csv_file' in request.files:
            file = request.files['csv_file']
            if file.filename == '':
                return jsonify({
                    "success": False,
                    "error": "Aucun fichier sélectionné"
                }), 400
            
            if not file.filename.endswith('.csv'):
                return jsonify({
                    "success": False,
                    "error": "Le fichier doit être un CSV"
                }), 400
            
            csv_content = file.read().decode('utf-8')
        
        else:
            return jsonify({
                "success": False,
                "error": "Aucun contenu CSV fourni. Utilisez 'csv_content' (JSON) ou 'csv_file' (multipart)"
            }), 400
        
        # Générer un ID unique pour ce CV
        cv_id = str(uuid.uuid4())
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{cv_id}.pdf")
        
        # Générer le CV
        generate_cv_from_csv(csv_content, output_path)
        
        # Construire l'URL de téléchargement
        download_url = url_for('download_cv', cv_id=cv_id, _external=True)
        
        return jsonify({
            "success": True,
            "cv_id": cv_id,
            "download_url": download_url,
            "message": "CV généré avec succès"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/download-cv/<cv_id>', methods=['GET'])
def download_cv(cv_id):
    """
    Télécharge un CV généré
    
    Params:
    - cv_id: UUID du CV généré
    
    Response:
    - Fichier PDF
    """
    try:
        # Sécuriser le cv_id
        cv_id = secure_filename(cv_id)
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{cv_id}.pdf")
        
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "CV non trouvé"
            }), 404
        
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='cv_generated.pdf'
        )
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/openapi.json', methods=['GET'])
def openapi_spec():
    """Retourne la spécification OpenAPI 3.1.0"""
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "CV Generator API",
            "description": "API pour générer des CV professionnels à partir de fichiers CSV",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": request.url_root.rstrip('/')
            }
        ],
        "paths": {
            "/generate-cv": {
                "post": {
                    "summary": "Génère un CV à partir d'un contenu CSV",
                    "description": "Prend un contenu CSV en entrée et génère un CV professionnel en PDF",
                    "operationId": "generateCV",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "csv_content": {
                                            "type": "string",
                                            "description": "Contenu du fichier CSV avec les colonnes: section, subsection, type, content, order"
                                        }
                                    },
                                    "required": ["csv_content"]
                                },
                                "example": {
                                    "csv_content": "section,subsection,type,content,order\nheader,nom,text,SUAN TAY,1\nheader,titre,text,Ingénieur IA,2\n"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "CV généré avec succès",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean"
                                            },
                                            "cv_id": {
                                                "type": "string",
                                                "format": "uuid"
                                            },
                                            "download_url": {
                                                "type": "string",
                                                "format": "uri"
                                            },
                                            "message": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Requête invalide"
                        },
                        "500": {
                            "description": "Erreur serveur"
                        }
                    }
                }
            },
            "/download-cv/{cv_id}": {
                "get": {
                    "summary": "Télécharge un CV généré",
                    "description": "Récupère le fichier PDF d'un CV précédemment généré",
                    "operationId": "downloadCV",
                    "parameters": [
                        {
                            "name": "cv_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string",
                                "format": "uuid"
                            },
                            "description": "UUID du CV à télécharger"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Fichier PDF du CV",
                            "content": {
                                "application/pdf": {
                                    "schema": {
                                        "type": "string",
                                        "format": "binary"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "CV non trouvé"
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Vérifie l'état de l'API",
                    "operationId": "healthCheck",
                    "responses": {
                        "200": {
                            "description": "API en ligne",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string"
                                            },
                                            "timestamp": {
                                                "type": "string",
                                                "format": "date-time"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(spec)


if __name__ == '__main__':
    print("🚀 Démarrage de l'API CV Generator")
    print(f"📁 Dossier uploads: {app.config['UPLOAD_FOLDER']}")
    print(f"📁 Dossier outputs: {app.config['OUTPUT_FOLDER']}")
    print("🌐 OpenAPI spec disponible sur: http://localhost:5000/openapi.json")
    app.run(debug=True, host='0.0.0.0', port=5000)
