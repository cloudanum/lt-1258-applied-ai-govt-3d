# Lab 3.1 — Troubleshoot task.
#
# Paste this whole file into your AI assistant and ask two things:
#   1. What is wrong with it?
#   2. How would you fix it, and why did it fail this way?
#
# It is meant to be broken. Do not fix it before you ask — the point of the
# exercise is to judge the assistant's explanation, not to get working code.
#
# Context: a caseworker wants the average number of days each service request
# stayed open, broken out by request type, from a 311 extract.

import csv


def average_days_open(path):
    totals = {}
    counts = {}

    with open(path) as f:
        rows = csv.DictReader(f)

        for row in rows:
            sr_type = row["sr_type"]
            days = row["days_open"]

            totals[sr_type] = totals[sr_type] + days
            counts[sr_type] = counts[sr_type] + 1

    averages = {}
    for sr_type in totals:
        averages[sr_type] = totals[sr_type] / counts[sr_type]

    return averages


if __name__ == "__main__":
    result = average_days_open("chicago_311.csv")
    for sr_type, avg in sorted(result.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{sr_type:<40} {avg:.1f} days")
