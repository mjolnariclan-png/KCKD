from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Font
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

# Output
output_dir = r"C:\Users\mille\Desktop\KCKD\rulebook"
os.makedirs(output_dir, exist_ok=True)
pdf_path = os.path.join(output_dir, "Klandestine_Rulebook_FULL_1.pdf")

# Document
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=1*inch,
    bottomMargin=1*inch
)

# Styles
title = ParagraphStyle('title', fontName='DejaVu', fontSize=28, alignment=TA_CENTER, spaceAfter=20)
section = ParagraphStyle('section', fontName='DejaVu', fontSize=18, textColor=colors.HexColor("#4a90d9"), spaceBefore=16, spaceAfter=10)
sub = ParagraphStyle('sub', fontName='DejaVu', fontSize=13, textColor=colors.HexColor("#d4af37"), spaceBefore=10, spaceAfter=6)
body = ParagraphStyle('body', fontName='DejaVu', fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle('bullet', fontName='DejaVu', fontSize=11, leftIndent=12, spaceAfter=4)

# Footer
def footer(canvas, doc):
    canvas.setFont('DejaVu', 9)
    canvas.drawString(0.75*inch, 0.5*inch, "Klandestine™ Rulebook")
    canvas.drawRightString(7.5*inch, 0.5*inch, f"Page {canvas.getPageNumber()}")

story = []

# COVER
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("KLANDESTINE™", title))
story.append(Paragraph("OFFICIAL RULEBOOK", title))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Created by Kloak & Daggurr’s", body))
story.append(Paragraph("A Strategic Trading Card Game", body))
story.append(Spacer(1, 0.5*inch))

# IMAGE (CENTERED)
img = Image(r"C:\Users\mille\Desktop\KCKD\rulebook\cover.png", width=4*inch, height=5*inch)
img.hAlign = 'CENTER'
story.append(img)

story.append(PageBreak())

# 1 OVERVIEW
story.append(Paragraph("1. GAME OVERVIEW", section))
story.append(Paragraph("Klandestine™ is a strategic trading card game where players summon creatures, manage Vigor, and convert fallen power into Ash to outmaneuver their opponent.", body))

story.append(Paragraph("WIN CONDITIONS", sub))
story.append(Paragraph("• The opponent’s Jester (35 HP) is reduced to 0", bullet))
story.append(Paragraph("• OR the opponent’s Player HP (35) is reduced to 0", bullet))
story.append(Paragraph("• OR the opponent cannot draw a card when required", bullet))

# 2 CARD TYPES
story.append(Paragraph("2. CARD TYPES", section))

card_table = Table([
["VIGOR", "CREATURES"],
["Primary resource used to play cards", "Used to attack and defend"],
["Gain +1 Vigor per turn", "Require Vigor to summon"],
["Spent Vigor attaches to creatures", "Max 4 creatures on field"],
["", ""],
["RUNES", "ACCOUTREMENTS"],
["One-time use effects", "Equipment and enhancement"],
["", ""],
["PRIMORDIALS", "JESTERS"],
["Unique powerful cards", "Visual placeholders with HP"],
["Limit 1 per deck", "If not used, player becomes target"],
["Not Resurrectable", "Has 35 HP"],
["", ""]

], colWidths=[3*inch, 3*inch])

