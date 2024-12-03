"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""

M=1000000007

payoff_matrix = [
        [[0, 0, 0], [7, 0, 3], [5, 0, 6]],
        [[3, 0, 7], [1, 1, 1], [3, 5, 2]],
        [[6, 0, 5], [2, 5, 3], [1, 8, 1]]
    ]

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

dp = [[[-1 for i in range(351)] for j in range(351)] for k in range(351)]

prob = [[[-1 for a in range(201)] for b in range(201)] for c in range(201)]

def expect(na, nb, t):

    if t==0:
        return 0
    if dp[na][nb][t] != -1:
        return dp[na][nb][t]

    x0 = (2*(nb/(nb+na)) + 2*(7/10) + 2*(5/11)) / 3 + ((nb / (nb + na) + (7 / 10) + (5 / 11)) * expect(na + 2, nb, t - 1) + (na / (na + nb) + 3/10 + 6/11) * expect(na, nb + 2, t - 1)) / 3
    x1 = (6/10 + 1 + 11/10)/3 + ((3/10 + 1/3 + 3/10)*expect(na+2, nb, t-1) + (1/3+1/2)*expect(na+1,nb+1, t-1) + (7/10 + 1/3 + 1/5)*expect(na, nb+2, t-1))/3
    x2 = (12/11 + 9/10 + 1)/3 + ((6/11 + 1/5 + 1/10) * expect(na+2, nb, t-1) + (1/2+4/5)*expect(na+1, nb+1, t-1) + (5/11+3/10+1/10)*expect(na, nb+2, t-1))/3
    dp[na][nb][t] = max(x0, x1, x2)
    return dp[na][nb][t]
# Problem 3b

# def calc_prob(na, nb, total):
#     # if na<2:
#     #     return 0
#     # if na == 2:
#     #     return 1
#     # if total == 0:
#     #     return 1
#
#
#     pw = 0
#     pd = 0
#     pl = 0
#     opt_strat = optimal_strategy(na, nb, total)
#
#     if opt_strat == 0:
#         pw = mod_divide(mod_add(mod_add(mod_divide(nb, mod_add(na, nb)) , mod_divide(7,10) ), mod_divide(5,11)), 3)
#         pd = 0
#         pl = mod_divide(mod_add(mod_add(mod_divide(na, mod_add(na, nb)), mod_divide(3, 10)), mod_divide(6, 11)), 3)
#     if opt_strat == 1:
#         pw = mod_divide(mod_add(mod_add(mod_divide(3 , 10) , mod_divide(1,3) ), mod_divide(3,10)), 3)
#         pd = mod_divide(mod_add(mod_add(0 , mod_divide(1,3) ), mod_divide(1,2)), 3)
#         pl = mod_divide(mod_add(mod_add(mod_divide(7 , 10) , mod_divide(1,3) ), mod_divide(1, 5)), 3)
#     if opt_strat == 2:
#         pw = mod_divide(mod_add(mod_add(mod_divide(6 , 11) , mod_divide(1,5) ), mod_divide(1,10)), 3)
#         pd = mod_divide(mod_add(mod_add(mod_divide(1 , 2) , mod_divide(4,5) ), 0), 3)
#         pl = mod_divide(mod_add(mod_add(mod_divide(5 , 11) , mod_divide(3,10) ), mod_divide(1, 10)), 3)
#     if na < 2:
#         return 0
#     if na == 2:
#         return 1
#     if total == 0:
#         return 1
#     x = mod_add(mod_add(mod_multiply(pw,prob[na+2][nb][total-1]) , mod_multiply(pd,prob[na+1][nb+1][total-1])) , mod_multiply(pl,prob[na][nb+2][total-1]))
#     prob[na][total] = x
#     return x

def prob_dep(na, nb, total):
    if total == 0:
        return 0, 0, 0
    opt_strat = optimal_strategy(na, nb, total)
    pw = 0
    pd = 0
    pl = 0
    if opt_strat[0] == 1:
        pw = mod_divide(mod_add(mod_add(mod_divide(nb, mod_add(na, nb)), mod_divide(7, 10)), mod_divide(5, 11)), 3)
        pd = 0
        pl = mod_divide(mod_add(mod_add(mod_divide(na, mod_add(na, nb)), mod_divide(3, 10)), mod_divide(6, 11)), 3)

    if opt_strat[1] == 1:
        pw = mod_divide(mod_add(mod_add(mod_divide(3, 10), mod_divide(1, 3)), mod_divide(3, 10)), 3)
        pd = mod_divide(mod_add(mod_add(0, mod_divide(1, 3)), mod_divide(1, 2)), 3)
        pl = mod_divide(mod_add(mod_add(mod_divide(7, 10), mod_divide(1, 3)), mod_divide(1, 5)), 3)
    if opt_strat[2] == 1:
        pw = mod_divide(mod_add(mod_add(mod_divide(6, 11), mod_divide(1, 5)), mod_divide(1, 10)), 3)
        pd = mod_divide(mod_add(mod_add(mod_divide(1, 2), mod_divide(4, 5)), 0), 3)
        pl = mod_divide(mod_add(mod_add(mod_divide(5, 11), mod_divide(3, 10)), mod_divide(1, 10)), 3)

    return pw, pd, pl
