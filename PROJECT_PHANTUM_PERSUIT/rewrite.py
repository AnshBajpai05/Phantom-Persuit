class Game:
    def __init__(self, player_name):
        self.name = player_name
        self.load_stats()
        self.reset_stats()
        self.difficulty = 1
        self.history = []

    def reset_stats(self):
        self.sanity = 0
        self.hearts_of_dead = self.user_stats.get('hearts_of_dead', 0)
        