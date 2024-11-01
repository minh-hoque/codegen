from pathlib import Path
from typing import Optional


def get_next_challenge_number() -> str:
    """Get the next available challenge number"""
    challenges_dir = Path("challenges")
    challenges_dir.mkdir(exist_ok=True)

    existing_files = list(challenges_dir.glob("coding_challenge_*.py"))
    if not existing_files:
        return "01"

    numbers = [int(f.stem.split("_")[-1]) for f in existing_files]
    next_num = max(numbers) + 1
    return f"{next_num:02d}"


def save_challenge_file(formatted_solution: str) -> str:
    """Save the formatted solution to a new challenge file"""
    challenge_num = get_next_challenge_number()
    filename = f"coding_challenge_{challenge_num}.py"

    challenges_dir = Path("challenges")
    filepath = challenges_dir / filename

    with open(filepath, "w") as f:
        f.write(formatted_solution)

    return str(filepath)
