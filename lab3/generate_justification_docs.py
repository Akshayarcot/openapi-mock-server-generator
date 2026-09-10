#!/usr/bin/env python3
"""
Generates the One-Page Written Justification Document for Lab 3:
1. Coffee_Kiosk_Architecture_Justification.docx (Microsoft Word format)
2. Coffee_Kiosk_Architecture_Justification.pdf (Print-ready PDF format)

Complies strictly with Lab 3 rubric and formatting constraints (Max 1 Page).
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def generate_docx(output_path: str):
    doc = Document()
    
    # 0.5 inch margins all around to comfortably fit 1 page
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.48)
        section.bottom_margin = Inches(0.48)
        section.left_margin = Inches(0.55)
        section.right_margin = Inches(0.55)

    # 1. Header Metadata Banner
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = header_table.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    p_title = cell.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LAB 3: ARCHITECTURAL PATTERN SELECTION & JUSTIFICATION\n")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(13)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_title.add_run("Course: Software Engineering (SELABS)  |  Student: A R Akshay Kumar  |  USN: PES1UG24CS705")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Spacing
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(4)

    # 2. Architecture Selection Callout Box
    sel_table = doc.add_table(rows=1, cols=1)
    sel_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sel = sel_table.cell(0, 0)
    set_cell_background(c_sel, "EFF6FF")
    set_cell_margins(c_sel, top=100, bottom=100, left=160, right=160)
    p_sel = c_sel.paragraphs[0]
    p_sel.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_sel_lbl = p_sel.add_run("Architecture Selection: ")
    r_sel_lbl.bold = True
    r_sel_lbl.font.name = "Arial"
    r_sel_lbl.font.size = Pt(11)
    r_sel_lbl.font.color.rgb = RGBColor(30, 58, 138)

    r_sel_val = p_sel.add_run('"We chose Layered Architecture for the Self-Service Coffee Kiosk System."')
    r_sel_val.bold = True
    r_sel_val.italic = True
    r_sel_val.font.name = "Arial"
    r_sel_val.font.size = Pt(11)
    r_sel_val.font.color.rgb = RGBColor(29, 78, 216)

    # Spacing
    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(4)
    p_space2.paragraph_format.space_after = Pt(4)

    # 3. Section 1: Architectural Choice
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(4)
    p_sec1.paragraph_format.space_after = Pt(2)
    p_sec1.paragraph_format.line_spacing = 1.1
    r_h1 = p_sec1.add_run("1. Architectural Choice: ")
    r_h1.bold = True
    r_h1.font.name = "Arial"
    r_h1.font.size = Pt(10)
    r_h1.font.color.rgb = RGBColor(15, 23, 42)

    r_t1 = p_sec1.add_run(
        "We selected the 3-Tier Layered Architecture style (Presentation Layer, Business Layer, Data Layer). "
        "The Presentation Layer encapsulates the User Interface Component, handling customer touch screen interactions, "
        "menu browsing, and size selection. The Business Layer hosts the Order Manager Component (orchestrator), "
        "Payment Service Component (card processing), and Receipt Printer Component (hardware abstraction). "
        "The Data Layer encapsulates the Database Component, storing menu catalog data, drink pricing rules, and order logs."
    )
    r_t1.font.name = "Arial"
    r_t1.font.size = Pt(9.5)
    r_t1.font.color.rgb = RGBColor(30, 41, 59)

    # 4. Section 2: Two Reasons
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(4)
    p_sec2.paragraph_format.space_after = Pt(2)
    r_h2 = p_sec2.add_run("2. Two Scenario-Related Reasons for Selection:")
    r_h2.bold = True
    r_h2.font.name = "Arial"
    r_h2.font.size = Pt(10)
    r_h2.font.color.rgb = RGBColor(15, 23, 42)

    p_r1 = doc.add_paragraph()
    p_r1.paragraph_format.left_indent = Inches(0.2)
    p_r1.paragraph_format.space_before = Pt(2)
    p_r1.paragraph_format.space_after = Pt(2)
    p_r1.paragraph_format.line_spacing = 1.08
    r_b1 = p_r1.add_run("• Decoupling Hardware Peripherals & Device Drivers: ")
    r_b1.bold = True
    r_b1.font.name = "Arial"
    r_b1.font.size = Pt(9.5)
    r_b1.font.color.rgb = RGBColor(30, 41, 59)
    r_t2 = p_r1.add_run(
        "The kiosk interacts directly with physical hardware—a touch screen interface, credit card terminal, and receipt printer. "
        "A layered architecture cleanly encapsulates hardware communication protocols (e.g., ESC/POS printer commands) within dedicated "
        "service components. Replacing or upgrading the printer hardware or touch screen OS requires zero modifications to the core order workflow logic."
    )
    r_t2.font.name = "Arial"
    r_t2.font.size = Pt(9.5)
    r_t2.font.color.rgb = RGBColor(30, 41, 59)

    p_r2 = doc.add_paragraph()
    p_r2.paragraph_format.left_indent = Inches(0.2)
    p_r2.paragraph_format.space_before = Pt(2)
    p_r2.paragraph_format.space_after = Pt(2)
    p_r2.paragraph_format.line_spacing = 1.08
    r_b2 = p_r2.add_run("• Independent Menu, Pricing & Business Rule Administration: ")
    r_b2.bold = True
    r_b2.font.name = "Arial"
    r_b2.font.size = Pt(9.5)
    r_b2.font.color.rgb = RGBColor(30, 41, 59)
    r_t3 = p_r2.add_run(
        "Café pricing, beverage options (Espresso, Americano, Latte), and size upcharges (Small vs. Large) fluctuate frequently. "
        "Separating data storage from the presentation and business logic allows café operators to update catalog items and prices directly in "
        "the database without recompiling, restarting, or risking regressions in kiosk UI workflows."
    )
    r_t3.font.name = "Arial"
    r_t3.font.size = Pt(9.5)
    r_t3.font.color.rgb = RGBColor(30, 41, 59)

    # 5. Section 3: Security Advantage
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.space_before = Pt(4)
    p_sec3.paragraph_format.space_after = Pt(2)
    p_sec3.paragraph_format.line_spacing = 1.1
    r_h3 = p_sec3.add_run("3. Security Advantage (PCI-DSS Cardholder Data Isolation): ")
    r_h3.bold = True
    r_h3.font.name = "Arial"
    r_h3.font.size = Pt(10)
    r_h3.font.color.rgb = RGBColor(15, 23, 42)

    r_t4 = p_sec3.add_run(
        "Because the kiosk accepts credit card payments exclusively, protecting payment information is critical. "
        "The Layered Architecture enforces strict tier boundaries: the touch UI layer never directly contacts external banking networks or data stores. "
        "The Payment Service Component operates in an isolated business layer boundary, transmitting encrypted Primary Account Numbers (PAN) "
        "exclusively through secure, certified payment APIs. Cardholder data is never persisted to the local database, preventing credential leakage "
        "or tampering via the publicly accessible touch terminal."
    )
    r_t4.font.name = "Arial"
    r_t4.font.size = Pt(9.5)
    r_t4.font.color.rgb = RGBColor(30, 41, 59)

    # 6. Section 4: Performance Benefit
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.space_before = Pt(4)
    p_sec4.paragraph_format.space_after = Pt(2)
    p_sec4.paragraph_format.line_spacing = 1.1
    r_h4 = p_sec4.add_run("4. Performance Benefit (In-Memory Caching & Immediate Touch Responsiveness): ")
    r_h4.bold = True
    r_h4.font.name = "Arial"
    r_h4.font.size = Pt(10)
    r_h4.font.color.rgb = RGBColor(15, 23, 42)

    r_t5 = p_sec4.add_run(
        "In a bustling café with high order volume, customer wait times directly impact revenue. "
        "In our Layered Architecture, the Order Manager and UI components load and cache menu catalog and pricing data in-memory at startup. "
        "Customer touch actions (selecting drinks, choosing sizes, reviewing totals) are processed instantaneously in-memory with sub-10ms latency, "
        "eliminating redundant disk/network queries. Database operations are strictly confined to an asynchronous transaction commit once payment is approved."
    )
    r_t5.font.name = "Arial"
    r_t5.font.size = Pt(9.5)
    r_t5.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")


def generate_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=1,  # Center
        textColor=colors.HexColor("#0F172A")
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )

    sel_style = ParagraphStyle(
        "SelStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0F172A")
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.5,
        leftIndent=14,
        textColor=colors.HexColor("#1E293B")
    )

    elements = []

    # 1. Header Banner Table
    banner_data = [[
        Paragraph("<b>LAB 3: ARCHITECTURAL PATTERN SELECTION & JUSTIFICATION</b>", title_style),
    ], [
        Paragraph("Course: Software Engineering (SELABS) &nbsp;|&nbsp; Student: <b>A R Akshay Kumar</b> &nbsp;|&nbsp; USN: <b>PES1UG24CS705</b>", meta_style)
    ]]
    banner_table = Table(banner_data, colWidths=[536])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(banner_table)
    elements.append(Spacer(1, 7))

    # 2. Architecture Selection Box
    sel_data = [[
        Paragraph("<b>Architecture Selection:</b> <i>\"We chose <b>Layered Architecture</b> for the Self-Service Coffee Kiosk System.\"</i>", sel_style)
    ]]
    sel_table = Table(sel_data, colWidths=[536])
    sel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(sel_table)
    elements.append(Spacer(1, 8))

    # 3. Section 1: Architectural Choice
    elements.append(Paragraph("<b>1. Architectural Choice:</b>", heading_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(
        "We selected the <b>3-Tier Layered Architecture</b> style (Presentation Layer, Business Layer, Data Layer). "
        "The Presentation Layer encapsulates the User Interface Component, handling customer touch screen interactions, "
        "menu browsing, and drink size selection. The Business Layer hosts the Order Manager Component (workflow orchestrator), "
        "Payment Service Component (card validation), and Receipt Printer Component (hardware abstraction). "
        "The Data Layer encapsulates the Database Component, maintaining menu catalog definitions, drink pricing rules, and order logs.",
        body_style
    ))
    elements.append(Spacer(1, 7))

    # 4. Section 2: Two Reasons
    elements.append(Paragraph("<b>2. Two Scenario-Related Reasons for Selection:</b>", heading_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(
        "• <b>Decoupling Hardware Peripherals & Device Drivers:</b> The kiosk interfaces directly with physical peripherals "
        "(touch screen display, thermal receipt printer) and financial hardware (credit card reader). Layered architecture isolates "
        "low-level hardware communications (ESC/POS printer serial commands) within dedicated components. Upgrading printer hardware or "
        "redesigning the touch screen UI requires zero changes to core order calculation and pricing logic.",
        bullet_style
    ))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "• <b>Independent Menu, Pricing & Business Rule Administration:</b> Café menu items (Espresso, Americano, Latte) and size pricing "
        "multipliers (Small vs. Large) change frequently. By isolating persistence inside the Data Layer (Database Component), prices and recipes "
        "can be updated directly in the database without recompiling, redeploying, or risking regressions in kiosk UI workflows.",
        bullet_style
    ))
    elements.append(Spacer(1, 7))

    # 5. Section 3: Security Advantage
    elements.append(Paragraph("<b>3. Security Advantage (PCI-DSS Cardholder Data Isolation):</b>", heading_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(
        "Because the kiosk accepts credit card payments exclusively, securing payment data is essential. The Layered Architecture enforces strict "
        "layer boundaries: the touch UI layer never directly communicates with payment processing backends or internal database storage. "
        "The Payment Service Component resides in an isolated business layer boundary, transmitting Primary Account Numbers (PAN) strictly through "
        "PCI-DSS certified gateway APIs and masking account numbers. Unencrypted card numbers are never stored in the local database or logs, "
        "protecting customer financial data against physical terminal tampering.",
        body_style
    ))
    elements.append(Spacer(1, 7))

    # 6. Section 4: Performance Benefit
    elements.append(Paragraph("<b>4. Performance Benefit (In-Memory Caching & Sub-Second Responsiveness):</b>", heading_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(
        "In a busy café with peak morning ordering spikes, kiosk latency directly influences customer queue times. In our Layered Architecture, "
        "the Order Manager and UI components load and cache menu catalog and pricing definitions in-memory upon kiosk startup. "
        "Customer touch actions (selecting coffee types, switching drink sizes, viewing order totals) are resolved instantaneously in-memory "
        "with sub-10ms response times without incurring disk I/O or network queries. Database writes are restricted to asynchronous transaction "
        "persistence upon payment completion, ensuring uninterrupted high customer throughput.",
        body_style
    ))

    doc.build(elements)
    print(f"Generated PDF: {output_path}")


if __name__ == "__main__":
    out_dir = "/Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab3"
    docx_file = os.path.join(out_dir, "Coffee_Kiosk_Architecture_Justification.docx")
    pdf_file = os.path.join(out_dir, "Coffee_Kiosk_Architecture_Justification.pdf")
    generate_docx(docx_file)
    generate_pdf(pdf_file)
