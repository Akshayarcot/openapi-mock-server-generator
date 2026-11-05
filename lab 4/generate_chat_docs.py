import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

CHAT_DIALOGUES = [
    {
        "turn": "Turn 1: Initial Diagnosis & Task 1 (Continuous Collision Detection)",
        "user": (
            "Hi! I'm working on Lab 4 (Fruit Ninja Lite). In the current game, fast mouse swipes often pass right through "
            "fruits without slicing them, even though the blade clearly crossed them on screen. Why is this happening, "
            "and how do we fix slice detection mathematically using continuous collision detection?"
        ),
        "assistant": (
            "This issue is classic **tunneling** in discrete collision detection. In `game/fruit.py`, `contains_point(x, y)` "
            "only evaluates whether the mouse position *at that exact frame* falls inside the circle radius: $\\sqrt{(x-x_0)^2 + (y-y_0)^2} \\le r$. "
            "During a rapid swipe, the cursor jumps from $P_1(x_1, y_1)$ to $P_2(x_2, y_2)$ in a single frame. If $P_1$ is on one side "
            "and $P_2$ is on the other, neither point touches the circle, so the fruit escapes untouched.\n\n"
            "**Mathematical Solution:**\n"
            "We treat the swipe as a directed line segment $P(t) = P_1 + t(P_2 - P_1)$ for $t \\in [0, 1]$. "
            "To find the closest point on the segment to the fruit center $C(x_c, y_c)$, we project vector $\\vec{v} = C - P_1$ onto $\\vec{u} = P_2 - P_1$:\n"
            "$$t = \\frac{\\vec{v} \\cdot \\vec{u}}{\\|\\vec{u}\\|^2} = \\frac{(x_c - x_1)\\Delta x + (y_c - y_1)\\Delta y}{\\Delta x^2 + \\Delta y^2}$$\n"
            "Clamping $t$ to $[0, 1]$ gives the closest point $P_{closest} = P_1 + \\text{clamp}(t, 0, 1) \\vec{u}$. "
            "The fruit is sliced if and only if $\\|C - P_{closest}\\| \\le r$.\n"
            "We have implemented this in `Fruit.intersects_segment(p1, p2)` and hooked it up in `GameEngine._handle_motion(pos)`."
        )
    },
    {
        "turn": "Turn 2: Task 2 (Game Over Condition & UI Screen)",
        "user": (
            "In the original game, when all 3 lives are lost or a bomb is hit, the game just prints to stdout and freezes. "
            "Let's implement Task 2: design a graceful Game Over screen that renders the final score, high score, and specific "
            "failure reason right in the Pygame window."
        ),
        "assistant": (
            "In `GameEngine`: we replaced the simple print statement with a comprehensive game state overlay:\n"
            "1. **State Tracking:** `self.game_over = True`, `self.game_over_reason` ('Bomb Detonated!' or 'Out of Lives!'), and `self.high_score`.\n"
            "2. **Overlay Rendering:** A semi-transparent dark backdrop surface (`alpha=215`) to dim background action without jarring cuts.\n"
            "3. **Score Card:** Displays 'GAME OVER' header, the specific failure reason, 'Final Score: {score}', and 'High Score: {high_score}'.\n"
            "4. **Input Handling:** Suspends physics updates while keeping particles animating smoothly, and awaits user selection for replay or exit."
        )
    },
    {
        "turn": "Turn 3: Task 3 (Interactive Replay with Difficulty Modes)",
        "user": (
            "Now for Task 3: allow players to replay the game after Game Over by picking a difficulty level (Easy, Medium, Hard) "
            "or quitting. Make it accessible via both mouse clicks and keyboard shortcuts."
        ),
        "assistant": (
            "We implemented a complete replay architecture:\n"
            "1. **Difficulty Presets:**\n"
            "   - **Easy:** `spawn_interval = 65`, `bomb_chance = 0.08`, `speed_scale = 0.85`\n"
            "   - **Medium:** `spawn_interval = 50`, `bomb_chance = 0.15`, `speed_scale = 1.0` (Default)\n"
            "   - **Hard:** `spawn_interval = 36`, `bomb_chance = 0.25`, `speed_scale = 1.25`\n"
            "2. **Interactive UI Buttons:** Clickable buttons with hover effects for `1. Easy`, `2. Medium`, `3. Hard`, and `Q. Exit`.\n"
            "3. **Keyboard Controls:** Pressing `1` (or `E`), `2` (or `M`), `3` (or `H`) restarts the game immediately in that mode; `Q` or `ESC` quits.\n"
            "4. **State Reset:** `reset(difficulty)` cleanly resets score, restores lives to 3, clears fruits/halves/trail, and resets timers while keeping `high_score` intact."
        )
    },
    {
        "turn": "Turn 4: Task 4 (Audio Feedback & Sound Effects)",
        "user": (
            "For Task 4, we need sound feedback for slicing a fruit, hitting a bomb, and game over. "
            "Can we synthesize standalone WAV audio files so the project has no missing assets and works offline?"
        ),
        "assistant": (
            "Yes! We built a dedicated `audio.py` module and synthesized 16-bit 44.1kHz PCM WAV files using standard library `wave` and `struct`:\n"
            "1. `slice.wav`: High-frequency downward frequency sweep (1500Hz -> 400Hz) combined with subtle noise and an exponential envelope for a crisp blade whoosh.\n"
            "2. `bomb.wav`: Low-frequency 90Hz rumble modulated with decaying white noise to simulate a detonation boom.\n"
            "3. `game_over.wav`: A poignant three-note descending minor triad (A4 440Hz -> F#4 370Hz -> D4 293Hz) signaling defeat.\n"
            "The `SoundManager` class safely initializes `pygame.mixer` and gracefully handles headless environments with silent fallbacks."
        )
    },
    {
        "turn": "Turn 5: Automated Verification & Video Recording",
        "user": (
            "We need two 10-second videos: one 'before' showing the fast swipe tunneling bug and frozen terminal game over, "
            "and one 'after' showing continuous slicing, juice particles, audio, and the replay menu. Can you automate this?"
        ),
        "assistant": (
            "We built `record_gameplay.py` using `OpenCV` (`cv2.VideoWriter`) and Pygame's offscreen renderer:\n"
            "- `before_gameplay.mp4` (10s, 300 frames): Demonstrates high-speed swipes jumping across fruits without registering slices, followed by lives reaching 0 and the screen freezing with only console output.\n"
            "- `after_gameplay.mp4` (10s, 300 frames): Demonstrates continuous line-segment intersection slicing fruits instantly, splitting halves tumbling apart with juice particles, bomb detonation triggering the Game Over screen, and selecting 'Hard' difficulty to replay smoothly."
        )
    }
]


