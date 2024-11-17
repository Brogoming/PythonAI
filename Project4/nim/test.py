import math

q = {((1,1,3,5), (1,1)): 1, ((0,1,3,5), (1,2)): 2, ((1,1,3,5), (2,1)): 2}

def get_q_value(state, action):
    """
    Return the Q-value for the state `state` and the action `action`.
    If no Q-value exists yet in `self.q`, return 0.
    """
    if type(state) is list:
        state = tuple(state)
    if (state, action) in q.keys():
        return q[(state, action)]
    else:
        return 0

def best_future_reward(state):
    """
    Given a state `state`, consider all possible `(state, action)`
    pairs available in that state and return the maximum of all
    of their Q-values.

    Use 0 as the Q-value if a `(state, action)` pair has no
    Q-value in `self.q`. If there are no available actions in
    `state`, return 0.
    """
    if type(state) is list:
        state = tuple(state)
    actions = []  # all available actions
    for qState, qAction in q:
        if qState == state:
            actions.append(q[(state, qAction)])
    if len(actions) == 0:
        return 0
    return max(actions)


def get_unassigned_actions(state):
    actions = []
    for qState, qAction in q:
        if qState == state:
            for i in range(0, len(state)):
                for j in range(0, state[i]):
                    if (i, j) != qAction and (i, j) not in actions:
                        actions.append((i, j))
    return actions


print(get_unassigned_actions((1, 1, 3, 5)))
print(best_future_reward((1, 1, 3, 5)))
print(get_q_value([0, 0, 0, 2], (3, 2)))