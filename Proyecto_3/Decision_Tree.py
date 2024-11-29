from abc import ABC, abstractmethod

class DecisionTreeNode(ABC):
    @abstractmethod
    def make_decision(self):
        pass

class Action(DecisionTreeNode):
    def make_decision(self):
        return self

class Decision(DecisionTreeNode):
    def __init__(self, true_node: DecisionTreeNode, false_node: DecisionTreeNode):
        self.true_node = true_node
        self.false_node = false_node

    @abstractmethod
    def test_value(self):
        pass

    def get_branch(self):
        if self.test_value():
            return self.true_node
        return self.false_node

    def make_decision(self):
        branch = self.get_branch()
        return branch.make_decision()