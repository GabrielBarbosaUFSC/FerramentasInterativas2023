from tkinter import*
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CreateWaveForm import center_win

class Save:
    def __init__(self, win, pos_x, pos_y, number, t):
        self.t = t
        self.datas = [[], [], [], []] # [y, u, sp, q]
        self.condicions = [] # [tau, u_max, u_min, ke, kq, l, kp, ki, kd]
        self.number = number
        self.in_use = False
        self.win = win
        self.posx = pos_x
        self.posy = pos_y

        self.label_var = StringVar(master=self.win)
        self.label_var.set(f'#{self.number}: Vazio')
        self.label = Label(self.win, textvariable = self.label_var).place(x=pos_x, y=pos_y)  

        self.check_var = IntVar() 
        self.check = Checkbutton(self.win, text= "Mostrar", variable=self.check_var, onvalue= 1, offvalue= 0)
        self.check.place(x=pos_x+140, y=pos_y)

        Button(self.win, text="I", command=self.show_wave_form).place(x=pos_x+120, y=pos_y, height= 20, width=20)

    def clear(self):
        self.in_use = False
        self.label_var.set(f'#{self.number}: Vazio')
        self.check_var.set(0)

    def set(self, params):
        self.in_use = True
        self.time = self.t()
        self.datas[0] = params[0]
        self.datas[1] = params[1]
        self.datas[2] = params[2]
        self.datas[3] = params[3]
        self.condicions = params[4:13]
        self.label_var.set(f'#{self.number}: {params[13]}')

    def show_wave_form(self):
        if not self.in_use:
            return
        try:
            self.top.destroy()
        except:
            pass

        self.top = Toplevel(self.win)
        self.top.geometry(center_win(self.win, 720, 480))
        self.top.resizable(width=False, height= False)      

        self.fig = Figure(figsize = (7, 4), dpi = 100, layout = 'tight')
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.top)
        self.canvas.get_tk_widget().place(x= 0, y = 0)
        self.plot_area = self.fig.add_subplot(2, 1, 1)

        self.plot_area.plot(self.time, self.datas[0], label = "y")
        self.plot_area.plot(self.time, self.datas[3], label = "q")
        self.plot_area.plot(self.time, self.datas[2], label = "sp")

        self.plot_area.legend(loc = "lower right") #Adiciona legendas
        self.plot_area.set_xlabel("Tempo - Segundos") 
        self.plot_area.set_ylabel("Saída") 
        self.plot_area.grid() 
        self.canvas.draw()

        self.plot_area = self.fig.add_subplot(2, 1, 2)
        self.plot_area.plot(self.time, self.datas[1], label = "u")
        self.plot_area.legend(loc = "lower right") #Adiciona legendas
        self.plot_area.set_xlabel("Tempo - Segundos") 
        self.plot_area.set_ylabel("Controle") 
        self.plot_area.grid() 
        self.canvas.draw()
        #[tau, u_max, u_min, ke, kq, l]
        labels = ["\u03c4", "Umax", "Umin", "Ke", "Kq", "L", "kp", "ki", "kd"]
        text = ""
        for i in range(len(labels)):
            text += f'\t{labels[i]}: {self.condicions[i]}  '
        self.label = Label(self.top, text=text)
        self.label.place(x = 20, y= 420)

class SaveBox:
    def __init__(self, win, pos_x, pos_y, getdata, t):
        self.win = win
        self.getdata = getdata

        self.saves = [Save(self.win, pos_x=pos_x, pos_y= 30+ pos_y + 20*i, number = i,t=t) for i in range(5)] 
        
        self.save_btn = Button(win, text= "Salvar", command= self.save_draw)
        self.save_btn.place(x =pos_x, y = pos_y, height= 25, width= 75)

    def save_draw(self):
        try:
            self.top.destroy()
        except:
            pass

        self.top = Toplevel(self.win)
        self.top.geometry(center_win(self.win, 250, 120))
        self.top.resizable(width=False, height= False)

        label = Label(self.top, text="Nome:")
        label.place(x=20, y=0, height=30, width=100)

        self.entry = Entry(self.top, bd=3)
        self.entry.place(x=130, y=0, height=30, width=100)

        label2 = Label(self.top, text="Sobrescrever:")
        label2.place(x=20, y=40, height=30, width=100)

        self.combobox_var = StringVar()
        self.combobox = Combobox(self.top, width = 10, textvariable = self.combobox_var)
        self.combobox['values'] = [i.label_var.get() for i in self.saves]
        self.combobox.place(x=130, y=40, height=30, width=100)
        self.combobox_var.set(self.saves[0].label_var.get())

        Button(self.top, text="Salvar", command=self.save_data).place(x= 100, y= 80, height=40, width=60)

    def save_data(self):
        names = [i.label_var.get() for i in self.saves]
        try:
            a = names.index(self.combobox_var.get())
            self.saves[a].set(self.getdata()+[self.entry.get()])
            self.top.destroy()
        except:
            pass
        
    def clear(self):
        for save in self.saves:
            save.clear()




