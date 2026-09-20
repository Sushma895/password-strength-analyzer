import re


# =========================================================
# PASSWORD STRENGTH ANALYZER
# =========================================================

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "welcome123",
    "letmein",
    "abc123",
    "iloveyou"
}


COMMON_WORDS = {
    "password",
    "admin",
    "welcome",
    "qwerty",
    "letmein",
    "student",
    "user",
    "login",
    "secret",
    "hello",
    "love"
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
    "def",
    "qwerty"
]


# =========================================================
# PASSWORD ANALYSIS
# =========================================================

def check_password(password):

    score = 0
    warnings = []
    suggestions = []

    password_lower = password.lower()

    # -----------------------------------------------------
    # Basic characteristics
    # -----------------------------------------------------

    length = len(password)

    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_lowercase = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"\d", password))

    has_special = bool(
        re.search(r"""[!@#$%^&*(),.?":{}|<>_\-+=/\\\[\]]""", password)
    )

    # -----------------------------------------------------
    # Length scoring
    # -----------------------------------------------------

    if length < 8:

        suggestions.append(
            "Use at least 8 characters."
        )

    elif length < 12:

        score += 2

        suggestions.append(
            "For better security, use at least 12 characters."
        )

    elif length < 16:

        score += 3

    else:

        score += 4

    # -----------------------------------------------------
    # Character variety
    # -----------------------------------------------------

    if has_uppercase:
        score += 1
    else:
        suggestions.append(
            "Add at least one uppercase letter."
        )

    if has_lowercase:
        score += 1
    else:
        suggestions.append(
            "Add at least one lowercase letter."
        )

    if has_number:
        score += 1
    else:
        suggestions.append(
            "Add at least one number."
        )

    if has_special:
        score += 2
    else:
        suggestions.append(
            "Add at least one special character "
            "(for example: @, #, $, %, !)."
        )

    # -----------------------------------------------------
    # Repeated characters
    # -----------------------------------------------------

    has_repeated_characters = bool(
        re.search(r"(.)\1\1", password)
    )

    if has_repeated_characters:

        score -= 2

        warnings.append(
            "The password contains repeated characters."
        )

        suggestions.append(
            "Avoid repeating the same character three or more times."
        )

    # -----------------------------------------------------
    # Exact common password check
    # -----------------------------------------------------

    is_common_password = password_lower in COMMON_PASSWORDS

    if is_common_password:

        score = 0

        warnings.append(
            "This is a commonly used password."
        )

        suggestions.append(
            "Choose a unique password that is difficult to guess."
        )

    # -----------------------------------------------------
    # Common word inside password
    # -----------------------------------------------------

    detected_common_words = []

    for word in COMMON_WORDS:

        if word in password_lower:

            detected_common_words.append(word)

    contains_common_word = len(detected_common_words) > 0

    if contains_common_word and not is_common_password:

        score -= 2

        words_found = ", ".join(detected_common_words)

        warnings.append(
            f"The password contains a common word: {words_found}."
        )

        suggestions.append(
            "Avoid using common words such as password, admin, "
            "welcome, or qwerty."
        )

    # -----------------------------------------------------
    # Sequential pattern detection
    # -----------------------------------------------------

    detected_patterns = []

    for pattern in SEQUENTIAL_PATTERNS:

        if pattern in password_lower:

            detected_patterns.append(pattern)

    has_sequential_pattern = len(detected_patterns) > 0

    if has_sequential_pattern:

        score -= 2

        patterns_found = ", ".join(detected_patterns)

        warnings.append(
            f"The password contains a predictable pattern: "
            f"{patterns_found}."
        )

        suggestions.append(
            "Avoid predictable sequences such as 123, abc, or qwerty."
        )

    # -----------------------------------------------------
    # Common personal-style words
    # -----------------------------------------------------

    personal_words = [
        "sushma",
        "student",
        "college",
        "school"
    ]

    detected_personal_words = []

    for word in personal_words:

        if word in password_lower:

            detected_personal_words.append(word)

    contains_personal_word = len(detected_personal_words) > 0

    if contains_personal_word:

        score -= 2

        warnings.append(
            "The password may contain a personal or easily "
            "guessable word."
        )

        suggestions.append(
            "Avoid using names or personal information in passwords."
        )

    # -----------------------------------------------------
    # Prevent negative score
    # -----------------------------------------------------

    score = max(score, 0)

    # -----------------------------------------------------
    # Strength classification
    # -----------------------------------------------------

    if score <= 3:

        strength = "WEAK"

    elif score <= 5:

        strength = "MEDIUM"

    elif score <= 7:

        strength = "STRONG"

    else:

        strength = "VERY STRONG"

    return {
        "length": length,
        "uppercase": has_uppercase,
        "lowercase": has_lowercase,
        "number": has_number,
        "special": has_special,
        "repeated": has_repeated_characters,
        "common": is_common_password,
        "common_word": contains_common_word,
        "sequential": has_sequential_pattern,
        "personal": contains_personal_word,
        "score": score,
        "strength": strength,
        "warnings": warnings,
        "suggestions": suggestions
    }


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(results):

    print("\n" + "=" * 55)
    print("              PASSWORD ANALYSIS")
    print("=" * 55)

    print("\nSecurity Characteristics")
    print("-" * 40)

    print(f"Length              : {results['length']}")

    print(
        f"Uppercase           : "
        f"{'✓ Yes' if results['uppercase'] else '✗ No'}"
    )

    print(
        f"Lowercase           : "
        f"{'✓ Yes' if results['lowercase'] else '✗ No'}"
    )

    print(
        f"Numbers             : "
        f"{'✓ Yes' if results['number'] else '✗ No'}"
    )

    print(
        f"Special Characters  : "
        f"{'✓ Yes' if results['special'] else '✗ No'}"
    )

    print(
        f"Repeated Characters : "
        f"{'⚠ Yes' if results['repeated'] else '✓ No'}"
    )

    print(
        f"Common Password     : "
        f"{'⚠ Yes' if results['common'] else '✓ No'}"
    )

    print(
        f"Common Word         : "
        f"{'⚠ Yes' if results['common_word'] else '✓ No'}"
    )

    print(
        f"Predictable Pattern : "
        f"{'⚠ Yes' if results['sequential'] else '✓ No'}"
    )

    print(
        f"Personal Information: "
        f"{'⚠ Yes' if results['personal'] else '✓ No'}"
    )

    # -----------------------------------------------------
    # Strength
    # -----------------------------------------------------

    print("\n" + "-" * 40)

    print(f"Strength            : {results['strength']}")
    print(f"Security Score      : {results['score']}/10")

    # -----------------------------------------------------
    # Warnings
    # -----------------------------------------------------

    if results["warnings"]:

        print("\n⚠ Security Warnings")
        print("-" * 40)

        for warning in results["warnings"]:

            print(f"• {warning}")

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    if results["suggestions"]:

        print("\n💡 Recommendations")
        print("-" * 40)

        unique_suggestions = list(
            dict.fromkeys(results["suggestions"])
        )

        for suggestion in unique_suggestions:

            print(f"• {suggestion}")

    else:

        print("\n✓ No major weaknesses detected.")
        print("✓ Good password structure.")

    print("\n" + "=" * 55)


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=" * 55)
    print("             PASSWORD STRENGTH ANALYZER")
    print("=" * 55)

    print("\nThis tool analyzes password security locally.")
    print("Passwords are not stored or transmitted.")

    password = input("\nEnter password: ")

    if not password:

        print("\n❌ Password cannot be empty.")

        return

    results = check_password(password)

    display_results(results)


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()