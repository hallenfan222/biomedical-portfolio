"""Doctor–hospital allocation; extracted from the BDD notebook.

All D/H identifiers in this demonstration are synthetic. See README for provenance.
"""
from __future__ import annotations

capacities = {"H1": 4, "H2": 3, "H3": 4, "H4": 3, "H5": 3, "H6": 3,}
preferences = {
    "D1": ["H2", "H1", "H3", "H4", "H6", "H5"],
    "D2": ["H1", "H4", "H5", "H2", "H6", "H3"],
    "D3": ["H1", "H3", "H5", "H2", "H4", "H6"],
    "D4": ["H1", "H2", "H6", "H5", "H4", "H3"],
    "D5": ["H5", "H3", "H6", "H2", "H4", "H1"],
    "D6": ["H2", "H6", "H1", "H3", "H4", "H5"],
    "D7": ["H2", "H6", "H3", "H1", "H5", "H4"],
    "D8": ["H4", "H5", "H1", "H3", "H2", "H6"],
    "D9": ["H1", "H2", "H5", "H3", "H6", "H4"],
    "D10": ["H1", "H4", "H2", "H3", "H6", "H5"],
    "D11": ["H2", "H6", "H1", "H4", "H5", "H3"],
    "D12": ["H2", "H1", "H3", "H4", "H6", "H5"],
    "D13": ["H1", "H6", "H2", "H4", "H5", "H3"],
    "D14": ["H1", "H2", "H3", "H4", "H5", "H6"],
    "D15": ["H1", "H2", "H3", "H6", "H4", "H5"],
    "D16": ["H3", "H1", "H6", "H2", "H5", "H4"],
    "D17": ["H1", "H5", "H2", "H6", "H3", "H4"],
    "D18": ["H3", "H1", "H2", "H6", "H4", "H5"],
    "D19": ["H2", "H3", "H1", "H5", "H4", "H6"],
    "D20": ["H1", "H2", "H4", "H3", "H6", "H5"],}

def validate_inputs(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
) -> None:
    if not isinstance(preferences, dict):
        raise TypeError("Preferences must be a dictionary.")
    if not isinstance(capacities, dict):
        raise TypeError("Capacities must be a dictionary.")
    if not preferences:
        raise ValueError("At least one doctor must be provided.")
    if not capacities:
        raise ValueError("At least one hospital must be provided.")

    hospital_names = set(capacities)
    for hospital, capacity in capacities.items():
        if not isinstance(hospital, str) or not hospital.strip():
            raise ValueError("Every hospital name must be a non-empty string.")
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError(f"Capacity for {hospital!r} must be an integer.")
        if capacity < 0:
            raise ValueError(f"Capacity for {hospital!r} cannot be negative.")

    for doctor, ranked_hospitals in preferences.items():
        if not isinstance(doctor, str) or not doctor.strip():
            raise ValueError("Every doctor name must be a non-empty string.")
        if not isinstance(ranked_hospitals, list):
            raise TypeError(f"Preferences for {doctor!r} must be a list.")
        if len(ranked_hospitals) != len(capacities):
            raise ValueError(f"{doctor!r} must rank every hospital exactly once.")
        if any(not isinstance(name, str) or not name.strip() for name in ranked_hospitals):
            raise ValueError(f"All hospitals ranked by {doctor!r} must have valid names.")
        if len(set(ranked_hospitals)) != len(ranked_hospitals):
            raise ValueError(f"Preferences for {doctor!r} contain duplicate hospitals.")
        if set(ranked_hospitals) != hospital_names:
            missing = sorted(hospital_names - set(ranked_hospitals))
            unknown = sorted(set(ranked_hospitals) - hospital_names)
            raise ValueError(
                f"Preferences for {doctor!r} do not match the hospital list. "
                f"Missing: {missing}; unknown: {unknown}."
            )

    total_capacity = sum(capacities.values())
    if total_capacity < len(preferences):
        raise ValueError(
            "Total hospital capacity must be at least the number of doctors. "
            f"Doctors: {len(preferences)}; total capacity: {total_capacity}."
        )

def create_slots(capacities: dict[str, int]) -> list[dict[str, str]]:
    """Expand each hospital capacity into one-to-one assignment slots."""
    return [
        {"hospital": hospital, "slot": f"{hospital}_{slot_number}"}
        for hospital, capacity in capacities.items()
        for slot_number in range(1, capacity + 1)
    ]