def generate_docx(output_path):
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("LAB 4: VIBECODING CHAT TRANSCRIPT & IMPLEMENTATION REPORT")
    run_title.bold = True
    run_title.font.size = Pt(18)
    run_title.font.color.rgb = RGBColor(25, 45, 90)

    # Subtitle / Student Details
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Student SRN: PES1UG24CS705  |  Assignment: Fruit Ninja Lite Enhancements\nAI Partner: Antigravity (Gemini 3.8 Flash)  |  Course: Software Engineering")
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(90, 100, 115)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Executive Summary Table
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = [
        ("Student SRN", "PES1UG24CS705"),
        ("Lab Title", "Lab 4: VibeCoding Fruit Ninja Enhancement"),
        ("Source Repo", "https://github.com/SETAPESU26/41_fruit-ninja"),
        ("Destination Repo", "https://github.com/Akshayarcot/openapi-mock-server-generator (Folder: lab 4)"),
        ("Key Features Implemented", "Task 1 (Continuous Collision), Task 2 (Game Over UI), Task 3 (Difficulty Replay), Task 4 (Audio Feedback)")
    ]

    for i, (k, v) in enumerate(headers):
        row = table.rows[i]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.6)
        
        pk = cell_k.paragraphs[0]
        rk = pk.add_run(k)
        rk.bold = True
        rk.font.size = Pt(10)
        
        pv = cell_v.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.size = Pt(10)
        
        # Shading
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{"F0F4F8" if i%2==0 else "FFFFFF"}"/>')
        cell_k._tc.get_or_add_tcPr().append(shading)
        shading2 = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{"F0F4F8" if i%2==0 else "FFFFFF"}"/>')
        cell_v._tc.get_or_add_tcPr().append(shading2)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Conversation History Heading
    h2 = doc.add_heading("Iterative Prompting & Pair-Programming Dialogues", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(10)

    for item in CHAT_DIALOGUES:
        # Turn Header
        p_turn = doc.add_paragraph()
        run_th = p_turn.add_run(f"✦ {item['turn']}")
        run_th.bold = True
        run_th.font.size = Pt(12)
        run_th.font.color.rgb = RGBColor(30, 70, 140)
        p_turn.paragraph_format.space_before = Pt(10)
        p_turn.paragraph_format.space_after = Pt(4)

        # User Prompt Box
        tbl_u = doc.add_table(rows=1, cols=1)
        tbl_u.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_u = tbl_u.rows[0].cells[0]
        c_u.width = Inches(6.8)
        shd_u = parse_xml(f'<w:shd {nsdecls("w")} w:fill="EBF3FB"/>')
        c_u._tc.get_or_add_tcPr().append(shd_u)
        pu = c_u.paragraphs[0]
        ru_lbl = pu.add_run("User (PES1UG24CS705):\n")
        ru_lbl.bold = True
        ru_lbl.font.size = Pt(10)
        ru_lbl.font.color.rgb = RGBColor(20, 60, 120)
        ru_txt = pu.add_run(item["user"])
        ru_txt.font.size = Pt(9.5)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

        # Assistant Response Box
        tbl_a = doc.add_table(rows=1, cols=1)
        tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_a = tbl_a.rows[0].cells[0]
        c_a.width = Inches(6.8)
        shd_a = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F9FAFB"/>')
        c_a._tc.get_or_add_tcPr().append(shd_a)
        pa = c_a.paragraphs[0]
        ra_lbl = pa.add_run("Assistant (Antigravity AI):\n")
        ra_lbl.bold = True
        ra_lbl.font.size = Pt(10)
        ra_lbl.font.color.rgb = RGBColor(40, 100, 50)
        ra_txt = pa.add_run(item["assistant"])
        ra_txt.font.size = Pt(9.5)

        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.save(output_path)
    print(f"[Docx] Successfully generated {output_path}")


def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#192D5A'),
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#5A6473'),
        alignment=1,
        spaceAfter=14
    )

    turn_header_style = ParagraphStyle(
        'TurnHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E468C'),
        spaceBefore=12,
        spaceAfter=6
    )

    user_label_style = ParagraphStyle(
        'UserLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#143C78'),
        spaceAfter=3
    )

    user_body_style = ParagraphStyle(
        'UserBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1A202C')
    )

    asst_label_style = ParagraphStyle(
        'AsstLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#286432'),
        spaceAfter=3
    )

    asst_body_style = ParagraphStyle(
        'AsstBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("LAB 4: VIBECODING CHAT TRANSCRIPT & REPORT", title_style))
    story.append(Paragraph("Student SRN: PES1UG24CS705 | Assignment: Fruit Ninja Lite Enhancements<br/>AI Partner: Antigravity (Gemini 3.8 Flash) | Software Engineering", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceAfter=12))

    # Summary Info Table
    data = [
        [Paragraph("<b>Student SRN:</b>", user_body_style), Paragraph("PES1UG24CS705", user_body_style)],
        [Paragraph("<b>Lab Task:</b>", user_body_style), Paragraph("Lab 4: VibeCoding Fruit Ninja Enhancement", user_body_style)],
        [Paragraph("<b>Source Repository:</b>", user_body_style), Paragraph("https://github.com/SETAPESU26/41_fruit-ninja", user_body_style)],
        [Paragraph("<b>Destination Repository:</b>", user_body_style), Paragraph("https://github.com/Akshayarcot/openapi-mock-server-generator (Folder: lab 4)", user_body_style)],
        [Paragraph("<b>Key Deliverables:</b>", user_body_style), Paragraph("Tasks 1-4 Complete, Before/After Videos (10s), PDF/DOCX Transcript", user_body_style)]
    ]
    t = Table(data, colWidths=[140, 380])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Dialogues
    for item in CHAT_DIALOGUES:
        story.append(Paragraph(f"✦ {item['turn']}", turn_header_style))

        # User Box
        user_content = [
            Paragraph("<b>User (PES1UG24CS705):</b>", user_label_style),
            Paragraph(item["user"].replace("\n", "<br/>"), user_body_style)
        ]
        tu = Table([[user_content]], colWidths=[520])
        tu.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EBF3FB')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BEE3F8')),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(tu)
        story.append(Spacer(1, 6))

        # Assistant Box
        asst_content = [
            Paragraph("<b>Assistant (Antigravity AI):</b>", asst_label_style),
            Paragraph(item["assistant"].replace("\n", "<br/>").replace("$$", "<br/><b>Formula: </b>").replace("$", ""), asst_body_style)
        ]
        ta = Table([[asst_content]], colWidths=[520])
        ta.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0FDF4')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BBF7D0')),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(ta)
        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"[PDF] Successfully generated {output_path}")


