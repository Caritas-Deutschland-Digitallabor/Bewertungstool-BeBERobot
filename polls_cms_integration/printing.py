# File to generate the PDF report!
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from .models import  *
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from functools import partial
# Chart with reportlab
from reportlab.lib.colors import green, white, lightgreen, beige, bisque, HexColor, lightgrey, grey
from reportlab.graphics.shapes import _DrawingEditorMixin, Drawing 
from reportlab.graphics.charts.spider import SpiderChart 
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(205 * mm, 5 * mm ,
                             "Seite %d von %d" % (self._pageNumber, page_count)) 

class QuickPieChart02(_DrawingEditorMixin,Drawing):
    """
    Radar Chart
    """
    def __init__(self, workshop_id, width=400,height=300,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)

        # Get all the questions answered of the workshop
        selected_setting = get_object_or_404(Setting, workshop_id=workshop_id)
        if selected_setting.setting == "langzeitstationär":
            care = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "care")
            technology = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "technology")
            embedding = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "embedding")
            law = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "law")
            ethics = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "ethics")
            economy = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "economy")

        elif selected_setting.setting == "akutstationär":
            care = AkuPoll_Answer.objects.filter(workshop_id=workshop_id, category = "care")
            technology = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "technology")
            embedding = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "embedding")
            law = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "law")
            ethics = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "ethics")
            economy = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "economy")
        else: 
            care = AmbuPoll_Answer.objects.filter(workshop_id=workshop_id, category = "care")
            technology = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "technology")
            embedding = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "embedding")
            law = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "law")
            ethics = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "ethics")
            economy = LangPoll_Answer.objects.filter(workshop_id=workshop_id, category = "economy")

        # Calculate the result for each category: ja = 1 point, ja_aber = 0.5, nein = 0. The maximum value for each category is the number of answered questions
        care_total = care.count()
        technology_total = technology.count()
        embedding_total = embedding.count()
        law_total = law.count()
        ethics_total = ethics.count()
        economy_total = economy.count()

        care_points = 0
        technology_points = 0
        embedding_points = 0
        law_points = 0
        ethics_points = 0
        economy_points = 0

        for care_question in care:
            print("CARE CHOICE: ", care_question.choice, flush=True)
            if care_question.choice == "Ja":
                care_points += 1 
            elif care_question.choice == "Ja_aber":
                care_points +=0.5
            else:
                continue

        for technology_question in technology:
            if technology_question.choice == "Ja":
                technology_points += 1 
            elif technology_question.choice == "Ja_aber":
                technology_points +=0.5
            else:
                continue

        for embedding_question in embedding:
            if embedding_question.choice == "Ja":
                embedding_points += 1 
            elif embedding_question.choice == "Ja_aber":
                embedding_points +=0.5
            else:
                continue
        
        for law_question in law:
            if law_question.choice == "Ja":
                law_points += 1 
            elif law_question.choice == "Ja_aber":
                law_points +=0.5
            else:
                continue

        for ethics_question in ethics:
            if ethics_question.choice == "Ja":
                ethics_points += 1 
            elif ethics_question.choice == "Ja_aber":
                ethics_points +=0.5
            else:
                continue

        for economy_question in economy:
            if economy_question.choice == "Ja":
                economy_points += 1 
            elif economy_question.choice == "Ja_aber":
                economy_points +=0.5
            else:
                continue

        care_percentage = (care_points*100)/care_total
        technology_percentage = (technology_points*100)/technology_total
        embedding_percentage = (embedding_points*100)/embedding_total
        law_percentage = (law_points*100)/law_total
        ethics_percentage = (ethics_points*100)/ethics_total
        economy_percentage = (economy_points*100)/economy_total

        # Define the radar chart
        self._add(self,SpiderChart(),name='chart',validate=None,desc="The main chart")
        self.chart.width = 200
        self.chart.height = 200
        self.chart.x = 100
        self.chart.y = 25
        self.chart.strands[0].strokeColor= grey #bisque
        self.chart.strands[0].fillColor = lightgrey #beige
        self.chart.strands[1].strokeColor= green
        self.chart.strands[1].fillColor = lightgreen
        self.chart.strands.strokeWidth = 1
        self.chart.strandLabels.fontName = 'Helvetica'
        self.chart.strandLabels.fontSize = 10
        self.chart.strands[0].symbol = "Square"
        self.chart.strands[1].symbol = "Circle"
        self.chart.strandLabels[1,0]._text = str(round(care_percentage)) + "%"
        self.chart.strandLabels[1,1]._text = str(round(technology_percentage)) + "%"
        self.chart.strandLabels[1,2]._text = str(round(law_percentage)) + "%"
        self.chart.strandLabels[1,3]._text = str(round(embedding_percentage)) + "%"
        self.chart.strandLabels[1,4]._text = str(round(ethics_percentage)) + "%"
        self.chart.strandLabels[1,5]._text = str(round(economy_percentage)) + "%"
        self.chart.strandLabels.format = 'values'
        self.chart.strandLabels.dR = 15
        self.chart.fillColor = white
        self.chart.data = [ (100, 100, 100, 100, 100, 100), (care_percentage, technology_percentage, law_percentage, embedding_percentage, ethics_percentage, economy_percentage)]
        self.chart.labels = ['Pflege','Technik & Infrastruktur', 'Datenschutz & Recht', 'Institutionelle & gesellschaftliche Einbettung', 'Ethik', 'Ökonomie']
        self.chart.strands.strokeWidth = 1
        self._add(self,0,name='preview',validate=None,desc=None)

