from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, Image, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "esp32-s3-xiaozhi-hardware-setup.pdf"
IMAGES = ROOT / "images"
PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#147D92")
TEAL = colors.HexColor("#18A999")
PALE = colors.HexColor("#E9F5F5")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
ORANGE = colors.HexColor("#F6A623")


def fit_image(path, max_width, max_height):
    with PILImage.open(path) as source:
        width, height = source.size
        cache_dir = ROOT / "tmp" / "pdfs" / "assets"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cached_path = cache_dir / f"{Path(path).stem.replace(' ', '_')}.jpg"
        optimized = source.convert("RGB")
        optimized.thumbnail((1800, 1800), PILImage.Resampling.LANCZOS)
        optimized.save(cached_path, "JPEG", quality=86, optimize=True)
    scale = min(max_width / width, max_height / height)
    image = Image(str(cached_path), width=width * scale, height=height * scale)
    image.hAlign = "CENTER"
    return image


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.setFillColor(colors.white)
    canvas.drawString(16 * mm, PAGE_H - 7.5 * mm, "XIAOZHI ESP32-S3 CUSTOM HARDWARE")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(16 * mm, 9 * mm, "Customized by mpuugaAbdu")
    canvas.drawRightString(PAGE_W - 16 * mm, 9 * mm, str(doc.page))
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=26, leading=29, textColor=NAVY, alignment=TA_CENTER, spaceAfter=5 * mm))
styles.add(ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, leading=16, textColor=MUTED, alignment=TA_CENTER, spaceAfter=7 * mm))
styles.add(ParagraphStyle("H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=NAVY, spaceBefore=3 * mm, spaceAfter=3 * mm))
styles.add(ParagraphStyle("H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=BLUE, spaceBefore=3 * mm, spaceAfter=2 * mm))
styles.add(ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontSize=9.5, leading=14, textColor=INK, spaceAfter=2.5 * mm))
styles.add(ParagraphStyle("Caption", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER, spaceBefore=1.5 * mm, spaceAfter=3 * mm))
styles.add(ParagraphStyle("Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=NAVY))
styles.add(ParagraphStyle("TableCell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=colors.black))
styles.add(ParagraphStyle("TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=colors.white))


def p(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def pin_table(rows):
    wrapped = []
    for row_number, row in enumerate(rows):
        style = styles["TableHead"] if row_number == 0 else styles["TableCell"]
        wrapped.append([Paragraph(str(value), style) for value in row])
    table = Table(wrapped, colWidths=[45 * mm, 30 * mm, 79 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm, bottomMargin=16 * mm, title="ESP32-S3 XiaoZhi Hardware Setup", author="mpuugaAbdu", subject="INMP441, MAX98357A and SH1106 wiring guide")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="content")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

story = [Spacer(1, 8 * mm), p("ESP32-S3 XiaoZhi", "TitleCustom"), p("Illustrated hardware setup for the ESP32-S3-N16R8, INMP441 microphone, MAX98357A amplifier, and SH1106 128x64 OLED", "Subtitle")]
story += [fit_image(IMAGES / "assembly 2.jpg", 150 * mm, 105 * mm), p("Completed enclosure during final assembly. The display, button, controller, and internal wiring remain accessible for inspection.", "Caption")]
summary = Table([[p("CONTROLLER", "Callout"), p("AUDIO INPUT", "Callout"), p("AUDIO OUTPUT", "Callout"), p("DISPLAY", "Callout")], [p("ESP32-S3-N16R8"), p("INMP441 I2S"), p("MAX98357A I2S"), p("SH1106 128x64")]], colWidths=[38.5 * mm] * 4)
summary.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PALE), ("BOX", (0, 0), (-1, -1), 0.5, TEAL), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9FB3C8")), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [summary, Spacer(1, 4 * mm), p("This guide documents mpuugaAbdu's hardware customization of the XiaoZhi ESP32 project. Power off the board before moving wires. Confirm module labels because breakout-board pin order and accepted supply voltage can vary."), PageBreak()]

story += [p("Signal map", "H1Custom"), p("INMP441 digital microphone", "H2Custom"), pin_table([["Module pin", "ESP32-S3", "Purpose"], ["WS", "GPIO 41", "I2S word select / left-right clock"], ["SCK", "GPIO 3", "I2S serial clock"], ["SD", "GPIO 40", "Microphone data into the ESP32-S3"], ["VDD", "3.3 V", "Microphone power"], ["GND", "GND", "Common ground"]]), p("The INMP441 L/R pin selects which I2S channel carries samples. If audio is silent, verify that selection against the firmware channel configuration; do not change signal pins at random.")]
story += [p("MAX98357A amplifier", "H2Custom"), pin_table([["Module pin", "ESP32-S3", "Purpose"], ["DIN", "GPIO 42", "Digital audio from the ESP32-S3"], ["BCLK", "GPIO 1", "I2S bit clock"], ["LRC / LRCLK", "GPIO 2", "I2S left-right clock"], ["GND", "GND", "Common ground"], ["VIN", "Per module label", "Use a clean supply within the breakout's rating"]]), p("<b>Speaker rule:</b> connect the speaker only between SPK+ and SPK-. The MAX98357A uses a bridge output, so neither speaker terminal should be tied to ground.")]
story += [p("SH1106 OLED", "H2Custom"), pin_table([["Module pin", "ESP32-S3", "Purpose"], ["SDA", "GPIO 21", "I2C data"], ["SCL", "GPIO 47", "I2C clock"], ["VCC", "3.3 V", "Display power / logic"], ["GND", "GND", "Common ground"]]), p("The selected firmware target is SH1106 128x64. Many modules answer at address 0x3C; confirm your module with an I2C scan if the display stays blank.")]

story += [PageBreak(), p("Build sequence", "H1Custom"), fit_image(IMAGES / "Breadboard_work.jpg", 105 * mm, 102 * mm), p("1. Breadboard validation - prove the display, microphone, amplifier, and speaker independently before soldering.", "Caption")]
checks = ["Use short I2S clock wires and keep microphone wiring away from the speaker leads.", "Use one common ground for the ESP32-S3 and all peripheral modules.", "Start at low speaker volume to reduce feedback and protect the speaker.", "Verify that USB power is disconnected before continuity checks or rewiring."]
story += [Table([[p(f"<b>{index}.</b> {item}")] for index, item in enumerate(checks, 1)], colWidths=[154 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 0.6, TEAL), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))]

story += [PageBreak(), p("Permanent assembly", "H1Custom"), fit_image(IMAGES / "soldered_board.jpg", 154 * mm, 92 * mm), p("2. Transfer the tested circuit to permanent wiring. Label each connector and add strain relief before enclosure installation.", "Caption"), fit_image(IMAGES / "assembly.jpg", 154 * mm, 88 * mm), p("3. Arrange the ESP32-S3, power circuitry, and cable bundle so solder joints cannot contact the enclosure or pull against headers.", "Caption")]

story += [PageBreak(), p("Pre-power checklist", "H1Custom")]
story += [pin_table([["Check", "Status", "Pass condition"], ["Power rails", "[  ]", "No short; voltage matches every module."], ["Grounding", "[  ]", "ESP32-S3 and all peripherals share ground."], ["Microphone", "[  ]", "WS=41, SCK=3, SD=40; stable capture."], ["Amplifier", "[  ]", "DIN=42, BCLK=1, LRCLK=2; speaker only across SPK+ / SPK-."], ["OLED", "[  ]", "SDA=21, SCL=47; SH1106 and address verified."], ["Mechanical", "[  ]", "No exposed conductor can touch another signal."]])]
story += [Spacer(1, 4 * mm), Table([[p("Bring-up order", "Callout")], [p("1. OLED test  |  2. Microphone capture  |  3. Low-volume playback  |  4. Full voice-assistant session")]], colWidths=[154 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), ORANGE), ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FFF7E6")), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("BOX", (0, 0), (-1, -1), 0.6, ORANGE), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))]
story += [Spacer(1, 5 * mm), p("Firmware configuration", "H2Custom"), p("The board uses simplex I2S with separate microphone and speaker buses. Build the SH1106 variant with:")]
code = Table([["python3 scripts/build.py bread-compact-wifi --name bread-compact-wifi-sh1106-128x64"]], colWidths=[154 * mm])
code.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("TEXTCOLOR", (0, 0), (-1, -1), colors.white), ("FONTNAME", (0, 0), (-1, -1), "Courier"), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [code, Spacer(1, 6 * mm), p("Attribution", "H2Custom"), p("Customized hardware, assembly, and documentation: mpuugaAbdu (github.com/mpuugaAbdu). Original XiaoZhi software copyright (c) 2025 Shenzhen Xinzhi Future Technology Co., Ltd. and Project Contributors. Distributed under the repository's MIT License.")]

doc.build(story)
print(OUTPUT)
