#!/usr/bin/env python3
"""
Generates high-precision, publication-quality UML Component Diagrams for:
Coffee Kiosk System (Layered Architecture)
Deliverables:
- Coffee_Kiosk_Component_Diagram.png (300 DPI)
- Coffee_Kiosk_Component_Diagram.pdf (Vector PDF)
- Coffee_Kiosk_Component_Diagram.svg (Vector SVG)
- Coffee_Kiosk_Component_Diagram.drawio (draw.io XML)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_uml_component_diagram(output_dir: str):
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1200)
    ax.axis("off")

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # -------------------------------------------------------------
    # Layer Boundary Box
    # -------------------------------------------------------------
    def draw_layer_box(x, y, w, h, title, fill_color, border_color):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0,rounding_size=12",
            facecolor=fill_color,
            edgecolor=border_color,
            linestyle="--",
            linewidth=2.0,
            zorder=1
        )
        ax.add_patch(rect)
        tag_w = len(title) * 11 + 30
        tag = patches.FancyBboxPatch(
            (x + 20, y + h - 28), tag_w, 28,
            boxstyle="round,pad=0,rounding_size=5",
            facecolor=border_color,
            edgecolor="none",
            zorder=2
        )
        ax.add_patch(tag)
        ax.text(
            x + 35, y + h - 14, title,
            fontsize=12, fontweight="bold", color="#FFFFFF",
            va="center", ha="left", fontfamily="sans-serif", zorder=3
        )

    # -------------------------------------------------------------
    # UML 2.0 Component Rectangle
    # -------------------------------------------------------------
    def draw_component(x, y, w, h, name, subtitle=None, bg="#FEF3C7", border="#D97706"):
        # Rounded component box for modern look
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0,rounding_size=6",
            facecolor=bg,
            edgecolor=border,
            linewidth=2.2,
            zorder=4
        )
        ax.add_patch(box)

        # UML Component Icon in upper right corner
        icon_w, icon_h = 26, 20
        icon_x = x + w - icon_w - 14
        icon_y = y + h - icon_h - 12
        icon_box = patches.Rectangle(
            (icon_x, icon_y), icon_w, icon_h,
            facecolor="#FFFFFF", edgecolor=border, linewidth=1.5, zorder=5
        )
        ax.add_patch(icon_box)
        tab1 = patches.Rectangle(
            (icon_x - 5, icon_y + 11), 8, 4.5,
            facecolor="#FFFFFF", edgecolor=border, linewidth=1.2, zorder=6
        )
        tab2 = patches.Rectangle(
            (icon_x - 5, icon_y + 4.5), 8, 4.5,
            facecolor="#FFFFFF", edgecolor=border, linewidth=1.2, zorder=6
        )
        ax.add_patch(tab1)
        ax.add_patch(tab2)

        # Stereotype «component»
        ax.text(
            x + w / 2, y + h - 26, "«component»",
            fontsize=11, fontstyle="italic", color="#4B5563",
            va="center", ha="center", fontfamily="sans-serif", zorder=6
        )

        # Component Name
        ax.text(
            x + w / 2, y + h - 62, name,
            fontsize=13.5, fontweight="bold", color="#0F172A",
            va="center", ha="center", fontfamily="sans-serif", zorder=6
        )

        # Subtitle
        if subtitle:
            ax.text(
                x + w / 2, y + 36, subtitle,
                fontsize=9.5, fontstyle="italic", color="#475569",
                va="center", ha="center", fontfamily="sans-serif", zorder=6
            )

    # -------------------------------------------------------------
    # Title & Subtitle Header
    # -------------------------------------------------------------
    ax.text(
        800, 1165, "Coffee Kiosk System — UML Component Diagram",
        fontsize=22, fontweight="bold", color="#0F172A",
        va="center", ha="center", fontfamily="sans-serif"
    )
    ax.text(
        800, 1135, "Architectural Style: 3-Tier Layered Architecture (Presentation • Business Logic • Data Persistence)",
        fontsize=12, fontstyle="italic", color="#475569",
        va="center", ha="center", fontfamily="sans-serif"
    )

    # -------------------------------------------------------------
    # LAYERS
    # -------------------------------------------------------------
    # Presentation Layer: Y from 910 to 1105 (h=195)
    draw_layer_box(60, 910, 1480, 195, "Presentation Layer", fill_color="#F0F7FF", border_color="#2563EB")
    draw_component(
        580, 935, 440, 145,
        "User Interface Component",
        subtitle="Touchscreen Event Processing • Beverage Selection • Checkout UI",
        bg="#DBEAFE", border="#1D4ED8"
    )

    # Business Layer: Y from 380 to 825 (h=445)
    draw_layer_box(60, 380, 1480, 445, "Business Layer", fill_color="#F0FDF4", border_color="#059669")
    draw_component(
        580, 645, 440, 150,
        "Order Manager Component",
        subtitle="Orchestrator • Order Lifecycle • Pricing Multipliers • Workflow State",
        bg="#DCFCE7", border="#047857"
    )
    draw_component(
        100, 425, 410, 140,
        "Payment Service Component",
        subtitle="Credit Card Authorization • PCI-DSS Integration • PAN Masking",
        bg="#DCFCE7", border="#047857"
    )
    draw_component(
        600, 425, 400, 140,
        "Receipt Printer Component",
        subtitle="ESC/POS Hardware Driver • Receipt Formatting & Cut Command",
        bg="#DCFCE7", border="#047857"
    )

    # Data Layer: Y from 60 to 310 (h=250)
    draw_layer_box(60, 60, 1480, 250, "Data Layer", fill_color="#FAF5FF", border_color="#7C3AED")
    draw_component(
        1050, 110, 430, 140,
        "Database Component",
        subtitle="Menu Catalog • Drink Sizes & Pricing Rules • Transaction Log",
        bg="#F3E8FF", border="#6D28D9"
    )

    # -------------------------------------------------------------
    # INTERFACE 1: Order Interface (UI <-> Order Manager)
    # -------------------------------------------------------------
    # UI bottom at y=935, Order Manager top at y=795. Midpoint = 865.
    ix = 800
    iy = 865
    ax.plot([ix, ix], [935, iy + 8], color="#1E293B", lw=2, zorder=7)
    arc1 = patches.Arc((ix, iy + 8), 24, 18, angle=0, theta1=0, theta2=180, color="#1E293B", lw=2.5, zorder=8)
    ax.add_patch(arc1)

    ax.plot([ix, ix], [795, iy - 2], color="#1E293B", lw=2, zorder=7)
    ball1 = patches.Circle((ix, iy - 2), 7, facecolor="#FFFFFF", edgecolor="#1E293B", lw=2.5, zorder=9)
    ax.add_patch(ball1)

    ax.text(
        ix + 24, iy + 10, "○—) Order Interface",
        fontsize=11, fontweight="bold", color="#1E3A8A", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )
    ax.text(
        ix + 24, iy - 10, "[Touchscreen Events / IPC]",
        fontsize=9.5, fontstyle="italic", color="#475569", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )

    # -------------------------------------------------------------
    # INTERFACE 2: Payment Interface (Order Manager <-> Payment Service)
    # -------------------------------------------------------------
    px = 440
    py = 600
    ax.plot([580, px], [720, 720], color="#1E293B", lw=2, zorder=7)
    ax.plot([px, px], [720, py + 8], color="#1E293B", lw=2, zorder=7)
    arc2 = patches.Arc((px, py + 8), 24, 18, angle=0, theta1=0, theta2=180, color="#1E293B", lw=2.5, zorder=8)
    ax.add_patch(arc2)

    ax.plot([305, 305], [565, py - 2], color="#1E293B", lw=2, zorder=7)
    ax.plot([305, px], [py - 2, py - 2], color="#1E293B", lw=2, zorder=7)
    ball2 = patches.Circle((px, py - 2), 7, facecolor="#FFFFFF", edgecolor="#1E293B", lw=2.5, zorder=9)
    ax.add_patch(ball2)

    ax.text(
        px + 18, py + 12, "○—) Payment Interface",
        fontsize=11, fontweight="bold", color="#1E3A8A", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )
    ax.text(
        px + 18, py - 10, "[PCI-DSS Card Processing API]",
        fontsize=9.5, fontstyle="italic", color="#475569", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )

    # -------------------------------------------------------------
    # INTERFACE 3: Receipt Interface (Order Manager <-> Receipt Printer)
    # -------------------------------------------------------------
    rx = 800
    ry = 605
    ax.plot([rx, rx], [645, ry + 8], color="#1E293B", lw=2, zorder=7)
    arc3 = patches.Arc((rx, ry + 8), 24, 18, angle=0, theta1=0, theta2=180, color="#1E293B", lw=2.5, zorder=8)
    ax.add_patch(arc3)

    ax.plot([rx, rx], [565, ry - 2], color="#1E293B", lw=2, zorder=7)
    ball3 = patches.Circle((rx, ry - 2), 7, facecolor="#FFFFFF", edgecolor="#1E293B", lw=2.5, zorder=9)
    ax.add_patch(ball3)

    ax.text(
        rx + 24, ry + 10, "○—) Receipt Interface",
        fontsize=11, fontweight="bold", color="#1E3A8A", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )
    ax.text(
        rx + 24, ry - 10, "[ESC/POS Hardware Serial/USB]",
        fontsize=9.5, fontstyle="italic", color="#475569", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )

    # -------------------------------------------------------------
    # INTERFACE 4: Database Interface (Order Manager <-> Database)
    # -------------------------------------------------------------
    dx = 1265
    dy = 345
    ax.plot([1020, dx], [720, 720], color="#1E293B", lw=2, zorder=7)
    ax.plot([dx, dx], [720, dy + 8], color="#1E293B", lw=2, zorder=7)
    arc4 = patches.Arc((dx, dy + 8), 24, 18, angle=0, theta1=0, theta2=180, color="#1E293B", lw=2.5, zorder=8)
    ax.add_patch(arc4)

    ax.plot([dx, dx], [250, dy - 2], color="#1E293B", lw=2, zorder=7)
    ball4 = patches.Circle((dx, dy - 2), 7, facecolor="#FFFFFF", edgecolor="#1E293B", lw=2.5, zorder=9)
    ax.add_patch(ball4)

    ax.text(
        dx + 22, dy + 10, "○—) Database Interface",
        fontsize=11, fontweight="bold", color="#1E3A8A", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )
    ax.text(
        dx + 22, dy - 10, "[SQL / ORM Query Interface]",
        fontsize=9.5, fontstyle="italic", color="#475569", va="center", ha="left", fontfamily="sans-serif", zorder=10
    )

    # -------------------------------------------------------------
    # NOTATION LEGEND (Bottom Left of Data Layer)
    # -------------------------------------------------------------
    lx, ly, lw, lh = 100, 90, 520, 190
    legend_bg = patches.FancyBboxPatch(
        (lx, ly), lw, lh,
        boxstyle="round,pad=0,rounding_size=8",
        facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.5, zorder=10
    )
    ax.add_patch(legend_bg)

    ax.text(
        lx + 20, ly + lh - 25, "UML Component Diagram Notation Guide",
        fontsize=11.5, fontweight="bold", color="#0F172A", fontfamily="sans-serif", zorder=11
    )

    # Item 1: Component Rectangle
    ax.add_patch(patches.Rectangle((lx + 25, ly + 118), 24, 18, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5, zorder=11))
    ax.add_patch(patches.Rectangle((lx + 21, ly + 128), 8, 4, facecolor="#FFFFFF", edgecolor="#2563EB", lw=1, zorder=12))
    ax.add_patch(patches.Rectangle((lx + 21, ly + 121), 8, 4, facecolor="#FFFFFF", edgecolor="#2563EB", lw=1, zorder=12))
    ax.text(lx + 65, ly + 127, "«component» — Modular, executable unit of software", fontsize=9.5, color="#1E293B", zorder=11)

    # Item 2: Provided Interface (Ball)
    ax.plot([lx + 20, lx + 35], [ly + 93, ly + 93], color="#1E293B", lw=2, zorder=11)
    ax.add_patch(patches.Circle((lx + 35, ly + 93), 6, facecolor="#FFFFFF", edgecolor="#1E293B", lw=2, zorder=12))
    ax.text(lx + 65, ly + 93, "○ Provided Interface (Ball: services offered by component)", fontsize=9.5, color="#1E293B", va="center", zorder=11)

    # Item 3: Required Interface (Socket)
    ax.plot([lx + 20, lx + 36], [ly + 63, ly + 63], color="#1E293B", lw=2, zorder=11)
    ax.add_patch(patches.Arc((lx + 36, ly + 63), 16, 18, angle=0, theta1=270, theta2=90, color="#1E293B", lw=2, zorder=12))
    ax.text(lx + 65, ly + 63, ") Required Interface (Socket: services needed by component)", fontsize=9.5, color="#1E293B", va="center", zorder=11)

    # Item 4: Assembly Connector
    ax.plot([lx + 20, lx + 32], [ly + 33, ly + 33], color="#1E293B", lw=2, zorder=11)
    ax.add_patch(patches.Circle((lx + 32, ly + 33), 5, facecolor="#FFFFFF", edgecolor="#1E293B", lw=1.8, zorder=12))
    ax.add_patch(patches.Arc((lx + 40, ly + 33), 14, 16, angle=0, theta1=90, theta2=270, color="#1E293B", lw=1.8, zorder=12))
    ax.plot([lx + 40, lx + 52], [ly + 33, ly + 33], color="#1E293B", lw=2, zorder=11)
    ax.text(lx + 65, ly + 33, "○—) Assembly Connector (Connects provided to required interface)", fontsize=9.5, color="#1E293B", va="center", zorder=11)

    plt.tight_layout()

    png_path = os.path.join(output_dir, "Coffee_Kiosk_Component_Diagram.png")
    fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Generated PNG: {png_path}")

    pdf_path = os.path.join(output_dir, "Coffee_Kiosk_Component_Diagram.pdf")
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Generated PDF: {pdf_path}")

    svg_path = os.path.join(output_dir, "Coffee_Kiosk_Component_Diagram.svg")
    fig.savefig(svg_path, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Generated SVG: {svg_path}")

    plt.close()


def generate_drawio_xml(output_dir: str):
    drawio_content = """<mxfile host="app.diagrams.net" modified="2026-09-10T16:25:00.000Z" agent="Antigravity" version="21.0.0" type="device">
  <diagram id="coffee-kiosk-component" name="Coffee Kiosk Component Diagram">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title -->
        <mxCell id="title" value="Coffee Kiosk System — UML Component Diagram&#xa;Architectural Pattern: 3-Tier Layered Architecture" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;fontColor=#0F172A;" vertex="1" parent="1">
          <mxGeometry x="300" y="20" width="560" height="40" as="geometry" />
        </mxCell>

        <!-- Presentation Layer -->
        <mxCell id="layer_pres" value="Presentation Layer" style="swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=5 5;fillColor=#EFF6FF;strokeColor=#3B82F6;strokeWidth=2;fontStyle=1;fontSize=13;fontColor=#1E3A8A;startSize=30;" vertex="1" parent="1">
          <mxGeometry x="60" y="80" width="1040" height="150" as="geometry" />
        </mxCell>

        <mxCell id="comp_ui" value="&amp;laquo;component&amp;raquo;&#xa;&lt;b&gt;User Interface Component&lt;/b&gt;&#xa;&lt;i&gt;(Touch Screen Handler &amp;bull; Menu &amp;bull; Sizes)&lt;/i&gt;" style="shape=module;jettyWidth=8;jettyHeight=4;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#2563EB;strokeWidth=2;fontSize=12;" vertex="1" parent="layer_pres">
          <mxGeometry x="380" y="45" width="280" height="80" as="geometry" />
        </mxCell>

        <!-- Business Layer -->
        <mxCell id="layer_biz" value="Business Layer" style="swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=5 5;fillColor=#F0FDF4;strokeColor=#10B981;strokeWidth=2;fontStyle=1;fontSize=13;fontColor=#065F46;startSize=30;" vertex="1" parent="1">
          <mxGeometry x="60" y="270" width="1040" height="300" as="geometry" />
        </mxCell>

        <mxCell id="comp_om" value="&amp;laquo;component&amp;raquo;&#xa;&lt;b&gt;Order Manager Component&lt;/b&gt;&#xa;&lt;i&gt;(Workflow &amp;bull; Pricing &amp;bull; State Machine)&lt;/i&gt;" style="shape=module;jettyWidth=8;jettyHeight=4;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#059669;strokeWidth=2;fontSize=12;" vertex="1" parent="layer_biz">
          <mxGeometry x="380" y="50" width="280" height="80" as="geometry" />
        </mxCell>

        <mxCell id="comp_pay" value="&amp;laquo;component&amp;raquo;&#xa;&lt;b&gt;Payment Service Component&lt;/b&gt;&#xa;&lt;i&gt;(Credit Card Only &amp;bull; PCI-DSS Gateway)&lt;/i&gt;" style="shape=module;jettyWidth=8;jettyHeight=4;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#059669;strokeWidth=2;fontSize=12;" vertex="1" parent="layer_biz">
          <mxGeometry x="60" y="190" width="270" height="80" as="geometry" />
        </mxCell>

        <mxCell id="comp_print" value="&amp;laquo;component&amp;raquo;&#xa;&lt;b&gt;Receipt Printer Component&lt;/b&gt;&#xa;&lt;i&gt;(ESC/POS Hardware Protocol &amp;bull; Formatter)&lt;/i&gt;" style="shape=module;jettyWidth=8;jettyHeight=4;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#059669;strokeWidth=2;fontSize=12;" vertex="1" parent="layer_biz">
          <mxGeometry x="390" y="190" width="260" height="80" as="geometry" />
        </mxCell>

        <!-- Data Layer -->
        <mxCell id="layer_data" value="Data Layer" style="swimlane;whiteSpace=wrap;html=1;dashed=1;dashPattern=5 5;fillColor=#FAF5FF;strokeColor=#8B5CF6;strokeWidth=2;fontStyle=1;fontSize=13;fontColor=#5B21B6;startSize=30;" vertex="1" parent="1">
          <mxGeometry x="60" y="600" width="1040" height="150" as="geometry" />
        </mxCell>

        <mxCell id="comp_db" value="&amp;laquo;component&amp;raquo;&#xa;&lt;b&gt;Database Component&lt;/b&gt;&#xa;&lt;i&gt;(Menu Catalog &amp;bull; Pricing &amp;bull; Orders Table)&lt;/i&gt;" style="shape=module;jettyWidth=8;jettyHeight=4;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#7C3AED;strokeWidth=2;fontSize=12;" vertex="1" parent="layer_data">
          <mxGeometry x="720" y="45" width="280" height="80" as="geometry" />
        </mxCell>

        <!-- Connectors & Interfaces -->
        <mxCell id="edge_ui_om" value="Order Interface&#xa;[Touch IPC / GUI Events]" style="endArrow=oval;endFill=1;startArrow=halfCircle;startFill=0;strokeWidth=2;strokeColor=#1E3A8A;fontColor=#1E3A8A;fontSize=11;fontStyle=1;edgeStyle=orthogonalEdgeStyle;rounded=0;" edge="1" parent="1" source="comp_ui" target="comp_om">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="edge_om_pay" value="Payment Interface&#xa;[PCI-DSS Card API]" style="endArrow=oval;endFill=1;startArrow=halfCircle;startFill=0;strokeWidth=2;strokeColor=#1E3A8A;fontColor=#1E3A8A;fontSize=11;fontStyle=1;edgeStyle=orthogonalEdgeStyle;rounded=0;" edge="1" parent="1" source="comp_om" target="comp_pay">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="edge_om_print" value="Receipt Interface&#xa;[ESC/POS Hardware Driver]" style="endArrow=oval;endFill=1;startArrow=halfCircle;startFill=0;strokeWidth=2;strokeColor=#1E3A8A;fontColor=#1E3A8A;fontSize=11;fontStyle=1;edgeStyle=orthogonalEdgeStyle;rounded=0;" edge="1" parent="1" source="comp_om" target="comp_print">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="edge_om_db" value="Database Interface&#xa;[SQL / ORM Query]" style="endArrow=oval;endFill=1;startArrow=halfCircle;startFill=0;strokeWidth=2;strokeColor=#1E3A8A;fontColor=#1E3A8A;fontSize=11;fontStyle=1;edgeStyle=orthogonalEdgeStyle;rounded=0;" edge="1" parent="1" source="comp_om" target="comp_db">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    drawio_path = os.path.join(output_dir, "Coffee_Kiosk_Component_Diagram.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_content.strip())
    print(f"Generated draw.io XML: {drawio_path}")


if __name__ == "__main__":
    out_dir = "/Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab3"
    create_uml_component_diagram(out_dir)
    generate_drawio_xml(out_dir)
