import numpy as np
import matplotlib.pyplot as plt
from casadi import *

# NMPC parameters
T = 0.05  # Time step
N = 30   # Prediction horizon
robot_speed = 1.0  # Constant robot speed

# Define robot model
def robot_model(x, u):
    px, py, theta = x[0], x[1], x[2]
    v, omega = u[0], u[1]

    # Unicycle model equations
    px_next = px + T * v * cos(theta)
    py_next = py + T * v * sin(theta)
    theta_next = theta + T * omega

    return vertcat(px_next, py_next, theta_next)

# Define cost function (tracking waypoints and penalizing control input changes)
def stage_cost(x, ref, u, u_prev, weight_control=0.01):
    weight_position = 100  # Penalty for position tracking error
    weight_smooth = weight_control  # Penalty for control effort
    position_error = (x[0] - ref[0])**2 + (x[1] - ref[1])**2
    control_smoothing = weight_smooth * ((u[0] - u_prev[0])**2 + (u[1] - u_prev[1])**2)
    return weight_position * position_error + control_smoothing

# Generate a track (circular waypoints for simplicity)
def generate_track(num_points=200, radius=5.0):
    waypoints = []
    for i in range(num_points):
        theta = 2 * np.pi * i / num_points
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        waypoints.append([x, y])
    return np.array(waypoints)

# NMPC setup
def nmpc_controller():
    x = MX.sym('x', 3)  # Current state: [px, py, theta]

    U = MX.sym('U', 2, N)  # Control over horizon
    X = MX.sym('X', 3, N+1)  # State over horizon
    ref = MX.sym('ref', 2, N)  # Reference over horizon

    # Initialize cost function and dynamics constraints
    cost = 0
    g = []

    # Starting state constraint
    g.append(X[:, 0] - x)

    # Initial guess for the previous control input
    u_prev = MX([robot_speed, 0.0])

    # Loop through the prediction horizon
    for i in range(N):
        # Update cost with control input and smoothing
        cost += stage_cost(X[:, i], ref[:, i], U[:, i], u_prev)

        # Predict the next state
        x_next = robot_model(X[:, i], U[:, i])
        g.append(X[:, i+1] - x_next)

        # Update u_prev for the next iteration
        u_prev = U[:, i]

    # Stack constraints vertically
    opt_variables = vertcat(X.reshape((-1, 1)), U.reshape((-1, 1)))
    opt_constraints = vertcat(*g)

    # Define the NLP problem with parameters
    nlp = {
        'x': opt_variables,
        'f': cost,
        'g': opt_constraints,
        'p': vertcat(x, ref.reshape((-1, 1)))
    }

    # Define optimizer
    opts = {"ipopt.print_level": 0, "print_time": 0}
    solver = nlpsol('solver', 'ipopt', nlp, opts)

    return solver

# Main simulation loop
def simulate_nmpc(waypoints, num_steps=200):
    solver = nmpc_controller()
    x0 = np.array([0.0, 0.0, 0.0])  # Starting at origin
    u_prev = np.array([robot_speed, 0.0])  # Initial control guess
    states = [x0]

    for t in range(num_steps):
        # Get reference (next set of waypoints)
        idx = np.arange(t, t + N) % len(waypoints)
        ref_traj = waypoints[idx].T  # Shape (2, N)

        # Initial guesses for optimization variables
        X0 = np.tile(x0.reshape(-1, 1), N+1)
        U0 = np.tile([robot_speed, 0.0], (N, 1))  # Start with constant forward motion

        # Prepare parameters
        p = np.concatenate([x0, ref_traj.flatten()])

        # Solve NMPC problem
        initial_guess = np.concatenate([X0.flatten(), U0.flatten()])
        solution = solver(x0=initial_guess, lbg=0, ubg=0, p=p)

        # Extract optimal control
        opt_result = solution['x'].full().flatten()
        X_opt = opt_result[:3*(N+1)].reshape((3, N+1))
        U_opt = opt_result[3*(N+1):].reshape((2, N))

        # Apply control and update state
        u0 = U_opt[:, 0]
        x0 = robot_model(x0, u0).full().flatten()
        u_prev = u0  # Update previous control
        states.append(x0)

    return np.array(states)

# Visualization
def visualize_simulation(track, states):
    plt.figure(figsize=(8, 8))
    plt.plot(track[:, 0], track[:, 1], 'r--', label='Track')
    plt.plot(states[:, 0], states[:, 1], 'b-', label='Robot Path')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('NMPC Robot Track Following')
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# Generate circular track
waypoints = generate_track()
# Simulate NMPC
states = simulate_nmpc(waypoints)
# Visualize result
visualize_simulation(waypoints, states)


