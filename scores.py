import os

SCORE_FILE = "score.txt"

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = self.load_high_score()

    def add_score(self, amount):
        self.current_score += amount

    def reset_score(self):
        self.current_score = 0

    def load_high_score(self):
        if not os.path.exists(SCORE_FILE):
            return 0

        try:
            with open(SCORE_FILE, "r") as file:
                scores = [int(line.strip()) for line in file if line.strip().isdigit()]
                return max(scores) if scores else 0
        except Exception:
            return 0

    def save_score(self):
        with open(SCORE_FILE, "a") as file:
            file.write(f"{self.current_score}\n")

        self.high_score = max(self.high_score, self.current_score)
