import casadi as ca
import numpy as np
import matplotlib.pyplot as plt

# Time step and prediction horizon
dt = 0.1  # Time step [s]
N = 20  # Prediction horizon (number of steps)

# Boat parameters
L = 2.5  # Wheelbase/distance between the two motors (affects turning radius)
max_thrust = 1.0  # Max thrust for each motor

# Define symbolic variables for boat state
x = ca.SX.sym('x')  # x position
y = ca.SX.sym('y')  # y position
theta = ca.SX.sym('theta')  # heading angle

# Define control inputs (thrust for left and right motors)
T_left = ca.SX.sym('T_left')  # Left motor thrust
T_right = ca.SX.sym('T_right')  # Right motor thrust

# Boat dynamics
v = (T_left + T_right) / 2  # Linear velocity (average thrust)
omega = (T_right - T_left) / L  # Angular velocity (difference in thrust)

# State update equations
xdot = v * ca.cos(theta)
ydot = v * ca.sin(theta)
thetadot = omega

# State and control vectors
state = ca.vertcat(x, y, theta)
controls = ca.vertcat(T_left, T_right)

# Define boat dynamics function
f = ca.Function('f', [state, controls], [ca.vertcat(xdot, ydot, thetadot)])

# Create symbolic optimization problem
U = ca.SX.sym('U', 2, N)  # Control inputs over the prediction horizon (thrusts)
P = ca.SX.sym('P', 6)  # Initial state (x, y, theta) and target state (x_ref, y_ref, theta_ref)

# State trajectory matrix
X = ca.SX.sym('X', 3, N+1)

# Initialize cost function and constraints
cost = 0
g = []

# Set the initial state
X[:, 0] = P[0:3]

# Define target state (goal)
target = P[3:6]

# Cost function weights
Q = np.diag([10, 10, 5])  # State error weights
R = np.diag([1, 1])  # Control effort weights

# Loop over the prediction horizon to calculate cost and constraints
for k in range(N):
    # Predict the next state using the boat's dynamics
    X_next = X[:, k] + dt * f(X[:, k], U[:, k])
    X[:, k+1] = X_next

    # Cost: minimize error to target and control effort
    state_error = X[:, k+1] - target
    cost += ca.mtimes([state_error.T, Q, state_error]) + ca.mtimes([U[:, k].T, R, U[:, k]])

    # Constraints: system dynamics must hold
    g.append(X_next - X[:, k+1])

# Flatten constraints
g = ca.vertcat(*g)

# Optimization variables
opt_vars = ca.vertcat(ca.reshape(U, -1, 1))

# Define the optimization problem
nlp = {'x': opt_vars, 'f': cost, 'g': g, 'p': P}

# Solver options
opts = {'ipopt.print_level': 0, 'print_time': 0, 'ipopt.max_iter': 500}
solver = ca.nlpsol('solver', 'ipopt', nlp, opts)

# Function to simulate NMPC for the differential drive boat
def nmpc_controller(initial_state, target_state):
    P_val = np.concatenate((initial_state, target_state))
    
    u0 = np.zeros((N, 2))  # Initial guess for controls
    
    # Control bounds (thrust limits)
    lbx = np.tile([-max_thrust, -max_thrust], N)
    ubx = np.tile([max_thrust, max_thrust], N)
    
    # Solve optimization problem
    sol = solver(x0=u0.flatten(), lbx=lbx, ubx=ubx, p=P_val)
    
    u_opt = sol['x'].full().reshape(N, 2)
    
    return u_opt[0, :]  # Return first control input

# Simulate the NMPC-controlled boat trajectory
def simulate_nmpc(initial_state, target_state, total_time):
    state = np.array(initial_state)
    trajectory = [state]

    for t in np.arange(0, total_time, dt):
        u = nmpc_controller(state, target_state)
        
        # Update the state using boat dynamics
        v = (u[0] + u[1]) / 2
        omega = (u[1] - u[0]) / L
        x_dot = np.array([v * np.cos(state[2]), v * np.sin(state[2]), omega])
        
        state = state + dt * x_dot
        trajectory.append(state)

    return np.array(trajectory)

# Initial and target states
initial_state = [0, 0, 0]  # (x, y, theta)
target_state = [10, 10, np.pi/4]  # (x_ref, y_ref, theta_ref)

# Simulate for 10 seconds
trajectory = simulate_nmpc(initial_state, target_state, total_time=10)

# Plot the trajectory
plt.figure()
plt.plot(trajectory[:, 0], trajectory[:, 1], 'b-', label='NMPC Trajectory')
plt.plot(target_state[0], target_state[1], 'rx', label='Target')
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('NMPC Trajectory for Differential Drive Boat')
plt.legend()
plt.grid(True)
plt.show()