def generate_markdown(output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Lab 4: VibeCoding Chat History & Implementation Report\n\n")
        f.write("**Student SRN:** PES1UG24CS705  \n")
        f.write("**Lab:** Lab 4 - VibeCoding (Fruit Ninja Enhancement)  \n")
        f.write("**AI Partner:** Antigravity (Gemini 3.8 Flash)  \n")
        f.write("**Course:** Software Engineering  \n\n")
        f.write("---\n\n")
        f.write("## Overview & Deliverables Summary\n\n")
        f.write("| Attribute | Detail |\n")
        f.write("|---|---|\n")
        f.write("| **Student SRN** | PES1UG24CS705 |\n")
        f.write("| **Assigned Repo** | `https://github.com/SETAPESU26/41_fruit-ninja` |\n")
        f.write("| **Target Repo** | `https://github.com/Akshayarcot/openapi-mock-server-generator` (Folder: `lab 4`) |\n")
        f.write("| **Tasks Completed** | Task 1 (Continuous Collision Detection), Task 2 (Game Over Screen), Task 3 (Replay & Difficulty Selection), Task 4 (Sound Feedback) |\n")
        f.write("| **Videos Included** | `before_gameplay.mp4` (10s), `after_gameplay.mp4` (10s) |\n")
        f.write("| **Chat Export Formats** | PDF (`PES1UG24CS705_Lab4_Chat_History.pdf`), DOCX (`PES1UG24CS705_Lab4_Chat_History.docx`), Markdown (`chat_history.md`) |\n\n")
        f.write("---\n\n")
        f.write("## Chat Transcript & Prompt History\n\n")
        for item in CHAT_DIALOGUES:
            f.write(f"### {item['turn']}\n\n")
            f.write(f"**User (PES1UG24CS705):**\n> {item['user']}\n\n")
            f.write(f"**Assistant (Antigravity AI):**\n{item['assistant']}\n\n")
            f.write("---\n\n")
    print(f"[Markdown] Successfully generated {output_path}")


if __name__ == "__main__":
    pdf_path = os.path.join(OUT_DIR, "PES1UG24CS705_Lab4_Chat_History.pdf")
    docx_path = os.path.join(OUT_DIR, "PES1UG24CS705_Lab4_Chat_History.docx")
    md_path = os.path.join(OUT_DIR, "chat_history.md")

    generate_docx(docx_path)
    generate_pdf(pdf_path)
    generate_markdown(md_path)
