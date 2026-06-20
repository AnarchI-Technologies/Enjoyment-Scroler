import unittest

from enjoyment_scroler import ScrollEvent, summarize_session


class SessionTests(unittest.TestCase):
    def test_phase_one_empty_session(self):
        self.assertEqual(summarize_session([]).recommendation, "NO_SESSION")

    def test_phase_two_healthy_session_continues(self):
        events = [ScrollEvent(12, 2), ScrollEvent(9, 2), ScrollEvent(8, 1)]

        self.assertEqual(summarize_session(events).recommendation, "CONTINUE")

    def test_phase_three_skip_heavy_session_slows_down(self):
        events = [ScrollEvent(1, 0, True), ScrollEvent(2, 0, True), ScrollEvent(1, 0, True)]

        self.assertEqual(summarize_session(events).recommendation, "SLOW_DOWN")


if __name__ == "__main__":
    unittest.main()

