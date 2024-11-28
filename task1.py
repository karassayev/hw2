import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def generate_random_department_data():
    departments = ['Engineering', 'Marketing', 'Finance', 'HR', 'Science']
    data = {}

    for dept in departments:
        num_users = np.random.randint(10, 200)
        threat_scores = generate_random_data(45, 20, num_users)
        data[dept] = {
            'users': num_users,
            'threat_scores': threat_scores
        }
    return data



def calculate_aggregated_threat_score(data):
    total_weighted_variance = 0
    total_users = 0

    for dept, dept_data in data.items():
        num_users = dept_data['users']
        threat_scores = dept_data['threat_scores']

        if num_users == 0 or len(threat_scores) == 0:
            continue

        # Calculate the variance of the threat scores
        var_score = np.var(threat_scores)

        # Add the weighted variance to the total
        total_weighted_variance += var_score * num_users
        total_users += num_users

    # Return the weighted average of variances, or 0 if there are no users
    return total_weighted_variance / total_users if total_users > 0 else 0


class TestThreatScoreAggregation(unittest.TestCase):
    def test_case_similar_threats(self):
        data = {
            'Engineering': {'users': 10, 'threat_scores': [50] * 10},
            'Marketing': {'users': 15, 'threat_scores': [50] * 15},
            'Finance': {'users': 20, 'threat_scores': [50] * 20},
            'HR': {'users': 5, 'threat_scores': [50] * 5},
            'Science': {'users': 25, 'threat_scores': [50] * 25},
        }
        score = calculate_aggregated_threat_score(data)
        self.assertEqual(score, 0)

    def test_case_high_threat_user(self):
        data = {
            'Engineering': {'users': 10, 'threat_scores': [10] * 9 + [90]},
            'Marketing': {'users': 15, 'threat_scores': [30] * 15},
            'Finance': {'users': 20, 'threat_scores': [40] * 20},
            'HR': {'users': 5, 'threat_scores': [20] * 5},
            'Science': {'users': 25, 'threat_scores': [50] * 25},
        }

        # Calculate the score using the actual function
        score = calculate_aggregated_threat_score(data)

        expected_score = ((10 * np.var([10] * 9 + [90]) + 15 * np.var([30] * 15) + 20 * np.var([40] * 20) + 5 * np.var([20] * 5) + 25 * np.var([50] * 25)) /(10 + 15 + 20 + 5 + 25)
        )

        print(f"Calculated Score: {score}")
        print(f"Expected Score: {expected_score}")

        self.assertAlmostEqual(score, expected_score, places=2)

        print(f"Calculated Score: {score}")
        print(f"Expected Score: {expected_score}")

        # Check with the precision you need
        self.assertAlmostEqual(score, expected_score, places=2)

    def test_empty_data(self):
        data = {}
        score = calculate_aggregated_threat_score(data)
        self.assertEqual(score, 0)

    def test_zero_users(self):
        data = {
            'Engineering': {'users': 0, 'threat_scores': []},
            'Marketing': {'users': 10, 'threat_scores': [30] * 10}
        }
        score = calculate_aggregated_threat_score(data)
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()