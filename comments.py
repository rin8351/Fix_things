from tkinter import *
import os
from saving import PickClass, save_object

class Comms():
    def __init__(self, time_zan, tab4,table,comm):
        super().__init__()
        self.time_zan = time_zan
        self.comm = comm
        self.frame_com = Frame(tab4)
        self.frame_com.pack(anchor=W)
        self.table = table
        self.font = ("Verdana", 10)
        self.frame_com_left = Frame(self.frame_com)
        self.frame_com_left.pack(side=LEFT)
        self.frame_com_right = Frame(self.frame_com)
        self.frame_com_right.pack()
        self.update_comment()
        self.spis_comm()

    def update_comment(self):
        self.spisok3 = []
        for i in self.time_zan:
            for j in self.time_zan[i]:
                if '_d' not in j:
                    self.spisok3.append(j)
        self.variable4 = StringVar()
        self.variable4.set('Комментарий для занятия')
        if self.spisok3 == []:
            self.spisok3.append('Комментарий для занятия')
        self.w2 = OptionMenu(self.frame_com_left, self.variable4, *self.spisok3, command=self.comment_text)
        self.w2.config(font=self.font, bg='light blue',activebackground='light blue',width=22)
        self.w2.grid(row=2, column=1, padx=4, pady=4)
        self.text_com = Text(self.frame_com_left, width=40, height=10)
        self.text_com.grid(row=3, column=1, padx=4, pady=4)
        self.but_com = Button(self.frame_com_left, text="Сохранить",font=self.font, bg='#0076A3',fg='#ffffff',command=lambda: self.add_del_com("Сохранить"))
        self.but_com.grid(row=4, column=1, padx=4, pady=4)
        self.but_del_com = Button(self.frame_com_left, text="Удалить",font=self.font, bg='#0076A3',fg='#ffffff',command=lambda: self.add_del_com("Удалить"))
        self.but_del_com.grid(row=5, column=1, padx=4, pady=4)
        self.comm_error = Label(self.frame_com_left, text="", font=("Verdana", 12),fg='red')
        self.comm_error.grid(row=6, column=1, padx=4, pady=4)

    def add_del_com(self,text):
        if self.variable4.get() != 'Комментарий для занятия':
            if text == 'Сохранить':
                self.comm[self.variable4.get()] = self.text_com.get("1.0", END)
                self.comm[self.variable4.get()] = self.comm[self.variable4.get()][:-1]
            else:
                self.comm.pop(self.variable4.get())
            self.text_com.delete("1.0", END)
            save_object(PickClass(self.comm), 'comm.pickle')
            self.table()
            self.spis_comm()
        else:
            self.comm_error.config(text="Выберите занятие")

    def spis_comm(self):
        self.frame_com_right.destroy()
        self.frame_com_right = Frame(self.frame_com)
        self.frame_com_right.pack()
        lb_zan_witn_com = Label(self.frame_com_right, text="Занятия с комментариями", font=("Verdana", 12), bg='white',fg='#0076A3')
        lb_zan_witn_com.grid(row=2, column=1, padx=4, pady=4)
        x = 3
        for i in self.comm:
            lb_zan_witn_com = Label(self.frame_com_right, text=i, font=("Verdana", 12))
            lb_zan_witn_com.grid(row=x, column=1, padx=4, pady=4, sticky=W)
            x += 1

    def comment_text(self, event):
        name_button = self.variable4.get()
        if name_button in self.comm:
            self.text_com.delete('1.0', END)
            self.text_com.insert(END, self.comm[name_button])

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text

        def enter(event):
            self.showTooltip()
        def leave(event):
            self.hideTooltip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def showTooltip(self):
        self.tooltipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1) 
        tw.wm_geometry("+{}+{}".format(self.widget.winfo_rootx(), self.widget.winfo_rooty()))
        label = Label(tw, text = self.text, background = "#ffffe0", relief = 'solid', borderwidth = 1,font=("Verdana", 10)).pack()

    def hideTooltip(self):
        tw = self.tooltipwindow
        tw.destroy()
        self.tooltipwindow = None