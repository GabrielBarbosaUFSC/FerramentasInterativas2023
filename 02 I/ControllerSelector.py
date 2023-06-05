from enum import Flag
from tkinter import ttk
from turtle import pos
from NonLinearSlider import* 

class ControllerSelector:
    def __init__(self, win, pos_x, pos_y, plot):
        self.win = win
        self.plot = plot
        self.state = 0

        self.n = StringVar()
        self.ctrlselector = ttk.Combobox(self.win, width = 10, textvariable = self.n)
        self.ctrlselector['values']=['P', 'PI', 'PD', 'PID']
        self.ctrlselector.place(x= pos_x, y = pos_y)
        
        self.sliders = [NonLinearSlider(self.win, pos_x, 30 + pos_y + 50*i, plot, label="") for i in range(5)]
        for slider in self.sliders:
            slider.hide()
        
        self.ctrlselector.set('P')
        self.select(0)
        self.ctrlselector.bind('<<ComboboxSelected>>', self.select)

    def select(self, event):
        labels = []
        initial_values = []
        max = []
        min = []
        non_zero = []

        if self.ctrlselector.get() == 'P':
            labels = ['Kp', 'bias']
            initial_values = [1, 0]
            max = [25, 25]
            min = [-25, -25]
            non_zero = [False, False]

        elif self.ctrlselector.get() == 'PI':
            labels = ['Kp', 'Ki', 'b', 'Ks']
            initial_values = [1, 1, 1, 0]
            max = [25, 25, 1, 25]
            min = [-25, -25, 0, -25]
            non_zero = [False, False, False, False]

        elif self.ctrlselector.get() == 'PD':
            labels = ['Kp', 'Kd', 'bias']
            initial_values = [1, 1, 0]
            max = [25, 25, 25]
            min = [-25, -25, -25]
            non_zero = [False, False, False]

        elif self.ctrlselector.get() == 'PID':
            labels = ['Kp', 'Ki', 'Kd', 'b', 'Ks']
            initial_values = [1, 1, 1, 1, 0]
            max = [25, 25, 25, 1, 25]
            min = [-25, -25, -25, 0, -25]
            non_zero = [False, False, False, False, False]

        for i in range(len(self.sliders)):
            if i >= len(labels):
                self.sliders[i].hide()
            else:
                self.sliders[i].set_params(labels[i], min[i], max[i], non_zero[i], initial_values[i])
                self.sliders[i].show()
        
    def released(self):
        for slider in self.sliders:
            slider.update_released()

    def get_params(self):
        params = [] #[Kp, Ki, Kd, b, Ks, bias]

        if self.ctrlselector.get() == 'P':
            params = [
                self.sliders[0].get(),
                0,
                0,
                1,
                0,
                self.sliders[1].get()
            ]
        elif self.ctrlselector.get() == 'PI':
            params = [
                self.sliders[0].get(),
                self.sliders[1].get(),
                0,
                self.sliders[2].get(),
                self.sliders[3].get(),
                0
            ]
        elif self.ctrlselector.get() == 'PD':
            params = [
                self.sliders[0].get(),
                0,
                self.sliders[1].get(),
                1,
                0,
                self.sliders[2].get()
            ]
        elif self.ctrlselector.get() == 'PID':
            params = [
                self.sliders[0].get(),
                self.sliders[1].get(),
                self.sliders[2].get(),
                self.sliders[3].get(),
                self.sliders[4].get(),
                0
            ]

        return params