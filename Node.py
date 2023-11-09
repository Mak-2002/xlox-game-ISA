from ast import Compare
import copy
from State import State

class Node:
    def __init__(self, state: 'State', parent: 'Node' = None, cost: int = 0, depth: int = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
    
    # def __copy__(self):
    #     new_obj = Node(self, self.parent, self.cost, self.depth)
    #     return new_obj

    def __deepcopy__(self, memo):
        new_obj = Node(copy.copy(self.state), self.parent, self.cost, self.depth)
        memo[id(self)] = new_obj
        return new_obj

    def __eq__(self, other: 'Node') -> bool:
        return isinstance(other, Node) and other.state == self.state
    
    def get_possible_next_nodes(self):
        return [ Node(next_state, self, self.cost + 1, self.depth + 1)
                for next_state in self.state.get_possible_next_states() ]
    

    def __lt__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost < other.cost

    def __le__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost <= other.cost

    def __eq__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost == other.cost

    def __ne__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost != other.cost

    def __gt__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost > other.cost

    def __ge__(self, other : 'Node'):
        return isinstance(other, Node) and self.cost >= other.cost