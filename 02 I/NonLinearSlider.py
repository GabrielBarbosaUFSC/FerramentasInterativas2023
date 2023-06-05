#Implementa a classe de Sliders não lineares

from tkinter import*

class NonLinearSlider:
    def __init__ (self, win, pos_x, pos_y, plot_func, label, min = -25, max = 25, non_zero = False, initial_value = 0):
        self.non_zero = non_zero #Armazena se a variavel pode ser igual a zero
        self.pos_x = pos_x
        self.pos_y = pos_y
         #Inicializa Valores os valores a depender de se ele pode ou n ser zero
        if initial_value != 0: 
            self.new_value = initial_value 
            self.old_value = initial_value  
        else:
            self.new_value = (non_zero)*0.01 
            self.old_value = 1

        self.label_name = label #Salva a Label como propriedade
        self.disable = False #Desabilita a atualização do valor de K com o movimento da barra
        self.min = min  #Limite minímo do valor de K
        self.max = max  #Limite máximo do valor de K
        self.plot_func = plot_func
        #Cria o Slider da biblioteca do tkinter
        self.scale = Scale(win, from_= -10, to=10, orient= HORIZONTAL, command=self.update_motion, resolution= 0.1, length=200, repeatdelay=50, showvalue=0, sliderlength= 15)
        self.scale.set(0) #Inicializa ele em 0
        
        self.value_string = StringVar(master= win) #Cria um texto variável que irá mostrar o valor de K
        self.label = Label(win, textvariable = self.value_string) #Cria uma label pra mostrar esse texto variável
        
        self.value_string.set(f'{self.label_name} = {self.new_value:00}') #Define o valor inicial
    
        self.input_string = StringVar(master= win) #Cria outro texto variável para receber o valor de K escrito manualmente
        self.input = Entry(win, textvariable= self.input_string) #Cria um entrada do tkinter
        
        self.button = Button(win, command = self.update_button, text= "Aplique") #Cria um botão que será usado para setar o K
        self.show()
   
    def get(self): #Retorna o valor de K
        return self.new_value
    
    def update_motion(self, param): #Atualiza o valor de K se o slider estiver se movido
        if self.disable: #Desabilita isso a causa do movimento tiver sido a recentralização depois que vc solta o switch
            self.disable = False  #Habilita após ignorar uma vez  
            return self.new_value # Retorna o valor sem alterar ele

        temp = self.scale.get()**3/500 #aplica um função no valor da escala linear do tkinter

        #Manipulação necessária pra manter a ferramenta intuitiva quando o valor é negativo
        if self.old_value < 0: 
            temp = -temp

        temp = self.old_value*(1+temp) #Aplica esse valor obtido no restante da função

        #Limita o valor de K
        if temp < self.min:
            temp = self.min
        if temp > self.max:
            temp = self.max
            
        #Ignora as casas após os centésimos na notação decimal
        temp = (temp*1000)//1 
        temp = temp/1000

        #Atribui esse valor a K
        if temp == 0 and self.non_zero:
            temp = (-1+2*(self.old_value > 0))*0.01
        self.new_value = temp

        #Atualiza o valor de K na label em que ele é mostrado
        self.value_string.set(f'{self.label_name} = {self.new_value}')
        self.plot_func()
        #return self.new_value #Retorna o novo valor de K

    def update_released(self):
        #Atualiza o valor que é usado como base
        #Se o valor passado for igual a zero, você fica preso em 0, já que qualquer coisa vezes 0 é 0
        if self.new_value == 0:
            self.old_value = 1
        else:
            self.old_value = self.new_value 
          
        self.disable = True # Desabilita a atualização de valores quando o slider é mudado de posição 
        self.scale.set(0) #Reposiciona o slider em 0

    def update_button(self):
        #Tenta converter o valor escrito na seleção manual em um número. Se não conseguir, ele atribui 0 ao valor em questão
        try:
            temp = float(self.input_string.get()) 
        except:
            temp = 0 
        self.update_values(temp)

    def update_values(self, temp):
        self.input_string.set("")
        #Limita o valor máximo
        if temp > self.max:
            temp = self.max 
        if temp < self.min:
            temp = self.min
        if temp == 0 and self.non_zero:
            temp = 0.1
        #Atualiza as variáveis necessárias 
        self.new_value = temp
        self.update_released()
        self.value_string.set(f'{self.label_name} = {self.new_value}')
        self.plot_func()

    #Mostra o sldier
    def show(self):
        self.scale.place(x= self.pos_x, y = self.pos_y+20) #Posiciona ele
        self.label.place(x = self.pos_x, y = self.pos_y) #Posiciona a label
        self.input.place(x = self.pos_x + 90, y = self.pos_y, width= 50, height= 20) #Posiciona essa entrada de dados
        self.button.place(x = self.pos_x + 140, y = self.pos_y, width=60, height= 20) #Posiciona o botão

    #Esconde o slider
    def hide(self):
        self.scale.place_forget()
        self.label.place_forget()
        self.input.place_forget()
        self.button.place_forget()

    #Seta a etiqueta e o valor do slider
    def set_params(self, label, min = -25, max = 25, non_zero = False, initial_value = 0):
        self.label_name = label
        self.min = min
        self.max = max
        self.non_zero = non_zero
        self.update_values(initial_value)
    