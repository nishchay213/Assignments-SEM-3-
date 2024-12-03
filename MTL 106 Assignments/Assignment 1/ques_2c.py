import numpy as np
import random

payoff_matrix = [[[0, 0, 0], [7, 0, 3], [5, 0, 6]],
                             [[3, 0, 7], [1, 1, 1], [3, 5, 2]],
                             [[6, 0, 5], [2, 5, 3], [1, 8, 1]]]
class Alice:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [1,0]
        self.opp_play_styles =[1,1]
        self.points = 1
        self.wins = 1

    def play_move(self):
        if self.results[-1] == 1:
            matches = len(self.results)
            if (matches - self.points) / matches > 6 / 11:
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

        if result == 1:
            self.wins += 1
       

class Bob:
    def __init__(self):
        # Initialize numpy arrays to store Bob's past play styles, results, and opponent's play styles
        self.past_play_styles = [1,1]
        self.results =[0,1]
        self.opp_play_styles = [1,1]
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
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

def monte_carlo(T):
    payoff_matrix = [
        [[0, 0, 0], [7, 0, 3], [5, 0, 6]],
        [[3, 0, 7], [1, 1, 1], [3, 5, 2]],
        [[6, 0, 5], [2, 5, 3], [1, 8, 1]]
    ]
    alice = Alice()
    bob = Bob()
    for i in range(1000):
        if (alice.wins == T):
            return i + 3

        simulate_round(alice, bob, payoff_matrix)

    return 1000


def estimate_tau(T):

    """
    Estimate the expected value of the number of rounds taken for Alice to win 'T' rounds.
    Your total number of simulations must not exceed 10^5.

    Returns:
        Float: estimated value of E[tau]
    """

    x = 0
    for i in range(10**5):
        alice = Alice()
        bob = Bob()
        for j in range(1000):
            simulate_round(alice, bob, payoff_matrix)
            if alice.wins == T:
                x += j+3
                break
    return x/10**5


print(estimate_tau(10))


        
        
    