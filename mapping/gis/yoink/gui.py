import os

import wx

from . import config


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        self.init_menus()

        self.Show(True)

    def init_menus(self):
        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        self.Bind(
            wx.EVT_MENU,
            self.on_open,
            filemenu.Append(
                wx.ID_OPEN,
                '&Open',
                'Open a config file'))

        self.Bind(
            wx.EVT_MENU,
            self.on_about,
            filemenu.Append(
                wx.ID_ABOUT,
                "&About",
                "Information about this program"))

        filemenu.AppendSeparator()

        self.Bind(
            wx.EVT_MENU,
            self.on_exit,
            filemenu.Append(
                wx.ID_EXIT,
                "E&xit",
                "Terminate the program"))

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

    def on_about(self, e):
        dlg = wx.MessageDialog(self, "An editor for yoink configurations.", "About yoink_conf", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)

    def on_open(self, e):
        dlg = wx.FileDialog(self, 'Choose a file', '', '', '*.*', wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            with config.Config(os.path.join(dirname, filename)) as c:
                self.control.SetValue(
                    '\n'.join([f.url for f in c.feeds.values()]))

        dlg.Destroy()


app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()