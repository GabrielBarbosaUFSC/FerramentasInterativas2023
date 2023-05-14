import numpy as np

class sim_on_off: 
    def __init__(self):
        self.noise = np.random.normal(0, 0.001, 500)    #Cria uma lista para simular o ruido branco
        self.tn = 0.1   #Tempo de simulação
        self.t = [i*self.tn for i in range(500)] #Lista com os pontos do tempo

        #Planta: y[k] = cte_y*y[k-1] + cte_u*u[k] + cte_q*q[k] 
        self.cte_y = 0 
        self.cte_u = 0
        self.cte_q = 0

        #Limites de saturação
        self.u_max = 5
        self.u_min = -5

        self.tau = 0
        self.l = 0

    def set_plant(self, tau, u_max, u_min, ke, kq, l):     #Define os parametros da planta
        #Utilizando uma aproximação de dy/dt = (y[k] - y[k-1])/ts
        self.tau = tau

        #Atualiza os parâmetros da planta
        self.cte_y = tau/(self.tn+tau)
        self.cte_u = (ke*self.tn)/(self.tn+tau)
        self.cte_q = (kq*self.tn)/(self.tn+tau)
        self.u_max = u_max
        self.u_min = u_min 
        self.kq = kq
        self.ke = ke
        self.l = l
    
    def saturation(self, v): #Retorna os valores de atuação considerando a saturação
        if v > self.u_max:
            return self.u_max
        if v < self.u_min:
            return self.u_min
        return v

    def get_params(self):
        return [self.tau, self.u_max, self.u_min, self.ke, self.kq, self.l]

    def plot(self, setpoint, qe, phi_noise, amp_noise, kp, ki, kd, u = 0):
        amp_noise *= 10
        sp_len = len(setpoint)

        noise = [amp_noise*self.noise[i]*(self.t[i]>phi_noise) for i in range(len(self.t))]

        #Ajusta a lista da perturbação de acordo com o tamanho da lista do setpoint
        if len(qe) < sp_len:
            self.q = qe + [0]*(sp_len-len(qe))
        if len(qe) == sp_len:
            self.q = qe
        if len(qe) > sp_len:
            self.q = qe[0:sp_len]

        #Ajusta a lista de controle, se ela existir
        if u != 0:
            if len(u) < sp_len:
                self.q = u + [0]*(sp_len-len(u))
            if len(u) == sp_len:
                self.u = u
            if len(u) > sp_len:
                self.u = u[0:sp_len]
        else:
            self.u = [0]*sp_len

        self.ue = [(1/self.ke)*(setpoint[i] - self.kq*self.q[i]) for i in range(sp_len)]

        self.u[1] = self.u[0] = 0
        temI = 0 
        #Cria listas com o mesmo tamanho do setpoint
        self.y = [0]*sp_len

        it = int((self.l//self.tn) )
        pasterror = 0
        sat = 0
        #Roda N-2 iterações 
        for i in range(2, sp_len):
            if i <= (it + 2):
                self.y[i] = noise[i]
            else:
                self.y[i] =  self.cte_y*self.y[i-1] + self.cte_u*self.u[i-1-it] + self.cte_q*qe[i-1-it] + noise[i]   #Calcula o valor de y, y[k] = cte_y1*y[k-1] + cte_u*u[k] + cte_q*q[k] + noise
 
            #Verifica se você quer usar o sinal de controle do criador de wave forms
            if u == 0: 
                error = setpoint[i] - self.y[i]
                temP = kp*error
                temI += self.tn*ki*(error+pasterror)/2
                temD = -(self.y[i]-self.y[i-1])/self.tn*kd
                pasterror = error
                self.u[i] = self.saturation(temP+temI+temD) 
                
    def get_time(self):
        return self.t
    
    def set_time(self, time, plot):
        self.t = [time/500*i for i in range(500)]
        self.tn = time/500
        plot()