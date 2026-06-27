from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs"
OUTPUT_FILE = OUTPUT_DIR / "dragon-ball-oop-study-guide.pdf"

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.55 * inch
CONTENT_WIDTH = PAGE_WIDTH - (MARGIN * 2)

BG = colors.HexColor("#FFF9F1")
INK = colors.HexColor("#1F2937")
SOFT = colors.HexColor("#4B5563")
ORANGE = colors.HexColor("#F97316")
GOLD = colors.HexColor("#FACC15")
BLUE = colors.HexColor("#2563EB")
GREEN = colors.HexColor("#16A34A")
RED = colors.HexColor("#DC2626")
PURPLE = colors.HexColor("#7C3AED")
CARD = colors.HexColor("#FFFDF8")
LIGHT_ORANGE = colors.HexColor("#FFEDD5")
LIGHT_BLUE = colors.HexColor("#DBEAFE")
LIGHT_GREEN = colors.HexColor("#DCFCE7")
LIGHT_PURPLE = colors.HexColor("#EDE9FE")
LIGHT_RED = colors.HexColor("#FEE2E2")
LIGHT_GOLD = colors.HexColor("#FEF3C7")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="GuideTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=13,
            textColor=SOFT,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=INK,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.2,
            leading=13.2,
            textColor=INK,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=11.2,
            textColor=INK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=10.5,
            textColor=SOFT,
            alignment=TA_LEFT,
            spaceBefore=2,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardTitle",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=11.5,
            textColor=INK,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=9.6,
            textColor=INK,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeLabel",
            parent=styles["BodyText"],
            fontName="Courier",
            fontSize=8.8,
            leading=10.4,
            textColor=BLUE,
        )
    )
    return styles


STYLES = build_styles()


def draw_page_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    canvas.setFillColor(LIGHT_GOLD)
    canvas.circle(42, PAGE_HEIGHT - 42, 24, fill=1, stroke=0)
    canvas.setFillColor(LIGHT_BLUE)
    canvas.circle(PAGE_WIDTH - 42, PAGE_HEIGHT - 70, 18, fill=1, stroke=0)
    canvas.setFillColor(LIGHT_PURPLE)
    canvas.circle(PAGE_WIDTH - 52, 48, 16, fill=1, stroke=0)
    canvas.setFillColor(SOFT)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 18, "Dragon Ball OOP Study Guide")
    canvas.drawRightString(PAGE_WIDTH - MARGIN, 18, f"Page {doc.page}")
    canvas.restoreState()


def add_arrow(drawing, x1, y1, x2, y2, color=INK, label=None, label_dx=0, label_dy=0):
    drawing.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.5))
    dx = x2 - x1
    dy = y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux = dx / length
    uy = dy / length
    size = 6
    left_x = x2 - (ux * size) - (uy * size / 2)
    left_y = y2 - (uy * size) + (ux * size / 2)
    right_x = x2 - (ux * size) + (uy * size / 2)
    right_y = y2 - (uy * size) - (ux * size / 2)
    drawing.add(
        Polygon(
            points=[x2, y2, left_x, left_y, right_x, right_y],
            fillColor=color,
            strokeColor=color,
        )
    )
    if label:
        mx = (x1 + x2) / 2 + label_dx
        my = (y1 + y2) / 2 + label_dy
        drawing.add(String(mx, my, label, fontName="Helvetica", fontSize=8, fillColor=SOFT))


def add_box(drawing, x, y, w, h, title, subtitle="", fill=CARD, stroke=INK, title_color=INK):
    drawing.add(Rect(x, y, w, h, rx=10, ry=10, fillColor=fill, strokeColor=stroke, strokeWidth=1.1))
    drawing.add(String(x + 8, y + h - 18, title, fontName="Helvetica-Bold", fontSize=11, fillColor=title_color))
    if subtitle:
        lines = subtitle.split("\n")
        top = y + h - 33
        for idx, line in enumerate(lines):
            drawing.add(String(x + 8, top - (idx * 11), line, fontName="Helvetica", fontSize=8.5, fillColor=SOFT))


