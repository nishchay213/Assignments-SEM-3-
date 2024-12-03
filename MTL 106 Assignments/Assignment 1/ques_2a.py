import numpy as np
import random



class Alice:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [1,0]
        self.opp_play_styles = [1,1]
        self.points = 1

    def play_move(self):
        if self.results[-1] == 1:
            matches = len(self.results)
            if (matches-self.points)/matches > 6/11:
                return 0
            return 2
        elif self.results[-1] == 0.5:
            return 0
        else:
            return 1



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

    alice = Alice()
    bob = Bob()
    for i in range(num_rounds):
        simulate_round(alice, bob, payoff_matrix)

    # print(f"Alice's points: {alice.points}")
    # print(f"Bob's points: {bob.points}")
    return alice.points

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    # monte_carlo(num_rounds=10 ** 5 - 2)

    x = 0
    for i in range(100000):
        x+=monte_carlo(15)
    x/=100000
    print(x)

