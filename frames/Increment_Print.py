from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
import subprocess
import sys, os
import db_conn

class Increment_Print:

    def __init__(self, print_date):
        self.c = canvas.Canvas("increment_sanction.pdf", pagesize=A4)

        #Database Connection and pull Data from the Table
        conn = db_conn.Connection().connect()
        cursor = conn.cursor()
        cursor.execute("SELECT t1.id, t1.emp_id, t1.name, t2.designation, \
        t3.branch_name, t1.increment_amt, strftime('%d-%m-%Y', t1.wef) AS wef, \
        t1.present_basic, t1.gender, strftime('%d-%m-%Y', t1.print_date) AS \
        print_date, t3.manager_desig, t3.district, t2.scale FROM tbl_increment \
        t1 INNER JOIN tbl_pay_scale t2 ON t1.designation = t2.id INNER JOIN \
        tbl_manager_desig t3 ON t3.id = t1.posting_place WHERE t1.print_date \
        ='" + print_date + "'")
        self.rows = cursor.fetchall()
        conn.close()

    def Main_Body(self):
        self.top_y_pos = 797
        self.width, self.height = A4
        self.left_margin = 50
        self.c.drawImage(os.path.join(db_conn.img_dir, "bn_ibbl.jpg"), self.left_margin + 180, self.top_y_pos, 180, 19)
        self.c.drawImage(os.path.join(db_conn.img_dir, "ibbl.jpg"), self.left_margin + 141, self.top_y_pos - 15, 35, 35)
        self.c.setFont("Helvetica", 14)
        self.top_y_pos -= 15
        self.c.drawImage(os.path.join(db_conn.img_dir, "ar_ibbl.jpg"), self.left_margin + 180, self.top_y_pos, 180, 19)
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

        self.c.setFont("Helvetica", 11)
        self.top_y_pos -= 15
        cur_year = str(int(self.print_date[-4:]))
        self.c.drawString(self.left_margin, self.top_y_pos, "Ref.IBBL/ZO/KLN/Incre-" + cur_year + "/ID-" + self.emp_id + "/")
        self.c.drawString(self.left_margin + 437, self.top_y_pos, "Date: " + self.print_date)

        self.top_y_pos -= 77
        if not "Jb." in self.name:
            self.name = "Jb. " + self.name if self.gender != 'F' else self.name
        address = """
        <font size=11><b>%s</b> <br/>
        %s<br/>
        Islami Bank Bangladesh Limited <br/>
        %s<br/>
        %s</font>""" % (self.name, self.designation, self.branch_name, self.district)
        styles = getSampleStyleSheet()
        p = Paragraph(address, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 27
        # create return address
        subject = """
        <font size=13><b>Sub: <u>Annual Increment.</u></b> <br/></font>
        """
        styles = getSampleStyleSheet()
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin + 200, self.top_y_pos)

        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Muhtaram,")
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Assalamu Alaikum.")

        self.top_y_pos -= 57 
        ptext = """
        <font size=11>We are pleased to sanction you an Annual Increment of Tk. %s/- per month with effect from 
        %s in the scale of pay of %s raising your basic pay from Tk. %s/- to Tk. %s/- only together with other admissible
        allowance in the grade.</font>""" % (self.increment_amt, self.wef, self.scale, self.present_basic, self.new_basic) 

        styles = getSampleStyleSheet()
        style = styles["Normal"]
        ps = ParagraphStyle("title", alignment=TA_JUSTIFY, leading=17)
        p = Paragraph(ptext, ps) 
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        next_year = str(int(self.wef[-4:]) + 1)
        next_incr_date = str(self.wef[:-4]) + next_year
        self.top_y_pos -= 27
        styles = getSampleStyleSheet()
        subject = """<font size=11>
        Your next Annual Increment will fall due on <b><u>%s.</u></b> <br/> </font>""" % next_incr_date
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 10
        self.c.drawString(self.left_margin, self.top_y_pos, "Ma-assalam.")
        self.top_y_pos -= 17
        self.c.drawString(self.left_margin, self.top_y_pos, "Yours faithfully,")
        self.top_y_pos -= 17

    def CC_Footer(self):
        self.c.drawString(self.left_margin + 20, self.top_y_pos, "Sd/-")
        self.top_y_pos -= 17
        styles = getSampleStyleSheet()
        subject = """<font size=11>
        <b>(Abu Naser Mohammed Nazmul Bari)</b></font>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 17
        styles = getSampleStyleSheet()
        subject = """<font size=11>
        <u>EXECUTIVE VICE PRESIDENT & HEAD OF ZONE</u>
        </font>"""
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 110
        styles = getSampleStyleSheet()
        # self.branch_name = self.branch_name if "Zonal" in self.branch_name else self.branch_name + " Branch"
        subject = """
        <font size=7><u>Copy forwarded for kind information to:</u><br/>
        i.   The Executive Vice President, HRD, IBBL, HO, Dhaka<br/>
        ii.  The Executive Vice President, FAD, IBBL, HO, Dhaka<br/>
        iii. The %s, IBBL, %s, %s <br/>
        iv.  Personal File <br/><br/><br/><br/></font>
        <u>EXECUTIVE VICE PRESIDENT & HEAD OF ZONE</u>
        """ % (self.manager_desig, self.branch_name, self.district)
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 290
        self.c.line(self.left_margin, self.top_y_pos, 570, self.top_y_pos)

        self.c.setFont("Helvetica", 5)
        self.top_y_pos -= 10
        self.c.drawString(self.left_margin + 157, self.top_y_pos, "Fax: 041-722988 Phone: 041-723941 PABX: 041-720688 Mobile: 01711-437411 email: khulnazone@islamibankbd.com")
        self.c.showPage()
        self.c.save()

    def Main_Footer(self):
        self.top_y_pos -= 37
        styles = getSampleStyleSheet()
        subject = """
        <b>(Abu Naser Mohammed Nazmul Bari)</b>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 10
        styles = getSampleStyleSheet()
        subject = """
        <u>EXECUTIVE VICE PRESIDENT & HEAD OF ZONE</u>
        """
        p = Paragraph(subject, styles["Normal"])
        p.wrapOn(self.c, self.width-60, self.height)
        p.drawOn(self.c, self.left_margin, self.top_y_pos)

        self.top_y_pos -= 380
        self.c.line(self.left_margin, self.top_y_pos, 570, self.top_y_pos)

        self.c.setFont("Helvetica", 5)
        self.top_y_pos -= 10
        self.c.drawString(self.left_margin + 157, self.top_y_pos, "Fax: 041-722988 Phone: 041-723941 PABX: 041-720688 Mobile: 01711-437411 email: khulnazone@islamibankbd.com")
        self.c.showPage()
        self.c.save()

if __name__ == '__main__':
    incr = Increment_Print('2016-02-21')
    for i in incr.rows:
        incr.emp_id = i[1]
        incr.name = i[2]
        incr.designation = i[3]
        incr.branch_name = i[4]
        incr.increment_amt = "{:,}".format(int(i[5]))
        incr.wef = i[6]
        incr.present_basic = "{:,}".format(int(i[7]))
        incr.new_basic = "{:,}".format(int(i[5] + i[7]))
        incr.gender = i[8]
        incr.print_date = i[9]
        incr.manager_desig = i[10]
        incr.district = i[11]
        incr.scale = i[12]
        incr.Main_Body()
        incr.CC_Footer()
        incr.Main_Body()
        incr.Main_Footer()

    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", "increment_sanction.pdf"])
    else:
        os.system("start " + "increment_sanction.pdf")
