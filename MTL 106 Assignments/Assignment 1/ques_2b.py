import numpy as np
import random


dp = [[[[-1 for i in range(3)] for j in range(101)] for k in range(101)] for l in range(101)]

def expect(na, nb, t, res):
    if t==0:
        return 0
    if dp[int(na)][int(nb)][t][res] != -1:
        return dp[na][nb][t][res]

    if res == 0:
        x0 = (2*5/11) + (5/11)*expect(na+2, nb, t-1, 2) + (6/11)*expect(na, nb+2, t-1, 0)
        x1 = (6/10 + 1/2) + (3/10)*expect(na+2, nb, t-1, 2) + (1/2)*expect(na+1, nb+1, t-1, 1) + (1/5)*expect(na, nb+2, t-1, 0)
        x2 = 1 + (1/10)*expect(na+2, nb, t-1, 2) + (4/5)*expect(na+1, nb+1, t-1, 1) + (1/10)*expect(na, nb+2, t-1, 0)
        dp[na][nb][t][0] = max(x0, x1, x2)
        return dp[na][nb][t][res]
    if res == 1:
        x0 = (2*7/10) + (7/10)*expect(na+2, nb, t-1, 2) + (3/10)*expect(na, nb+2, t-1, 0)
        x1 = 1 + (1/3)*expect(na+2, nb, t-1, 2) + (1/3)*expect(na+1, nb+1, t-1, 1) + (1/3)*expect(na, nb+2, t-1, 0)
        x2 = (9/10) + (1/5)*expect(na+2, nb, t-1, 2) + (1/2)*expect(na+1, nb+1, t-1, 1) + (3/10)*expect(na, nb+2, t-1, 0)
        dp[na][nb][t][1] = max(x0, x1, x2)
        return dp[na][nb][t][res]
    if res == 2:
        x0 = (2*(nb/(na+nb))) + (nb/(na+nb))*expect(na+2, nb, t-1, 2) + (na/(na+nb))*expect(na, nb+2, t-1, 0)
        x1 = (6/10) + (3/10)*expect(na+2, nb, t-1, 2) + (7/10)*expect(na, nb+2, t-1, 0)
        x2 = (12/11) + (6/11)*expect(na+2, nb, t-1, 2) + (5/11)*expect(na, nb+2, t-1, 0)
        dp[na][nb][t][2] = max(x0, x1, x2)
        return dp[na][nb][t][res]
    return 0

def optimal_strategy(na, nb, t, res):
    if res == 0:
        x0 = (2*5/11) + (5/11)*expect(na+2, nb, t-1, 2) + (6/11)*expect(na, nb+2, t-1, 0)
        x1 = (6/10 + 1/2) + (3/10)*expect(na+2, nb, t-1, 2) + (1/2)*expect(na+1, nb+1, t-1, 1) + (1/5)*expect(na, nb+2, t-1, 0)
        x2 = 1 + (1/10)*expect(na+2, nb, t-1, 2) + (4/5)*expect(na+1, nb+1, t-1, 1) + (1/10)*expect(na, nb+2, t-1, 0)
        if x0>x1 and x0>x2:
            return 0
        else:
            if x1>x2:
                return 1
            else:
                return 2
    if res == 1:
        x0 = (2*7/10) + (7/10)*expect(na+2, nb, t-1, 2) + (3/10)*expect(na, nb+2, t-1, 0)
        x1 = 1 + (1/3)*expect(na+2, nb, t-1, 2) + (1/3)*expect(na+1, nb+1, t-1, 1) + (1/3)*expect(na, nb+2, t-1, 0)
        x2 = (9/10) + (1/5)*expect(na+2, nb, t-1, 2) + (1/2)*expect(na+1, nb+1, t-1, 1) + (3/10)*expect(na, nb+2, t-1, 0)
        if x0>x1 and x0>x2:
            return 0
        else:
            if x1>x2:
                return 1
            else:
                return 2
    if res == 2:
        x0 = (2*nb/(na+nb)) + (nb/(na+nb))*expect(na+2, nb, t-1, 2) + (na/(na+nb))*expect(na, nb+2, t-1, 0)
        x1 = (6/10) + (3/10)*expect(na+2, nb, t-1, 2) + (7/10)*expect(na, nb+2, t-1, 0)
        x2 = (12/11) + (6/11)*expect(na+2, nb, t-1, 2) + (5/11)*expect(na, nb+2, t-1, 0)
        if x0>x1 and x0>x2:
            return 0
        else:
            if x1>x2:
                return 1
            else:
                return 2
    return 0
class Alice:
    def __init__(self, T):
        self.past_play_styles = [1,1]
        self.results = [1,0]
        self.opp_play_styles = [1,1]
        self.points = 1
        self.T = T


    def play_move(self):
        return optimal_strategy(int(2*self.points), int(2*(len(self.results)-self.points)), self.T-(len(self.results)-2), int(2*self.results[-1]))


    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result


class Bob:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [0,1]
        self.opp_play_styles = [1,1]
        self.points = 1

    def play_move(self):
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:
            return 0

    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result


def simulate_round(alice, bob, payoff_matrix):
    alice_style = alice.play_move()
    bob_style = bob.play_move()
    choices = [1, 0.5, 0]
    payoff_matrix[0][0] = [bob.points, 0, alice.points]
    weights = payoff_matrix[alice_style][bob_style]
    result = random.choices(choices, weights, k=1)[0]

    alice.observe_result(alice_style, bob_style, result)
    bob.observe_result(bob_style, alice_style, 1 - result)


def monte_carlo(num_rounds):
    payoff_matrix = [
        [[0, 0, 0], [7, 0, 3], [5, 0, 6]],
        [[3, 0, 7], [1, 1, 1], [3, 5, 2]],
        [[6, 0, 5], [2, 5, 3], [1, 8, 1]]
    ]


    alice = Alice(num_rounds)
    bob = Bob()

    for i in range(num_rounds):
        simulate_round(alice, bob, payoff_matrix)

    # print(f"Alice's points: {alice.points}")
    # print(f"Bob's points: {bob.points}")
    return alice.points

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    x = 0
    for i in range(100000):
        x += monte_carlo(15)
    x/=100000
    print(x)

# print((expect(2,2,3, 0))/2)