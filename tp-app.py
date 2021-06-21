from definitions import Environment, Agent
import numpy as np
import matplotlib.pyplot as plt

class ToilletPaperEnv(Environment):

    def __init__(self, nTP=10 , price=0.6):
        self.nTP = nTP
        self.price = price
        self.minTP = 10
        self.maxTP = 100

    def initial_percepts(self):
        return {'nTP' : self.nTP,
                'price' : self.price,
                'minTP' : self.minTP,
                'maxTP' : self.maxTP}

    def signal(self, action):
        self.nTP +=  action['buy']

        use = 8 + np.random.randn()*2
        self.nTP = max(self.nTP-use, 0) 
        self.price += 0.01 + np.random.randn()*0.005  

        return {'nTP' : self.nTP,
                'price' : self.price,
                'minTP' : self.minTP,
                'maxTP' : self.maxTP}

class TPAgent(Agent):

    def __init__(self, env):
        super().__init__(env)
        self.current_percepts = env.initial_percepts()
        self.average_price = self.current_percepts['price']
        self.n = 1
        self.tp_to_buy = 0


    def act(self):
        self.tp_to_buy = 0

        if self.current_percepts['nTP'] < self.current_percepts['minTP'] + 10:
            self.tp_to_buy =  self.current_percepts['minTP'] - self.current_percepts['nTP'] + 10
        elif (self.current_percepts['nTP'] < self.average_price*1.1):
           self. tp_to_buy = self.current_percepts['maxTP'] - self.current_percepts['nTP']

        self.current_percepts = self.env.signal({'buy': self.tp_to_buy})

        
        self.average_price = (self.average_price * self.n +  self.current_percepts['price'])/(self.n+1)
        self.n += 1 
        
class TPAgent2(TPAgent):
    
    def act(self):
        tp_to_buy = 0

        if self.current_percepts['nTP'] < self.current_percepts['minTP']:
            tp_to_buy =  self.current_percepts['minTP'] - self.current_percepts['nTP']
        elif (self.current_percepts['nTP'] < self.average_price):
            tp_to_buy = self.current_percepts['maxTP'] - self.current_percepts['nTP']

        self.current_percepts = self.env.signal({'buy': tp_to_buy})

        self.average_price = (self.average_price * self.n +  self.current_percepts['price'])/(self.n+1)
        self.n += 1 


if __name__ == "__main__":
    
    env1 = ToilletPaperEnv()
    env2 = ToilletPaperEnv()

    ag1 = TPAgent(env1)
    ag2 = TPAgent(env2)

    stock1 = []
    prices1 = []
    spendings1 = []

    stock2 = []
    prices2 = []
    spendings2 = []

    for i in range(1000):
        prices1.append(env1.price)
        n_prev = env1.nTP
        ag1.act()
        n_bought = env1.nTP - n_prev
        spendings1.append(n_bought*env1.price)
        stock1.append(env1.nTP)

        prices2.append(env2.price)
        n_prev = env2.nTP
        ag2.act()
        n_bought = env2.nTP - n_prev
        spendings2.append(n_bought*env2.price)
        stock2.append(env2.nTP)

    plt.plot(spendings1)
    plt.plot(spendings2)
    plt.show()

