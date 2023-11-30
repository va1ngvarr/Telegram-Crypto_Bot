def retrieve_percent(expression: str) -> float:
    if "%" in expression:
        expression = expression.replace("%", "")
        a, b = expression.split("*")
        a, b = float(a), float(b)
    return a * b / 100
