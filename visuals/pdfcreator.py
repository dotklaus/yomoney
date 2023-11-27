
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

class PdfCreator:
    def __init__(self, filename_p):
        self.pdfFilename = filename_p
        self.pdfCanvas = canvas.Canvas(filename_p, pagesize=landscape(A4))

    def Finalize(self):
        self.pdfCanvas.save()

    def Add_Page(self):
        self.pdfCanvas.showPage()

    def Save_Current_Figure_To_Pdf(self):

        currentFigure = plt.gcf()

        # Set the figure size to match A4 landscape
        a4_width_mm = 0.7 * 297
        a4_height_mm = 0.7 * 210
        a4_width_inches = a4_width_mm / 25.4
        a4_height_inches = a4_height_mm / 25.4
        fig_size = (a4_width_inches, a4_height_inches)
        # plt.gcf().set_size_inches(fig_size)
        currentFigure.set_size_inches(fig_size)
        
        imgdata = BytesIO()
        currentFigure.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data

        drawing=svg2rlg(imgdata)
        
        # Save the PDF file
        renderPDF.draw(drawing, self.pdfCanvas, 10, 40)