def create_rank_lookup(
    preferences: dict[str, list[str]],
) -> dict[str, dict[str, int]]:
    """Convert ordered preference lists to one-based rank costs."""
    return {
        doctor: {
            hospital: rank
            for rank, hospital in enumerate(preference_list, start=1)
        }
        for doctor, preference_list in preferences.items()
    }


def build_cost_matrix(
    doctors: list[str],
    slots: list[dict[str, str]],
    rank_lookup: dict[str, dict[str, int]],
) -> list[list[int]]:
    """Build a doctor-by-slot rank cost matrix."""
    return [
        [rank_lookup[doctor][slot["hospital"]] for slot in slots]
        for doctor in doctors
    ]


def hungarian_algorithm(cost_matrix: list[list[int]]) -> list[int]:
    """Return the minimum-cost slot index for every matrix row."""
    if not cost_matrix or not cost_matrix[0]:
        raise ValueError("Cost matrix cannot be empty.")
    if any(len(row) != len(cost_matrix[0]) for row in cost_matrix):
        raise ValueError("Cost matrix must be rectangular.")

    row_count = len(cost_matrix)
    column_count = len(cost_matrix[0])
    if row_count > column_count:
        raise ValueError(
            "Number of hospital slots must be at least the number of doctors."
        )

    row_potential = [0] * (row_count + 1)
    column_potential = [0] * (column_count + 1)
    matched_row = [0] * (column_count + 1)
    previous_column = [0] * (column_count + 1)

    for row in range(1, row_count + 1):
        matched_row[0] = row
        current_column = 0
        minimum_reduced_cost = [float("inf")] * (column_count + 1)
        used = [False] * (column_count + 1)

        while True:
            used[current_column] = True
            current_row = matched_row[current_column]
            delta = float("inf")
            next_column = 0

            for column in range(1, column_count + 1):
                if not used[column]:
                    reduced_cost = (
                        cost_matrix[current_row - 1][column - 1]
                        - row_potential[current_row]
                        - column_potential[column]
                    )
                    if reduced_cost < minimum_reduced_cost[column]:
                        minimum_reduced_cost[column] = reduced_cost
                        previous_column[column] = current_column
                    if minimum_reduced_cost[column] < delta:
                        delta = minimum_reduced_cost[column]
                        next_column = column

            for column in range(column_count + 1):
                if used[column]:
                    row_potential[matched_row[column]] += delta
                    column_potential[column] -= delta
                else:
                    minimum_reduced_cost[column] -= delta

            current_column = next_column
            if matched_row[current_column] == 0:
                break

        while True:
            next_column = previous_column[current_column]
            matched_row[current_column] = matched_row[next_column]
            current_column = next_column
            if current_column == 0:
                break

    assignment = [-1] * row_count
    for column in range(1, column_count + 1):
        if matched_row[column] != 0:
            assignment[matched_row[column] - 1] = column - 1
    return assignment


def solve_hungarian(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
) -> dict[str, dict[str, str]]:
    """Validate and solve a complete doctor-hospital assignment problem."""
    validate_inputs(preferences, capacities)
    doctors = list(preferences)
    slots = create_slots(capacities)
    rank_lookup = create_rank_lookup(preferences)
    cost_matrix = build_cost_matrix(doctors, slots, rank_lookup)
    slot_indices = hungarian_algorithm(cost_matrix)

    return {
        doctor: {
            "hospital": slots[slot_index]["hospital"],
            "slot": slots[slot_index]["slot"],
        }
        for doctor, slot_index in zip(doctors, slot_indices)
    }

import random
def _greedy_assignment(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
    doctor_order: list[str],
) -> dict[str, dict[str, str]]:
    remaining_capacity = capacities.copy()
    assignment = {}
    for doctor in doctor_order:
        for hospital in preferences[doctor]:
            if remaining_capacity[hospital] > 0:
                assignment[doctor] = {"hospital": hospital}
                remaining_capacity[hospital] -= 1
                break
    return assignment


def greedy_assignment(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
    doctor_order: list[str] | None = None,
) -> dict[str, dict[str, str]]:
    validate_inputs(preferences, capacities)
    order = list(preferences) if doctor_order is None else list(doctor_order)
    if set(order) != set(preferences) or len(order) != len(preferences):
        raise ValueError("Doctor order must contain every doctor exactly once.")
    return _greedy_assignment(preferences, capacities, order)


