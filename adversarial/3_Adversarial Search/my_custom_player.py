
from sample_players import DataPlayer
import random, math


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
        depth = 5

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            while True:
                action = self.alpha_beta_decision(state, depth)
                self.queue.put(action)
                depth += 1

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
            beta = min(beta, v)
            if v <= alpha:
               return v
        return v

    def max_value(self, state, depth, alpha, beta):
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0:
            return self.my_moves(state)

        v = float('-inf')
        for a in state.actions():
            v = max(self.min_value(state.result(a), depth-1, alpha, beta), v)
            alpha = max(alpha, v)
            if v >= beta:
               return v
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

'''
Implements the Monte Carlo Search Tree Advanced Search Algorithm 
'''
class CustomPlayer(DataPlayer):
    
    class Node:
        def __init__(self, state, parent=None):
            self.state = state
            self.parent = parent
            self.children = {} # key is the action that leads the parent to the action
            self.Q = 0
            self._untried_actions = None
            self.n = 0 # how many times this node is visited

        @property
        def untried_actions(self):
            if self._untried_actions is None:
                self._untried_actions = self.state.actions()
            return self._untried_actions

        def best_child(self, c = 1.4):
            return max(self.children.values(), key=lambda x: x.Q/x.n + c*math.sqrt(math.log(self.n)/x.n))
            
        def best_action(self):
            if len(self.children) == 0:
                return random.choice(self.state.actions())
            _, best_move = max([(c.Q/c.n, a) for a, c in self.children.items()])
            return best_move

        def expand(self):
            action = self.untried_actions.pop()
            next_state = self.state.result(action)
            child_node = CustomPlayer.Node(next_state, self)
            self.children[action] = child_node
            return child_node

        def rollout_policy(self):
            state = self.state
            while not state.terminal_test():
                state = state.result(random.choice(state.actions()))
            return +1 if state.utility(self.state.player()) < 0 else -1

        def backpropagate(self, result):
            self.n += 1
            self.Q += result
            if self.parent:
                self.parent.backpropagate(-result)

    def __init__(self, player_id):
        super().__init__(player_id)
        self.root = None

    def get_action(self, state):
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.root = CustomPlayer.Node(state)
            self.queue.put(random.choice(state.actions()))
            while True:
                # for i in range(900):
                #     node = self._tree_policy()
                #     result = node.rollout_policy()
                #     node.backpropagate(result)
                #     if i%10==0:
                self.queue.put(self._monte_carlo())

    # adds another action to the queue to update everytime expansion and backup is done
    def _monte_carlo(self,):
        node = self._tree_policy()
        result = node.rollout_policy()
        node.backpropagate(result)
        return self.root.best_action()

    def _tree_policy(self):
        node = self.root
        while not node.state.terminal_test():
            if not len(node.untried_actions) == 0:
                return node.expand()
            else:
                node = node.best_child()
        return node