def calc_prob(na, nb, total, T):
    if na<2 or nb<2 == 0:
        return 0



    if total == 0:
        if na==2 and nb == 2:
            return 1
        return 0

    if prob[na][nb][total] != -1:
        return prob[na][nb][total]
    x = mod_add(mod_add(mod_multiply(prob_dep(na-2, nb, T-(total-1))[0],calc_prob(na-2, nb, total-1, T)), mod_multiply(prob_dep(na-1, nb-1, T-(total-1))[1],calc_prob(na-1, nb-1, total-1, T))), mod_multiply(prob_dep(na, nb-2,T-(total-1))[2],calc_prob(na, nb-2, total-1, T)))
    prob[na][nb][total] = x
    return x







def optimal_strategy(na, nb, tot_rounds):
    """
    Calculate the optimal strategy for Alice maximize her points in the future rounds
    given the current score of Alice(na) and Bob(nb) and the total number of rounds(tot_rounds).
    
    Return the answer in form of a list [p1, p2, p3],
    where p1 is the probability of playing Attacking
    p2 is the probability of playing Balanced
    p3 is the probability of playing Defensive
    """
    x0 = (2*(nb/(nb+na)) + 2*(7/10) + 2*(5/11)) / 3 + ((nb / (nb + na) + (7 / 10) + (5 / 11)) * expect(na + 2, nb, tot_rounds - 1) + (na / (na + nb) + 3/10 + 6/11) * expect(na, nb + 2, tot_rounds - 1)) / 3
    x1 = (6 / 10 + 1 + 11 / 10) / 3 + ((3 / 10 + 1 / 3 + 3 / 10) * expect(na + 2, nb, tot_rounds - 1) + (1 / 3 + 1 / 2) * expect(na + 1, nb + 1, tot_rounds - 1) + (7 / 10 + 1 / 3 + 1 / 5) * expect(na, nb + 2, tot_rounds - 1)) / 3
    x2 = (12 / 11 + 9 / 10 + 1) / 3 + ((6 / 11 + 1 / 5 + 1 / 10) * expect(na + 2, nb, tot_rounds - 1) + (1 / 2 + 4 / 5) * expect(na + 1, nb + 1, tot_rounds - 1) + (5 / 11 + 3 / 10 + 1 / 10) * expect(na, nb + 2, tot_rounds - 1)) / 3
    # print(f"x0: {x0/2}, x1: {x1/2}, x2: {x2/2}, na: {na}, nb: {nb}, tot_rounds: {tot_rounds}")
    if x0 > x1 and x0 > x2:
        return [1, 0, 0]
    else:
        if x1 > x2:
            return [0, 1, 0]
        else:
            return [0, 0, 1]




def expected_points(tot_rounds):
    # na = 2
    # ex = 0
    # while True:
    #     if na > (tot_rounds*2 + 2):
    #         break
    #     ex = mod_add(ex, mod_multiply(calc_prob(na, 4+ 2*tot_rounds - na, tot_rounds, tot_rounds), na-2))
    #     na = na+1
    #
    # return mod_divide(ex, 2)

    return expect(2,2,tot_rounds-2)/2 + 1
    # """
    # Given the total number of rounds(tot_rounds), calculate the expected points that Alice can score after the tot_rounds,
    # assuming that Alice plays optimally.
    #
    # Return : The expected points that Alice can score after the tot_rounds.
    # """


#if decimal answer is required run expect(na, nb, t) function where na=2, nb=2, t= future rounds, and divide by 2 (this is done to account for indexing)
#if answer is required in modulo run expected_points(tot_rounds) function where tot_rounds = future rounds
# print(expect(2,2,69)/2)
#At the end of t rounds, just do 1+expect(na, nb, t-2)/2, where t is the total number of rounds
# print(1+(expect(2,2, 69-2))/2)
# print(expected_points(2))


#if optimal strategy is required for any (na, nb, t) where na = alice_points, nb = bob_points, t = future rounds, run optimal_strategy(na, nb, t) function
# print(optimal_strategy(2,2,69))
#if any
print(expected_points(102))