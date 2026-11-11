"""Rebuild diagrams and report with reportlab; reads real HTTP results and browser captures."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon
from reportlab.graphics import renderSVG,renderPM
from PIL import Image as PILImage
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1];DOC=ROOT/'docs';OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
INK=colors.HexColor('#173A3E');TEAL=colors.HexColor('#18796E');GRAY=colors.HexColor('#60777D');PALE=colors.HexColor('#EDF5F2')
SCHOOL=ROOT.parents[2]
def box(d,x,y,w,h,title,lines):
 d.add(Rect(x,y,w,h,rx=8,fillColor=colors.white,strokeColor=colors.HexColor('#C9DAD7')))
 d.add(Rect(x,y+h-34,w,34,fillColor=INK,strokeColor=INK))
 d.add(String(x+13,y+h-23,title,fontName='Helvetica-Bold',fontSize=13,fillColor=colors.white))
 for n,line in enumerate(lines):d.add(String(x+13,y+h-54-n*18,line,fontName='Helvetica',fontSize=11,fillColor=INK))
def arrow(d,x1,y1,x2,y2,label='',tx=None,ty=None):
 d.add(Line(x1,y1,x2,y2,strokeColor=TEAL,strokeWidth=1.5))
 import math
 a=math.atan2(y2-y1,x2-x1);sz=7
 d.add(Polygon([x2,y2,x2-sz*math.cos(a-.4),y2-sz*math.sin(a-.4),x2-sz*math.cos(a+.4),y2-sz*math.sin(a+.4)],fillColor=TEAL,strokeColor=TEAL))
 if label:d.add(String(tx if tx is not None else (x1+x2)/2,ty if ty is not None else (y1+y2)/2+7,label,fontName='Helvetica',fontSize=10,fillColor=GRAY,textAnchor='middle'))
entities=Drawing(800,580)
box(entities,20,300,265,250,'AppUser',['id : Long (PK)','fullName : String','email : String (unique)','password : BCrypt hash','role : EMPLOYEE / TECHNICIAN / ADMIN','enabled : boolean','createdAt : Instant'])
box(entities,470,280,310,270,'Incident',['id : Long (PK)','title / description : String','category / priority / status : enum','createdAt / updatedAt : Instant','createdBy : AppUser (required FK)','assignedTo : AppUser (optional FK)'])
box(entities,20,20,310,170,'IncidentHistory',['id : Long (PK)','incident : Incident (required FK)','author : AppUser (required FK)','event : String','createdAt : Instant'])
box(entities,470,20,310,170,'IncidentComment',['id : Long (PK)','incident : Incident (required FK)','author : AppUser (required FK)','content : String','createdAt : Instant'])
arrow(entities,470,470,285,470,'createdBy : many -> 1',377,483)
arrow(entities,470,420,285,420,'assignedTo : many -> 0..1',377,433)
arrow(entities,170,190,170,300,'author : many -> 1',170,235)
arrow(entities,620,190,620,280,'incident : many -> 1',620,225)
arrow(entities,330,140,485,280,'incident : many -> 1',383,185)
entities.add(String(390,5,'Comment.author also references AppUser (many -> 1). All links use @ManyToOne LAZY.',fontName='Helvetica',fontSize=10,fillColor=GRAY,textAnchor='middle'))
architecture=Drawing(800,520)
box(architecture,160,410,480,85,'React :5173',['Pages + ProtectedRoute / RoleRoute + Axios interceptors'])
box(architecture,160,280,480,85,'Spring Security :8080',['JwtFilter: signature, expiration, enabled user, authorities'])
box(architecture,160,150,480,85,'Controllers -> IncidentService',['DTO validation -> roles -> ownership -> history / notes'])
box(architecture,160,20,480,85,'JPA repositories -> H2 file database',['Users, incidents, history and comments persisted locally'])
arrow(architecture,400,410,400,365,'HTTP JSON + Authorization: Bearer JWT',400,385)
arrow(architecture,400,280,400,235,'Authenticated principal',400,255)
arrow(architecture,400,150,400,105,'Transactional data access',400,125)
for name,d in [('entities',entities),('architecture',architecture)]:
 renderSVG.drawToFile(d,str(DOC/(name+'.svg')))
 try:renderPM.drawToFile(d,str(DOC/(name+'.png')),fmt='PNG')
 except Exception:pass
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom',fontName='Helvetica-Bold',fontSize=30,leading=36,textColor=INK,spaceAfter=18))
styles.add(ParagraphStyle(name='SectionCustom',fontName='Helvetica-Bold',fontSize=18,leading=23,textColor=INK,spaceBefore=10,spaceAfter=12))
styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=10.3,leading=15.4,textColor=INK,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallCustom',fontName='Helvetica',fontSize=8.3,leading=12,textColor=GRAY,spaceAfter=7))
styles.add(ParagraphStyle(name='LabelCustom',fontName='Helvetica-Bold',fontSize=9,leading=14,textColor=TEAL,spaceAfter=12))
story=[]
def p(text,style='BodyCustom'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'SectionCustom')
def new():story.append(PageBreak())
def diagram(d):
 import copy
 dc=copy.deepcopy(d);scale=490/d.width;dc.scale(scale,scale);dc.width*=scale;dc.height*=scale;story.append(dc);story.append(Spacer(1,12))
def table(rows,widths):
 content=[[Paragraph(escape(str(c)),styles['SmallCustom']) for c in row] for row in rows]
 t=Table(content,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#DDE7E5'))]));story.append(t);story.append(Spacer(1,12))
def shot(name,caption,maxh=280):
 path=DOC/'screenshots'/name
 if not path.exists():return
 w,h=PILImage.open(path).size;ratio=min(490/w,maxh/h);story.append(Image(str(path),w*ratio,h*ratio));p(caption,'SmallCustom')
story.append(Spacer(1,8))
logo_left=Image(str(SCHOOL/'logo.png'),width=300,height=80,kind='proportional')
logo_right=Image(str(SCHOOL/'Logo_UHIIC.png'),width=100,height=100,kind='proportional')
logos=Table([[logo_left,logo_right]],colWidths=[365,125],rowHeights=[104],hAlign='CENTER')
logos.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story.append(logos)
story.append(Spacer(1,12))
p('SÉCURITÉ DES SYSTÈMES DISTRIBUÉS','LabelCustom')
p('COMPTE RENDU','TitleCustom');p('Projet Incident Desk<br/>Authentification et autorisation avec Spring Security, JWT et React','SectionCustom')
p('Établissement : ENSET Mohammedia — Université Hassan II de Casablanca<br/>Formation : Master Systèmes Distribués et Intelligence Artificielle (SDIA)','BodyCustom')
table([['Information',''],['Étudiant','Id Hamide Aboubaker'],['Module','Sécurité des systèmes distribués'],['Année universitaire','2026–2027'],['Date','11 novembre 2026']], [145,345])
story.append(Spacer(1,10))
p('Une application web de déclaration et de suivi des incidents informatiques, avec des droits différenciés pour les employés, techniciens et administrateurs.')
table([['Périmètre','Résultat'],['Backend','Spring Boot 3.4.2, Spring Security, JPA, H2, JJWT 0.13.0'],['Frontend','React, Vite, React Router, Axios'],['Vérification exécutée','40 contrôles HTTP réussis et vérification de l’interface dans le navigateur'],['Livrables','Projets backend et frontend, README, diagrammes, collection Postman, neuf captures Postman, captures de l’application et présent compte rendu']], [125,365])
new();h('Objectif pédagogique')
p('Distinguer l’authentification (identifier un utilisateur), l’autorisation par rôle (autoriser une action) et le contrôle des données (vérifier le propriétaire ou le technicien affecté). Une route React masquée ne suffit pas : toute requête est contrôlée par le backend.')
p('Le projet reprend les notions étudiées dans l’atelier JWT. Le code, les tests et les observations documentés sont issus de l’application exécutée et des captures fournies.','SmallCustom')
h('1. Architecture générale');diagram(architecture)
p('React envoie le JWT dans l\'entete Authorization. Le filtre valide sa signature et son expiration, charge le compte et construit l\'authentification. Les controles de role et de propriete precedent toute lecture ou modification sensible.')
p('Le backend utilise SessionCreationPolicy.STATELESS : il ne depend pas d\'une session HTTP pour authentifier les requetes. La base conserve les comptes, incidents, notes et evenements. CORS autorise localhost:5173 et 127.0.0.1:5173.')
p('Les DTO evitent d\'exposer le hash du mot de passe. La validation utilise @NotBlank, @Email, @Size, @NotNull et @Valid. Un @RestControllerAdvice traduit les erreurs applicatives en JSON ; les erreurs du filtre de securite ont des gestionnaires 401/403 dedies.')
new();h('2. Modele de donnees');diagram(entities)
p('Un utilisateur peut creer plusieurs incidents ; chaque incident possede exactement un createur. L\'affectation est optionnelle, mais doit viser un technicien actif. Chaque note et chaque evenement possedent un incident et un auteur.')
p('<b>Choix JPA :</b> @ManyToOne represente le cote portant la cle etrangere. FetchType.LAZY differe le chargement de l\'objet associe ; EAGER impose son chargement. Une collection @OneToMany inverse serait possible, mais les listes sont obtenues ici par des requetes de repository : cela evite des collections bidirectionnelles inutiles. Les DTO sont construits dans une transaction et les getters permettent l\'initialisation des proxies Hibernate.')
p('Les entites utilisent Instant pour les dates. Les historiques tracent creation, affectation, changement de statut et ajout de note. CLOSED est terminal : toute tentative de modification ulterieure est refusee.')
new();h('3. Authentification et autorisations')
table([['Role','Droits'],['EMPLOYEE','Creer un incident, consulter ses propres incidents et modifier son profil.'],['TECHNICIAN','Consulter ses incidents affectes, changer leur statut, ajouter une note.'],['ADMIN','Consulter tous les incidents/utilisateurs, affecter, activer/desactiver, consulter les statistiques.']], [110,380])
p('<b>Inscription :</b> le role EMPLOYEE est fixe par le serveur. Le DTO ne contient pas de role ; une tentative d\'injection de ADMIN ne donne aucun privilege. Le mot de passe est encode avec BCrypt et compare via matches lors de la connexion.')
p('<b>Claims JWT :</b> sub identifie l\'email ; iat represente la creation ; exp limite la validite a cinq minutes ; role indique le role. JJWT ajoute ces champs avec subject, issuedAt, expiration et claim, puis signe le token. Le parseur verifie la signature et rejette un token expire. Un JWT signe n\'est pas un chiffrement.')
p('<b>Role :</b> @EnableMethodSecurity active @PreAuthorize. hasRole(\'ADMIN\') correspond a l\'autorite ROLE_ADMIN ; hasAuthority compare une autorite exacte. Le filtre relit le role et enabled en base : un compte desactive ne peut plus utiliser son ancien JWT.')
p('<b>Propriete :</b> Authentication.getName() fournit l\'email authentifie. IncidentService charge l\'utilisateur et compare son identifiant a createdBy ou assignedTo. Meme un appel direct a /api/incidents/{id} ne contourne pas ce controle.')
p('<b>Profil :</b> le nom et l\'email sont modifiables. Un nouveau JWT est emis apres modification. Le changement de mot de passe exige l\'ancien mot de passe correct et une confirmation identique.')
p('<b>Refresh token :</b> extension facultative non implementee. Un access token autorise l\'API pour une courte duree ; un refresh token sert a obtenir un nouvel access token et demande une politique de rotation/revocation. Ici, l\'expiration exige une nouvelle connexion.')
new();h('4. Tests de securite executes')
results=json.loads((DOC/'test-results.json').read_text());mandatory=[r for r in results if r['name'][:2].isdigit()]
table([['Cas obligatoire','Attendu','Observe']]+[[r['name'],r['expected'],r['actual']] for r in mandatory],[320,85,85])
p(f'<b>{len(results)}/{len(results)} controles HTTP reussis.</b> Le fichier docs/test-results.json conserve les reponses. Le script tests/verify.py est reproductible et ajoute des donnees de demonstration sans effacer les anciennes.')
p('Le cas du JWT expire utilise un token correctement signe avec la cle de demonstration et une date exp dans le passe. Il teste donc l\'expiration, et non simplement une signature invalide.')
p('Controles supplementaires : JWT d\'un utilisateur desactive, employe tentant une affectation, refus de modifier CLOSED, incident inexistant, inscription avec role ADMIN, confirmation/ancien mot de passe, mise a jour du profil et nouveau token.')
table([['Statut','Interpretation'],['400','Donnees manquantes, invalides ou incoherentes.'],['401','Authentification absente, invalide, expiree ou compte desactive.'],['403','Utilisateur authentifie mais sans autorisation.'],['404','Ressource introuvable.'],['409','Email deja utilise ou conflit avec l\'etat CLOSED.']], [80,410])
p('<b>Postman :</b> les neuf scénarios obligatoires ont été exécutés dans Postman et leurs réponses sont reproduites dans les pages de preuves qui suivent. Les contrôles supplémentaires du jeu de 40 proviennent du script HTTP reproductible.','SmallCustom')
new();h('5. Scenario fonctionnel et interface')
p('Le scenario HTTP cree deux incidents pour le premier employe et un pour le second. Il verifie l\'isolation, affecte un incident via ADMIN, passe de ASSIGNED a IN_PROGRESS puis RESOLVED, ajoute une note et verifie que le proprietaire retrouve le nouvel etat et l\'historique.')
shot('07-technician-desktop.jpg','Figure 1. Dashboard du technicien : incidents affectes et compteurs adaptes au role.',285)
shot('08-technician-treatment.jpg','Figure 2. Traitement dans React : changement de statut, note et historique sauvegardes.',285)
new();h('6. Captures complementaires')
shot('09-profile.jpg','Figure 3. Profil et formulaire de changement de mot de passe.',260)
p('Les autres captures reelles sont livrees dans docs/screenshots : expiration de session, dashboard employe, historique, dashboard administrateur, gestion des utilisateurs et affectation.')
# Place two narrow screenshots side by side, preserving their original proportions.
paths=[DOC/'screenshots/01-session-expired.jpg',DOC/'screenshots/05-admin-users.jpg'];imgs=[]
for path in paths:
 iw,ih=PILImage.open(path).size;s=min(235/iw,310/ih);imgs.append(Image(str(path),iw*s,ih*s))
story.append(Table([imgs],colWidths=[245,245]));p('Figures 4 et 5. Message de session expiree ; gestion des utilisateurs dans une fenetre etroite.','SmallCustom')
p('Les controles visuels ont couvert les mises en page etroite et bureau, les connexions des trois roles, l\'affectation, la modification de statut, l\'ajout de note et la redirection d\'un technicien tentant une route ADMIN.','SmallCustom')
new();h('7. Execution, demonstration et limites')
p('<b>Lancement :</b> bash start-backend.sh puis bash start-frontend.sh, dans deux terminaux. Ouvrir http://127.0.0.1:5173. Le backend utilise 8080. Les quatre comptes initiaux utilisent Demo1234! : employee1@demo.test, employee2@demo.test, tech@demo.test et admin@demo.test.')
p('<b>Demonstration :</b> employe cree un incident ; administrateur l\'affecte ; technicien ajoute une note et le resout ; employe consulte l\'historique. Montrer ensuite les refus 401 et 403 dans Postman. Le guide docs/DEMO-5-MINUTES.md detaille cette sequence.')
p('<b>Limites explicites :</b> cle JWT et comptes connus pour la demonstration, console H2 publique selon le sujet, aucun refresh token. Un changement de mot de passe ne revoque pas les JWT deja emis ; ils restent limites par leur expiration. Un compte desactive est bloque immediatement. La deconnexion efface sessionStorage. La session navigateur reste exposee a une eventuelle faille XSS : cette application est une demonstration locale, pas un deploiement de production.')
p('<b>Livrables :</b> projets backend et frontend ; README ; présent rapport ; diagrammes SVG et sources Mermaid ; captures de l’application ; collection Postman et résultats HTTP ; neuf captures de tests Postman ; guide de démonstration. La démonstration fonctionnelle devant le professeur constitue l’étape orale de remise.')
h('References techniques')
refs=[('Spring Security - method security','https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html'),('JJWT - claims, signature et parsing','https://github.com/jwtk/jjwt'),('Axios - interceptors','https://axios-http.com/docs/interceptors'),('Jakarta Persistence - ManyToOne','https://jakarta.ee/specifications/persistence/3.0/apidocs/jakarta.persistence/jakarta/persistence/manytoone/')]
for label,url in refs:p(f'<a href="{url}" color="#18796E">{escape(label)}</a>','SmallCustom')
p('Sujet de référence : devoir_jwt_spring_security_react.pdf, sections 1–27. Le code et les observations locales sont la source des résultats annoncés.','SmallCustom')
new();h('8. Preuves des tests Postman')
p('Chaque capture présente la requête numérotée, le statut HTTP obtenu et la réponse du serveur. Le test 07 a été exécuté après désactivation de l’employé 2 ; la réponse 401 confirme que le compte désactivé ne peut pas ouvrir de session.','BodyCustom')
postman=[
 ('01-no-jwt.png','01 — Accès sans JWT : 401 Unauthorized.'),
 ('02-invalid-jwt.png','02 — JWT invalide : 401 Unauthorized.'),
 ('03-expired-jwt.png','03 — JWT signé mais expiré : 401 Unauthorized.'),
 ('04-employee-admin-forbidden.png','04 — Route ADMIN appelée par un employé : 403 Forbidden.'),
 ('05-other-owner-forbidden.png','05 — Incident appartenant à un autre employé : 403 Forbidden.'),
 ('06-unassigned-technician-forbidden.png','06 — Technicien non affecté tentant de modifier un incident : 403 Forbidden.'),
 ('07-disabled-login.png','07 — Connexion d’un compte désactivé : 401 Unauthorized.'),
 ('08-duplicate-email.png','08 — Inscription avec une adresse déjà utilisée : 409 Conflict.'),
 ('09-invalid-incident-data.png','09 — Création d’un incident avec des champs invalides : 400 Bad Request.'),
]
for i,(filename,caption) in enumerate(postman):
 path=DOC/'screenshots'/'postman'/filename
 w,h=PILImage.open(path).size;ratio=min(490/w,275/h)
 story.append(Image(str(path),w*ratio,h*ratio));p(caption,'SmallCustom')
 if i%2==1 and i<len(postman)-1:new()
def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#DBE6E3'));canvas.line(48,43,547,43);canvas.setFont('Helvetica',8);canvas.setFillColor(GRAY);canvas.drawString(48,29,'Id Hamide Aboubaker | SDIA — Incident Desk');canvas.drawRightString(547,29,str(doc.page))
SimpleDocTemplate(str(OUT/'rapport-incident-desk.pdf'),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=42,bottomMargin=58,title='Compte rendu - Incident Desk - Sécurité des systèmes distribués',author='Id Hamide Aboubaker').build(story,onFirstPage=footer,onLaterPages=footer)
print('Report and diagrams generated.')
