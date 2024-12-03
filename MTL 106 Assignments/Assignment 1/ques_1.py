"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
M=1000000007

def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

# Problem 1a
dp = [[-1 for i in range(1001)] for j in range(1001)]

def numer(i, j):
    if j==0:
        return 0
    if i==0:
        return 0
    if i == 1:
        return 1
    if j == 1:
        return 1
    if dp[i][j] != -1:
        return dp[i][j]
    dp[i][j] = mod_add(mod_multiply(numer(i - 1, j), j), mod_multiply(numer(i, j - 1), i))
    return dp[i][j]

def calc_prob(alice_wins, bob_wins):
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """
    matches = alice_wins + bob_wins
    n = 1
    for i in range(1, matches):
        n = mod_multiply(n, i)
    return mod_divide(numer(alice_wins, bob_wins), n)







#
# Problem 1b (Expectation)
def calc_expectation(t):
    # """
    # Returns:
    #     The expected value of \sum_{i=1}^{t} Xi will be of the form p/q,
    #     where p and q are positive integers,
    #     return p.q^(-1) mod 1000000007.
    #
    # """
    matches = t
    n = 1
    for i in range(1, matches):
        n = mod_multiply(n, i)
    exp = 0
    for i in range(1, matches):
        exp = mod_add(exp , mod_multiply(numer(i, matches - i), i))
        exp = mod_add(exp , -1*mod_multiply(numer(matches - i, i), matches - i))


    return mod_divide(exp, n)




# Problem 1b (Variance)
def calc_variance(t):
    # """
    # Returns:
    #     The variance of \sum_{i=1}^{t} Xi will be of the form p/q,
    #     where p and q are positive integers,
    #     return p.q^(-1) mod 1000000007.
    #
    # """
    matches = t
    # n = 1
    # for i in range(1, matches):
    #     n = mod_multiply(n, i)
    # exp1 = 0
    # for i in range(1, matches):
    #     exp1 = mod_add(exp1, mod_multiply(numer(i, matches - i), i))
    #     exp1 = mod_add(exp1, mod_multiply(numer(matches - i, i), matches - i))
    # x_square_exp = mod_divide(exp1, n)
    exp = calc_expectation(t)
    exp1 = 0
    for i in range(1, matches):
        exp1 = mod_add(exp1, mod_multiply(calc_prob(i, matches-i), mod_multiply(2*i-matches, 2*i-matches)))
    return mod_add(exp1, -1*mod_multiply(exp, exp))


print(calc_prob(92,69))
print(calc_expectation(100))
print(calc_variance(69))


print(mod_divide(71789,65340))


