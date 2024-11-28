import numpy as np
import unittest


# Function to generate random user threat scores for departments
def generate_random_data(mean, variance, num_samples):
    """Generates random threat scores based on mean, variance, and number of samples."""
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance + 1, 90)
    return np.random.randint(lower_bound, upper_bound, num_samples)


# Function to calculate the mean threat score for a department
def calculate_mean_threat_score(department_data):
    """Calculates the mean threat score for a department."""
    if len(department_data) == 0:  # Handle empty data case
        return 0
    return np.mean(department_data)


# Function to calculate the aggregated cybersecurity threat score for the company
def calculate_aggregated_threat_score(departments):
    """
    Calculates the aggregated cybersecurity threat score for all departments.
    Departments are weighted by importance.
    """
    weighted_sum = 0
    total_importance = 0

    for department in departments:
        department_data = department['data']
        department_importance = department['importance']

        # Skip departments with zero importance or no data
        if department_importance == 0 or len(department_data) == 0:
            continue

        # Calculate the mean threat score for the department
        department_mean = calculate_mean_threat_score(department_data)

        # Weighted sum of the threat score based on department importance
        weighted_sum += department_mean * department_importance
        total_importance += department_importance

    # Return the aggregated threat score as a value between 0 and 90
    return min(max(weighted_sum / total_importance, 0), 90) if total_importance > 0 else 0


class TestThreatScoreCalculation(unittest.TestCase):

    def test_calculate_mean_threat_score(self):
        """Test mean calculation for a department."""
        department_data = np.array([10, 20, 30, 40, 50])
        result = calculate_mean_threat_score(department_data)
        expected_result = np.mean(department_data)
        self.assertEqual(result, expected_result)

    def test_calculate_mean_threat_score_empty(self):
        """Test mean calculation for an empty department."""
        department_data = np.array([])
        result = calculate_mean_threat_score(department_data)
        self.assertEqual(result, 0)

    def test_calculate_aggregated_threat_score(self):
        """Test aggregated score calculation with multiple departments."""
        departments = [
            {'name': 'Dept1', 'data': np.array([10, 20, 30]), 'importance': 1},
            {'name': 'Dept2', 'data': np.array([40, 50, 60]), 'importance': 2}
        ]
        result = calculate_aggregated_threat_score(departments)
        expected_result = (np.mean([10, 20, 30]) * 1 + np.mean([40, 50, 60]) * 2) / (1 + 2)
        self.assertEqual(result, expected_result)

    def test_aggregated_score_empty_data(self):
        """Test aggregated score with an empty department."""
        departments = [
            {'name': 'Dept1', 'data': np.array([]), 'importance': 1},
            {'name': 'Dept2', 'data': np.array([40, 50, 60]), 'importance': 2}
        ]
        result = calculate_aggregated_threat_score(departments)
        expected_result = np.mean([40, 50, 60])
        self.assertEqual(result, expected_result)

    def test_aggregated_score_zero_importance(self):
        """Test aggregated score with a department with zero importance."""
        departments = [
            {'name': 'Dept1', 'data': np.array([10, 20, 30]), 'importance': 0},
            {'name': 'Dept2', 'data': np.array([40, 50, 60]), 'importance': 2}
        ]
        result = calculate_aggregated_threat_score(departments)
        expected_result = np.mean([40, 50, 60])
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    # Run unit tests
    unittest.main()

    # Example departments data for functional testing
    departments = [
        {'name': 'Engineering', 'data': generate_random_data(50, 10, 50), 'importance': 3},
        {'name': 'Marketing', 'data': generate_random_data(40, 15, 50), 'importance': 2},
        {'name': 'Finance', 'data': generate_random_data(60, 20, 50), 'importance': 5},
        {'name': 'HR', 'data': generate_random_data(30, 5, 50), 'importance': 4},
        {'name': 'Science', 'data': generate_random_data(55, 10, 50), 'importance': 1}
    ]

    # Calculate the aggregated cybersecurity threat score
    aggregated_score = calculate_aggregated_threat_score(departments)
    print(f"Aggregated Cybersecurity Threat Score: {aggregated_score}")
