#importa as bibliotecas necessárias
from tkinter import*
from graph import*
from math import sin
from tkinter import ttk
from NonLinearSlider import* 

#Define as funções para criar as formas de onda, todas retornam uma lista
def func_seno       (t, A, omega, phi, offset):
    return [A*sin(omega*i + phi) + offset for i in t()]
def func_degree     (t, A, phi):
    return [(i>=phi)*A for i in t()]
def func_triangle   (t, A, T, phi, offset):
    if abs(T) <= 0.1:
        return [0]*len(t())
    m = 4*A/T
    y = [0]*len(t())
    for i, time in enumerate(t()):
        passo = (time+phi) // (T/2)
        step = (time+phi) % (T/2)
        if (passo%2)//1:
            y[i] = A - m*step + offset
        else:
            y[i] = -A + m*step + offset
    return y
def func_square     (t, A, T, phi, offset):
    if abs(T) <= 0.1:
        return [0]*len(t())
    return [((((i+phi) // (T/2))%2)//1)*A + offset for i in t()]

#Centraliza a janela criada
def center_win(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    return "{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate)

class CreateWaveForm:
    #Cria os parâmetros iniciais 
    def __init__(self, win, t, plot_extern):
        self.plot_extern = plot_extern #função que plota os dados no programa principal
        self.win = win
        self.t = t  #Vetor de tempo de base
        self.wave = [0]*len(t()) #Wave criada

        #Flags que sinalizam o estado do checkbox
        self.flag_sp = False
        self.flag_q = False
        self.flag_u = False

        self.fc_y = 1
        self.filter_y = False

        self.fc_setpoint = 1
        self.filter_setpoint = False

        self.noise = False
        self.phi_noise = 0

    #Cria a nova janela
    def create_win(self):
        #Se tiver alguma outra janela aberta, ele fecha
        try: 
            self.top.destroy()
        except:
            pass

        #Cria a janela
        self.top = Toplevel(self.win)
        self.top.geometry(center_win(self.win, 720, 570))
        self.top.resizable(width=False, height= False)
        #Cria o gráfico
        self.graph = Graph(self.top, 10, 230, self.t, "Amostras", "Y")

        #Cria o select box para selecionar o tipo de onda
        self.n = StringVar()
        self.wave_form_choosen = ttk.Combobox(self.top, width = 10, textvariable = self.n)
        self.wave_form_choosen['values'] = ['Seno', 'Triangular', 'Quadrada', 'Degrau']
        self.wave_form_choosen.place(x= 20, y = 70)
        self.wave_form_choosen.bind('<<ComboboxSelected>>', self.select_wave_form)

        #Cria os sliders e os esconde
        self.sliders = [NonLinearSlider(self.top, 20 + 220*(i > 1), 100 +50*(i%2), self.plot, label="") for i in range(4)]
        for slider in self.sliders:
            slider.hide()
        
        #Cria o checkbox para usar a onda como setpoint
        self.sp_var = IntVar() 
        self.sp_check = Checkbutton(self.top, text= "Usar como SP", variable=self.sp_var, onvalue= 1, offvalue= 0)
        self.sp_check.place(x=500, y= 100)   

        #Cria o checkbox para usar a onda como perturbação
        self.q_var = IntVar() 
        self.q_check = Checkbutton(self.top, text= "Usar como Q", variable=self.q_var, onvalue= 1, offvalue= 0)
        self.q_check.place(x=500, y= 130)

        #Cria o checkbox para usar a onda como sinal do controle
        self.u_var = IntVar() 
        self.u_check = Checkbutton(self.top, text= "Usar como U", variable=self.u_var, onvalue= 1, offvalue= 0)
        self.u_check.place(x=500, y= 160)      


        self.noise_var = IntVar() 
        self.noise_check = Checkbutton(self.top, text= "Adicionar Ruído", variable=self.noise_var, onvalue= 1, offvalue= 0)
        self.noise_check.place(x=40, y= 20)
        
        self.slider_fi_noise = NonLinearSlider(self.top, 200, 5, self.plot, "t0", min= 0, max=500, IsInt=True)
        self.slider_amp_noise = NonLinearSlider(self.top, 450, 5, self.plot, "Amp_n",initial_value= 1, min=0, max=25)

        #Habilita as interruções
        self.wave_form_choosen.bind('<<ComboboxSelected>>', self.select_wave_form)
        self.top.bind("<ButtonRelease>", self.released_update)

        #Define o primeiro plot
        self.wave_form_choosen.set('Degrau')
        self.select_wave_form(0)
        self.plot()

    #Habilita os Sliders de acordo com o tipo de onda selecioando
    def select_wave_form(self, event):
        labels = []
        initial_values = []
        max = []
        min = []
        non_zero = []
        isInt = []

        if self.wave_form_choosen.get() == 'Seno':
            labels = ['Amp', '\u03C9_n', '\u03C6', 'offset']
            initial_values = [1, 1, 0, 0]
            max = [25, 3, 3.2, 25]
            min = [-25, 0.01, -3.2, -25]
            non_zero = [False, True, False, False]
            isInt = [False, False, False, False]

        elif self.wave_form_choosen.get() == 'Triangular':
            labels = ['Amp', 'T', '\u03C6', 'offset']
            initial_values = [1, 10, 0, 0]
            max = [25, 50, 50, 25]
            min = [-25, 5, 0, -25]
            non_zero = [False, True, False, False]
            isInt = [False, False, False, False]

        
        elif self.wave_form_choosen.get() == 'Quadrada':
            labels = ['Amp', 'T', '\u03C6', 'offset']
            initial_values = [1, 10, 0, 0]
            max = [25, 50, 50, 25]
            min = [-25, 5, 0, -25]
            non_zero = [False, True, False, False]
            isInt = [False, False, False, False]


        elif self.wave_form_choosen.get() == 'Degrau':
            labels = ['Amp', 't0']
            initial_values = [1, 0]
            max = [25, 500]
            min = [-25, 0]
            non_zero = [False, False]
            isInt = [False, True]


        for i in range(len(self.sliders)):
            if i >= len(labels):
                self.sliders[i].hide()
            else:
                self.sliders[i].set_params (labels[i], min[i], max[i], non_zero[i], initial_values[i], isInt[i])
                self.sliders[i].show()

    #Atualiza as flags que indicam os checkboxes
    def released_update(self, event):
        for slider in self.sliders:
            slider.update_released()
         
        self.slider_fi_noise.update_released()
        self.slider_amp_noise.update_released()

        self.flag_q = self.q_var.get()
        self.flag_sp = self.sp_var.get()
        self.flag_u = self.u_var.get()

        self.plot()

    #Plota os dados no gráfico da janela
    def plot(self):
        wave_type = self.wave_form_choosen.get()
        param = [slider.get() for slider in self.sliders]

        if wave_type == 'Seno':
            self.wave = func_seno(self.t, param[0], param[1], param[2], param[3])
        elif wave_type == 'Triangular':
            self.wave = func_triangle(self.t, param[0], param[1], param[2], param[3])
        elif wave_type == 'Quadrada':
            self.wave = func_square(self.t, param[0], param[1], param[2], param[3])
        elif wave_type == 'Degrau':
            self.wave = func_degree(self.t, param[0], param[1])
            
        self.noise = self.noise_var.get()*self.slider_amp_noise.get()
        self.phi_noise = self.slider_fi_noise.get()

        self.graph.set_data([self.wave], ["Sinal"])
        self.plot_extern()

