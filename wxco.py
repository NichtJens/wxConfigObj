#!/usr/bin/env python

import wx
import configobj
import argparse

from wx.lib.scrolledpanel import ScrolledPanel


def _remove_duplicates(iterable):
    seen = set()
    return [i for i in iterable if not (i in seen or seen.add(i))]

def _move_to_front(item, iterable):
    if item in iterable:
        iterable.remove(item)
    iterable = [item] + iterable
    return iterable


class wxConfigObj(wx.Dialog):

    def __init__(self, iniFile):
        self.config = configobj.ConfigObj(iniFile)

        title = "{} - {}".format(iniFile, type(self).__name__)
        wx.Dialog.__init__(self, None, wx.ID_ANY, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        bxsSizer = self.mkBoxes()
        btnSizer = self.mkButtons()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bxsSizer, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.SetSizer(mainSizer)
        self.ShowModal()


    def mkBoxes(self):
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)

        scroll = ScrolledPanel(self)
        sizer = wx.FlexGridSizer(len(self.config), 2)
        sizer.AddGrowableCol(1)

        for key, value in self.config.items():
            lbl = wx.StaticText(scroll, label=key)
            lbl.SetFont(font)
            sizer.Add(lbl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

            if isinstance(value, list):
                inp = wx.ComboBox(scroll, name=key, value=value[0], choices=value)
            else:
                inp = wx.TextCtrl(scroll, name=key, value=value)

            sizer.Add(inp, 0, wx.ALL|wx.EXPAND, 5)

        scroll.SetSizer(sizer)
        scroll.SetupScrolling()
        return scroll


    def mkButtons(self):
        sizer = wx.StdDialogButtonSizer()

        saveBtn = wx.Button(self, wx.ID_SAVE)
        saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        sizer.AddButton(saveBtn)

        cancelBtn = wx.Button(self, wx.ID_CANCEL)
        sizer.AddButton(cancelBtn)

        sizer.Realize()
        return sizer


    def onSave(self, event):
        for key in self.config:
            inp = wx.FindWindowByName(key)
            if isinstance(inp, wx.ComboBox):
                selection = inp.GetValue()
                value = inp.GetItems()
                value = _remove_duplicates(value)
                value = _move_to_front(selection, value)
            else:
                value = inp.GetValue()

            self.config[key] = value
        self.config.write()
        self.EndModal(0)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file", help="name of the .ini file", nargs='?', default="config.ini")
    args = parser.parse_args()

    app = wx.App()
    wxConfigObj(args.file)



