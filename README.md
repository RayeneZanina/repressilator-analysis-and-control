# Analysis of synthetic repressilator system under regime control


This project studies the dynamics of a synthetic repressilator gene circuit under external control input \(u(t)\) first in a symmetric system, then in an assymetric 1-control system, and analyzes how feedback control can regulate oscillatory behavior near a Hopf bifurcation.

For this project, we analyze a 3-gene repressilator system with control input $\(u(t)\)$:

$\dot{P}_1 =u(t) \frac{\alpha}{1 + P_3^n} - \gamma P_1$

$\dot{P}_2 =u(t) \frac{\alpha}{1 + P_1^n}- \gamma P_2$

$\dot{P}_3 =u(t) \frac{\alpha}{1 + P_2^n}- \gamma P_3$

Note that, we assume the control input changes the rate at which the protein is produced in a multiplicative way. We assume the control is between 0.2 and 5. 

We define $x = \[P_1, P_2, P_3\]$. Therefore, $\dot{x} = f(x, u)$

To find the equilibrium points, we assume symmetry $P_{eq} = P_1 = P_2 = P_3$. We simply need to solve $u(t) \frac{\alpha}{1 + P_{eq}^n} - \gamma P_{eq} = 0$. We can demonstrate a solution exists using the Intermediate Value theorem by setting $f(P) = u \frac{\alpha}{1 + P^n} - \gamma P$. $f$ is continuous on the interval $[0,\infty)$ with $f(0) = u\alpha > 0$ and $\lim\limits_{P \to \infty}f(P) = -\infty < 0$. Therefore, there exists a solution to the equation $f(P) = 0$. The solution can be determined numerically.

The equilibrium points are then given by the implicit relation $\gamma P_{eq} (1 + P_{eq}^n) = u(t) \alpha$. We note that $P_{eq}$ is a function of $u(t)$.

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

where $\beta(u) = -u \frac{\partial}{\partial{P}} (\frac{\alpha}{1 + P^n}) |\_{P = P_{eq}} = u \frac{\alpha n P_{eq}^{n-1}}{(1 + P_{eq}^n)^2}$. The negative sign is added to ensure $\beta > 0$

To determine the eigenvalues of the linear system, we solve the following equation $\det(J - \lambda I) = 0$. We obtain $\lambda + \gamma = \beta(u) (-1)^{\frac{1}{3}}$

The eigenvalues are then $\lambda_k = -\gamma + \beta(u) e^{i\frac{(2k+1)\pi}{3}}, k = 0, 1, 2$

We note that $\lambda_1 = -\gamma -\beta(u)$ is real, and $\lambda_{0,2} = -\gamma + \frac{\beta(u)}{2} \pm i \frac{\sqrt{3}}{2} \beta(u)$ are complex conjugate pairs. Hopf bifurcation occurs when the complex conjugate pairs become purely imaginary, meaning $\Re(\lambda_{0,2}) = 0$, which leads to the critical value of $\beta(u)$, $\beta_c = 2\gamma$

An important thing to note is that, since we have introduced time-varying control, the parameter $\beta$ is now a function of time and and subsequently eigenvalues evolve through time. This leads to local time-varying stability regimes relative to the Hopf bifurcation threshold.

To determine whether we can generalize the conclusion from the linearization near the equilibrium points to the entire system, we use an oscillation detector and compare its results to the hopf bifurcation boundary condition in a confusion matrix. 

<img width="744" height="455" alt="image" src="https://github.com/user-attachments/assets/928a60f4-5f75-484f-ba82-b27d4dae05d9" />

We can see that the linearization sometimes falsely predicts an oscillatory behaviour and displays a F1-score of 0.58. To try to understand this phenomenon, we can plot the points in parameter space for false positives and true negatives.

<img width="1587" height="855" alt="image" src="https://github.com/user-attachments/assets/242686ad-ce91-456e-a5e3-6f7fc284af87" />

We can see that the linearization doesn't generalize well for points with low $n$ and high $\alpha$, or for high $n$ and $\alpha \approx \gamma$. One way to explain this is that, for those parameters, the non-linearity of the model is more important, making the linearization less reliable. The linearization works well with the rest of the points. In the rest of the work, we study the Hopf condition, but we must keep in mind the regions where it isn't reliable. 

