
from sample_players import DataPlayer
import random


class AlphaBetaPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation
    """

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        depth = 8

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(random.choice(state.actions()))
            action = self.alpha_beta_decision(state, depth)
            self.queue.put(action)
            #print(self.player_id, action)
            #self.queue.put(random.choice(state.actions()))
            # while True:
            #     #print(depth)
            #     depth += 1
            #     action = self.alpha_beta_decision(state, depth)
            #     #print("adding ", action)
            #     self.queue.put(action)

    def my_moves(self, state):
        opponent = (1-self.player_id)
        return len(state.liberties(state.locs[self.player_id])) - len(state.liberties(state.locs[opponent]))

    def min_value(self, state, depth, alpha, beta):
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0:
            return self.my_moves(state)

        v = float('inf')
        for a in state.actions():
            v = min(self.max_value(state.result(a), depth-1, alpha, beta), v)
            if v <= alpha:
               return v
            beta = min(beta, v)
        return v

    def max_value(self, state, depth, alpha, beta):
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0:
            return self.my_moves(state)

        v = float('-inf')
        for a in state.actions():
            v = max(self.min_value(state.result(a), depth-1, alpha, beta), v)
            if v >= beta:
               return v
            alpha = max(alpha, v)
        return v

    def alpha_beta_decision(self, state, depth):
        alpha = float('-inf')
        beta = float('inf')
        best_score = float('-inf')
        best_move = None
        for a in state.actions():
            v = self.min_value(state.result(a), depth-1, alpha, beta)
            alpha = max(alpha, v)
            #print(v)
            if v > best_score:
                best_score = v
                best_move = a
        #print(best_score, best_move, state.actions())
        if best_move == None:
            return random.choice(state.actions())
        return best_move

class CustomPlayer(AlphaBetaPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """

    # def get_action(self, state):
    #     """ Employ an adversarial search technique to choose an action
    #     available in the current state calls self.queue.put(ACTION) at least

    #     This method must call self.queue.put(ACTION) at least once, and may
    #     call it as many times as you want; the caller will be responsible
    #     for cutting off the function after the search time limit has expired.

    #     See RandomPlayer and GreedyPlayer in sample_players for more examples.

    #     **********************************************************************
    #     NOTE: 
    #     - The caller is responsible for cutting off search, so calling
    #       get_action() from your own code will create an infinite loop!
    #       Refer to (and use!) the Isolation.play() function to run games.
    #     **********************************************************************
    #     """
    #     # TODO: Replace the example implementation below with your own search
    #     #       method by combining techniques from lecture
    #     #
    #     # EXAMPLE: choose a random move without any search--this function MUST
    #     #          call self.queue.put(ACTION) at least once before time expires
    #     #          (the timer is automatically managed for you)
    #     import random
    #     self.queue.put(random.choice(state.actions()))
