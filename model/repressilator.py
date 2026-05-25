import numpy as np
from scipy.optimize import fsolve

class Repressilator:

    def __init__(self, alpha = 10, gamma = 1, n = 2):
        self.base_alpha = alpha
        self.base_gamma = gamma
        self.base_n = n

        self.alpha = alpha
        self.gamma = gamma
        self.n = n

    def update(self, state, u):
        P1, P2, P3 = state
        dP1 = u * self.alpha / (1 + P3**self.n) - self.gamma * P1
        dP2 = u * self.alpha / (1 + P1**self.n) - self.gamma * P2
        dP3 = u * self.alpha / (1 + P2**self.n) - self.gamma * P3

        return np.array([dP1, dP2, dP3])
    
    def equilibrium_eq(self, P, u):
        return u * self.alpha / (1 + P**self.n) - self.gamma * P
    
    def get_equilibrium(self, u):
        eq_point = fsolve(lambda P: self.equilibrium_eq(P, u), 1)[0]
        return eq_point
    
    def beta(self, u):
        P_eq = self.get_equilibrium(u)
        return u * self.alpha * self.n * (P_eq ** (self.n - 1)) / ((1 + P_eq ** self.n) ** 2)
    
    def regime(self, u):
        return self.beta(u) - 2 * self.gamma
    
    def simulate(self, initial_state, control = None, u0 = 1.0, dt = 0.01, t = 200):
        t_values = np.arange(0, t, dt)

        state = np.zeros((len(t_values), 3))
        u = np.zeros(len(t_values))
        r = np.zeros(len(t_values))
        p_eq = np.zeros(len(t_values))

        state[0] = initial_state
        u[0] = u0
        r[0] = self.regime(u[0])
        p_eq[0] = self.get_equilibrium(u[0])

        for i in range(len(t_values) - 1):
            curr_u = u[i]

            if control is not None:
                curr_u = control.update(curr_u, self.regime(curr_u), dt)
            
            u[i+1] = curr_u
            r[i+1] = self.regime(curr_u)
            p_eq[i+1] = self.get_equilibrium(curr_u)

            dx = self.update(state[i], curr_u)
            state[i+1] = state[i] + dx * dt

        return t_values, state, u, r, p_eq
    
    def noisy_simulate(self, initial_state, control = None, u0 = 1.0, dt = 0.01, t = 200):
        t_values = np.arange(0, t, dt)

        state = np.zeros((len(t_values), 3))
        u = np.zeros(len(t_values))
        r = np.zeros(len(t_values))
        p_eq = np.zeros(len(t_values))

        state[0] = initial_state
        u[0] = u0
        r[0] = self.regime(u[0])
        p_eq[0] = self.get_equilibrium(u[0])

        for i in range(len(t_values) - 1):
            curr_u = u[i]
            self.alpha = self.base_alpha + 0.1 * np.random.randn()
            self.gamma = self.base_gamma + 0.1 *np.random.randn()
            self.n = self.base_n + 0.05 * np.random.randn()

            if control is not None:
                curr_u = control.update(curr_u, self.regime(curr_u), dt)
            
            u[i+1] = curr_u
            r[i+1] = self.regime(curr_u)
            p_eq[i+1] = self.get_equilibrium(curr_u)

            dx = self.update(state[i], curr_u)
            state[i+1] = state[i] + dx * dt

        return t_values, state, u, r, p_eq
            