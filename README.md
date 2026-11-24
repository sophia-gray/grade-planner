# Grade Planner

A small command-line tool that answers the question every student asks near exams: **"What do I need on the final to get an 80?"**

You describe a course in a JSON file (assessments, weights, scores so far) and Grade Planner shows your current standing and the average you need on the remaining work to hit a target.

## Demo

```
$ python grade_planner.py summary examples/sample_course.json
Sample Course 101
-----------------
Assignments             20%   88%
Quizzes                 10%   76%
Midterm                 30%   71%
Final Exam              40%   not graded

Graded so far: 60% of the course
Current average on graded work: 77.5%
Points banked toward final grade: 46.5 / 100

$ python grade_planner.py needed examples/sample_course.json --target 80
To finish with 80.0%, average 83.8% on the remaining work.
```

## Usage

Requires Python 3.8+ and nothing else.

```
python grade_planner.py summary path/to/course.json
python grade_planner.py needed path/to/course.json --target 80
```

Course file format (`score: null` means not graded yet; weights must add up to 100):

```json
{
  "name": "My Course",
  "assessments": [
    {"name": "Midterm", "weight": 40, "score": 72},
    {"name": "Final", "weight": 60, "score": null}
  ]
}
```

## Run the tests

```
python -m unittest
```

## What I learned

- Structuring a Python project with a CLI (`argparse`), JSON input, and unit tests
- Handling edge cases: nothing graded yet, targets that are already locked in or impossible

## Ideas for next steps

- [ ] Support multiple courses and a GPA calculator
- [ ] Add drop-the-lowest-quiz rules
- [ ] Build a small web UI
