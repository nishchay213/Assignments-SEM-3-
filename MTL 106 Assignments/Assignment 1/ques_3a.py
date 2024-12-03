import numpy as np
import random
import time

class Alice:
    def __init__(self):
        self.past_play_styles =[1,1]
        self.results = [1,0]
        self.opp_play_styles = [1,1]
        self.points = 1


    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 3a here.
        
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        al_points = self.points
        bob_points = len(self.results) - al_points
        if bob_points * 29 > al_points * 15:
            return 0
        else:
            return 2
        # return 0


    
    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result


class Bob:
    def __init__(self):
        # Initialize numpy arrays to store Bob's past play styles, results, and opponent's play styles
        self.past_play_styles = [1,1]
        self.results = [0,1]
        self.opp_play_styles = [1,1]
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns:
            Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        move = np.random.choice([0, 1, 2])
        return move
        
    
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
    # print (alice.points)
    # print (bob.points)

    return alice.points, bob.points

    
 

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    al_pts, bob_pts = 0, 0
    x = 100
    start_time = time.time()
    for i in range(x):
        a, b = monte_carlo(100)
        # print(a,b)
        al_pts += a
        bob_pts += b
    al_pts /= x
    bob_pts /= x
    print (al_pts-1)
    print (bob_pts-1)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