class MyPrint:
    def __init__(self, buffer, workshop_id): 
        self.buffer = buffer
        self.pagesize = A4
        self.width, self.height = self.pagesize
        self.selected_workshop = get_object_or_404(Workshop, workshop_id=workshop_id)

    # Function to create a footer and header on each page
    @staticmethod
    def _header_footer(canvas, doc, header):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + 2*h)

        # # Footer
        # footer = Paragraph('This is a multi-line footer.  It goes on every page.   ', styles['Normal'])
        # w, h = footer.wrap(doc.width, doc.bottomMargin)
        # footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    # function to print 
    def print_users(self):
        buffer = self.buffer

        # Get all the values for the information we want to print on the PDF
        workshop = self.selected_workshop
        # Get all the questions answered of the workshop
        selected_setting = get_object_or_404(Setting, workshop_id=workshop.workshop_id)
        if selected_setting.setting == "langzeitstationär":
            question_care = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="care")
            question_technology = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="technology")
            question_embedding = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="embedding")
            question_law = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="law")
            question_ethics = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="ethics")
            question_economy = LangPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="economy")
        elif selected_setting.setting == "akutstationär":
            question_care = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="care")
            question_technology = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="technology")
            question_embedding = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="embedding")
            question_law = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="law")
            question_ethics = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="ethics")
            question_economy = AkuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="economy")
        else: 
            question_care = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="care")
            question_technology = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="technology")
            question_embedding = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="embedding")
            question_law = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="law")
            question_ethics = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="ethics")
            question_economy = AmbuPoll_Answer.objects.filter(workshop_id=workshop.workshop_id, category="economy")
        saved_roles = Roles.objects.filter(workshop_id=workshop.workshop_id)

        doc = SimpleDocTemplate(buffer,
                                rightMargin= 2.5*cm,
                                leftMargin= 2.5*cm,
                                topMargin= 2.5*cm,
                                bottomMargin= 2.5*cm,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='LeftAlign', alignment=TA_LEFT)) 

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        date = workshop.workshop_date
        elements.append(Paragraph("Ergebnis des Workshops " + workshop.workshop_name + " mit Datum " + date.strftime('%m.%d.%Y'), styles['Heading1']))
        elements.append(Spacer(1, 1*cm)) # Introduce spaces between the elements

        # ------------------ PARTICIPANTS TABLE ------------------
        elements.append(Paragraph("Liste der Teilnehmer*innen", styles['Heading1']))
        elements.append(Spacer(1, 1*cm))

        # Text to indicate if all the participants were present
        elements.append(Paragraph("Bitte beachten Sie, dass falls nicht aus allen erforderlichen Personengruppen mindestens eine Person an dem Workshop teilgenommen hat, wichtige Perspektiven für die Meinungsbildung fehlen.", styles['LeftAlign']))
        elements.append(Spacer(1, 1*cm))

        # Need a place to store our table rows
        title_role = Paragraph('''<b> Teilnehmende </b>''', styles["Normal"])
        title_name = Paragraph('''<b> Name </b>''', styles["Normal"])


        table_data_roles = [[title_role, title_name]] # Heather of table, only once

        try:
            for j, saved_roles in enumerate(saved_roles):
                # Add a row to the table
                pdf_role = Paragraph(saved_roles.role, styles["Normal"])
                pdf_name = Paragraph(saved_roles.names, styles["Normal"])
                table_data_roles.append([pdf_role, pdf_name])
        except:
            pass
        # Create the table
        roles_table = Table(table_data_roles, colWidths=[doc.width/2.0]*2)
        roles_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(roles_table)
        elements.append(Spacer(1, 1*cm))


        # ------------------ DISCUSSION SECTION ------------------
        elements.append(Paragraph("Diskussionsergebnisse", styles['Heading1']))
        elements.append(Spacer(1, 1*cm))

        # Introductory text for the result of the questions
        elements.append(Paragraph("„Robotik für die Pflege. Eine Option für unseren Dienst/ unsere Einrichtung?“ Mit dieser Frage haben Sie sich als Team im Rahmen des Workshops anhand der Bereiche Pflege, Technik und Infrastruktur, Institutionelle und gesellschaftliche Einbettung, Datenschutz und Recht, Ethik sowie Ökonomie intensiv auseinandergesetzt. Zu folgenden Ergebnissen sind Sie im Laufe der Diskussion gekommen: ", styles['LeftAlign']))
        elements.append(Spacer(1, 1*cm))

        # ------------------ RADAR CHART ------------------------------

        # Radar chart with the overview of the question's answers
        elements.append(Paragraph("1. Übersicht Ihrer Ergebnisse als Diagramm", styles['Heading2']))
        elements.append( QuickPieChart02(workshop.workshop_id) )
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("„Anteil der Fragen, bei denen kein weiterer Diskussionsbedarf hinsichtlich der (möglichen) Einführung von Robotik in dem Dienst / der Einrichtung besteht. Bei manchen Fragen ergeben sich Hinweise,  die bei einer (möglichen) Umsetzung zu beachten sind. Fragen, die im Ampelsystem der Farbe Grün zugeordnet wurden, wurden mit dem Faktor 1 gewichtet, Fragen denen die Ampelfarbe Gelb zugeordnet wurde, wurden mit 0,5 gewichtet.", styles['LeftAlign']))
        elements.append(Spacer(1, 1*cm))


        # ------------------ ANSWERED QUESTIONS TABLE ------------------
        # Table for care questions
        elements.append(Paragraph("2. Tabellarische Übersicht Ihrer Ergebnisse", styles['Heading2']))
        elements.append(Spacer(1, 1*cm))

        elements.append(Paragraph("Tabellenlegende", styles['Heading4']))
        
        elements.append(Paragraph('''<font color='green'> Grün: </font>''' "Fragen, die im Hinblick auf einen (möglichen) Einsatz von Robotik nicht mehr weiter diskutiert  werden müssen.", styles["Normal"], bulletText='-'))
        elements.append(Paragraph('''<font color='orange'>Gelb: </font>''' "Fragen, die im Hinblick auf einen (möglichen) Einsatz von Robotik nicht mehr weiter diskutiert werden müssen, bei deren tatsächlichen Einführung aber wichtige Aspekte zu berücksichtigen sind.", styles["Normal"], bulletText='-'))
        elements.append(Paragraph('''<font color='red'>Rot: </font>''' "Fragen, die im Hinblick auf einen (möglichen) Einsatz von Robotik auf jeden Fall in dem Dienst/ der Einrichtung nochmals diskutiert  bzw. bei denen die entsprechenden Rahmenbedingungen für den Einsatz zuerst geschaffen werden müssen.", styles["Normal"], bulletText='-'))

        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.1. Pflege", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 
     
        try:
            # First we order the elements on the list of questions in care
            final_list_question_care = []
            list_question_care = list(question_care)

            while list_question_care:
                minimum_element = list_question_care[0]

                for question_care in list_question_care: 
                    if question_care.id < minimum_element.id:
                        minimum_element = question_care
                final_list_question_care.append(minimum_element)
                list_question_care.remove(minimum_element)

            # We add the ordered answers to a table
            for i, question_care in enumerate(final_list_question_care):
                # Add a row to the table
                pdf_question = Paragraph(question_care.question, styles["Normal"])

                if question_care.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_care.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_care.comment_unless == "":
                    pdf_comment = Paragraph(question_care.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_care.comment + " Folgende Bedingungen müssten für einen Einsatz erfüllt sein " + question_care.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass

        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        
        elements.append(question_table)

        # Table for technology questions
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.2. Technik & Infrastruktur", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 
     
        try:
            # First we order the elements on the list of questions in care
            final_list_question_technology = []
            list_question_technology = list(question_technology)

            while list_question_technology:
                minimum_element = list_question_technology[0]

                for question_technology in list_question_technology: 
                    if question_technology.id < minimum_element.id:
                        minimum_element = question_technology
                final_list_question_technology.append(minimum_element)
                list_question_technology.remove(minimum_element)

            # We add the ordered answers to a table  
              
            for i, question_technology in enumerate(final_list_question_technology):
                # Add a row to the table
                pdf_question = Paragraph(question_technology.question, styles["Normal"])

                if question_technology.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_technology.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_technology.comment_unless == "":
                    pdf_comment = Paragraph(question_technology.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_technology.comment + " es sei denn " + question_technology.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass
        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        elements.append(question_table)

        # Table for embedding questions
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.3. Institutionelle & gesellschaftliche Einbettung", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 

        try:
            # First we order the elements on the list of questions in care
            final_list_question_embedding = []
            list_question_embedding = list(question_embedding)

            while list_question_embedding:
                minimum_element = list_question_embedding[0]

                for question_embedding in list_question_embedding: 
                    if question_embedding.id < minimum_element.id:
                        minimum_element = question_embedding
                final_list_question_embedding.append(minimum_element)
                list_question_embedding.remove(minimum_element)

            # We add the ordered answers to a table  

            for i, question_embedding in enumerate(final_list_question_embedding):
                # Add a row to the table
                pdf_question = Paragraph(question_embedding.question, styles["Normal"])
                
                if question_embedding.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_embedding.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_embedding.comment_unless == "":
                    pdf_comment = Paragraph(question_embedding.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_embedding.comment + " es sei denn " + question_embedding.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass
        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        elements.append(question_table)

        # Table for law questions
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.4. Datenschutz & Recht", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 
     
        try:
            # First we order the elements on the list of questions in care
            final_list_question_law = []
            list_question_law = list(question_law)

            while list_question_law:
                minimum_element = list_question_law[0]

                for question_law in list_question_law: 
                    if question_law.id < minimum_element.id:
                        minimum_element = question_law
                final_list_question_law.append(minimum_element)
                list_question_law.remove(minimum_element)

            # We add the ordered answers to a table  

            for i, question_law in enumerate(final_list_question_law):
                # Add a row to the table
                pdf_question = Paragraph(question_law.question, styles["Normal"])
                
                if question_law.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_law.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_law.comment_unless == "":
                    pdf_comment = Paragraph(question_law.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_law.comment + " es sei denn " + question_law.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass
        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        elements.append(question_table)

        # Table for ethics questions
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.5. Ethik", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 
     
        try:
            # First we order the elements on the list of questions in care
            final_list_question_ethics = []
            list_question_ethics = list(question_ethics)

            while list_question_ethics:
                minimum_element = list_question_ethics[0]

                for question_ethics in list_question_ethics: 
                    if question_ethics.id < minimum_element.id:
                        minimum_element = question_ethics
                final_list_question_ethics.append(minimum_element)
                list_question_ethics.remove(minimum_element)

            # We add the ordered answers to a table 

            for i, question_ethics in enumerate(final_list_question_ethics):
                # Add a row to the table
                pdf_question = Paragraph(question_ethics.question, styles["Normal"])
                
                if question_ethics.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_ethics.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_ethics.comment_unless == "":
                    pdf_comment = Paragraph(question_ethics.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_ethics.comment + " es sei denn " + question_ethics.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass
        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        elements.append(question_table)

        # Table for economy questions
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("2.6. Ökonomie", styles['Heading3']))
        elements.append(Spacer(1, 1*cm))
        
        # Need a place to store our table rows
        title_question = Paragraph('''<b> Frage </b>''', styles["Normal"])
        title_choice = Paragraph('''<b> Antwort </b>''', styles["Normal"])
        title_comment = Paragraph('''<b> Kommentar </b>''', styles["Normal"])
       
        table_data_question = [[title_question, title_choice, title_comment]] # Heather of table, only once 
     
        try:
            # First we order the elements on the list of questions in care
            final_list_question_economy = []
            list_question_economy = list(question_economy)

            while list_question_economy:
                minimum_element = list_question_economy[0]

                for question_economy in list_question_economy: 
                    if question_economy.id < minimum_element.id:
                        minimum_element = question_economy
                final_list_question_economy.append(minimum_element)
                list_question_economy.remove(minimum_element)

            # We add the ordered answers to a table 

            for i, question_economy in enumerate(final_list_question_economy):
                # Add a row to the table
                pdf_question = Paragraph(question_economy.question, styles["Normal"])
                
                if question_economy.choice == "Ja":
                    pdf_choice = Paragraph("Wir haben keinen Diskussionsbedarf", styles["Normal"])
                elif question_economy.choice == "Ja_aber":
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung geben wir folgenden Hinweis", styles["Normal"])
                else:
                    pdf_choice = Paragraph("In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil", styles["Normal"])

                if question_economy.comment_unless == "":
                    pdf_comment = Paragraph(question_economy.comment, styles["Normal"])
                else:
                    pdf_comment = Paragraph(question_economy.comment + " es sei denn " + question_economy.comment_unless, styles["Normal"])

                table_data_question.append([pdf_question, pdf_choice, pdf_comment]) 
        except:
            pass
        # Create the table
        question_table = Table(table_data_question, colWidths=[doc.width/3.0]*3)
        table_style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),])
        
        # Color each row of the table according to the value of the selected answer
        for row, values in enumerate(table_data_question):
            for column, value in enumerate(values):
                if value.text == "Wir haben keinen Diskussionsbedarf":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#90ee90'))
                elif value.text == "In Bezug auf die Fragestellung geben wir folgenden Hinweis":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#FFD580'))
                elif value.text == "In Bezug auf die Fragestellung ist der Einsatz robotischer Systeme nicht möglich, weil":
                    table_style.add('BACKGROUND',(column-1,row),(column+1,row), HexColor('#ffcccb'))
                else:
                    pass

        question_table.setStyle(table_style)
        elements.append(question_table)

        # Text for the heather
        header_content =  Paragraph(workshop.workshop_name + " " + date.strftime('%m.%d.%Y'), styles['Normal'])

        doc.build(elements, onLaterPages=partial(self._header_footer, header = header_content), canvasmaker=NumberedCanvas)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