def run_randomized_greedy(
    preferences: dict[str, list[str]],
    capacities: dict[str, int],
    trials: int = 100,
    seed: int | None = 0,
) -> list[dict[str, dict[str, str]]]:
    if isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0:
        raise ValueError("Trials must be a positive integer.")
    validate_inputs(preferences, capacities)
    generator = random.Random(seed)
    doctors = list(preferences)
    assignments = []
    for _ in range(trials):
        order = doctors.copy()
        generator.shuffle(order)
        assignments.append(_greedy_assignment(preferences, capacities, order))
    return assignments

from collections import Counter
from statistics import mean
def evaluate_assignment(
    doctors: list[str],
    assignment: dict[str, dict[str, str]],
    preferences: dict[str, list[str]],
) -> dict[str, object]:
    """Evaluate a complete assignment using rank-based metrics."""
    if len(doctors) != len(set(doctors)):
        raise ValueError("Doctor list cannot contain duplicate names.")
    if set(doctors) != set(preferences):
        raise ValueError("Doctor list must match the preference dictionary.")
    if set(assignment) != set(doctors) or len(assignment) != len(doctors):
        raise ValueError("Every doctor must have exactly one assignment.")

    rank_lookup = create_rank_lookup(preferences)
    assigned_ranks = {}
    for doctor in doctors:
        hospital = assignment[doctor].get("hospital")
        if hospital not in rank_lookup[doctor]:
            raise ValueError(
                f"Assignment for {doctor!r} contains an unknown hospital."
            )
        assigned_ranks[doctor] = rank_lookup[doctor][hospital]
    ranks = list(assigned_ranks.values())
    total_cost = sum(ranks)
    first_choice_rate = sum(rank == 1 for rank in ranks)/len(doctors)
    top_three_count = sum(rank <= 3 for rank in ranks)

    return {
        "total_cost": total_cost,
        "average_rank": total_cost / len(doctors),
        "first_choice_rate": first_choice_rate,
        "top_three_rate": top_three_count / len(doctors),
        "worst_assigned_rank": max(ranks),
        "rank_distribution": dict(sorted(Counter(ranks).items())),
        "assigned_ranks": assigned_ranks,
    }


def summarize_trials(trial_metrics: list[dict[str, object]]) -> dict[str, float]:
    """Summarize repeated randomized greedy trials."""
    if not trial_metrics:
        raise ValueError("At least one trial is required.")
    costs = [float(metrics["total_cost"]) for metrics in trial_metrics]
    return {
        "mean_total_cost": mean(costs),
        "best_total_cost": min(costs),
        "worst_total_cost": max(costs),
        "mean_average_rank": mean(
            float(metrics["average_rank"]) for metrics in trial_metrics
        ),
        "mean_first_choice_rate": mean(
            float(metrics["first_choice_rate"]) for metrics in trial_metrics
        ),
        "mean_top_three_rate": mean(
            float(metrics["top_three_rate"]) for metrics in trial_metrics
        ),
        "mean_worst_assigned_rank": mean(
            float(metrics["worst_assigned_rank"]) for metrics in trial_metrics
        ),
    }
def main() -> None:
    validate_inputs(preferences, capacities)
    doctors = list(preferences)
    hungarian_assignment = solve_hungarian(preferences, capacities)
    hungarian_metrics = evaluate_assignment(doctors, hungarian_assignment, preferences)
    greedy_assignments = run_randomized_greedy(preferences, capacities, trials=1_000, seed=10)
    greedy_metrics = [
        evaluate_assignment(doctors, assignment, preferences)
        for assignment in greedy_assignments
    ]
    print("Input summary")
    print("-" * 50)
    print(f"Doctors: {len(doctors)}")
    print(f"Hospitals: {len(capacities)}")
    print(f"Total capacity: {sum(capacities.values())}")

    print("\nHungarian assignment")
    print("-" * 50)
    for doctor, result in hungarian_assignment.items():
        rank = hungarian_metrics["assigned_ranks"][doctor]
        print(f"{doctor:<4} -> {result['hospital']} (rank {rank})")
    print("\nHungarian metrics")
    print(hungarian_metrics)
    print("\nRandomized greedy summary (1,000 trials)")
    print(summarize_trials(greedy_metrics))
if __name__ == "__main__":
    main()
