class Bot:
    def __init__(self):
        pass

    def make_move(self, board):
        """
        This method should be overridden by subclasses to implement specific move strategies.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def evaluate_board(self, board):
        """
        This method should be overridden by subclasses to implement specific evaluation strategies.
        """
        raise NotImplementedError("Subclasses should implement this method.")