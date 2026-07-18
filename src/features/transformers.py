def calculate_severity_score(row):
    score = 0
    # Environment
    if row["environment_id"] == 2:
        score += 2
    elif row["environment_id"] == 3:
        score += 1
    # Bug Category
    if row["category_id"] == 16:
        score += 4
    elif row["category_id"] in [
        2,
        15,
        9,
        4,
        12
    ]:
        score += 3
    elif row["category_id"] in [
        14,
        11,
        1,
        13,
        3
    ]:
        score += 2
    else:
        score += 1
    # Error Code
    if row["error_code"] >= 500:
        score += 2
    elif row["error_code"] >= 400:
        score += 1
    return score


def severity_class(score):
    if score <= 2:
        return 1      # Low
    elif score <= 4:
        return 2      # Medium
    elif score <= 6:
        return 3      # High
    else:
        return 4      # Critical


def priority_class(row):
    score = row["severity"]
    if row["environment_id"] == 2:
        score += 1
    if score >= 5:
        return 4      # P1 Critical
    elif score == 4:
        return 3      # P2 High
    elif score == 3:
        return 2      # P3 Normal
    else:
        return 1      # P4 Low
