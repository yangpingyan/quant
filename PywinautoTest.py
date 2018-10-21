# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:12:55 2018

@author: ypy
"""

from pywinauto.application import Application

app = application.Application()

app.start(r"notepad.exe")
app['无标题 - 记事本'].wait('ready')
app['无标题 - 记事本'].print_control_identifiers()
app['无标题 - 记事本'].menu_select("文件->页面设置")

# describe the window inside Notepad.exe process
#dlg_spec = app['无标题 - 记事本']
#dlg_spec = app.window(title='无标题 - 记事本')
#dlg_spec = app.window(best_match='无标题 - 记事本')

#app[u'your dlg title'][u'your ctrl title']
#app['dialog_ident']['control_ident'].click()
#
# wait till the window is really open


#app['无标题 - 记事本'].menu_select("帮助->关于记事本")
#dlg_spec = app.window(title='Untitled - Notepad')


#app['页面设置'].print_control_identifiers()
app['页面设置']['确定'].click()
app['无标题 - 记事本'].menu_select("文件->退出")
#app[u'无标题 - 记事本'][u'关于“记事本”'].print_control_identifiers()
#dlg_spec.Edit.type_keys("pywinauto Works!", with_spaces = True)


print("Mission complete")