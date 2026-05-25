import numpy as np

class PID:

    def __init__(self, kp=0.05, ki=0, kd=0, target_regime=0.5, umin=0.2, umax=5.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target_regime = target_regime
        
        self.umin = umin
        self.umax = umax

        self.integral = 0
        self.derivative = 0
        self.prev_error = 0

    def update(self, curr_u, current_regime, dt):
        error = self.target_regime - current_regime
        
        self.integral += error * dt
        self.derivative = (error - self.prev_error) / dt
        new_u = curr_u + self.kp * error + self.ki * self.integral + self.kd * self.derivative

        self.prev_error = error
        return  np.clip(new_u, self.umin, self.umax)
    