from reportlab.lib.pagesizes import A4 
import subprocess
import sys, os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
 
 
########################################################################
class LetterMaker(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, pdf_file, org, seconds):
        self.c = canvas.Canvas(pdf_file, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4 
        self.organization = org
        self.seconds  = seconds
 
 
    #----------------------------------------------------------------------
    def createDocument(self):
        """"""
        voffset = 25
 
        # create return address
        address = """<font size="11">
        Islami Bank Bangladesh Limited<br/>
        Zonal Office, Khulna<br/>
        Galls, TX 75081-4016</font>
        """
        p = Paragraph(address, self.styles["Normal"])
 
        # add a logo and size it
        logo = Image(r"d:\workspace\prj_klnz\ibbl.jpg")
        logo.drawHeight = 0.5*inch
        logo.drawWidth = 0.5*inch
##        logo.wrapOn(self.c, self.width, self.height)
##        logo.drawOn(self.c, *self.coord(140, 60, mm))
##

        data = [[logo, p]]
        table = Table(data, colWidths=5*inch)
        table.setStyle([("VALIGN", (0,0), (0,0), "TOP")])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(8, 20, mm))
 
        # insert body of letter
        ptext = "Dear Sir or Madam:"
        self.createParagraph(ptext, 10, voffset+30)
 
        ptext = """
        The document you are holding is a set of requirements for your next mission, should you
        choose to accept it. In any event, this document will self-destruct <b>%s</b> seconds after you
        read it. Yes, <b>%s</b> can tell when you're done...usually.
        """ % (self.seconds, self.organization)
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.c, self.width-70, self.height)
        p.drawOn(self.c, *self.coord(10, voffset+40, mm))
 
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y    
 
    #----------------------------------------------------------------------
    def createParagraph(self, ptext, x, y, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))
 
    #----------------------------------------------------------------------
    def savePDF(self):
        """"""
        self.c.save()   
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    doc = LetterMaker("example.pdf", "IBBL", 10)
    doc.createDocument()
    doc.savePDF()
    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", "example.pdf"])
    else:
        os.system("start " + "example.pdf")
        
