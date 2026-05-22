# Analysis of synthetic repressillator system and control design


This project studies the dynamics of a synthetic repressilator gene circuit under external control input \(u(t)\), and analyzes how feedback control can regulate oscillatory behavior near a Hopf bifurcation.

For this project, we analyze a 3-gene repressillator system with control input $\(u(t)\)$:

$\dot{P}_1 =u(t) \frac{\alpha}{1 + P_3^n} - \gamma P_1$

$\dot{P}_2 =u(t) \frac{\alpha}{1 + P_1^n}- \gamma P_2$

$\dot{P}_3 =u(t) \frac{\alpha}{1 + P_2^n}- \gamma P_3$

We define $x = \[P_1, P_2, P_3\]$. Therefore, $x = f(x, u)$

To find the equilibrium points, we assume symmetry $P_{eq} = P_1 = P_2 = P_3$

The equilibrium points are then given by the implicit relation $\gamma P_{eq} (1 + P_{eq}^n) = u(t) \alpha$. We note that $P_{eq}$ is a function of $u$

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
