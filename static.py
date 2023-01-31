import datetime
from tkinter import *
from tkscrolledframe import ScrolledFrame
from tkcalendar import Calendar as cl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Statistic():
    def __init__(self, time_zan, tab2):
        self.time_zan = time_zan
        self.tab2 = tab2
        self.font = ("Verdana", 10)
        self.main = Frame(self.tab2)
        self.main.pack(anchor=W)
        self.frame_s = Frame(self.main)
        self.frame_s.pack(side=LEFT, anchor=N)
        self.frame_up_s = Frame(self.frame_s)
        self.frame_up_s.pack()
        self.frame_down_s = Frame(self.frame_s)
        self.frame_down_s.pack()
        self.frame_right = Frame(self.main)
        self.frame_right.pack()

        # список всех дат из архива
        self.spisok_date = []
        for i in self.time_zan:
            for j in self.time_zan[i]:
                for k in self.time_zan[i][j]:
                    if k not in self.spisok_date:
                        self.spisok_date.append(k)
        self.spisok_date = list(set(self.spisok_date))
        self.spisok_date.sort()
        if self.spisok_date == []:
            self.spisok_date_min  = datetime.date.today()
            self.spisok_date_max = datetime.date.today()
            self.spisok_date_min0  = str(self.spisok_date_min)
            self.spisok_date_max0 = str(self.spisok_date_max)
        else:
            self.spisok_date_min0 = self.spisok_date[0]
            self.spisok_date_min = datetime.datetime.strptime(self.spisok_date_min0, '%Y-%m-%d')
            self.spisok_date_max0 = self.spisok_date[-1]
            self.spisok_date_max = datetime.datetime.strptime(self.spisok_date_max0, '%Y-%m-%d')
        self.date1 = self.spisok_date_min0
        self.date2 = self.spisok_date_max0
        label_chose_start = Label(self.frame_up_s, text='Начальная\n дата', font=self.font)
        label_chose_start.grid(row=0, column=0, padx=4, pady=4)
        label_choose_end = Label(self.frame_up_s, text='Конечная\n дата', font=self.font)
        label_choose_end.grid(row=0, column=2, padx=4, pady=4)
        self.labelTop = Button(self.frame_up_s, text = self.spisok_date_min0,font=self.font, bg='white',fg='#0076A3', command= lambda: self.calendar_chose(self.spisok_date_min0,self.date1))
        self.labelTop.grid(column=1, row=0) 
        self.labelTop2 = Button(self.frame_up_s, text = self.spisok_date_max0,font=self.font, bg='white',fg='#0076A3', command=lambda: self.calendar_chose(self.spisok_date_max0,self.date2))
        self.labelTop2.grid(column=3, row=0)

        but_period = Button(self.frame_up_s, text="Показать\n по категориям", font=self.font, bg='#0076A3',fg='#ffffff' )
        but_period.grid(column=0, row=2)
        but_period.bind("<Button-1>", self.period_cat)
        but_per_zan = Button(self.frame_up_s, text="Показать\n по занятиям", font=self.font, bg='#0076A3',fg='#ffffff')
        but_per_zan.grid(column=1, row=2)
        but_per_zan.bind("<Button-1>", self.period_cat)
        but_cat_one = Button(self.frame_up_s, text="Одна категория", font=self.font, bg='#0076A3',fg='#ffffff',height=2)
        but_cat_one.grid(column=2, row=2)
        but_cat_one.bind("<Button-1>", self.cat_one)
        but_zan_one = Button(self.frame_up_s, text="Одно занятие", font=self.font, bg='#0076A3',fg='#ffffff',height=2)
        but_zan_one.grid(column=3, row=2)
        but_zan_one.bind("<Button-1>", self.cat_one)
        self.err_gragh = Label(self.frame_up_s, text='',font=self.font,bg='white',fg='red')
        self.err_gragh.grid(column=0, row=3, columnspan=3)
        self.frame_for_scroll = Frame(self.frame_right)
        self.frame_for_scroll.pack()
        self.update_for_statistic(self.time_zan)

    def update_for_statistic(self,time_zan):
        self.frame_for_scroll.destroy()
        self.frame_for_scroll = Frame(self.frame_right)
        self.frame_for_scroll.pack()
        self.time_zan = time_zan
        self.sf2 = ScrolledFrame(self.frame_for_scroll, width=600, height=600)
        self.sf2.pack()
        self.sf2.bind_arrow_keys(self.main)
        self.sf2.bind_scroll_wheel(self.main)
        self.inner_frame2 = self.sf2.display_widget(Frame)
        self.lb_choose_cat = Label(self.inner_frame2, text="Выберите категорию",font=self.font, bg='#ffffff',fg='#0076A3')                      
        self.lb_choose_cat.grid(column=1, row=0)
        self.lb_choose_zan = Label(self.inner_frame2, text="Выберите занятие",font=self.font, bg='#ffffff',fg='#0076A3')
        self.lb_choose_zan.grid(column=4, row=0)

        self.spisok_cat = []
        self.spisok_cat2 = {}
        for i in self.time_zan:
            self.spisok_cat.append(i)
            a=[]
            for j in self.time_zan[i]:
                a.append(j)
            self.spisok_cat2[i] = a
        self.check_button_spisok(self.spisok_cat2, 4)
        self.check_button_spisok(self.spisok_cat, 1)

    def check_button_spisok(self,spisok1,num_col):
        z=1
        if type(spisok1) == dict:
            self.save_checb = {}
            for i in spisok1:
                self.lb_choose_cat = Label(self.inner_frame2, text=i,font=self.font, bg='#ffffff',fg='#0076A3')                      
                self.lb_choose_cat.grid(column=num_col, row=z,sticky=W)
                z+=1
                for value in spisok1[i]:
                    var = BooleanVar()
                    check_button = Checkbutton(self.inner_frame2, text=value, variable=var)
                    check_button.grid(column=num_col, row=z,sticky=W)
                    check_button.select()
                    self.save_checb[value] = var
                    z+=1
        else:
            self.save_checb_cat={}
            for value in spisok1:
                var = BooleanVar()
                check_button_cat = Checkbutton(self.inner_frame2, text=value, variable=var)
                # утановить включность по умолчанию
                check_button_cat.select()
                check_button_cat.grid(column=num_col, row=z, sticky=W)
                self.save_checb_cat[value] = var
                z+=1
        self.but_all_cat = Button(self.inner_frame2, text="Выбрать все", font=self.font, bg='#0076A3',fg='#ffffff',command = lambda: self.all_zan(spisok1))
        self.but_all_cat.grid(column=num_col, row=z, sticky=W)
        
        self.but_all_cat = Button(self.inner_frame2, text="Убрать все", font=self.font, bg='#0076A3',fg='#ffffff',command=lambda: self.all_zan2(spisok1))
        self.but_all_cat.grid(column=num_col, row=z+1, sticky=W)

    def all_zan(self, spisok1):
        if type(spisok1) == dict:
            for _,var in self.save_checb.items():
                var.set(1)
        else:
            for _,var in self.save_checb_cat.items():
                var.set(1)

    def all_zan2(self, spisok1):
        if type(spisok1) == dict:
            for _,var in self.save_checb.items():
                var.set(0)
        else:
            for _,var in self.save_checb_cat.items():
                var.set(0)

    def calendar_chose(self,text,date):
        self.top = Toplevel()
        if text ==self.spisok_date_min0:
            self.top.title("Начальная дата")
        else:
            self.top.title("Конечная дата")
        text_cal = datetime.datetime.strptime(date, '%Y-%m-%d')
        self.calendars = cl(self.top, font=self.font, selectmode='day', year=text_cal.year, month=text_cal.month, day=text_cal.day)
        self.calendars.grid(column=1, row=1)
        Button(self.top, text = "Выбрать", command = lambda: self.calendar_chose2(text)).grid(column=1, row=2)

    def calendar_chose2(self,text):
        if text == text ==self.spisok_date_min0:
            self.date1 = str(self.calendars.selection_get())
            self.labelTop.configure(text=str(self.calendars.selection_get()))
        else:
            self.date2 = str(self.calendars.selection_get())
            self.labelTop2.configure(text=str(self.calendars.selection_get()))
        self.top.destroy()

    def cat_one(self, event):
        name_button = event.widget.cget('text')
        self.zapol_for_graph()

        if name_button == 'Одна категория':
            if len(self.cat_check) > 1:
                self.err_gragh.config(text="Выберите только одну категорию")
            else:
                self.err_gragh.config(text="")
                a = self.cat_one_graph
                self.graphik(a)
        else:
            if len(self.cat_check2) > 1:
                self.err_gragh.config(text="Выберите только одно занятие")
            else:
                self.err_gragh.config(text="")
                a = self.zan_one_graph
                self.graphik(a)

    def graphik(self,a):
        new = {}
        for key in a:
            if a[key]==[]:
                continue
            else:
                a[key] = sorted(a[key])
                dates = a[key]
                start_date = dates[0]
                end_date = dates[-1]

                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                dates_list = []

                while start_date <= end_date:
                    dates_list.append(start_date.strftime('%Y-%m-%d'))
                    start_date += datetime.timedelta(days=1)

                for date in dates_list:
                    if date not in dates:
                        new[date]=0
                    else:
                        new[date]=1
        if new != {}:
            if len(new )==1:
                self.frame_down_s.destroy()
                self.frame_down_s = Frame(self.frame_s)
                self.frame_down_s.pack()
                for key in new:
                    t = 'Всего одно занятие за период - '+ str(key)
                self.err_gragh.config(text=t)
            else:
                self.frame_down_s.destroy()
                self.frame_down_s = Frame(self.frame_s)
                self.frame_down_s.pack()

                self.frame_for_scroll = Frame(self.frame_down_s)
                self.frame_for_scroll.pack(anchor=W)
                self.sf2 = ScrolledFrame(self.frame_for_scroll, width=400, height=500)
                self.sf2.pack(anchor=W)

                self.sf2.bind_arrow_keys(self.main)
                self.sf2.bind_scroll_wheel(self.main)

                self.inner_frame = self.sf2.display_widget(Frame)

                self.fig = plt.figure(figsize=(9, 5), dpi=80)
                self.ax = self.fig.add_subplot(111)
                self.ax.plot(dates_list, new.values(), '-')
                self.ax.set_yticks([0.5])
                self.ax.grid(True)

                self.fig.autofmt_xdate(rotation=45)
                self.ax.tick_params(axis='x', labelrotation=90)

                self.canvas = FigureCanvasTkAgg(self.fig, self.inner_frame)
                self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True, anchor=W)
                self.canvas.draw()
                plt.close(self.fig)

        else:
            self.err_gragh.config(text="Нет данных по выбранной категории\занятию ")

    def period_cat(self, event):
        self.err_gragh.config(text="")
        name_button = event.widget.cget('text')
        self.zapol_for_graph()
        # заполнить self.graph_cat галочками из self.spisok_cat_check
        if name_button == 'Показать\n по категориям':
            a = self.graph_cat
        else:
            a = self.graph_zan
        if a != {}:
            self.frame_down_s.destroy()
            self.frame_down_s = Frame(self.frame_s)
            self.frame_down_s.pack()

            data = list(a.values())
            ind = list(a.keys())
            width = .5
            fig = Figure(figsize=(5,12), dpi=85)
            ax = fig.add_subplot(111)
            ax.grid(True)
            fig.autofmt_xdate(rotation=45)
            ax.tick_params(axis='x', labelrotation=90)
            rects1 = ax.bar(ind, data, width)
            # установить ширину столбцов = 1
            ax.set_xlim(-width, len(ind) + width)
            canvas = FigureCanvasTkAgg(fig, self.frame_down_s)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        else:
            self.err_gragh.config(text="Нет данных по выбранной категории\занятию")

    def zapol_for_graph(self):
        self.graph_zan = {}
        self.graph_cat = {}
        self.cat_check =  []
        self.cat_check2 = []
        self.cat_one_graph = {}
        self.zan_one_graph = {}

        for value,var in self.save_checb_cat.items():
            if var.get() == 1:
                self.cat_check.append(value)

        for value,var in self.save_checb.items():
            if var.get() == 1:
                self.cat_check2.append(value)

        for i in self.time_zan:
            for j in self.time_zan[i]:
                for k in self.time_zan[i][j]:
                    if k >= self.date1 and k <= self.date2:
                        if j in self.cat_check2:
                            if j not in self.graph_zan:
                                self.graph_zan[j] = 1
                            else:
                                self.graph_zan[j] += 1

                            if j not in self.zan_one_graph:
                                self.zan_one_graph[j] = []
                            if k not in self.zan_one_graph[j]:
                                self.zan_one_graph[j].append(k)

                        if i in self.cat_check:
                            if i not in self.graph_cat:
                                self.graph_cat[i] = 1
                            else:
                                self.graph_cat[i] += 1

                            if i not in self.cat_one_graph:
                                self.cat_one_graph[i] = []
                            if k not in self.cat_one_graph[i]:
                                self.cat_one_graph[i].append(k)