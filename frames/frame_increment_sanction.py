import wx
import db_conn
import TextCtrlAutoComplete as tcac
import wx.grid
from common import is_number
import Increment_Print
import os, sys
import subprocess


class EditPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        box = wx.StaticBox(self, wx.ID_ANY, "Increment Sanction")

        self.editSizer = wx.GridBagSizer(hgap=27, vgap=4)

        self.lbl_id = wx.StaticText(self, label="ID")
        self.txt_id = wx.TextCtrl(self, value="", style=wx.TE_READONLY)
        self.editSizer.Add(self.lbl_id, pos=(0, 0))
        self.editSizer.Add(self.txt_id, pos=(0, 1))

        self.lbl_emp_id = wx.StaticText(self, label="Employee ID")
        self.txt_emp_id = wx.TextCtrl(self, value="")
        self.editSizer.Add(self.lbl_emp_id, pos=(1, 0))
        self.editSizer.Add(self.txt_emp_id, pos=(1, 1))

        self.lbl_name = wx.StaticText(self, label="Name")
        self.txt_name = wx.TextCtrl(self, value="", size=(290, 30))
        self.editSizer.Add(self.lbl_name, pos=(2, 0))
        self.editSizer.Add(self.txt_name, pos=(2, 1))

        self.lbl_designation = wx.StaticText(self, label="Designation")
        self.designation = tcac.ComboData().data_import("tbl_pay_scale", "id", "designation")
        self.cbo_designation = tcac.TextCtrlAutoComplete(self, choices=self.designation.values(), size=(200, 30))

        self.editSizer.Add(self.lbl_designation, pos=(3, 0))
        self.editSizer.Add(self.cbo_designation, pos=(3, 1))

        self.lbl_posting = wx.StaticText(self, label="Place of Posting")
        self.posting = tcac.ComboData().data_import("tbl_manager_desig", "id", "branch_name")
        self.cbo_posting = tcac.TextCtrlAutoComplete(self, choices=self.posting.values(), size=(200, 30))

        self.editSizer.Add(self.lbl_posting, pos=(4, 0))
        self.editSizer.Add(self.cbo_posting, pos=(4, 1))

        self.lbl_incre_amt = wx.StaticText(self, label="Increment Amount")
        self.txt_incre_amt = wx.TextCtrl(self, value="", size=(90, 30))
        self.editSizer.Add(self.lbl_incre_amt, pos=(5, 0))
        self.editSizer.Add(self.txt_incre_amt, pos=(5, 1))

        self.lbl_wef = wx.StaticText(self, label="Increment Date(m/d/yyyy)")
        self.dpc_incre_date = wx.DatePickerCtrl(self, size=(130, -1))
        self.editSizer.Add(self.lbl_wef, pos=(6, 0))
        self.editSizer.Add(self.dpc_incre_date, pos=(6, 1))

        self.lbl_present_basic = wx.StaticText(self, label="Present Basic")
        self.txt_present_basic = wx.TextCtrl(self, value="", size=(90, 30))
        self.editSizer.Add(self.lbl_present_basic, pos=(7, 0))
        self.editSizer.Add(self.txt_present_basic, pos=(7, 1))

        self.lbl_gender = wx.StaticText(self, label="Female")
        self.chk_box_gender = wx.CheckBox(self)
        self.editSizer.Add(self.lbl_gender, pos=(8, 0))
        self.editSizer.Add(self.chk_box_gender, pos=(8, 1))

        self.lbl_print_date = wx.StaticText(self, label="Print Date(m/d/yyyy)")
        self.dpc_print_date = wx.DatePickerCtrl(self, size=(130, -1))
        self.editSizer.Add(self.lbl_print_date, pos=(9, 0))
        self.editSizer.Add(self.dpc_print_date, pos=(9, 1))

        self.SaveBtn = wx.Button(self, label="&Save")
        self.UpdateBtn = wx.Button(self, label="&Update")
        self.DeleteBtn = wx.Button(self, label="&Delete")
        self.ClearBtn = wx.Button(self, label="&Clear")
        self.PrintBtn = wx.Button(self, label="&Print")
        self.ExitBtn = wx.Button(self, label="E&xit")

        self.SaveBtn.Bind(wx.EVT_BUTTON, self.SaveBtnClick)
        self.UpdateBtn.Bind(wx.EVT_BUTTON, self.UpdateButtonClick)
        self.ClearBtn.Bind(wx.EVT_BUTTON, self.ClearBtnClick)
        self.ExitBtn.Bind(wx.EVT_BUTTON, self.ExitButtonClick)
        self.PrintBtn.Bind(wx.EVT_BUTTON, self.PrintBtnClick)

        self.txt_name.Bind(wx.EVT_KILL_FOCUS, self.txt_name_KillFocus)
        self.cbo_designation.Bind(wx.EVT_KILL_FOCUS, self.CboDesignationKillFocus)
        self.cbo_posting.Bind(wx.EVT_KILL_FOCUS, self.CboPostingKillFocus)

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(self.SaveBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        Sizer.Add(self.UpdateBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        Sizer.Add(self.DeleteBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        Sizer.Add(self.ClearBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        Sizer.Add(self.PrintBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        Sizer.Add(self.ExitBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)

        self.vbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.vbox.Add(self.editSizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(Sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=30)

        self.SetSizerAndFit(self.vbox)
        self.txt_emp_id.SetFocus()

    def PrintBtnClick(self, event):
        incr = Increment_Print.Increment_Print(self.dpc_print_date.GetValue().Format("%Y-%m-%d"))
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

    def CboDesignationKillFocus(self, event):
        if not self.cbo_designation.GetValue().strip():
            pass
        else:
            if self.cbo_designation.GetValue() not in self.designation.values():
                wx.MessageBox("Invalid Data", "Please Enter Again", style=wx.ICON_EXCLAMATION|wx.STAY_ON_TOP)
                self.cbo_designation.SetValue("")
                self.cbo_designation.SetFocus()

    def CboPostingKillFocus(self, event):
        if not self.cbo_posting.GetValue().strip():
            pass
        else:
            if self.cbo_posting.GetValue() not in self.posting.values():
                wx.MessageBox("Invalid Data", "Please Enter Again", style=wx.ICON_EXCLAMATION|wx.STAY_ON_TOP)
                self.cbo_posting.SetValue("")
                self.cbo_posting.SetFocus()

    def txt_name_KillFocus(self, event):
        if len(self.txt_name.GetValue()) > 0:
            self.txt_name.SetValue(self.txt_name.GetValue().title())

    def ExitButtonClick(self, event):
#        self.GetParent().Enable(True)
        self.GetTopLevelParent().Close()

    def AutoGenID(self):
        conn = db_conn.Connection().connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) AS max_id FROM tbl_increment")

        last_id = 0
        exist = cursor.fetchone()
        if 'None' in str(exist):
            last_id = 0
        else:
            for row in exist:
                last_id = int(row[1:])
        cur_id = last_id + 1
        if cur_id < 10:
            return "I0000" + str(cur_id)
        elif cur_id < 100:
            return "I000" + str(cur_id)
        elif cur_id < 1000:
            return "I00" + str(cur_id)
        elif cur_id < 10000:
            return "I0" + str(cur_id)
        elif cur_id < 100000:
            return "I" + str(cur_id)
        else:
            return "I000001"

    def ValidateData(self):
        if not self.txt_emp_id.GetValue().strip():
            self.txt_emp_id.SetFocus()
            return "Employee ID is required"
        elif not self.txt_name.GetValue().strip():
            self.txt_name.SetFocus()
            return "Employee Name is required"
        elif not self.cbo_designation.GetValue().strip():
            self.cbo_designation.SetFocus()
            return "Designation is required"
        elif not self.cbo_posting.GetValue().strip():
            self.cbo_posting.SetFocus()
            return "Posting Place is required"
        elif not self.txt_incre_amt.GetValue().strip():
            self.txt_incre_amt.SetFocus()
            return "Increment is required"
        elif not self.dpc_incre_date.GetValue():
            self.dpc_incre_date.SetFocus()
            return "Increment Date is required"
        elif not self.txt_present_basic.GetValue().strip():
            self.txt_present_basic.SetFocus()
            return "Present Basic is required"
        elif not self.dpc_print_date.GetValue():
            self.dpc_print_date.SetFocus()
            return "Print date is required"
        elif self.cbo_designation.GetValue() not in self.designation.values():
            self.cbo_designation.SetValue("")
            self.cbo_designation.SetFocus()
            return "Designation is not correct"
        elif self.cbo_posting.GetValue() not in self.posting.values():
            self.cbo_posting.SetValue("")
            self.cbo_posting.SetFocus()
            return "Posting is not Correct"
        elif not is_number(self.txt_emp_id.GetValue().strip()):
            self.txt_emp_id.SetValue("")
            self.txt_emp_id.SetFocus()
            return "Employee ID is not Numeric"
        elif not  is_number(self.txt_incre_amt.GetValue().strip()):
            self.txt_incre_amt.SetValue("")
            self.txt_incre_amt.SetFocus()
            return "Increment is not Numeric"
        elif not is_number(self.txt_present_basic.GetValue().strip()):
            self.txt_present_basic.SetValue("")
            self.txt_present_basic.SetFocus()
            return "Present Basic is not Numeric"
        else:
            return "valid"

    def SaveBtnClick(self, event):
        valid_msg = self.ValidateData()

        #TODO: Use Python Database Library
        if valid_msg == "valid":
            try:
                conn = db_conn.Connection().connect()
                cursor = conn.cursor()
                wef = self.dpc_incre_date.GetValue().Format("%Y-%m-%d")
                pdate = self.dpc_print_date.GetValue().Format("%Y-%m-%d")
                gender = "F" if self.chk_box_gender.Value == True else "M"
                next_id = self.AutoGenID()
                desig_id = self.designation.keys()[self.designation.values().index(self.cbo_designation.GetValue())]
                post_id = self.posting.keys()[self.posting.values().index(self.cbo_posting.GetValue())]

                cursor.execute("INSERT INTO tbl_increment \
                VALUES ('" + next_id + "', '" + self.txt_emp_id.GetValue() + "', '" + \
                self.txt_name.GetValue() + "', '" + desig_id + "', '" + \
                post_id + "', '" + self.txt_incre_amt.GetValue() + "', '" + \
                wef  + "', '" + self.txt_present_basic.GetValue() + \
                "', '" + gender + "', '" + pdate + "')" );
                dlg = wx.MessageBox("Increment Saved", "Successful", style=wx.ICON_INFORMATION|wx.STAY_ON_TOP|wx.OK)
                conn.commit()
                conn.close()
                self.grid = self.TopLevelParent.notebook.tabTwo.increGrid
                self.grid.AppendRows(1)
                self.ClearField()
            except Exception as e:
                wx.MessageBox(e.message, "Error!")
        else:
            wx.MessageBox(valid_msg, "Information Missing!",
                          style=wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

    def UpdateButtonClick(self, event):
        valid_msg = self.ValidateData()
        #TODO: Use Python Database Library
        if valid_msg == "valid":
            try:
                conn = db_conn.Connection().connect()
                cursor = conn.cursor()
                wef = self.dpc_incre_date.Value.Format("%Y-%m-%d")
                pdate = self.dpc_print_date.Value.Format("%Y-%m-%d")
                gender = "F" if self.chk_box_gender.Value == True else "M"
                next_id = self.AutoGenID()
                desig_id = self.designation.keys()[self.designation.values().index(self.cbo_designation.Value)]
                post_id = self.posting.keys()[self.posting.values().index(self.cbo_posting.Value)]

                cursor.execute("UPDATE tbl_increment SET emp_id = ?, name = ?, designation = ?, posting_place = ?, increment_amt = ?, wef = ?, present_basic = ?, gender = ?, print_date = ? WHERE id = ?" , 
                               (self.txt_emp_id.Value, self.txt_name.Value, desig_id, post_id, self.txt_incre_amt.Value, wef, self.txt_present_basic.Value, gender, pdate, self.txt_id.Value))
                dlg = wx.MessageBox("Successful", "Increment Update", style=wx.ICON_INFORMATION|wx.STAY_ON_TOP|wx.OK)
                conn.commit()
                conn.close()
                self.grid = self.TopLevelParent.notebook.tabTwo.increGrid
                self.ClearField()
            except Exception as e:
                wx.MessageBox(e.message, "Error!")
        else:
            wx.MessageBox(valid_msg, "Information Missing!",
                          style=wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

    def ClearField(self):
        controls = self.editSizer.GetChildren()
        for ctrl in controls:
            widget = ctrl.GetWindow()
            if isinstance(widget, wx.TextCtrl):
                widget.Clear()
            elif isinstance(widget, wx.DatePickerCtrl):
                widget.SetValue(wx.DateTime_Now())
            elif isinstance(widget, wx.CheckBox):
                widget.SetValue(False)
        self.txt_emp_id.SetFocus()
        self.refreshData(self.grid)
        self.SaveBtn.Enable(True)
        self.UpdateBtn.Enable(False)
#        ViewPanel(self).refreshData()

    def ClearBtnClick(self, event):
        self.grid = self.TopLevelParent.notebook.tabTwo.increGrid
        self.ClearField()

    def refreshData(self, increGrid):
        conn = db_conn.Connection().connect()
        cursor = conn.cursor()
        cursor.execute("SELECT t1.id, t1.emp_id, t1.name, t2.designation, t3.branch_name, t1.increment_amt, strftime('%d-%m-%Y', t1.wef) AS wef, t1.present_basic, t1.gender, strftime('%d-%m-%Y', t1.print_date) AS print_date FROM tbl_increment t1 INNER JOIN tbl_pay_scale t2 ON t1.designation = t2.id INNER JOIN tbl_manager_desig t3 ON t3.id = t1.posting_place")
        rows = cursor.fetchall()
        for i in range(0, len(rows)):
            for j in range(0, 10):
                cell = rows[i]
                increGrid.SetCellValue(i, j, str(cell[j]))
                if j == 5 or j== 7:
                    increGrid.SetCellAlignment(i, j, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        conn.close()


class ViewPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)
        self.increGrid = wx.grid.Grid(self, -1, size=(700, 380))
        self.BtnLoad = wx.Button(self, label="Load")
        r = self.CountRow()
        self.increGrid.CreateGrid(r, 10)

        self.resizeGridColumn()
        self.refreshData()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.increGrid, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        sizer.Add(self.BtnLoad, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        self.SetSizerAndFit(sizer)

        self.BtnLoad.Bind(wx.EVT_BUTTON, self.increGridClick)
#        self.increGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.increGridClick)

    def increGridClick(self, event):
        try:
            row_index = self.increGrid.GetSelectedRows()[0]
#            row_ind = self.increGrid.GetSelectedCells()
            cell_value=[]
            for i in range(0, 10):
                cell_value.append(self.increGrid.GetCellValue(row_index, i))
            self.EditPanel = self.TopLevelParent.notebook.tabOne
            self.EditPanel.txt_id.Value = str(cell_value[0])
            self.EditPanel.txt_emp_id.Value = str(cell_value[1])
            self.EditPanel.txt_name.Value = str(cell_value[2])
            self.EditPanel.cbo_designation.Value = str(cell_value[3])
            self.EditPanel.cbo_designation._showDropDown(False)
            self.EditPanel.cbo_posting.Value = str(cell_value[4])
            self.EditPanel.cbo_posting._showDropDown(False)
            self.EditPanel.txt_incre_amt.Value = str(cell_value[5])
            self.EditPanel.txt_present_basic.Value = str(cell_value[7])
            if str(cell_value[8]) == "F":
                self.EditPanel.chk_box_gender.Value = True
            else:
                self.EditPanel.chk_box_gender.Value = False
            day, month, year = str(cell_value[6]).split('-')
            incr_date = wx.DateTimeFromDMY(int(day), int(month)-1, int(year))
            self.EditPanel.dpc_incre_date.Value = incr_date

            day, month, year = str(cell_value[9]).split('-')
            pr_date = wx.DateTimeFromDMY(int(day), int(month)-1, int(year))
            self.EditPanel.dpc_print_date.Value = pr_date

            self.EditPanel.SaveBtn.Enabled=False
            self.EditPanel.UpdateBtn.Enabled=True
            event.Skip()
            self.TopLevelParent.notebook.SetSelection(0)
            self.EditPanel.txt_emp_id.SetFocus()
        except IndexError:
            wx.MessageBox("You did not select any row to load")

    def refreshData(self):
        conn = db_conn.Connection().connect()
        cursor = conn.cursor()
        cursor.execute("SELECT t1.id, t1.emp_id, t1.name, t2.designation, t3.branch_name, t1.increment_amt, strftime('%d-%m-%Y', t1.wef) AS wef, t1.present_basic, t1.gender, strftime('%d-%m-%Y', t1.print_date) AS print_date FROM tbl_increment t1 INNER JOIN tbl_pay_scale t2 ON t1.designation = t2.id INNER JOIN tbl_manager_desig t3 ON t3.id = t1.posting_place")
        rows = cursor.fetchall()
        for i in range(0, len(rows)):
            for j in range(0, 10):
                cell = rows[i]
                self.increGrid.SetCellValue(i, j, str(cell[j]))
                if j == 5 or j== 7:
                    self.increGrid.SetCellAlignment(i, j, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        conn.close()
        self.increGrid.SetColMinimalAcceptableWidth(0)
        self.increGrid.SetColSize(0, 0)
        self.increGrid.SetColSize(5, 0)
        self.increGrid.SetColSize(7, 0)
        self.increGrid.SetColSize(8, 0)

    def resizeGridColumn(self):
        self.increGrid.SetColLabelValue(0, ("ID"))
        self.increGrid.SetColSize(0, 50)
        self.increGrid.SetColLabelValue(1, ("Emp_ID"))
        self.increGrid.SetColSize(1, 60)
        self.increGrid.SetColLabelValue(2, ("Name"))
        self.increGrid.SetColSize(2, 130)
        self.increGrid.SetColLabelValue(3, ("Designation"))
        self.increGrid.SetColSize(3, 90)
        self.increGrid.SetColLabelValue(4, ("Posting"))
        self.increGrid.SetColSize(4, 120)
        self.increGrid.SetColLabelValue(5, ("Increment"))
        self.increGrid.SetColSize(5, 80)
        self.increGrid.SetColLabelValue(6, ("wef"))
        self.increGrid.SetColSize(6, 85)
        self.increGrid.SetColLabelValue(7, ("Pr. Basic"))
        self.increGrid.SetColSize(7, 70)
        self.increGrid.SetColLabelValue(8, ("Gender"))
        self.increGrid.SetColSize(8, 60)
        self.increGrid.SetColLabelValue(9, ("Print Date"))
        self.increGrid.SetColSize(9, 85)

    def CountRow(self):
        conn = db_conn.Connection().connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_increment")
        rows = cursor.fetchall()
        i = 0
        for r in rows:
            i += 1
        return i
        conn.close()


class NoteBookIncrement(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_TOP, size=(700, 450))
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.tabOne = EditPanel(self)
        self.AddPage(self.tabOne, "Enter Data")
        self.sizer.Add(self.tabOne)

        self.tabTwo = ViewPanel(self)
        self.AddPage(self.tabTwo, "View Increment")
        self.sizer.Add(self.tabTwo)

        self.SetSizer(self.sizer)


class FrameIncrementSanction(wx.Frame):
    def __init__(self, parent, pid):
        wx.Frame.__init__(self, parent, pid, "Increment Sanction Register")
        self.notebook = NoteBookIncrement(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.notebook)
        self.SetSizerAndFit(self.sizer)
#        self.GetParent().Enable(False)
        self.Show()
        self.CenterOnScreen()
