def merge_field(existing: str, incoming: str) -> str:
    """Combine an existing text field with a new value without dropping either.

    Blank incoming is a no-op, blank existing is filled, identical (trimmed)
    values collapse to one, otherwise both are kept, joined by "; ".
    """
    existing_trimmed = existing.strip()
    incoming_trimmed = incoming.strip()
    if not incoming_trimmed:
        return existing_trimmed
    if not existing_trimmed:
        return incoming_trimmed
    if existing_trimmed == incoming_trimmed:
        return existing_trimmed
    return f"{existing_trimmed}; {incoming_trimmed}"
