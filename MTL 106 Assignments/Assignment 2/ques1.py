def win_probability(p, q, k, N):
    """
    Return the probability of winning a game of chance.
    """
    if p == q:  # Fair game case
        return k / N
    else:
        r = q / p
        if r == 1:
            return k / N
        return (1 - r ** k) / (1 - r ** N)


def limit_win_probability(p, q, k):
    """
    Return the probability of winning when the maximum wealth is infinity.
    """
    if p <= q:  # Unfair game or fair game
        return 0.0
    else: # p>0.5 case
        return 1 - (q / p) ** k



def game_duration(p, q, k, N):
    """
    Return the expected number of rounds to either win or get ruined.
    """
    if p == q == 0.5:  # Fair game
        return k * (N - k)

    r = q / p

    if r == 1:
        return k * (N - k)

    return (k - N * (1 - r ** k)/(1 - r ** N))/(1 - 2 * p)

