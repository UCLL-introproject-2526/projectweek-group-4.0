
# highscore.py

# Points per shark kill
POINTS_PER_KILL = 50

# In-memory score state
current_score: int = 0       # score for the current run
high_score: int = 0          # highest single-run score seen this session
total_points: int = 0        # cumulative total across runs (this session)


def reset_current() -> None:
    """Reset only the current run score."""
    global current_score
    current_score = 0


def reset_all() -> None:
    """Reset everything (current, high, total)."""
    global current_score, high_score, total_points
    current_score = 0
    high_score = 0
    total_points = 0


def add_kill(points: int = POINTS_PER_KILL) -> int:
    """
    Add points for a kill.
    Defaults to 50 per kill. Returns the new current score.
    """
    global current_score, total_points
    current_score += points
    total_points += points
    return current_score


def add_points(points: int) -> int:
    """
    Generic adder in case you grant points from other actions later.
    Returns the new current score.
    """
    global current_score, total_points
    current_score += points
    total_points += points
    return current_score


def update_high_score() -> int:
    """
    If current run beats the high score, update it.
    Returns the latest high score.
    """
    global high_score, current_score
    if current_score > high_score:
        high_score = current_score
    return high_score


def get_current() -> int:
    """Return the current run score."""
    return current_score


def get_high() -> int:
    """Return the high score."""
    return high_score


def get_total() -> int:
    """Return total points accumulated this session."""
