import os
import shutil
import sys
import json
import splittext

from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('yahei','msyh.ttc'))

from PyPDF2 import PdfFileMerger


from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='yahei',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=10,
            bulletFontName='yahei',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='yahei',
        fontSize=14,
        leading=42,
        alignment=TA_CENTER,
        textColor=black,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles
def build_pdf(filename, flowables):
    doc = BaseDocTemplate(filename)
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )
    doc.build(flowables)

def build_flowables(stylesheet, title, text):
    text_segments = text.split("\n\n")
    paragraphs = []
    paragraphs.append(Paragraph(title, stylesheet['title']))
    for segment in text_segments:
        paragraphs.append(Paragraph(segment, stylesheet['default']))
    
    return paragraphs
    


# find json files in folder and subfolders
def load_json_files(folder):
    json_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files
    
# create title from file name ; remove extension, replace _ with space, capitalize first letter of each word
def create_title(file_name):
    title = file_name.replace(".mp3.json","").replace("_"," ").title()
    return title

# merge pdf files in folder into one single pdf
def merge_pdf(folder):
    pdf_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    merger = PdfFileMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write("expandcontract-merged.pdf")
    merger.close()

def main():
    json_files = load_json_files("transcribe")
    info_files = load_json_files("info")
    for json_file in json_files:
        #load json file content
        with open(json_file, 'r', encoding="utf-8") as f:
            json_content = f.read()

        #load info json
        with open(json_file.replace("transcribe\\","info\\").replace("mp3","info"), 'r', encoding="utf-8") as f:
            info_content = f.read()

        #load json  
        json_data = json.loads(json_content)
        info_data = json.loads(info_content)

        #print(json_data["text"])
        title = info_data["title"]
        text = json_data["text"]
        print(text)
        try:
            paragraphs = splittext.split(text)
        except:
            paragraphs = text
        #print(paragraphs)
        build_pdf(json_file.replace(".mp3.json",".pdf"), build_flowables(stylesheet(), title, paragraphs))
    
    merge_pdf("transcribe")

if __name__ == '__main__':
    main()













