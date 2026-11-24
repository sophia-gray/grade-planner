import unittest

from grade_planner import current_standing, needed_on_remaining

COURSE = [
    {"name": "A", "weight": 50, "score": 80},
    {"name": "B", "weight": 50, "score": None},
]


class TestGradePlanner(unittest.TestCase):
    def test_current_standing(self):
        earned, graded, avg = current_standing(COURSE)
        self.assertAlmostEqual(earned, 40)
        self.assertEqual(graded, 50)
        self.assertAlmostEqual(avg, 80)

    def test_nothing_graded(self):
        _, graded, avg = current_standing([{"name": "A", "weight": 100, "score": None}])
        self.assertEqual(graded, 0)
        self.assertIsNone(avg)

    def test_needed(self):
        self.assertAlmostEqual(needed_on_remaining(COURSE, 85), 90)

    def test_unreachable_and_locked_in(self):
        self.assertGreater(needed_on_remaining(COURSE, 99), 100)
        self.assertLessEqual(needed_on_remaining(COURSE, 40), 0)

    def test_all_graded(self):
        done = [{"name": "A", "weight": 100, "score": 90}]
        self.assertIsNone(needed_on_remaining(done, 80))


if __name__ == "__main__":
    unittest.main()