We first look at the system before any control input to try to determine the Hopf bifurcation boundary of the system.

<img width="1572" height="746" alt="image" src="https://github.com/user-attachments/assets/1834be99-0e52-43e0-9415-4103c6308c7f" />

The controller will then try to keep the regime close to the Hopf bifurcation boundary, slightly above it so that the oscillations do not die out. For this, we use a PID controller. Note that this controller will be regulating the parameter $u$, and has access to information directly from the system that is not accessible in real conditions. It is possible to infer these parameters from the dynamic evolution of the system by keeping a memory of the states. This can be approached in different ways, using a state estimator with an EKF or using a MLP fitted on generated data using the model (If I had to choose, I would probably go with this if it's reliable enough as it is a very fast way to recover the parameters).

For the PID, we define a quantity for the regime $r(u) = \beta(u) - 2 \gamma$. The error is then defined as $e = r(u) - r_{target}$ where $r_{target}$ can be manually decided, but should be positive and small. Note that, we are using the equation we derived that characterizes the regime, but it is only an approximation. That equation is only valid locally near the equilibrium point, but away from that point, the non-linearity makes the system less predictable. 

Another important point is the function $\beta(u)$. It's hard to tell what it looks like just by looking at it, considering $P_{eq}$ is itself a function of $u$ given by an implicit relation. I first investigated the function with different parameters, and the function has a horizontal asymptote that depends on $\gamma$ and $n$. $\alpha$ determines how fast the function increases. This means that, for some sets of parameters, $\beta(u)$ never exceeds $2 \gamma$, which means the system can never oscillate. 

To prove this, we determine $\lim\limits_{u \to \infty}\beta(u)$. For this we need to determine $\lim\limits_{u \to \infty}P_{eq}(u)$. We know that $\gamma P_{eq} (1 + P_{eq}^n) = u \alpha$. Assume $P_{eq}$ is bounded above by $M, M \in ℝ$. The left sign of the equation is then bounded by $\gamma M (1 + M^n)$ as the right side goes to infinity as $u \to \infty$, which creates a contradiction. Therefore, $\lim\limits_{u \to \infty}P_{eq}(u) = \infty$. We can then substitute $u$

$$\beta = u \frac{\alpha n P_{eq}^{n-1}}{(1 + P_{eq}^n)^2} = \frac{\gamma}{\alpha} P_{eq} (1 + P_{eq}^n) \frac{\alpha n P_{eq}^{n-1}}{(1 + P_{eq}^n)^2} = \frac{\gamma n P_{eq}^n}{1 + P_{eq}^n} $$

$$\lim\limits_{u \to \infty}\beta(u) = \lim\limits_{P_{eq} \to \infty} \frac{\gamma n P_{eq}^n}{1 + P_{eq}}$$ can then easily be seen to be $\gamma n$, which means for $n<2$, the system will exist below the Hopf bifurcation boundary no matter the control input, and will never be able to maintain its oscillations.

<img width="582" height="455" alt="image" src="https://github.com/user-attachments/assets/3cdacf6b-914c-4fbb-8be5-58fb17aaf43e" />

However, this does not mean that, for our system, we can reach non-decaying oscillations for every set of parameters as long as $n>2$, since our control is bounded by 5, which correspond to a 5-fold increase in protein production. We can then determine the region in parameter space for which the system under control can oscillate and where it cannot.

<img width="1572" height="746" alt="image" src="https://github.com/user-attachments/assets/89733115-eb65-4584-bda2-ffc0d6031821" />

We then simulate a system without the controller in the region of the parameter space that allows for oscillations.

<img width="567" height="455" alt="image" src="https://github.com/user-attachments/assets/9d7bc280-0926-4c3b-b010-4ac06d67057b" />
<img width="2396" height="855" alt="image" src="https://github.com/user-attachments/assets/69e90e1d-8937-4e45-9366-84b8b87d19fe" />

We then add the controller and simulate the system. We notice that the system reaches a limit cycle and is able to oscillate. 

<img width="567" height="455" alt="image" src="https://github.com/user-attachments/assets/1b37defb-ab71-4307-aca8-b89d9ec6fe5c" />
<img width="2396" height="855" alt="image" src="https://github.com/user-attachments/assets/f61ddf81-1318-499b-a903-f0a1eb1c5442" />

We can use Fast Fourier Transform to characterize how the system oscillates and extract the dominant frequency. $r_{target}$ changes the frequency as well as the amplitude of the oscillations.

<img width="622" height="547" alt="image" src="https://github.com/user-attachments/assets/bcf0cce7-51ec-441d-b753-e0b5e717a4a9" />

Although the controller is able to maintain the oscillations, all it does is actually maintain the control at the critical value, and simply computing the critical value and making it a constant leads to the same behaviour. However, the model might be imperfect, and the parameters might change. Using the initial critical value as a constant in a noisy simulation leads to slight decay of the oscillations, although the system does manage to maintain its oscillatory behaviour. 

<img width="567" height="455" alt="image" src="https://github.com/user-attachments/assets/a4efeea3-adb7-4ba5-a4dc-8f112dc68ca3" />

The regime indicator shows many instances where the Hopf bifurcation boundary is crossed and the regime indicator becomes negative, indicating decay of the oscillations. Note that this means decay of the oscillations if the parameters are kept constant, however we can imagine that over time, repeated crossing of the boundary might lead to the oscillations slowly decaying. 

<img width="578" height="455" alt="image" src="https://github.com/user-attachments/assets/1fd407c1-fdc6-4c8e-bd4a-3a2f343802a3" />

Now, we add the controller. We notice that the system is able to maintain its oscillations pretty well.

<img width="567" height="455" alt="image" src="https://github.com/user-attachments/assets/603d879b-775f-4894-9480-6709b7bce3ce" />

The regime indicator shows a much more stable regime, in the sense that it becomes negative less often and stays closer to $r_{target}$

<img width="587" height="455" alt="image" src="https://github.com/user-attachments/assets/51c2a765-121d-48b7-b191-eefe7beb32e7" />

To conclude on the PID controller for this system, it has two main functions. First, it expands the region in parameter space where the system can maintain its oscillations by changing the control input ($u\alpha$ can be viewed as one parameter $\alpha'$ with a wider range of values). Second, the controller is able to dynamically change its input in response to a change in the parameter values used in the model.

This system however isn't really interesting from a biological standpoint. A setup where all proteins are controlled by the same control is unrealistic. A more interesting and more complex system is then studied. We imagine that $P_1$ is the target protein that we want to make oscillate, but we can only control $P_3$. We can then model the system as follows:

$\dot{P}_1 =\frac{\alpha}{1 + P_3^n} - \gamma P_1$

$\dot{P}_2 =\frac{\alpha}{1 + P_1^n}- \gamma P_2$

$\dot{P}_3 =u(t) \frac{\alpha}{1 + P_2^n}- \gamma P_3$

The system is no longer symmetric, so we need to solve the system:

$\frac{\alpha}{1 + P_3^n} = \gamma P_1$

$\frac{\alpha}{1 + P_1^n} = \gamma P_2$

$u(t) \frac{\alpha}{1 + P_2^n} = \gamma P_3$

Since we can't use symmetry, we must use a different approach to show that there exists a solution. We define the vector-valued function $f(x) = \[f_1(x), f_2(x), f_3(x)\]$ with $x = \[P_1, P_2, P_3\]$ such that 

$f_1(x) = \frac{\alpha}{\gamma (1 + P_3^n)}$

$f_2(x) = \frac{\alpha}{\gamma (1 + P_1^n)}$

$f_3(x) = u(t) \frac{\alpha}{\gamma (1 + P_2^n)}$

We note that $f$ is continuous, and $0 < f_1(x) \leq  \frac{\alpha}{\gamma}, 0 < f_2(x) \leq \frac{\alpha}{\gamma}, 0 < f_3(x) \leq u_{max}\frac{\alpha}{\gamma}$ We can then define the set  $K = \[0, \frac{\alpha}{\gamma}\] \times \[0, \frac{\alpha}{\gamma}\] \times \[0, u_{max}\frac{\alpha}{\gamma}\]$. $K$ is a closed and bounded cubic subset of $ℝ^3_+$, making it convex and compact. By construction, $f(ℝ^3_+) \subseteq K$, and $K \subseteq ℝ^3_+$, meaning $f(K) \subseteq K$. Using the Brouwer's fixed point theorem, we can then conclude that there exists a solution to the equation $f(x) = x$. The solution can then be determined numerically

We can now linearize the system similarly to how we approached the first system. We use a similar definition for $\beta$ : $\beta(P_{eq}) = \frac{\alpha n P_{eq}^{n-1}}{(1 + P_{eq}^n)^2}$, with $\beta_1 = \beta(P_{eq,1})$

We obtain the linear system $\delta \dot{x} = J(x_{eq}) \delta x$ with 

$$
J =
\begin{bmatrix}
-\gamma & 0 & -\beta_1 \\
-\beta_2 & -\gamma & 0 \\
0 & -u\beta_3 & -\gamma
\end{bmatrix}
$$

We determine the eigenvalues of the matrix. We obtain $\lambda + \gamma = (-u \beta_1 \beta_2 \beta_3)^{\frac{1}{3}}$

We obtain the following eigenvalues $\lambda_k = -\gamma + (u \beta_1 \beta_2 \beta_3)^{\frac{1}{3}} e^{i\frac{(2k+1)\pi}{3}}, k = 0, 1, 2$

Similarly to the previous system, $\lambda_1 = -\gamma - (u \beta_1 \beta_2 \beta_3)^{\frac{1}{3}}$ is real, and $\lambda_{0,2} = -\gamma + \frac{1}{2} (u \beta_1 \beta_2 \beta_3)^{\frac{1}{3}} \pm i \frac{\sqrt{3}}{2} (u \beta_1 \beta_2 \beta_3)^{\frac{1}{3}}$ 

The Hopf bifurcation boundary occurs then at $\Re(\lambda_{0,2}) = 0$, which leads to the equation $u \beta_1 \beta_2 \beta_3 = 8 \gamma^3$. This the asymmetric version of the critical value for the first system.

Due to the asymmetry of the system, $\beta$ for the different proteins evolve differently with respect to $u$. This means the regime indicator doesn't simply increase as $u$ increases, and we need to find $u_c$ to reach the target regime. This makes the parameter sweep more expensive computationally. To find regions where the system doesn't normally oscillate, but we can introduce oscillations with control (without simulating for too long), we first sweep for 25x25x25 parameters, then use KNN to smoothen out the region. To prevent data imbalance since there are more points that don't oscillate, we take points where control introduces oscillations and add small perturbations. We also add more points around the boundary of the prediction to smoothen out the edges. We then pass the probability through a sigmoid function for the opacity for the visualization. We check for oscillations rather than using the regime indicator as we saw it isn't very reliable.

<img width="957" height="820" alt="image" src="https://github.com/user-attachments/assets/1b0b0c27-495f-47bd-988b-e087e06467c2" />

We can then take a new system before any control input within this region.

<img width="567" height="455" alt="image" src="https://github.com/user-attachments/assets/658d0cfe-3dd4-4915-a935-f9813f9a6911" />

We can then introduce the controller to introduce the oscillations.

<img width="576" height="455" alt="image" src="https://github.com/user-attachments/assets/cd3bbc67-08cb-4fbf-b9a2-0e3848dd7ea3" />

<img width="2396" height="855" alt="image" src="https://github.com/user-attachments/assets/cabd497c-eae7-4f70-abf8-069f1c47b16b" />

We notice that because of the asymmetry, the proteins oscillate around different equilibrium values, but they all exhibit the same amplitude and dominant frequency.

Adding control is also able to recover oscillations if added after a latency.

<img width="576" height="455" alt="image" src="https://github.com/user-attachments/assets/91f62ceb-5bfb-46d6-8e96-741c03b42b70" />



Reference I used: 
J. Bois and M. Elowitz, “Blinking bacteria: The repressilator enables self-sustaining oscillations,” Caltech.edu, 2019. http://be150.caltech.edu/2019/handouts/08_repressilator.html.




