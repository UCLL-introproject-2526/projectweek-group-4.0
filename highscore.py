# highscore.py
import os

SCORE_FILE = "scores.txt"
POINTS_PER_KILL = 50

current_score = 0
high_score = 0
total_points = 0


# -------------------------
# INTERNAL FILE FUNCTIONS
# -------------------------
def _load_scores():
    """Load all past scores from file."""
    if not os.path.exists(SCORE_FILE):
        return []

    with open(SCORE_FILE, "r") as f:
        try:
            return [int(line.strip()) for line in f]
        except ValueError:
            return []


def _save_score(score: int):
    """Append score to the file."""
    with open(SCORE_FILE, "a") as f:
        f.write(f"{score}\n")


def _update_high_from_file():
    """Refresh high_score from file."""
    global high_score
    scores = _load_scores()
    high_score = max(scores) if scores else 0
    return high_score


# -------------------------
# SCORE MANAGEMENT
# -------------------------
def reset_current():
    global current_score
    current_score = 0


def add_kill(points: int = POINTS_PER_KILL) -> int:
    global current_score, total_points
    current_score += points
    total_points += points
    return current_score


def add_points(points: int) -> int:
    global current_score, total_points
    current_score += points
    total_points += points
    return current_score


def update_high_score() -> int:
    """
    Updates high_score if current_score is larger.
    Also saves the new high score to file.
    """
    global high_score, current_score
    if current_score > high_score:
        high_score = current_score
    return high_score


def end_round():
    """Call this on GAME OVER. Saves score and updates high score."""
    global current_score
    _save_score(current_score)
    _update_high_from_file()


# -------------------------
# GETTERS
# -------------------------
def get_current() -> int:
    return current_score


def get_high() -> int:
    _update_high_from_file()
    return high_score


def get_total() -> int:
    return total_points
