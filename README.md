# Analysis of synthetic repressillator system under PID control


This project studies the dynamics of a synthetic repressilator gene circuit under external control input \(u(t)\), and analyzes how feedback control can regulate oscillatory behavior near a Hopf bifurcation.

For this project, we analyze a 3-gene repressillator system with control input $\(u(t)\)$:

$\dot{P}_1 =u(t) \frac{\alpha}{1 + P_3^n} - \gamma P_1$

$\dot{P}_2 =u(t) \frac{\alpha}{1 + P_1^n}- \gamma P_2$

$\dot{P}_3 =u(t) \frac{\alpha}{1 + P_2^n}- \gamma P_3$

We define $x = \[P_1, P_2, P_3\]$. Therefore, $x = f(x, u)$

To find the equilibrium points, we assume symmetry $P_{eq} = P_1 = P_2 = P_3$

The equilibrium points are then given by the implicit relation $\gamma P_{eq} (1 + P_{eq}^n) = u(t) \alpha$. We note that $P_{eq}$ is a function of $u(t)$, this will be important later.

We then linearize near the equilibrium point by defining a perturbation $\delta x = x - x_{eq}$

We obtain the linear system $\delta \dot{x} = J(x_{eq}) \delta x$ where $J = \frac{\partial{f}}{\partial{x}} |\_{x = x_{eq}}$. We obtain the following matrix

$$
J =
\begin{bmatrix}
-\gamma & 0 & -\beta(u) \\
-\beta(u) & -\gamma & 0 \\
0 & -\beta(u) & -\gamma
\end{bmatrix}
$$

where $\beta(u) = u \frac{\partial}{\partial{P}} (\frac{\alpha}{1 + P^n}) |\_{P = P_{eq}}$

To determine the eigenvalues of the linear system, we solve the following equation $\det(J - \lambda I) = 0$. We obtain $\lambda + \gamma = \beta(u) (-1)^{\frac{1}{3}}$

The eigenvalues are then $\lambda_k = -\gamma + \beta(u) e^{i\frac{(2k+1)\pi}{3}}, k = 0, 1, 2$

We note that $\lambda_1 = -\gamma -\beta(u)$ is real, and $\lambda_{0,2} = -\gamma + \frac{\beta(u)}{2} \pm i \frac{\sqrt{3}}{2} \beta(u)$ are complex conjugate pairs. Hopf bifurcation occurs when the complex conjugate pairs become purely imaginary, meaning $\Re(\lambda_{0,2}) = 0$, which leads to the critical value of $\beta(u)$, $\beta_c = 2\gamma$

An important thing to note is that, since we have introduced time-varying control, the parameter $\beta$ is now a function of time and and subsequently eigenvalues evolve through time. This leads to local time-varying stability regimes relative to the Hopf bifurcation threshold.

We use a PID controller for the control input. We define the error as $e(t) = P_1(t) - P_{eq}$

The PID control law is then $u(t) = u_0 + K_p e(t) + K_i \int{e(\tau) d\tau} + K_d \frac{de(t)}{dt}$. For $u_0$, we want our system to reach a limit cycle since we want oscillations. For this we use the critical value we determine from the equality $\beta(u_c) = 2\gamma$, and choose a slightly higher value like $u_0 = 1.1u_c$ so the system remains above the Hopf bifurcation boundary in an oscillatory limit cycle regime.

A very important thing to point out about the PID controller is that, for the error term, $P_{eq}$ as we determined earlier is a function of $u(t)$, meaning it is time-varying, which leads to a circular problem where the target adapts to the control. To avoid this, we assume that $P_{eq}(t)$ varies slowly. This allows us to make the approximation $P_{eq}(t) \approx P_{eq}(t - \Delta t)$, allowing us to use the previous timestep. Therefore, we initialize the control input to be $u(0) = u_0$ to stay consistent with the operating regime we are aiming for.