card_table.setStyle(TableStyle([
("BOX", (0,0), (-1,-1), 1, colors.grey),
("INNERGRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
("BACKGROUND", (0,5), (-1,5), colors.lightgrey),
("BACKGROUND", (0,8), (-1,8), colors.lightgrey)
]))

story.append(card_table)


story.append(Paragraph("3. CORE MECHANICS", section))

card_table = Table([
["ASH SYSTEM", "RESURRECTION"],
["Dead creatures convert Vigor → Ash", "1 resurrection per game"],
["Max 5 Ash per creature", "Play Phase only"],
["3 Ash = Draw 1 card", "Targets most recent creature"],
["", ""]

], colWidths=[3*inch, 3*inch])

card_table.setStyle(TableStyle([
("BOX", (0,0), (-1,-1), 1, colors.grey),
("INNERGRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
]))

story.append(card_table)

# 4 TURN
story.append(Paragraph("4. TURN STRUCTURE", section))

turn_table = Table([
["1. DRAW", "Draw 1 card"],
["2. PLAY", "Gain Vigor, play cards, use Ash"],
["3. ATTACK", "Declare and resolve combat"],
["4. END", "Pass turn"]
], colWidths=[2*inch, 4*inch])

turn_table.setStyle(TableStyle([
("BOX", (0,0), (-1,-1), 1, colors.grey),
("INNERGRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
("BACKGROUND", (0,0), (0,-1), colors.lightgrey)
]))

story.append(turn_table)

# 5 COMBAT
story.append(Paragraph("5. COMBAT RULES", section))
story.append(Paragraph("Summoning Rule = Creatures cannot attack the turn they are played", body))
story.append(Paragraph("Damage is based on creature stats.", body))
story.append(Paragraph("Strong type = +50% damage", body))
story.append(Paragraph("Mutual advantage = both deal +50%", body))
story.append(Paragraph("Field Limit = Max 4 creatures per player", body))

# --- TYPE CHART TITLE ---
story.append(Paragraph("6. TYPE CHART", section))
story.append(Paragraph(
    "<b>Columns = Weakness (Defender) → &nbsp;&nbsp;&nbsp; Rows = Strength (Attacker) ↓</b>",
    body
))

from reportlab.platypus import Image
import os

icon_path = r"C:\Users\mille\Desktop\KCKD\rulebook\icons"

def get_icon(name, size=0.3):
    path = os.path.join(icon_path, f"{name.lower()}.png")
    return Image(path, width=size*inch, height=size*inch)

types = ["Chaos","Earth","Fairy","Fungus","Greed","Lava","Lightning","Moon","Ocean","Purity","Sorcery","Spirit","Sun","Tar"]

# --- HEADER ROW (ICONS) ---
data = [[""] + [get_icon(t, 0.3) for t in types]]

# --- STRENGTH LOGIC ---
strengths = {
"Chaos": ["Earth","Purity","Sorcery","Spirit"],
"Earth": ["Fairy","Lava","Lightning","Moon"],
"Fairy": ["Earth","Greed","Lava","Lightning"],
"Fungus": ["Earth","Fairy","Ocean","Purity"],
"Greed": ["Fairy","Lightning","Spirit","Sun"],
"Lava": ["Fairy","Fungus","Ocean","Tar"],
"Lightning": ["Moon","Ocean","Sorcery","Tar"],
"Moon": ["Fairy","Greed","Purity","Sun"],
"Ocean": ["Earth","Lava","Sun","Tar"],
"Purity": ["Chaos","Fungus","Greed","Lightning"],
"Sorcery": ["Chaos","Fungus","Moon","Spirit"],
"Spirit": ["Fungus","Greed","Lava","Sorcery"],
"Sun": ["Chaos","Fungus","Moon","Spirit"],
"Tar": ["Lava","Purity","Spirit","Sun"]
}

# --- BUILD GRID ---
for defender in types:
    row = [get_icon(defender, 0.3)]
    for attacker in types:
        if defender in strengths[attacker]:
            row.append(Paragraph("<para align='center'><font color='purple'><b>●</b></font></para>", body))
        else:
            row.append("")
    data.append(row)

# --- TABLE ---
type_table = Table(
    data,
    colWidths=[0.5*inch] + [0.4*inch]*len(types),
    repeatRows=1
)

type_table.setStyle(TableStyle([
    ("GRID", (0,0), (-1,-1), 0.25, colors.grey),

    # Headers
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

    # Alignment
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

    # Font sizes
    ("FONTSIZE", (0,0), (-1,-1), 8),

    # Padding
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))

story.append(type_table)

# --- LEGEND ---
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("TYPE LEGEND", section))

legend_data = []
row = []

for i, t in enumerate(types):
    cell = Table([
        [get_icon(t, 0.35)],
        [Paragraph(t, body)]
    ])
    row.append(cell)

    if (i + 1) % 4 == 0:
        legend_data.append(row)
        row = []

if row:
    legend_data.append(row)

legend_table = Table(legend_data, colWidths=[1.5*inch]*4)

legend_table.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))

story.append(legend_table)

story.append(Paragraph("RULE NOTE", sub))
story.append(Paragraph("• If not listed → no bonus", bullet))
story.append(Paragraph("• Strength is one-directional unless both apply", bullet))

# 7 DECK
story.append(Paragraph(" 7. DECK BUILDING", section))
story.append(Paragraph("• 60–100 cards", bullet))
story.append(Paragraph("• Over 100 = disqualification", bullet))
story.append(Paragraph("• Max 1 Primordial", bullet))

story.append(Paragraph("Recommended 60 Cards:", sub))
story.append(Paragraph("• 22 Creatures", bullet))
story.append(Paragraph("• 20 Vigor", bullet))
story.append(Paragraph("• 9 Runes", bullet))
story.append(Paragraph("• 8 Accoutrements", bullet))
story.append(Paragraph("• 1 Primordial", bullet))

# BUILD
doc.build(story, onFirstPage=footer, onLaterPages=footer)

print("✅ FULL rulebook generated:", pdf_path)