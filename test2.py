from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
import os

class Increment_Print:

    def __init__(self):
        self.top_y_pos = 797
        self.c = canvas.Canvas("hello.pdf", pagesize=A4)

    def Main_Body(self):
        self.width, self.height = A4 
        self.left_margin = 50
        self.c.drawImage(r"d:\workspace\prj_klnz\bn_ibbl.jpg", self.left_margin + 180, self.top_y_pos, 180, 19)
        self.c.drawImage(r"d:\workspace\prj_klnz\ibbl.jpg", self.left_margin+141, self.top_y_pos - 15, 35, 35)
        self.c.setFont("Helvetica", 12)
        self.top_y_pos -= 15
        self.c.drawImage(r"d:\workspace\prj_klnz\ar_ibbl.jpg", self.left_margin + 180, self.top_y_pos, 180, 19)
        self.top_y_pos -= 10
        self.c.drawString(self.left_margin + 180, self.top_y_pos, "Islami Bank Bangladesh Limited")
        self.top_y_pos -= 15
        self.c.setFont("Helvetica", 10)
        self.c.drawString(self.left_margin + 210, self.top_y_pos, "Zonal Office, Khulna")
        self.top_y_pos -= 15
        self.c.setFont("Helvetica", 8)
        self.c.drawString(self.left_margin + 150, self.top_y_pos, "Khulna Shopping Complex, 4, Old Jessore Road, Khulna, Bangladesh")
        self.top_y_pos -= 7
        self.c.line(self.left_margin, self.top_y_pos, 570, self.top_y_pos)

        self.c.setFont("Helvetica", 10)
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Ref.IBBL/ZO/KLN/Incre-2015/ID-203051/")
        self.c.drawString(self.left_margin + 447, self.top_y_pos, "Date: 12.03.2016")

        self.top_y_pos -= 67
        styles = getSampleStyleSheet()
        # create return address
        address = """
        <b>Jb. Muhammad Moinuddin</b> <br/>
        Asstt. Officer Gr.-I<br/>
        Islami Bank Bangladesh Limited <br/>
        Zonal Office <br/>
        Khulna
        """
        p = Paragraph(address, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 27
        styles = getSampleStyleSheet()
        # create return address
        subject = """
        <b>Sub: <u>Annual Increment.</u></b> <br/>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin + 210, self.top_y_pos)

        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Muhtaram,")
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Assalamu Alaikum.")

        self.top_y_pos -= 47
        ptext = """
        We are pleased to sanction you an Annual Increment of Tk. 770/- per month with effect from
        14.10.2015 in the scale of pay of Tk.14,950-770x4-18,030-EB-840x6-23,070-910x3-25,800/-
        raising your basic pay from Tk. 15,720/- to Tk. 16,490/- only together with other admissible
        allowance in the grade.
        """ 
        styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT))
        p = Paragraph(ptext, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 17
        styles = getSampleStyleSheet()
        subject = """
        Your next Annual Increment will fall due on <b><u>14.10.2016</u></b> <br/>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Ma-assalam.")
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Yours faithfully,")
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin + 20, self.top_y_pos, "Sd/-")

        self.top_y_pos -= 17
        styles = getSampleStyleSheet()
        subject = """
        <b>(Abu Naser Mohammed Nazmul Bari)</b>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 17
        styles = getSampleStyleSheet()
        subject = """
        <u>EXECUTIVE VICE PRESIDENT & HEAD OF ZONE</u>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.CC_Footer()

        self.c.showPage()
        self.c.save()


    def CC_Footer(self):
        self.left_margin = 50
        self.top_y_pos -= 97
        styles = getSampleStyleSheet()
        subject = """
        <font size=7><u>Copy forwarded for kind information to:</u><br/>
        i.   The Executive Vice President, HRD, IBBL, HO, Dhaka<br/>
        ii.  The Executive Vice President, FAD, IBBL, HO, Dhaka<br/>
        iii. Personal File <br/><br/><br/><br/></font>
        <u>EXECUTIVE VICE PRESIDENT & HEAD OF ZONE</u>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 327
        self.c.line(self.left_margin, self.top_y_pos, 570, self.top_y_pos)

        self.c.setFont("Helvetica", 5)
        self.top_y_pos -= 10
        self.c.drawString(self.left_margin + 157, self.top_y_pos, "Fax: 041-722988 Phone: 041-723941 PABX: 041-720688 Mobile: 01711-437411 email: khulnazone@islamibankbd.com")


if __name__ == '__main__':
    incr = Increment_Print()
    incr.Main_Body()
    os.system("start " + "hello.pdf")
