#Blibliotecas importadas
from os import kill
from tkinter import*
from CreateWaveForm import*

#Blibiotecas criadas para manipular
from NonLinearSlider import*
from graph import*
from math_engine import sim_on_off #Roda as funções discretas
from Saving import*

y_sp = [1]*500 #Lista que armazena os valores do setpoint
q = [0]*500 #Lista que armazena os valores da perturbação
time_ = 50

#Plota os dados
def plot():
    global y_sp, q #Usa o setpoint de variável global
    
    u = 0 #usa um indicador para talvez pegar os valores do desenho da forma de onda
    if wave_create.flag_q:  #Verifica se o checkbox q está marcado
        q = wave_create.wave #Pega a forma de onda 

    if wave_create.flag_sp: #Verifica se o checkbox sp está marcado
        y_sp = wave_create.wave #Pega a forma de onda 

    if wave_create.flag_u: #Verifica se o checkbox u está marcado
        u = wave_create.wave #Pega a forma de onda 
    
    #Passa os valores dos sliders para o objeto que manipula os calculos
    math_engine.set_plant(
        tau= slider_tau.get(),
        u_max= slider_u_max.get(),
        u_min= slider_u_min.get(),
        ke= slider_ke.get(),
        kq= slider_kq.get(),
        l= slider_l.get()
    )

    #Passa os parâmetros dos outros sliders para o objeto que os calculos
    math_engine.plot( 
        setpoint= y_sp,
        qe= q,
        amp_noise= wave_create.noise,
        phi_noise= wave_create.phi_noise,
        u= u,
        kp = slider_kp.get(),
        ki=slider_ki.get(),
        b = slider_b.get()
    )
    
    data_plot_y = []
    data_plot_u = []
    data_plot_label = []
    for save in savebox.saves:
        if save.check_var.get() and len(save.datas[0]) == 500 and len(save.datas[1]) == 500:
            data_plot_label.append(save.label_var.get()) 
            data_plot_y.append(save.datas[0])  
            data_plot_u.append(save.datas[1]) 

    u_graph.set_data([math_engine.ue, math_engine.u]+data_plot_u, ["setpoint", "u"]+data_plot_label)
    y_graph.set_data([y_sp, math_engine.y, math_engine.q]+data_plot_y, ["setpoint", "y", "q"]+data_plot_label)
    
#Faz com que os sliders voltam para a posição zero depois que vc solta o cursor
def released(param):
    slider_tau.update_released()
    slider_u_max.update_released()
    slider_u_min.update_released()
    slider_ke.update_released()
    slider_kq.update_released()
    slider_l.update_released()
    slider_kp.update_released()
    slider_ki.update_released()
    slider_b.update_released()
    #Plota os dados
    plot()

def get_data():
    global y_sp, q
    return_list = []
    return_list.append(math_engine.y)
    return_list.append(math_engine.u)
    return_list.append(y_sp)
    return_list.append(q)
    return_list += math_engine.get_params() + [slider_kp.get(), slider_ki.get(), slider_b.get()]
    return return_list

def set_time():
    global time_
    number = 0
    try:
        number = int(entry_time.get())
    except:
        entry_time.delete(0, 'end')
        entry_time.insert(0, str(time_))
        return
    
    if number <= 0:
        entry_time.delete(0, 'end')
        entry_time.insert(0, str(time_))
        return
    else:
        time_ = number
        savebox.clear()
        math_engine.set_time(number, plot)

#Faz as configurações iniciais da janela
win = Tk()
win.title("Controlador PI + PSP")
win.geometry(center_win(win, 1080, 720))
win.resizable(width=False, height= False)
flag_controller_started = False

#Cria um objeto que manipula as funções de simulação discreta
math_engine = sim_on_off()

#Cria os gráficos 
y_graph = Graph(win, 290, 20, math_engine.get_time, "Tempo - Segundos", "Saída", )
u_graph = Graph(win, 290, 320, math_engine.get_time, "Tempo - Segundos", "Controle", )  

#Cria um objeto para poder criar formas de onda
wave_create = CreateWaveForm(win, math_engine.get_time, plot)

savebox = SaveBox(win,20, 580, get_data, math_engine.get_time)

#Cria e posiciona os sliders
slider_tau  = NonLinearSlider(win, 20, 10 , plot, label= '\u03c4', initial_value=25, min= 0, max=500) 
slider_u_max= NonLinearSlider(win, 20, 60 , plot, label= 'Umax',  initial_value=50)
slider_u_min= NonLinearSlider(win, 20, 110, plot, label= 'Umin',  initial_value=-50)
slider_ke   = NonLinearSlider(win, 20, 160, plot, label= 'Ke',    initial_value=1)
slider_kq   = NonLinearSlider(win, 20, 210, plot, label= 'Kq',    initial_value=1)
slider_l    = NonLinearSlider(win, 20, 260, plot, label= 'L',     initial_value=0, min=0, max=25)

slider_kp = NonLinearSlider(win, 20, 360, plot, label= 'Kp', initial_value=1, min=-50, max=50)
slider_ki = NonLinearSlider(win, 20, 410, plot, label= 'Ki', initial_value=1, min=-50, max=50)
slider_b = NonLinearSlider(win, 20, 460, plot, label= 'b', initial_value=1, min=0, max=1)

#Cria um botão para poder gerar uma forma de onda 
Button(win, text= "Sinal", command= wave_create.create_win).place(x = 20, y = 530, height= 30, width= 150)

x_time = 20
y_time = 310
label_time = Label(win, text="Tempo (s):")
label_time.place(x=x_time, y=y_time-3, height=30, width=80)
entry_time = Entry(win, bd=3)
entry_time.insert(0, str(time_))
entry_time.place(x=x_time+80, y=y_time, height=25, width=50)
Button(win, text= "Aplique", command= set_time).place(x = x_time+130, y = y_time-1, height= 25, width= 60)

#Plota os dados
plot()

#Habilita as funções de quando o botão do mouse é solto
win.bind("<ButtonRelease>", released)

#Deixa a página rodando
win.mainloop()   

