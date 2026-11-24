"""Grade Planner: track a course's grade and see what you need on what's left."""

import argparse
import json
import sys


def load_course(path):
    with open(path, encoding="utf-8") as f:
        course = json.load(f)
    total = sum(a["weight"] for a in course["assessments"])
    if abs(total - 100) > 1e-9:
        raise ValueError(f"Weights add up to {total}, expected 100.")
    return course


def current_standing(assessments):
    """Return (points_earned, weight_graded, current_average_percent)."""
    graded = [a for a in assessments if a.get("score") is not None]
    earned = sum(a["weight"] * a["score"] / 100 for a in graded)
    weight_graded = sum(a["weight"] for a in graded)
    average = earned / weight_graded * 100 if weight_graded else None
    return earned, weight_graded, average


def needed_on_remaining(assessments, target):
    """Average % needed on ungraded work to finish at `target`, or None if nothing is left."""
    earned, weight_graded, _ = current_standing(assessments)
    remaining = 100 - weight_graded
    if remaining == 0:
        return None
    return (target - earned) / remaining * 100


def cmd_summary(course):
    print(course["name"])
    print("-" * len(course["name"]))
    for a in course["assessments"]:
        score = "not graded" if a.get("score") is None else f"{a['score']}%"
        print(f"{a['name']:<20} {a['weight']:>5}%   {score}")
    earned, weight_graded, average = current_standing(course["assessments"])
    print()
    if average is None:
        print("Nothing graded yet.")
    else:
        print(f"Graded so far: {weight_graded}% of the course")
        print(f"Current average on graded work: {average:.1f}%")
        print(f"Points banked toward final grade: {earned:.1f} / 100")


def cmd_needed(course, target):
    needed = needed_on_remaining(course["assessments"], target)
    if needed is None:
        _, _, average = current_standing(course["assessments"])
        print(f"Everything is graded. Your final grade is {average:.1f}%.")
    elif needed > 100:
        print(f"A {target}% is out of reach: you'd need {needed:.1f}% on the remaining work.")
    elif needed <= 0:
        print(f"You've already locked in {target}%, whatever you score on the rest.")
    else:
        print(f"To finish with {target}%, average {needed:.1f}% on the remaining work.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Track your course grade.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summary", help="show scores and current average")
    p_sum.add_argument("file")

    p_need = sub.add_parser("needed", help="what you need on the rest to hit a target")
    p_need.add_argument("file")
    p_need.add_argument("--target", type=float, required=True, help="target final grade, e.g. 80")

    args = parser.parse_args(argv)
    try:
        course = load_course(args.file)
    except (OSError, ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.command == "summary":
        cmd_summary(course)
    else:
        cmd_needed(course, args.target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
