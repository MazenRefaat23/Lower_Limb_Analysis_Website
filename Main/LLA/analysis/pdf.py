from reportlab.lib.utils import ImageReader
from reportlab.platypus import *

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import TableStyle

from PyPDF2 import PdfFileWriter, PdfFileReader
import io

from reportlab.lib import colors


def get_image(path, width=1*cm):
    img = ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def dynamic_save_pdf(describe_sl, describe_sd, grd_sl, data_out2, mean_val):
    # Create first page
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    frame = Frame(1 * cm, 18.5 * cm, 19 * cm, 7 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_1.jpg', width=18 * cm))
    frame.addFromList(story, can)

    frame = Frame(1 * cm, 9.5 * cm, 19 * cm, 7 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_5.jpg', width=18 * cm))
    frame.addFromList(story, can)

    frame = Frame(1 * cm, 2.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_1.jpg', width=8 * cm))
    frame.addFromList(story, can)

    frame = Frame(11 * cm, 2.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_2.jpg', width=8 * cm))
    frame.addFromList(story, can)

    # ---------> Page 2 <--------------

    can.showPage()

    frame = Frame(1 * cm, 19 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_3.jpg', width=8 * cm))
    frame.addFromList(story, can)

    frame = Frame(11 * cm, 19 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_4.jpg', width=8 * cm))
    frame.addFromList(story, can)

    frame = Frame(1 * cm, 12.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_6.jpg', width=8 * cm))
    frame.addFromList(story, can)

    frame = Frame(11 * cm, 12.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_4_7.jpg', width=8 * cm))
    frame.addFromList(story, can)

    can.setFillColorRGB(255, 255, 255)

    textLines = [
        str('Average Stride Length = ') +str(mean_val[0])+str(' m'),
        str('Average Speed = ')+str(data_out2['Avg_speed'][0])+str(' m/sec')
    ]

    text = can.beginText(8 * cm, 10.5 * cm)

    text.setFont("Helvetica", 12)

    for line in textLines:
        text.textLine(line)
        text.moveCursor(0, 4)

    can.drawText(text)

    frame = Frame(1 * cm, 1.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_2_1.jpg', width=8 * cm))
    frame.addFromList(story, can)

    frame = Frame(11 * cm, 1.5 * cm, 9 * cm, 6 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_2_1.jpg', width=8 * cm))
    frame.addFromList(story, can)

    can.showPage()

    # ---------> Page 3 <--------------

    can.setFillColorRGB(255, 255, 255)

    textLines = [
        str('Average Stride Length = ') + str(data_out2['Avg_stride_length'][0])+str(' m'),
        str('Average Speed = ') + str(data_out2['Avg_speed'][0])+str(' m/sec'),
        str('Average Stride Time = ') + str(data_out2['Avg_stride_time'][0])+str(' sec'),
        str('Cadence = ') + str(data_out2['Avg_cadence'][0]) + str(' steps/min'),
    ]

    text = can.beginText(8 * cm, 24.5 * cm)

    text.setFont("Helvetica", 12)

    for line in textLines:
        text.textLine(line)
        text.moveCursor(0, 4)

    can.drawText(text)

    frame = Frame(0.5 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_1_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(8 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_1_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(15 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_1_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    can.setFillColorRGB(255, 255, 255)

    textLines = [
        str('Average Stride Length = ') + str(data_out2['Avg_stride_length'][1])+str(' m'),
        str('Average Speed = ') + str(data_out2['Avg_speed'][1])+str(' m/sec'),
        str('Average Stride Time = ') + str(data_out2['Avg_stride_time'][1])+str(' sec'),
        str('Cadence = ') + str(data_out2['Avg_cadence'][1])+str(' steps/min')
    ]

    text = can.beginText(8 * cm, 12.5 * cm)

    text.setFont("Helvetica", 12)

    for line in textLines:
        text.textLine(line)
        text.moveCursor(0, 4)

    can.drawText(text)

    frame = Frame(0.5 * cm, 3 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_2_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(8 * cm, 3 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_2_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(15 * cm, 3 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_2_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    can.showPage()

    # ---------> Page 4 <--------------

    can.setFillColorRGB(255, 255, 255)

    textLines = [
        str('Average Stride Length = ') + str(data_out2['Avg_stride_length'][2])+str(' m'),
        str('Average Speed = ') + str(data_out2['Avg_speed'][2])+str(' m/sec'),
        str('Average Stride Time = ') + str(data_out2['Avg_stride_time'][2])+str(' sec'),
        str('Cadence = ') + str(data_out2['Avg_cadence'][2])+str(' steps/min')
    ]

    text = can.beginText(8 * cm, 24.5 * cm)

    text.setFont("Helvetica", 12)

    for line in textLines:
        text.textLine(line)
        text.moveCursor(0, 4)

    can.drawText(text)

    frame = Frame(0.5 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_3_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(8 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_3_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    frame = Frame(15 * cm, 15 * cm, 6 * cm, 5 * cm, showBoundary=0)
    story = []
    story.append(get_image(r'media/out_3_3_1.jpg', width=5.5 * cm))
    frame.addFromList(story, can)

    data = [
        ['Activity', 'Count', 'Mean', 'Median', 'Std', 'Min', 'Max'],
        ['Level ground walking', describe_sl['count'][0], describe_sl['mean'][0], describe_sl['median'][0],
         describe_sl['std'][0], describe_sl['min'][0], describe_sl['max'][0]],
        ['Ramp ascent', describe_sl['count'][1], describe_sl['mean'][1], describe_sl['median'][1],
         describe_sl['std'][1], describe_sl['min'][1], describe_sl['max'][1]],
        ['Ramp descent', describe_sl['count'][2], describe_sl['mean'][2], describe_sl['median'][2],
         describe_sl['std'][2], describe_sl['min'][2], describe_sl['max'][2]]
    ]
    table = Table(data)

    MARGIN_LEFT = 3 * cm
    MARGIN_BOTTOM = 9 * cm

    # add style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (6, 0), colors.Color(red=(39 / 255), green=(32 / 255), blue=(99 / 255))),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(red=(1), green=(1), blue=(1))),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('RIGHTPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, 0), 12),

        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.Color(red=(37 / 255), green=(37 / 255), blue=(37 / 255))
        else:
            bc = colors.Color(red=(18 / 255), green=(18 / 255), blue=(18 / 255))

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.Color(red=(1), green=(1), blue=(1))),

            ('LINEBELOW', (0, 1), (-1, -1), 1, colors.Color(red=(39 / 255), green=(32 / 255), blue=(99 / 255))),
        ]
    )
    table.setStyle(ts)

    # what you need to add to canvas
    table.wrapOn(can, 0, 0)
    table.drawOn(can, MARGIN_LEFT, MARGIN_BOTTOM)

    data = [
        ['Activity', 'Count', 'Mean', 'Median', 'Std', 'Min', 'Max'],
        ['Level ground walking', describe_sd['count'][0], describe_sd['mean'][0], describe_sd['median'][0],
         describe_sd['std'][0], describe_sd['min'][0], describe_sd['max'][0]],
        ['Ramp ascent', describe_sd['count'][1], describe_sd['mean'][1], describe_sd['median'][1],
         describe_sd['std'][1], describe_sd['min'][1], describe_sd['max'][1]],
        ['Ramp descent', describe_sd['count'][2], describe_sd['mean'][2], describe_sd['median'][2],
         describe_sd['std'][2], describe_sd['min'][2], describe_sd['max'][2]]
    ]
    table = Table(data)

    MARGIN_LEFT = 3 * cm
    MARGIN_BOTTOM = 3 * cm

    # add style

    style = TableStyle([
        ('BACKGROUND', (0, 0), (6, 0), colors.Color(red=(39 / 255), green=(32 / 255), blue=(99 / 255))),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(red=(1), green=(1), blue=(1))),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('RIGHTPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, 0), 12),

        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.Color(red=(37 / 255), green=(37 / 255), blue=(37 / 255))
        else:
            bc = colors.Color(red=(18 / 255), green=(18 / 255), blue=(18 / 255))

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.Color(red=(1), green=(1), blue=(1))),

            ('LINEBELOW', (0, 1), (-1, -1), 1, colors.Color(red=(39 / 255), green=(32 / 255), blue=(99 / 255))),
        ]
    )
    table.setStyle(ts)

    # what you need to add to canvas
    table.wrapOn(can, 0, 0)
    table.drawOn(can, MARGIN_LEFT, MARGIN_BOTTOM)

    can.showPage()

    can.save()

    # add to the template

    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    existing_pdf = PdfFileReader(open(r'prediction/Template.pdf', "rb"))
    output = PdfFileWriter()

    page = existing_pdf.getPage(0)
    output.addPage(page)

    page = existing_pdf.getPage(1)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    page = existing_pdf.getPage(2)
    page.mergePage(new_pdf.getPage(1))
    output.addPage(page)

    page = existing_pdf.getPage(3)
    page.mergePage(new_pdf.getPage(2))
    output.addPage(page)

    page = existing_pdf.getPage(4)
    page.mergePage(new_pdf.getPage(3))
    output.addPage(page)

    outputStream = open(r'media/output.pdf', "wb")
    output.write(outputStream)
    outputStream.close()
