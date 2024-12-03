def create_matrix(rows, cols, default=0.0):
    """Create a matrix filled with the default value."""
    return [[default for _ in range(cols)] for _ in range(rows)]

import numpy as np
def gaussian_elimination(A, b):
    """
    Solve system of linear equations Ax = b using Gaussian elimination with partial pivoting.
    Returns the solution vector x.
    """
    n = len(A)
    # Create augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination with partial pivoting
    for i in range(n):
        # Find pivot
        max_element = abs(M[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > max_element:
                max_element = abs(M[k][i])
                max_row = k

        # Swap maximum row with current row
        M[i], M[max_row] = M[max_row], M[i]

        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            if abs(M[i][i]) < 1e-10:  # Numerical stability check
                continue
            c = -M[k][i] / M[i][i]
            for j in range(i, n + 1):
                if i == j:
                    M[k][j] = 0
                else:
                    M[k][j] += c * M[i][j]

    # Back substitution
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        if abs(M[i][i]) < 1e-10:  # Numerical stability check
            continue
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]

    return x


def stationary_distribution(p, q, r, N):
    """
    Compute the stationary distribution of a Markov chain given the transition probabilities.

    Parameters:
    - p: Probabilities of transitioning to the next state.
    - q: Probabilities of transitioning to the previous state.
    - r: Probabilities of staying in the current state.
    - N: Number of total states.

    Returns:
    - List containing the stationary distribution, with size N+1.
    """

    # Create a (N+1) x (N+1) matrix filled with zeros to set up equations
    transition_matrix = np.zeros((N + 1, N + 1))

    # Populate the matrix using given probabilities
    for index in range(N + 1):
        transition_matrix[index, index] = r[index]  # Self-loop probability
        if index > 0:
            transition_matrix[index, index - 1] = q[index]  # Transition to previous state
        if index < N:
            transition_matrix[index, index + 1] = p[index]  # Transition to next state

    # Formulate the equation system for the stationary distribution
    equation_matrix = np.eye(N + 1) - transition_matrix.T
    equation_matrix = np.vstack([equation_matrix, np.ones(N + 1)])  # Add sum constraint
    solution_vector = np.zeros(N + 2)
    solution_vector[-1] = 1  # The constraint to ensure the probabilities sum to 1

    # Solve the linear system to find the stationary distribution
    distribution = np.linalg.lstsq(equation_matrix, solution_vector.T, rcond=None)[0]

    # Return the distribution as a list of floats
    return [float(probability) for probability in distribution]


def expected_time(p, q, r, N, a, b):
    """
    Calculate expected time to reach state b from state a.

    Parameters:
    - p: Probabilities of transitioning to the next state
    - q: Probabilities of transitioning to the previous state
    - r: Probabilities of staying in the current state
    - N: Total number of states
    - a: Starting state
    - b: Target state

    Returns:
    - Expected time to reach state b from state a
    """
    if a == b:
        return 0.0

    # Create coefficient matrix
    A = create_matrix(N + 1, N + 1)
    expected_times = [1.0] * (N + 1)

    # Set up absorbing state
    A[b][b] = 1.0
    expected_times[b] = 0.0

    # Set up equations for other states
    for i in range(N + 1):
        if i == b:
            continue

        A[i][i] = 1.0 - r[i]
        if i < N:
            A[i][i + 1] = -p[i]
        if i > 0:
            A[i][i - 1] = -q[i]

    # Solve system
    solution = gaussian_elimination(A, expected_times)
    return solution[a]


def expected_wealth(p, q, r, N):
    Xi =stationary_distribution(p, q, r, N)
    sum = 0
    for i in range(N+1):
        sum += i*Xi[i]
    return sum

