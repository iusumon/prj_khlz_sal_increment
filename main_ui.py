#!/usr/bin/env python
import wx
import frames.frame_increment_sanction


class MainFrame(wx.MDIParentFrame):

    def __init__(self, parent, id):
        wx.MDIParentFrame.__init__(self, parent, id, "Zonal Office Resource Management")
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()

        menuItemIncrement = menu1.Append(wx.NewId(), "&Increment Sanction")
        menuItemExit = menu1.Append(wx.NewId(), "&Exit")

        menuItemAbout = menu2.Append(wx.ID_ANY, "About")

        menubar.Append(menu1, "&Main")
        menubar.Append(menu2, "&Help")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnCloseMe, menuItemExit)
        self.Bind(wx.EVT_MENU, self.OpenIncrementSanction, menuItemIncrement)

        self.Show()
        self.Maximize(True)

    def OnCloseMe(self, event):
        self.Close(True)

    def OpenIncrementSanction(self, event):
        frames.frame_increment_sanction.FrameIncrementSanction(self, -1)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, -1)
    app.MainLoop()
