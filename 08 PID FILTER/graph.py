#Classe para manipular o gráfico do programa

#importa as bibliotecas necessárias
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


class Graph:
    def __init__(self, win, pos_x, pos_y, t, t_label, y_label):
        self.fig = Figure(figsize = (7, 3), dpi = 100, layout = 'tight')  #Define o tamanho da figura  
        self.canvas = FigureCanvasTkAgg(self.fig, master = win) #Habilita a figura como widget do programa 
        
        self.canvas.get_tk_widget().place(x= pos_x, y = pos_y) #Posiciona a figura no aplicativo

        #Define as labels como propriedades da classe
        self.t = t
        self.tlabel = t_label 
        self.ylabel = y_label
        self.labels = []
        self.data = []  #Cria um pacote de dados para as curvas
        self.plot_area = self.fig.add_subplot(1, 1, 1) #Adiciona um área para plotagem na figura 
        self.flag = False #Cria uma flag para indicar novas plotagens
        self.thread = threading.Thread(target=self.thread_func) #Cria uma thread para cuidar do gráfico
        self.thread.daemon = True #Faz com que a thread seja deletada quando o programa é fechado
        self.thread.start() #Inicia a thread

    #Plota os dados em y
    def plot(self): 
        self.plot_area.clear() #apaga os dados antigos do gráfico
        if len(self.labels) != 0:
            for i in range(len(self.labels)):
                self.plot_area.plot(self.t(), self.data[i], label = self.labels[i]) #plota os dados no gráfico
            
            self.plot_area.legend(loc = "lower right") #Adiciona legendas
            self.plot_area.set_xlabel(self.tlabel) #Adiciona labels
            self.plot_area.set_ylabel(self.ylabel) #Adiciona labels
            self.plot_area.grid() #Adiciona grades
            self.canvas.draw() #Mostra os dados na figura

    #Cria uma task baseada em um loop com updates a cada 20 ms
    def thread_func (self):
        while True:
            #Se tiver algum dado novo, ele plota os dados e zera a flag
            if self.flag:
                self.plot()
                self.flag = False
            else: #Se não ele só espera 20ms
                time.sleep(0.02)

    def set_data(self, data, labels):
        self.data = data
        self.labels = labels
        self.flag = True