def title_block(title, subtitle):
    return [
        Paragraph(title, STYLES["GuideTitle"]),
        Paragraph(subtitle, STYLES["GuideSubtitle"]),
    ]


def quick_reference_map():
    d = Drawing(CONTENT_WIDTH, 112)
    add_box(d, 0, 36, 100, 52, "Class", "A blueprint", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 138, 36, 118, 52, "Object / Instance", "A real thing built\nfrom the blueprint", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_arrow(d, 100, 62, 138, 62, color=INK, label="creates", label_dy=8)

    add_box(d, 292, 48, 104, 40, "Fighter", "Shared base idea", fill=LIGHT_GREEN, stroke=GREEN, title_color=GREEN)
    add_box(d, 422, 64, 92, 28, "Saiyan", fill=LIGHT_GOLD, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 422, 28, 92, 28, "Namekian", fill=LIGHT_PURPLE, stroke=PURPLE, title_color=PURPLE)
    add_arrow(d, 344, 48, 344, 16, color=GREEN, label="must attack", label_dx=8)
    add_arrow(d, 396, 68, 422, 78, color=GREEN, label="is-a", label_dy=8)
    add_arrow(d, 396, 68, 422, 42, color=GREEN, label="is-a", label_dy=-10)

    add_box(d, 292, 0, 104, 24, "BattleArena", fill=LIGHT_RED, stroke=RED, title_color=RED)
    add_box(d, 422, 0, 92, 24, "Writer", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_arrow(d, 396, 12, 422, 12, color=RED, label="needs-a", label_dy=8)
    return d


def quick_card(term, meaning, code_hint):
    title = Paragraph(term, STYLES["CardTitle"])
    body = Paragraph(f"{meaning}<br/><font color='#2563EB'><b>In code:</b> {code_hint}</font>", STYLES["CardBody"])
    card = Table([[title], [body]], colWidths=[CONTENT_WIDTH / 2 - 8])
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CARD),
                ("BOX", (0, 0), (-1, -1), 0.9, colors.HexColor("#E5E7EB")),
                ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return card


def quick_reference_table():
    cards = [
        quick_card("Class", "A blueprint or mold used to make things.", "Fighter, Saiyan, Technique"),
        quick_card("Object", "A real thing created from a class.", "goku, piccolo, arena"),
        quick_card("Instance", "Another word for object.", "goku is an instance of Saiyan"),
        quick_card("Method", "An action an object can perform.", "Attack(), TakeDamage()"),
        quick_card("Field", "Private internal data stored inside a class.", "energy"),
        quick_card("Property", "A safe door for reading or changing data.", "Name, PowerLevel"),
        quick_card("Encapsulation", "Hide and protect internal state.", "energy is private"),
        quick_card("Abstraction", "Show the big idea, hide the low-level details.", "abstract Fighter"),
        quick_card("Interface", "A contract that says what must exist.", "IMessageWriter"),
        quick_card("Inheritance", "A child class reuses a parent class.", "Saiyan : Fighter"),
        quick_card("Polymorphism", "Same base type, different real behavior.", "Fighter goku = new Saiyan(...)"),
        quick_card("Composition", "One object contains another object.", "Saiyan has Technique"),
        quick_card("Dependency", "A class needs another piece to do its job.", "BattleArena needs writer"),
        quick_card("Dependency Injection", "That needed piece is handed in from outside.", "new BattleArena(writer)"),
    ]
    rows = []
    for idx in range(0, len(cards), 2):
        rows.append([cards[idx], cards[idx + 1]])
    table = Table(rows, colWidths=[CONTENT_WIDTH / 2 - 6, CONTENT_WIDTH / 2 - 6], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def project_map():
    d = Drawing(CONTENT_WIDTH, 210)
    add_box(d, 14, 150, 100, 42, "Program", "Starts everything", fill=LIGHT_GOLD, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 155, 145, 126, 52, "BattleArena", "Shows each turn\nNeeds a writer", fill=LIGHT_RED, stroke=RED, title_color=RED)
    add_box(d, 320, 158, 108, 34, "IMessageWriter", "Contract", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_box(d, 447, 150, 90, 42, "Console\nMessageWriter", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_box(d, 155, 74, 126, 46, "Fighter", "Shared base:\nName, PowerLevel, energy", fill=LIGHT_GREEN, stroke=GREEN, title_color=GREEN)
    add_box(d, 36, 18, 110, 34, "Saiyan", "Child class", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 180, 18, 110, 34, "Namekian", "Child class", fill=LIGHT_PURPLE, stroke=PURPLE, title_color=PURPLE)
    add_box(d, 337, 18, 120, 34, "Technique", "Kamehameha", fill=LIGHT_GOLD, stroke=ORANGE, title_color=ORANGE)

    add_arrow(d, 114, 171, 155, 171, color=INK, label="creates", label_dy=9)
    add_arrow(d, 281, 171, 320, 171, color=RED, label="needs", label_dy=9)
    add_arrow(d, 428, 171, 447, 171, color=BLUE, label="implemented by", label_dy=9)
    add_arrow(d, 218, 145, 218, 120, color=GREEN, label="receives", label_dx=8)
    add_arrow(d, 218, 74, 91, 52, color=GREEN, label="is-a", label_dy=6)
    add_arrow(d, 218, 74, 235, 52, color=GREEN, label="is-a", label_dy=6)
    add_arrow(d, 146, 36, 337, 36, color=ORANGE, label="has-a", label_dy=10)
    return d


def blueprint_diagram():
    d = Drawing(CONTENT_WIDTH, 120)
    add_box(d, 20, 30, 170, 60, "Class = Blueprint", "It describes what to make.\nExample: Saiyan", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 340, 30, 170, 60, "Object = Real Thing", "A real Saiyan object.\nExample: goku", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_arrow(d, 190, 60, 340, 60, color=INK, label="new Saiyan(...)", label_dy=10)
    return d


def fighter_anatomy_diagram():
    d = Drawing(CONTENT_WIDTH, 132)
    add_box(d, 80, 16, 380, 96, "Fighter object", "", fill=CARD, stroke=GREEN, title_color=GREEN)
    d.add(Rect(104, 58, 98, 34, fillColor=LIGHT_RED, strokeColor=RED, strokeWidth=1))
    d.add(String(113, 79, "Field", fontName="Helvetica-Bold", fontSize=10, fillColor=RED))
    d.add(String(113, 66, "energy", fontName="Courier", fontSize=10, fillColor=INK))
    d.add(String(104, 44, "Private data hidden inside", fontName="Helvetica", fontSize=8, fillColor=SOFT))

    d.add(Rect(220, 58, 110, 34, fillColor=LIGHT_BLUE, strokeColor=BLUE, strokeWidth=1))
    d.add(String(230, 79, "Property", fontName="Helvetica-Bold", fontSize=10, fillColor=BLUE))
    d.add(String(230, 66, "Name", fontName="Courier", fontSize=10, fillColor=INK))
    d.add(String(220, 44, "Safe public door", fontName="Helvetica", fontSize=8, fillColor=SOFT))

    d.add(Rect(348, 58, 88, 34, fillColor=LIGHT_GREEN, strokeColor=GREEN, strokeWidth=1))
    d.add(String(358, 79, "Method", fontName="Helvetica-Bold", fontSize=10, fillColor=GREEN))
    d.add(String(358, 66, "Attack()", fontName="Courier", fontSize=10, fillColor=INK))
    d.add(String(348, 44, "Action the object can do", fontName="Helvetica", fontSize=8, fillColor=SOFT))
    return d


def encapsulation_diagram():
    d = Drawing(CONTENT_WIDTH, 140)
    add_box(d, 190, 18, 170, 100, "Fighter", "Inside lives energy", fill=CARD, stroke=GREEN, title_color=GREEN)
    d.add(Rect(235, 44, 80, 28, fillColor=LIGHT_RED, strokeColor=RED, strokeWidth=1))
    d.add(String(251, 60, "energy", fontName="Courier", fontSize=10, fillColor=INK))
    d.add(String(31, 88, "Outside code", fontName="Helvetica-Bold", fontSize=11, fillColor=INK))
    add_arrow(d, 90, 78, 190, 60, color=RED, label="No direct access", label_dy=10)
    d.add(Line(144, 73, 164, 47, strokeColor=RED, strokeWidth=2))
    d.add(Line(164, 73, 144, 47, strokeColor=RED, strokeWidth=2))
    add_arrow(d, 368, 94, 480, 108, color=GREEN, label="Use methods", label_dy=8)
    add_box(d, 404, 28, 108, 48, "Safe doors", "TakeDamage()\nGetEnergy()", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    return d


def abstraction_diagram():
    d = Drawing(CONTENT_WIDTH, 140)
    add_box(d, 202, 78, 124, 40, "abstract Fighter", "Big shared idea", fill=LIGHT_GREEN, stroke=GREEN, title_color=GREEN)
    add_box(d, 84, 18, 120, 36, "Saiyan", "Own Attack()", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 324, 18, 120, 36, "Namekian", "Own Attack()", fill=LIGHT_PURPLE, stroke=PURPLE, title_color=PURPLE)
    add_arrow(d, 242, 78, 144, 54, color=GREEN, label="must define attack", label_dy=8)
    add_arrow(d, 286, 78, 384, 54, color=GREEN, label="must define attack", label_dy=8)
    d.add(String(171, 4, "One shared rule, many specific implementations.", fontName="Helvetica-Oblique", fontSize=9, fillColor=SOFT))
    return d


def interface_diagram():
    d = Drawing(CONTENT_WIDTH, 140)
    add_box(d, 42, 34, 160, 72, "IMessageWriter", "Rule:\nWrite(string message)", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_box(d, 332, 34, 160, 72, "ConsoleMessageWriter", "Real class:\nprints to Console", fill=LIGHT_GOLD, stroke=ORANGE, title_color=ORANGE)
    add_arrow(d, 202, 70, 332, 70, color=INK, label="implements", label_dy=10)
    return d


def inheritance_polymorphism_diagram():
    d = Drawing(CONTENT_WIDTH, 176)
    add_box(d, 218, 120, 118, 34, "Fighter", "Base type", fill=LIGHT_GREEN, stroke=GREEN, title_color=GREEN)
    add_box(d, 90, 62, 118, 34, "Saiyan", "Attack() says\nKamehameha", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 350, 62, 118, 34, "Namekian", "Attack() says\nenergy blast", fill=LIGHT_PURPLE, stroke=PURPLE, title_color=PURPLE)
    add_arrow(d, 262, 120, 149, 96, color=GREEN, label="inherits", label_dy=8)
    add_arrow(d, 292, 120, 409, 96, color=GREEN, label="inherits", label_dy=8)
    add_box(d, 176, 12, 200, 30, "Fighter fighter = ...", "Same variable shape, different real object", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_arrow(d, 238, 42, 149, 62, color=BLUE, label="can point to", label_dy=8)
    add_arrow(d, 314, 42, 409, 62, color=BLUE, label="can point to", label_dy=8)
    return d


def composition_dependency_diagram():
    d = Drawing(CONTENT_WIDTH, 180)
    add_box(d, 40, 98, 170, 56, "Saiyan", "Has FavoriteTechnique", fill=LIGHT_ORANGE, stroke=ORANGE, title_color=ORANGE)
    add_box(d, 270, 108, 160, 36, "Technique", "Name + Damage", fill=LIGHT_GOLD, stroke=ORANGE, title_color=ORANGE)
    add_arrow(d, 210, 126, 270, 126, color=ORANGE, label="has-a", label_dy=9)

    add_box(d, 40, 16, 170, 56, "BattleArena", "Needs writer", fill=LIGHT_RED, stroke=RED, title_color=RED)
    add_box(d, 270, 26, 160, 36, "IMessageWriter", "Dependency", fill=LIGHT_BLUE, stroke=BLUE, title_color=BLUE)
    add_box(d, 450, 26, 60, 36, "Program", "hands it in", fill=LIGHT_GREEN, stroke=GREEN, title_color=GREEN)
    add_arrow(d, 210, 44, 270, 44, color=RED, label="needs-a", label_dy=9)
    add_arrow(d, 450, 44, 430, 44, color=GREEN, label="injects", label_dy=9)
    return d


def keyword_signature_diagram():
    d = Drawing(CONTENT_WIDTH, 110)
    signature = "public static void Main()"
    d.add(String(84, 70, signature, fontName="Courier-Bold", fontSize=18, fillColor=INK))

    positions = {
        "public": 84,
        "static": 84 + stringWidth("public ", "Courier-Bold", 18),
        "void": 84 + stringWidth("public static ", "Courier-Bold", 18),
        "Main()": 84 + stringWidth("public static void ", "Courier-Bold", 18),
    }
    colors_map = {
        "public": LIGHT_ORANGE,
        "static": LIGHT_BLUE,
        "void": LIGHT_GREEN,
        "Main()": LIGHT_PURPLE,
    }
    labels = {
        "public": "visible from outside",
        "static": "belongs to the class",
        "void": "returns nothing",
        "Main()": "program starts here",
    }

    for word, x in positions.items():
        width = stringWidth(word, "Courier-Bold", 18) + 8
        d.add(Rect(x - 4, 62, width, 22, fillColor=colors_map[word], strokeColor=INK, strokeWidth=0.6))
        d.add(String(x, 70, word, fontName="Courier-Bold", fontSize=18, fillColor=INK))
        add_arrow(d, x + (width / 2), 62, x + (width / 2), 34, color=INK)
        d.add(String(x - 10, 18, labels[word], fontName="Helvetica", fontSize=8, fillColor=SOFT))
    return d


def code_sample(text):
    return Preformatted(text, STYLES["CodeLabel"], dedent=0)


def info_box(title, body, fill=LIGHT_BLUE, stroke=BLUE):
    table = Table(
        [[Paragraph(f"<b>{title}</b>", STYLES["BodySmall"])], [Paragraph(body, STYLES["BodySmall"])]],
        colWidths=[CONTENT_WIDTH],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 1, stroke),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def bullet_lines(items):
    text = "<br/>".join([f"• {item}" for item in items])
    return Paragraph(text, STYLES["Body"])


def build_story():
    story = []

    story.extend(
        title_block(
            "Dragon Ball OOP Study Guide for Absolute Beginners",
            "One-page quick reference first, then concept-by-concept notes with simple visuals and interview-friendly explanations.",
        )
    )
    story.append(quick_reference_map())
    story.append(Spacer(1, 8))
    story.append(Paragraph("Quick Reference", STYLES["SectionTitle"]))
    story.append(quick_reference_table())
    story.append(Spacer(1, 6))
    story.append(
        info_box(
            "Tiny memory trick",
            "Inheritance means <b>is-a</b>. Composition means <b>has-a</b>. Dependency means <b>needs-a</b>. Dependency injection means <b>someone else hands that needed piece in</b>.",
            fill=LIGHT_GOLD,
            stroke=ORANGE,
        )
    )
    story.append(PageBreak())

    story.extend(title_block("Project Map", "See the whole mini-project before studying each concept one by one."))
    story.append(project_map())
    story.append(Paragraph("Story of the program", STYLES["SubTitle"]))
    story.append(
        bullet_lines(
            [
                "The program starts in <b>Main</b>.",
                "It creates a writer so text can be shown on the screen.",
                "It creates two fighters: one <b>Saiyan</b> and one <b>Namekian</b>.",
                "It creates a <b>BattleArena</b> and gives it the writer.",
                "The arena asks each fighter to introduce itself and attack.",
                "Because of polymorphism, each fighter answers in its own way.",
            ]
        )
    )
    story.append(
        info_box(
            "Kid-friendly picture",
            "Think of this project like a toy battle set. <b>Fighter</b> is the general toy idea. <b>Saiyan</b> and <b>Namekian</b> are two real toys. <b>BattleArena</b> is the stage. <b>IMessageWriter</b> is the rule that says how speech bubbles must be shown.",
            fill=LIGHT_GREEN,
            stroke=GREEN,
        )
    )
    story.append(PageBreak())

    story.extend(title_block("Building Blocks", "These are the first ideas to master: class, object, instance, method, field, and property."))
    story.append(Paragraph("Class, Object, and Instance", STYLES["SectionTitle"]))
    story.append(blueprint_diagram())
    story.append(Paragraph("<b>Class</b>: a blueprint. It describes what we can create. In this project, <b>Fighter</b>, <b>Saiyan</b>, and <b>Technique</b> are classes.", STYLES["Body"]))
    story.append(Paragraph("<b>Object</b>: a real thing created from a class. When we write <font face='Courier'>new Saiyan(\"Goku\", 9000)</font>, we create an object.", STYLES["Body"]))
    story.append(Paragraph("<b>Instance</b>: another word for object. Saying '<b>goku</b> is an instance of <b>Saiyan</b>' means the same thing as saying '<b>goku</b> is a Saiyan object.'", STYLES["Body"]))
    story.append(code_sample('Fighter goku = new Saiyan("Goku", 9000);'))
    story.append(Paragraph("Method, Field, and Property", STYLES["SectionTitle"]))
    story.append(fighter_anatomy_diagram())
    story.append(Paragraph("<b>Method</b>: an action. <font face='Courier'>Attack()</font> and <font face='Courier'>TakeDamage()</font> are methods.", STYLES["Body"]))
    story.append(Paragraph("<b>Field</b>: private internal data stored inside a class. <font face='Courier'>energy</font> is the field that stores a fighter's energy.", STYLES["Body"]))
    story.append(Paragraph("<b>Property</b>: a safe door for data. <font face='Courier'>Name</font> and <font face='Courier'>PowerLevel</font> are properties.", STYLES["Body"]))
    story.append(
        info_box(
            "Why field and property are different",
            "A field is raw storage inside the object. A property is a controlled way to expose that data. In interviews, this distinction matters in C#.",
            fill=LIGHT_BLUE,
            stroke=BLUE,
        )
    )
    story.append(PageBreak())

    story.extend(title_block("Encapsulation and Abstraction", "These ideas help us design code that is safer and easier to understand."))
    story.append(Paragraph("Encapsulation", STYLES["SectionTitle"]))
    story.append(encapsulation_diagram())
    story.append(Paragraph("Encapsulation means the object protects its inside state. In this project, outside code cannot directly change <font face='Courier'>energy</font> because the field is private.", STYLES["Body"]))
    story.append(Paragraph("Instead, outside code must use safe doors such as <font face='Courier'>TakeDamage()</font> and <font face='Courier'>GetEnergy()</font>.", STYLES["Body"]))
    story.append(Paragraph("This protects the object from invalid states and keeps the rules in one place.", STYLES["Body"]))
    story.append(Paragraph("Abstraction", STYLES["SectionTitle"]))
    story.append(abstraction_diagram())
    story.append(Paragraph("Abstraction means we focus on the big idea first and leave details for later. <font face='Courier'>Fighter</font> says every fighter has shared data and every fighter must attack.", STYLES["Body"]))
    story.append(Paragraph("But <font face='Courier'>Fighter</font> does not decide the exact attack. Each child class decides that. That is why <font face='Courier'>Attack()</font> is abstract.", STYLES["Body"]))
    story.append(
        info_box(
            "Plain-English memory trick",
            "Encapsulation says: <b>protect the inside</b>. Abstraction says: <b>describe the important idea first</b>.",
            fill=LIGHT_GOLD,
            stroke=ORANGE,
        )
    )
    story.append(PageBreak())

    story.extend(title_block("Interface, Inheritance, and Polymorphism", "These three ideas are central to most OOP interviews."))
    story.append(Paragraph("Interface", STYLES["SectionTitle"]))
    story.append(interface_diagram())
    story.append(Paragraph("An interface is a contract. <font face='Courier'>IMessageWriter</font> says a class must know how to write a message, but it does not say how.", STYLES["Body"]))
    story.append(Paragraph("<font face='Courier'>ConsoleMessageWriter</font> implements that contract by printing to the terminal.", STYLES["Body"]))
    story.append(Paragraph("Inheritance and Polymorphism", STYLES["SectionTitle"]))
    story.append(inheritance_polymorphism_diagram())
    story.append(Paragraph("Inheritance means one class builds on another. <font face='Courier'>Saiyan : Fighter</font> and <font face='Courier'>Namekian : Fighter</font> mean both child classes reuse the base class.", STYLES["Body"]))
    story.append(Paragraph("Polymorphism means one base type can point to different real objects. A variable typed as <font face='Courier'>Fighter</font> can hold a <font face='Courier'>Saiyan</font> or a <font face='Courier'>Namekian</font>.", STYLES["Body"]))
    story.append(code_sample('Fighter goku = new Saiyan("Goku", 9000);\nFighter piccolo = new Namekian("Piccolo", 7000);'))
    story.append(Paragraph("When the program calls <font face='Courier'>fighter.Attack()</font>, the answer depends on the real object behind the variable. That is polymorphism in action.", STYLES["Body"]))
    story.append(PageBreak())

    story.extend(title_block("Composition, Dependency, and Dependency Injection", "These ideas explain how objects work together."))
    story.append(Paragraph("Composition and Dependency", STYLES["SectionTitle"]))
    story.append(composition_dependency_diagram())
    story.append(Paragraph("Composition means one object contains another object as part of itself. In this project, a <font face='Courier'>Saiyan</font> has a <font face='Courier'>Technique</font>.", STYLES["Body"]))
    story.append(Paragraph("Dependency means one class needs another piece to do its job. <font face='Courier'>BattleArena</font> needs something that can write messages.", STYLES["Body"]))
    story.append(Paragraph("Dependency Injection", STYLES["SectionTitle"]))
    story.append(Paragraph("Dependency injection means the needed piece is handed in from outside instead of being created inside the class.", STYLES["Body"]))
    story.append(code_sample("IMessageWriter writer = new ConsoleMessageWriter();\nBattleArena arena = new BattleArena(writer);"))
    story.append(Paragraph("This is called constructor injection because the dependency is passed into the constructor.", STYLES["Body"]))
    story.append(
        info_box(
            "Why this matters in interviews",
            "Dependency injection makes code more flexible, easier to swap, and easier to test. The class depends on the <b>contract</b>, not on one hardcoded concrete implementation.",
            fill=LIGHT_GREEN,
            stroke=GREEN,
        )
    )
    story.append(PageBreak())

    story.extend(title_block("C# Keywords Cheat Sheet", "These small words carry a lot of meaning."))
    story.append(Paragraph("Reading the signature <font face='Courier'>public static void Main()</font>", STYLES["SectionTitle"]))
    story.append(keyword_signature_diagram())
    story.append(Paragraph("<b>public</b> means code from outside the class can access it. <b>static</b> means it belongs to the class itself, not to one specific object. <b>void</b> means the method returns nothing. <b>Main</b> is the special entry point where the program starts.", STYLES["Body"]))
    keywords_table = Table(
        [
            [
                Paragraph("<b>Keyword</b>", STYLES["BodySmall"]),
                Paragraph("<b>Simple meaning</b>", STYLES["BodySmall"]),
                Paragraph("<b>Example in the project</b>", STYLES["BodySmall"]),
            ],
            [Paragraph("public", STYLES["BodySmall"]), Paragraph("Visible from anywhere.", STYLES["BodySmall"]), Paragraph("public class Fighter", STYLES["BodySmall"])],
            [Paragraph("private", STYLES["BodySmall"]), Paragraph("Visible only inside the same class.", STYLES["BodySmall"]), Paragraph("private int energy;", STYLES["BodySmall"])],
            [Paragraph("protected", STYLES["BodySmall"]), Paragraph("Visible in the class and child classes.", STYLES["BodySmall"]), Paragraph("protected Fighter(...)", STYLES["BodySmall"])],
            [Paragraph("abstract", STYLES["BodySmall"]), Paragraph("Incomplete by design; must be finished by child classes or cannot be directly created.", STYLES["BodySmall"]), Paragraph("abstract class Fighter", STYLES["BodySmall"])],
            [Paragraph("virtual", STYLES["BodySmall"]), Paragraph("Can be replaced by a child class.", STYLES["BodySmall"]), Paragraph("virtual string Introduce()", STYLES["BodySmall"])],
            [Paragraph("override", STYLES["BodySmall"]), Paragraph("Replaces inherited behavior.", STYLES["BodySmall"]), Paragraph("override string Attack()", STYLES["BodySmall"])],
            [Paragraph("new", STYLES["BodySmall"]), Paragraph("Creates an object.", STYLES["BodySmall"]), Paragraph('new Saiyan("Goku", 9000)', STYLES["BodySmall"])],
            [Paragraph("this", STYLES["BodySmall"]), Paragraph("The current object.", STYLES["BodySmall"]), Paragraph("this.writer = writer;", STYLES["BodySmall"])],
            [Paragraph("base", STYLES["BodySmall"]), Paragraph("The parent class part of the current object.", STYLES["BodySmall"]), Paragraph("base(name, powerLevel)", STYLES["BodySmall"])],
            [Paragraph("get / set", STYLES["BodySmall"]), Paragraph("Read and change rules for properties.", STYLES["BodySmall"]), Paragraph("Name { get; private set; }", STYLES["BodySmall"])],
            [Paragraph("readonly", STYLES["BodySmall"]), Paragraph("Can be assigned once, usually in the constructor.", STYLES["BodySmall"]), Paragraph("private readonly IMessageWriter writer;", STYLES["BodySmall"])],
        ],
        colWidths=[1.05 * inch, 2.6 * inch, 2.4 * inch],
    )
    keywords_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB")),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#D1D5DB")),
                ("BACKGROUND", (0, 1), (-1, -1), CARD),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(keywords_table)
    story.append(PageBreak())

    story.extend(title_block("Reading the Code as a Story", "If you can explain the program in order, you will sound much stronger in an interview."))
    flow = Table(
        [
            [Paragraph("<b>1. Main starts</b><br/>The program begins in <font face='Courier'>Main</font>.", STYLES["BodySmall"])],
            [Paragraph("<b>2. A writer is created</b><br/><font face='Courier'>ConsoleMessageWriter</font> will print messages.", STYLES["BodySmall"])],
            [Paragraph("<b>3. Two fighter objects are created</b><br/><font face='Courier'>goku</font> is a <font face='Courier'>Saiyan</font>. <font face='Courier'>piccolo</font> is a <font face='Courier'>Namekian</font>.", STYLES["BodySmall"])],
            [Paragraph("<b>4. Piccolo takes damage</b><br/>The method updates internal energy safely.", STYLES["BodySmall"])],
            [Paragraph("<b>5. BattleArena is created</b><br/>The writer is injected into it.", STYLES["BodySmall"])],
            [Paragraph("<b>6. The arena shows each turn</b><br/>It calls <font face='Courier'>Introduce()</font> and <font face='Courier'>Attack()</font>.", STYLES["BodySmall"])],
            [Paragraph("<b>7. Polymorphism appears</b><br/>The same method call shape produces different outputs for Goku and Piccolo.", STYLES["BodySmall"])],
        ],
        colWidths=[CONTENT_WIDTH],
    )
    flow.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CARD),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB")),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#E5E7EB")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(flow)
    story.append(Spacer(1, 10))
    story.append(
        info_box(
            "Final memory anchor",
            "To explain this project well, say it this way: <b>We model fighters with a shared abstract base class, specialize them through inheritance, swap behavior through polymorphism, protect state through encapsulation, and wire collaborating objects together through interfaces and dependency injection.</b>",
            fill=LIGHT_PURPLE,
            stroke=PURPLE,
        )
    )
    return story


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="Dragon Ball OOP Study Guide",
        author="OpenAI Codex",
    )
    story = build_story()
    doc.build(story, onFirstPage=draw_page_background, onLaterPages=draw_page_background)
    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
