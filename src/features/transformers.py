from src.features.CONSTANS import ENV_KEYWORDS, GENERIC_COMPONENTS, FRONTEND_TERMS, BACKEND_TERMS, SYSTEMS_TERMS, DATABASE_TERMS, DEVOPS_TERMS, PRODUCT_TERMS
import re

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

def severity_rating(row):
  score = 0
  if row["severity_category"] == "trivial":
    score = 1
  if row["severity_category"] == "minor":
    score = 1
  if row["severity_category"] == "normal":
    score = 2
  if row["severity_category"] == "major":
    score = 3
  if row["severity_category"] == "critical":
    score = 3
  if row["severity_category"] == "blocker":
    score = 3
  severity_rating = int(score)
  return severity_rating

def classify_environment(text: str) -> str:
    #Input Guard
    if not isinstance(text, str):
        return "unknown"
        
    text_lower = text.lower()
    
    # Calculate score per environment
    scores = {
        env: sum(1 for kw in keywords if kw in text_lower)
        for env, keywords in ENV_KEYWORDS.items()
    }
    
    dev, stg, prd = scores["development"], scores["staging"], scores["production"]

    # Simple tie-breaking logic using max key resolution
    # Production takes priority in ties (Production > Staging > Development)
    if prd >= stg and prd >= dev and prd > 0:
        return "production"
    if stg >= dev and stg > 0:
        return "staging"
    if dev > 0:
        return "development"
        
    return "unknown"

def contains_any_word(text: str, terms: set) -> bool:
    """Checks exact term presence or component matching safely."""
    # Split text into tokenized words for clean matching (avoids 'c' inside 'doc')
    words = set(text.lower().replace("-", " ").replace("_", " ").split())
    return bool(words.intersection(terms) or any(term in text for term in terms if len(term) > 2))

def assign_target_role(row: dict) -> str:
    component = str(row.get("component_name", "")).strip().lower()
    environment = str(row.get("environment", "")).strip().lower()
    
    # Safely convert severity_rating to integer with fallback
    try:
        severity = int(row.get("severity_rating", 0))
    except (ValueError, TypeError):
        severity = 0

    role_scores = {
        "Frontend Developer": 0,
        "Backend Developer": 0,
        "Systems Developer": 0,
        "Database Engineer": 0,
        "DevOps Engineer": 0,
        "Site Reliability Engineer": 0,
        "Product Specialist": 0,
        "Software Developer": 0,
    }

    is_generic = component in GENERIC_COMPONENTS

    if is_generic:
        if environment == "production":
            if severity == 3:
                role_scores["Site Reliability Engineer"] += 2
            else:
                role_scores["DevOps Engineer"] += 1
        elif environment == "development":
            if severity == 3:
                role_scores["Systems Developer"] += 1
            else:
                role_scores["Software Developer"] += 1
    else:
        # Evaluate component domain
        if contains_any_word(component, FRONTEND_TERMS):
            role_scores["Frontend Developer"] += 6
        if contains_any_word(component, BACKEND_TERMS):
            role_scores["Backend Developer"] += 6
        if contains_any_word(component, SYSTEMS_TERMS):
            role_scores["Systems Developer"] += 6
        if contains_any_word(component, DATABASE_TERMS):
            role_scores["Database Engineer"] += 6
        if contains_any_word(component, DEVOPS_TERMS):
            role_scores["DevOps Engineer"] += 6
        if contains_any_word(component, PRODUCT_TERMS):
            role_scores["Product Specialist"] += 6

        # Adjust for environment
        if environment == "production":
            role_scores["Site Reliability Engineer"] += 2
            role_scores["DevOps Engineer"] += 1
        elif environment == "development":
            role_scores["Software Developer"] += 1

        # Adjust for severity
        if severity == 3:
            role_scores["Systems Developer"] += 5
            if environment == "production":
                role_scores["Site Reliability Engineer"] += 2
                role_scores["DevOps Engineer"] += 4
            elif environment == "development":
                role_scores["Systems Developer"] += 1

    # Fallback default if all scores remain zero
    if max(role_scores.values()) == 0:
        role_scores["Software Developer"] = 3

    return max(role_scores, key=role_scores.get)

def clean_bug_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    #Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&\w+;', ' ', text)
    text = re.sub(r'0x[0-9a-fA-F]+', ' ', text)
    text = re.sub(r'/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\./]+', ' ', text)
    text = re.sub(r'[a-zA-Z]:\\[a-zA-Z0-9_\-\\]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\b\d+\b', ' ', text)
    text = re.sub(r'\b\w{1,3}\b', ' ', text)

    return text

#create priority variable
def assign_priority(row):
  if row["severity_rating"] == 3:
    if row["environment"] == "production":
      row["priority"] = "critical"
    elif row["environment"] == "staging":
      row["priority"] = "critical"
    elif row["environment"] == "development":
      row["priority"] = "high"
  elif row["severity_rating"] == 2:
    if row["environment"] == "production":
      row["priority"] = "medium"
    elif row["environment"] == "staging":
      row["priority"] = "medium"
    elif row["environment"] == "development":
      row["priority"] = "low"
  elif row["severity_rating"] == 1:
    if row["environment"] == "production":
      row["priority"] = "medium"
    elif row["environment"] == "staging":
      row["priority"] = "low"
    elif row["environment"] == "development":
      row["priority"] = "low"

  return row["priority"]

#report how quickly the bug should be handled
def assign_escalation_level(row):
    severity = int(row["severity_rating"])
    priority = row["priority"]
    environment = row["environment"]

    if priority == "critical":
        return "Immediate escalation"
    elif priority == "high" and environment == "production":
        return "Escalate within 1 hour"
    elif severity >= 3:
        return "Same-day review"

    return "Standard queue"

