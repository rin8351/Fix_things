import os
from tkinter import *
from tkinter import ttk
import copy
from tkscrolledframe import ScrolledFrame
import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
from saving import PickClass, save_object, load_object
import static
import tkinter.scrolledtext as scrolledtext
import changes
import comments
import time
import cProfile 

class Time_fix:
    def __init__(self):
        start = time.time()
        print('start')
        self.image_dict = {}
        for file in os.listdir("image"):
            name = os.path.splitext(file)[0]
            self.image_dict[name] = ImageTk.PhotoImage(Image.open("image/" + file))

        tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Основное',image=self.image_dict['house'], compound=LEFT)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, text='Статистика',image=self.image_dict['grafik'], compound=LEFT)
        self.tab3 = ttk.Frame(tab_control)
        tab_control.add(self.tab3, text='Занятия',image=self.image_dict['spisok'], compound=LEFT)
        self.tab4 = ttk.Frame(tab_control)
        tab_control.add(self.tab4, text='Комментарии', image=self.image_dict['comm'], compound=LEFT)
        self.tab5 = ttk.Frame(tab_control)
        tab_control.add(self.tab5, text='Подробные дела',image=self.image_dict['podr'], compound=LEFT)
        tab6 = ttk.Frame(tab_control)
        tab_control.add(tab6, text='Настройки',image=self.image_dict['nastr'], compound=LEFT)
        tab_control.pack(expand=1, fill='both')
        self.s = ttk.Style()
        self.s.configure('TNotebook.Tab', font=('Verdana', 10, 'bold'))
        self.s.configure('TNotebook', relief='sunken ', borderwidth=0)
        self.save_for_undo = []

        self.frame_main = Frame(self.tab1)
        self.frame_main.pack(side=TOP, anchor=W)
        self.font = ("Verdana", 10)
        self.frame_main_left_outside = Frame(self.frame_main, bg='#0B275B')
        self.frame_main_left_outside.pack(side=LEFT)
        lb_type = Label(self.frame_main_left_outside, text='Занятие        Всё вр. Неделя', font=self.font, fg='white', height=2, width=35, bg='#0B275B')
        lb_type.pack(pady=4, padx=4)
        self.frame_main_right = Frame(self.frame_main)
        self.frame_main_right.pack(side=LEFT)
        self.frame_main_right2 = Frame(self.frame_main, width=200, height=200)
        self.frame_main_right2.pack(side=LEFT,fill=BOTH, expand=True)
        self.frame_main_left = Frame(self.frame_main_left_outside)
        self.frame_main_left.pack()
        self.frame_rf = Canvas(self.frame_main_right)
        self.frame_rf.pack()

        self.save_zap = []
        self.hom = self.exists_files('hom.pickle')
        self.time_zan = self.exists_files('archive.pickle')
        self.spisok_del = []
        for i in self.time_zan:
            self.spisok_del.extend(j for j in self.time_zan[i] if '_d' in j)
        self.zan = []
        self.week = []
        self.week_this = [datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()) + datetime.timedelta(days=w) for w in range(7)]
        self.today = datetime.date.today()
        self.week.extend([str(self.today - datetime.timedelta(days=i)) for i in range(7)])
        data = self.exists_files('plan.pickle')
        if data != {}:
            self.zan = list(data.values())[0]
            self.need_date = list(data.keys())[0]
            self.kartina_save = self.image_dict['plan2']
        else:
            self.need_date = self.today
            self.kartina_save = self.image_dict['plan']
            
        self.household_wind()
        self.table()
        self.table2()
        self.canvass(self.kartina_save)
        self.comm_funk = comments.Comms(self.time_zan, self.tab4, self.table, self.comm)
        self.update_comment = self.comm_funk.update_comment
        self.static_funk = static.Statistic(self.time_zan, self.tab2)
        self.change_funk = changes.Change(self.time_zan, self.tab3, self.spisok_del, self.tab2, self.table, self.update_comment, self.static_funk)
        if str(self.need_date) != str(self.today):
            messagebox.showinfo("ВНИМАНИЕ", "Данные за дату "+str(self.need_date)+" не сохранены")
        end = time.time()
        print(end - start)

    def del_all(self):
        self.zan = []
        self.table2()

    def canvass(self, k_save):
        self.r2 = Canvas(self.frame_main_right2, width=400,height=540, bg='#024379')
        self.r2.create_image(0, 0, anchor=NW, image=self.image_dict['fon2'])
        self.r2.create_image(135, 80, anchor=NW, image=self.image_dict['save'])
        self.r2.create_image(135, 220, anchor=NW, image=self.image_dict['save2'])
        self.r2.create_image(135, 160, anchor=NW, image=k_save)
        self.r2.pack()
        self.variable0 = StringVar()
        data = load_object("plan.pickle").param
        if data != {}:
            self.table2()
            color_for_plan = '#84B1C2'
            self.need_date = list(data.keys())[0]
        else:
            color_for_plan = '#ffffff'
            self.need_date = self.today

        self.variable0.set(str(self.need_date))
        self.w0 = OptionMenu(self.r2, self.variable0, *self.week)
        self.w0.config(font=("Verdana", 10), bg='light blue', width=10, activebackground='light blue')
        self.w0.place(x=20, y=10)
        self.but_save = Button(self.r2, text='Сохранить\n день', command=self.save, font=self.font, width=12, height=2, bg='#ffffff')
        self.but_save.place(x=20, y=80)
        self.but_plan = Button(self.r2, text='Сохранить\n план', command=self.plan,font=self.font, width=12, height=2, bg=color_for_plan)
        self.but_plan.place(x=20, y=160)
        self.button_for_clear = Button(self.r2, text='Очистить\n план', command=self.clear_plan, font=self.font, width=8, height=2, bg='#ffffff')
        self.button_for_clear.place(x=190, y=160)
        self.but_otmen = Button(self.r2, text='Отменить\n сохранение', command=self.otmena, font=self.font, width=12, height=2, bg='#ffffff')
        self.but_otmen.place(x=20, y=220)

    def clear_plan(self):
        self.save_zap = []
        save_object(PickClass({}), "plan.pickle")
        self.r2.destroy()
        self.kartina_save = self.image_dict['plan']
        self.canvass(self.kartina_save)

    def exists_files(self, file):
        if not os.path.exists(file) or os.path.getsize(file) == 0:
            save_object(PickClass({}), file)
        return load_object(file).param or {}
    
    def table(self):
        self.comm = self.exists_files('comm.pickle')
        self.frame_main_left.destroy()
        self.frame_main_left = Frame(self.frame_main_left_outside)
        self.frame_main_left.pack()

        self.sf = ScrolledFrame(self.frame_main_left, width=300, height=480)
        self.sf.pack()
        self.sf.bind_arrow_keys(self.frame_main)
        self.sf.bind_scroll_wheel(self.frame_main)

        self.inner_frame = self.sf.display_widget(Frame)
        x = 1
        for i in self.time_zan:
            lb_type = Label(self.inner_frame, text=i,font=self.font, bg='#83B3E1')
            lb_type.grid(row=x, column=0, pady=4, padx=4)
            self.count_all_m = 0
            self.count_all_w = 0
            self.lb_all_m = Label(self.inner_frame, text='', font=self.font, bg='#83B3E1')
            self.lb_all_m.grid(row=x, column=1, pady=4, padx=4)
            self.lb_all_w = Label(self.inner_frame, text='', font=self.font, bg='#83B3E1')
            self.lb_all_w.grid(row=x, column=2, pady=4, padx=4)
            if self.spisok_del != []:
                x += 1
                var = StringVar()
                var.set('Удаленные занятия')
                spisok_del2 = [d for d in self.time_zan[i] if d in self.spisok_del]
                if spisok_del2 != []:
                    w = OptionMenu(self.inner_frame, var, *spisok_del2)
                    w.grid(row=x, column=0, padx=4, pady=4)
            for j in self.time_zan[i]:
                if '_d' not in j:
                    x += 1
                    self.bt = Button(self.inner_frame, text=j, font=self.font, width=15, height=1, bg='#0076A3', fg='#ffffff')
                    self.bt.grid(row=x, column=0, sticky=W, pady=4, padx=4)
                    self.bt.bind('<Button-1>', self.btn_click)
                    comments.ToolTip(self.bt, self.comm[j]) if j in self.comm else None
                    count_time = self.count_time_funk(j)
                    count_in_week = self.count_in_week_funk(j)
                    lb = Label(self.inner_frame, text=count_time, font=self.font, width=5, height=1, bg='#ffffff')
                    lb.grid(row=x, column=1, sticky=W, pady=4, padx=4)
                    lb2 = Label(self.inner_frame, text=count_in_week, font=self.font, width=5, height=1, bg='#ffffff')
                    lb2.grid(row=x, column=2, sticky=W, pady=4, padx=4)
                    x += 1
                self.count_all_m += count_time
                self.count_all_w += count_in_week
                x += 1
            x += 1
            self.lb_all_m.configure(text=self.count_all_m)
            self.lb_all_w.configure(text=self.count_all_w)

    def count_time_funk(self, i_from_table):
        return sum([len(self.time_zan[j][i_from_table]) for j in self.time_zan if i_from_table in self.time_zan[j]])

    def count_in_week_funk(self, i_from_table):
        for j in self.time_zan:
            if i_from_table in self.time_zan[j]:
                return len([k for k in self.week_this if str(k) in self.time_zan[j][i_from_table]])

    def btn_click(self, event):
        t = str(event.widget.cget('text'))
        if t not in self.zan:
            self.zan.append(t)
            self.table2()

    def table2(self):
        self.frame_rf.destroy()
        self.frame_rf = Canvas(self.frame_main_right)
        self.frame_rf.pack()

        self.frame_rf_up = Frame(self.frame_rf, bg='#0B275B')
        self.frame_rf_up.pack(side=TOP)

        self.lb_today = Label(self.frame_rf_up, text='Задачи на сегодня', font=self.font, fg='white', height=2, width=20, bg='#0B275B')
        self.lb_today.grid(row=0, column=0, columnspan=2, pady=4, padx=4)
        bt_del_all = Button(self.frame_rf_up, text='Удалить все', font=self.font, width=20, height=1, bg='#0076A3', fg='#ffffff', command=self.del_all)
        bt_del_all.grid(row=0, column=2, pady=4, padx=4, columnspan=2)

        self.frame_rf_down = ScrolledFrame(self.frame_rf, width=330, height=480)
        self.frame_rf_down.pack(side=TOP)
        self.frame_rf_down.bind_arrow_keys(self.frame_rf)
        self.frame_rf_down.bind_scroll_wheel(self.frame_rf)
        self.inner_frame2 = self.frame_rf_down.display_widget( Frame, width=330, height=480)

        self.y1 = 30
        self.list_cb = []
        for _ in range(len(self.zan)):
            self.list_cb.append(StringVar())
        for i in range(len(self.zan)):
            self.cb = Checkbutton(self.inner_frame2, text=self.zan[i], variable=self.list_cb[i],onvalue=self.zan[i], offvalue='', font=self.font, width=15, height=1, anchor=W)
            self.cb.grid(row=i, column=0, pady=6, padx=4, sticky=W)
            self.bt = Button(self.inner_frame2, text='Удалить', command=lambda text=self.zan[i]: self.del_label(text), font=self.font, width=10, height=1)
            self.bt.grid(row=i, column=1, pady=6, padx=4)
            self.buton_up = Button(self.inner_frame2, command=lambda text=self.zan[i]: self.move_label(text, 'up'), image=self.image_dict['up'], height=20, width=20)
            self.buton_up.grid(row=i, column=2, pady=6, padx=4)
            self.buton_down = Button(self.inner_frame2, command=lambda text=self.zan[i]: self.move_label( text, 'down'), image=self.image_dict['down'], height=20, width=20)
            self.buton_down.grid(row=i, column=3, pady=6, padx=4)
            self.y1 += 40

    def move_label(self, text, direction):
        for i in range(len(self.zan)):
            if self.zan[i] == text:
                if direction == 'up' and i != 0:
                    self.zan[i], self.zan[i-1] = self.zan[i-1], self.zan[i]
                elif direction == 'down' and i != len(self.zan)-1:
                    self.zan[i], self.zan[i+1] = self.zan[i+1], self.zan[i]
                self.table2()
                break

    def del_label(self, text):
        self.zan.remove(text)
        self.table2()

    def save(self):
        self.save_for_undo = copy.deepcopy(self.time_zan)
        for i in range(len(self.zan)):
            self.save_zap.append(self.list_cb[i].get())
        while ('' in self.save_zap):
            self.save_zap.remove('')
        chosen_date = self.variable0.get()
        for i in self.save_zap:
            for j in self.time_zan:
                if i in self.time_zan[j]:
                    if chosen_date not in self.time_zan[j][i]:
                        self.time_zan[j][i].append(chosen_date)
        messagebox.showinfo("Сохранено", "Начинается новый день")
        self.save_to_pickle()

    def save_to_pickle(self):
        save_object(PickClass(self.time_zan), 'archive.pickle')
        self.zan = []
        self.table2()
        self.table()
        self.static_funk.update_for_statistic(self.time_zan)
        self.save_zap = []
        save_object(PickClass({}), 'plan.pickle')
        self.but_plan.configure(bg='#ffffff')
        self.r2.destroy()
        self.kartina_save = self.image_dict['plan']
        self.canvass(self.kartina_save)

    def otmena(self):
        if self.save_for_undo != []:
            self.time_zan = copy.deepcopy(self.save_for_undo)
            messagebox.showinfo("Изменения отменены", "Отмена")
            self.save_to_pickle()
            self.save_for_undo = []

    def plan(self):
        if self.zan == []:
            self.but_plan.configure(bg='#ffffff')
            self.kartina_save = self.image_dict['plan']
        else:
            self.but_plan.configure(bg='#84B1C2')
            self.kartina_save = self.image_dict['plan2']
        save_object(PickClass({self.variable0.get():self.zan}), 'plan.pickle')
        self.r2.destroy()
        self.canvass(self.kartina_save)

    def household_wind(self):
        self.frame_hom = Frame(self.tab5)
        self.frame_hom.pack(anchor=W)
        self.text_hom = scrolledtext.ScrolledText(self.frame_hom, width=40, height=15)
        self.text_hom['font'] = self.font
        self.text_hom.grid(row=1, column=1, padx=4, pady=4)
        self.but_hom = Button(self.frame_hom, text="Сохранить", font=self.font, bg='#0076A3',fg='#ffffff', command=lambda: self.add_del_hom("Сохранить"))
        self.but_hom.grid(row=2, column=1, padx=4, pady=4)
        self.but_del_hom = Button(self.frame_hom, text="Удалить", font=self.font, bg='#0076A3',fg='#ffffff', command=lambda: self.add_del_hom("Удалить"))
        self.but_del_hom.grid(row=3, column=1, padx=4, pady=4)
        self.hom = '' if self.hom =={} else self.hom
        self.text_hom.insert(END, self.hom)

    def add_del_hom(self, text):
        if text == "Сохранить":
            self.hom = self.text_hom.get("1.0", END)
        else:
            self.hom = ''
            self.text_hom.delete("1.0", END)
        save_object(PickClass(self.hom), 'hom.pickle')
        self.r2.destroy()

if __name__ == "__main__":
    root = Tk()
    example = Time_fix()
    #cProfile.run('Time_fix()', filename='main_copy')
    root.geometry("970x510")
    root.title('Fix time')
    root.mainloop()