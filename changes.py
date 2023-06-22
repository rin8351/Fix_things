from tkinter import *
from saving import PickClass, save_object

class Change():
    def __init__(self, time_zan, tab3,spisok_del,tab2,table,update_comment,static_funk):
        super().__init__()
        self.time_zan = time_zan
        self.static_funk = static_funk
        self.tab3 = tab3
        self.tab2 = tab2
        self.font = ('Verdana', 10)
        self.spisok_del = spisok_del
        self.table = table
        self.update_comment = update_comment
        self.frame_e = Frame(self.tab3)
        self.frame_e.pack()

        self.spisok1 = []
        for i in self.time_zan:
            self.spisok1.append(i)
        self.spisok2_funk()

    def spisok2_funk(self):
        self.spisok2 = []
        for i in self.time_zan:
            for j in self.time_zan[i]:
                if '_d' not in j:
                    self.spisok2.append(j)
        self.stroy()

    def stroy(self):
        self.frame_e.destroy()
        self.frame_e = Frame(self.tab3)
        self.frame_e.pack(anchor=W)
        
        lb = Label(self.frame_e, text='Новая категория', font=self.font, bg='#ffffff',fg='#0076A3',width=18)
        lb.grid(row=0, column=0, pady=4, padx=4)
        self.categ = StringVar()
        self.categs = Entry(self.frame_e, width=30,textvariable=self.categ)
        self.categs.grid(row=0, column=1, pady=4, padx=4)
        btn2 = Button(self.frame_e,text="Добавить",command=lambda:self.Dobavit_cat(self.categs.get(),'add_cat'),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')  
        btn2.grid(row=0, column=2, padx=4, pady=4)

        if self.spisok1 != []:
            lb2 = Label(self.frame_e, text='Новое занятие', font=self.font, bg='#ffffff', width=18, fg='#0076A3')
            lb2.grid(row=1, column=0, pady=4, padx=4)
            self.num = StringVar()
            self.nums = Entry(self.frame_e, width=30,textvariable=self.num)
            self.nums.grid(row=1, column=1, padx=4, pady=4)
            self.variable = StringVar()
            self.variable.set('Выбор категории')
            btn5 = Button(self.frame_e,text="Добавить",command=lambda:self.Dobavit(self.variable.get(),self.nums.get()),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')  
            btn5.grid(row=1, column=2, padx=4, pady=4)
            self.w = OptionMenu(self.frame_e, self.variable, *self.spisok1)
            self.w.grid(row=1, column=3, padx=4, pady=4)
            self.w.config(font=self.font, bg='light blue', width=14, activebackground='light blue')
            lb3 = Label(self.frame_e, text='Изменить категорию', font=('Verdana',9), bg='#ffffff', width=18, fg='#0076A3')
            lb3.grid(row=2, column=0, pady=4, padx=4)
            self.change_cat = StringVar()
            self.change_cats = Entry(self.frame_e, width=30,textvariable=self.change_cat)
            self.change_cats.grid(row=2, column=1, padx=4, pady=4)
            self.variable8 = StringVar()
            self.variable8.set('Сменить категорию')
            self.wch = OptionMenu(self.frame_e, self.variable8, *self.spisok1)
            self.wch.grid(row=2, column=2, padx=4, pady=4)
            self.wch.config(font=self.font, bg='light blue', width=15, activebackground='light blue')
            btn9 = Button(self.frame_e,text="Изменить",command=lambda:self.change_cat1(self.variable8.get(),self.change_cats.get()),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')
            btn9.grid(row=2, column=3, padx=4, pady=4)

            lb4 = Label(self.frame_e, text='Изменить занятие', font=self.font, bg='#ffffff', width=18, fg='#0076A3')
            lb4.grid(row=3, column=0, pady=4, padx=4)
            self.change_zan = StringVar()
            self.change_zans = Entry(self.frame_e, width=30,textvariable=self.change_zan)
            self.change_zans.grid(row=3, column=1, padx=4, pady=4)

            self.variable5 = StringVar()
            self.variable5.set('Удаление категории')
            self.w4 = OptionMenu(self.frame_e, self.variable5, *self.spisok1)
            self.w4.config(width=17,font=self.font,bg='light blue',activebackground='light blue')
            self.w4.grid(row=5, column=1, padx=4, pady=4)
            btn8 = Button(self.frame_e,text="Удалить",command=lambda: self.Delete_cat(self.variable5.get(),'delete_cat'),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')
            btn8.grid(row=5, column=2, padx=4, pady=4)

        if self.spisok2 != []:
            self.variable9 = StringVar()
            self.variable9.set('Сменить занятие')
            self.wch = OptionMenu(self.frame_e, self.variable9, *self.spisok2)
            self.wch.grid(row=3, column=2, padx=4, pady=4)
            self.wch.config(font=self.font, bg='light blue', width=15, activebackground='light blue')
            btn9 = Button(self.frame_e,text="Изменить",command=lambda:self.change_zan1(self.variable9.get(),self.change_zans.get()),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')
            btn9.grid(row=3, column=3, padx=4, pady=4)

            self.variable2 = StringVar()
            self.variable2.set('Удалить занятие')
            self.w2 = OptionMenu(self.frame_e, self.variable2, *self.spisok2)
            self.w2.config(width=17,font=self.font,bg='light blue',activebackground='light blue')
            self.w2.grid(row=4, column=1, padx=4, pady=4)
            self.check_save=IntVar()
            btn6 = Button(self.frame_e,text="Удалить",command=lambda:self.Delete(self.variable2.get(),'delete'),font=self.font, width=18, height=1, bg='#0076A3', fg='#ffffff')  
            btn6.grid(row=4, column=2, padx=4, pady=4)
            check = Checkbutton(self.frame_e, text='Не сохранять в архив', font=self.font, bg='#ffffff', fg='#0076A3', variable=self.check_save,
                                onvalue=1, offvalue=0)
            check.grid(row=4, column=3, padx=4, pady=4)

        if self.spisok_del != {}:
            self.variable3 = StringVar()
            self.variable3.set('Выбор Для Возврата')
            self.w3 = OptionMenu(self.frame_e, self.variable3, *self.spisok_del)
            self.w3.config(width=17,font=self.font,bg='light blue',activebackground='light blue')
            self.w3.grid(row=6, column=1, padx=4, pady=4)
            self.btn7 = Button(self.frame_e,text="Вернуть",command=lambda:self.Return(self.variable3.get(),'return'),font=self.font, width=15, height=1, bg='#0076A3', fg='#ffffff')  
            self.btn7.grid(row=6, column=2, padx=4, pady=4)
        self.lb_error = Label(self.frame_e, text='', font=self.font, bg='#ffffff', fg='red')
        self.lb_error.grid(row=7, column=1, pady=4, padx=4)

    def check_condition(label_text, error_label_text,error_label_text2):
        def decorator(func):
            def wrapper(self, label_w,name,*args, **kwargs):
                if label_w != label_text:
                    if name !='':
                        func(self, label_w, name,*args, **kwargs)
                        self.stroy()
                        self.lb_error.config(text='Изменения внесены\n в таблицу')
                        save_object(PickClass(self.time_zan),'archive.pickle')
                        self.table()
                        self.static_funk.update_for_statistic(self.time_zan)
                        self.update_comment()
                    else:
                        self.lb_error.config(text=error_label_text2)
                else:
                    self.lb_error.config(text=error_label_text)
            return wrapper
        return decorator

    @check_condition('Выбор Для Возврата','Выберите занятие','')
    def Return(self,name3,name):
        for i in self.time_zan:
            if name3 in self.time_zan[i]:
                a=self.time_zan[i][name3]
                del self.time_zan[i][name3]
                new_name = name3.replace('_d','')
                self.time_zan[i][new_name] = a
        self.spisok2.append(new_name)
        self.spisok_del.remove(name3)

    @check_condition('Выбор категории','Выберите категорию','Введите название занятия')
    def Dobavit(self,cat,name):
        self.time_zan[cat][name] = []
        self.spisok2.append(name)

    @check_condition('Сменить категорию','Выберите категорию','Введите название\n категории')
    def change_cat1(self,smen,name):
        a=self.time_zan[smen]
        del self.time_zan[smen]
        self.time_zan[name] = a
        self.spisok1.remove(smen)
        self.spisok1.append(name)
    
    @check_condition('Сменить занятие','Выберите занятие','Введите название\n занятия')
    def change_zan1(self,smen,name):
        for i in self.time_zan:
            if smen in self.time_zan[i]:
                a=self.time_zan[i][smen]
                del self.time_zan[i][smen]
                self.time_zan[i][name] = a
                self.spisok2.remove(smen)
                self.spisok2.append(name)

    @check_condition('','Введите название\n категории','')
    def Dobavit_cat(self,name3,name):
        self.time_zan[name3] = {}
        self.spisok1.append(name3)

    @check_condition('Удаление категории','Выберите категорию','')
    def Delete_cat(self,name3,name):
        self.spisok1.remove(name3)
        self.time_zan.pop(name3)
        self.spisok2_funk()

    @check_condition('Удалить занятие','Выберите занятие','')
    def Delete(self,name2,name):
        for i in self.time_zan:
            if name2 in self.time_zan[i]:
                if self.check_save.get() == 0:
                    a=self.time_zan[i][name2]
                    del self.time_zan[i][name2]
                    new_name = name2 + '_d'
                    self.time_zan[i][new_name] = a
                else:
                    del self.time_zan[i][name2]
                    new_name = name2
        self.spisok_del.add(new_name)
        self.spisok2.remove(name2)