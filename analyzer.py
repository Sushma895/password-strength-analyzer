import re

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "qwerty123",
    "admin",
    "letmein",
    "welcome",
    "abc123",
}

COMMON_WORDS = {
    "password",
    "admin",
    "welcome",
    "login",
    "qwerty",
    "student",
    "college",
    "school",
    "user",
}

SEQUENTIAL_PATTERNS = [
    "123",
    "234",
    "345",
    "456",
    "567",
    "678",
    "789",
    "abc",
    "bcd",
    "cde",
    "qwe",
    "asd",
]


def analyze_password(password):
    if not password:
        return {
            "score": 0,
            "strength": "WEAK",
            "checks": {},
            "warnings": ["Password cannot be empty."],
            "recommendations": ["Enter a password to begin the analysis."]
        }

    length = len(password)
    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_lowercase = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    repeated_characters = bool(re.search(r"(.)\1\1", password))

    password_lower = password.lower()

    exact_common_password = password_lower in COMMON_PASSWORDS

    common_word_found = any(
        word in password_lower for word in COMMON_WORDS
    )

    sequential_pattern_found = any(
        pattern in password_lower
        for pattern in SEQUENTIAL_PATTERNS
    )

    # ---------------- SCORE ----------------

    score = 0

    # Length
    if length >= 16:
        score += 4
    elif length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    elif length >= 6:
        score += 1

    # Character variety
    if has_uppercase:
        score += 1

    if has_lowercase:
        score += 1

    if has_number:
        score += 1

    if has_special:
        score += 2

    # Bonus for using all four character types
    if has_uppercase and has_lowercase and has_number and has_special:
        score += 1

    # ---------------- PENALTIES ----------------

    if exact_common_password:
        score = 0

    if common_word_found:
        score -= 2

    if sequential_pattern_found:
        score -= 2

    if repeated_characters:
        score -= 1

    score = max(0, min(score, 10))

    # ---------------- STRENGTH ----------------

    if score <= 3:
        strength = "WEAK"
    elif score <= 5:
        strength = "MEDIUM"
    elif score <= 7:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    # ---------------- WARNINGS ----------------

    warnings = []

    if exact_common_password:
        warnings.append(
            "This is a commonly used password."
        )

    if common_word_found:
        warnings.append(
            "A common word appears in the password."
        )

    if sequential_pattern_found:
        warnings.append(
            "A predictable sequence was detected."
        )

    if repeated_characters:
        warnings.append(
            "Repeated characters make the password easier to guess."
        )

    if length < 12:
        warnings.append(
            "The password is shorter than the recommended 12 characters."
        )

    # ---------------- RECOMMENDATIONS ----------------

    recommendations = []

    if length < 12:
        recommendations.append(
            "Use at least 12 characters."
        )

    if not has_uppercase:
        recommendations.append(
            "Add uppercase letters."
        )

    if not has_lowercase:
        recommendations.append(
            "Add lowercase letters."
        )

    if not has_number:
        recommendations.append(
            "Add numbers."
        )

    if not has_special:
        recommendations.append(
            "Add special characters such as !, @, # or $."
        )

    if common_word_found:
        recommendations.append(
            "Avoid common words and predictable phrases."
        )

    if sequential_pattern_found:
        recommendations.append(
            "Avoid sequences such as 123 or abc."
        )

    if not recommendations:
        recommendations.append(
            "This password meets the main strength checks."
        )

    return {
        "score": score,
        "strength": strength,
        "checks": {
            "length": length >= 12,
            "uppercase": has_uppercase,
            "lowercase": has_lowercase,
            "number": has_number,
            "special": has_special,
            "no_common_password": not exact_common_password,
            "no_common_word": not common_word_found,
            "no_sequence": not sequential_pattern_found,
            "no_repeated_characters": not repeated_characters,
        },
        "warnings": warnings,
        "recommendations": recommendations
    }