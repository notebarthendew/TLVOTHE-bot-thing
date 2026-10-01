import time


POISON_STATUS = "poisoned"
POISON_DURATION_SECONDS = 1 * 60
POISON_WARNING_THRESHOLDS = (
    (0.50, "You feel a strange bump in your heart. It passes, but something feels wrong."),
    (0.25, "Your chest starts to hurt. Each breath feels tighter than the last."),
    (1 / 6, "The pain in your chest is getting worse. You are starting to panic."),
    (1 / 12, "Your heart is pounding painfully and your vision swims. You do not have much time."),
)


def ensure_status_effects(player):
    """Normalize the per-player status list for old save files."""
    statuses = player.setdefault("status", [])
    normalized = []

    for status in statuses:
        if isinstance(status, dict) and isinstance(status.get("name"), str):
            normalized.append(status)
        elif isinstance(status, str):
            normalized.append({"name": status})

    player["status"] = normalized
    return normalized


def add_status_effect(player, name, duration=None, **metadata):
    statuses = ensure_status_effects(player)
    now = time.time()
    status = {"name": name, "applied_at": now}

    if duration is not None:
        status["expires_at"] = now + duration

    status.update(metadata)
    statuses.append(status)
    return status


def has_status_effect(player, name):
    return any(
        status.get("name") == name
        for status in ensure_status_effects(player)
    )


def get_status_text(player):
    statuses = ensure_status_effects(player)
    if not statuses:
        return "None"

    now = time.time()
    visible = []
    for status in statuses:
        name = status["name"].replace("_", " ").title()
        expires_at = status.get("expires_at")
        if isinstance(expires_at, (int, float)) and expires_at > now:
            remaining = max(1, int(expires_at - now))
            visible.append(f"{name} ({remaining}s remaining)")
        else:
            visible.append(name)

    return ", ".join(visible)


def get_expired_statuses(player, now=None):
    now = time.time() if now is None else now
    return [
        status
        for status in ensure_status_effects(player)
        if isinstance(status.get("expires_at"), (int, float))
        and status["expires_at"] <= now
    ]


def get_due_poison_warnings(status, now=None):
    """Return newly due poison warnings and mark them so they are sent once."""
    if not isinstance(status, dict) or status.get("name") != POISON_STATUS:
        return []

    now = time.time() if now is None else now
    applied_at = status.get("applied_at")
    expires_at = status.get("expires_at")
    if not isinstance(applied_at, (int, float)) or not isinstance(expires_at, (int, float)):
        return []

    duration = expires_at - applied_at
    if duration <= 0:
        return []

    warnings_sent = status.setdefault("warnings_sent", [])
    remaining = expires_at - now
    due = []

    for index, (remaining_fraction, message) in enumerate(POISON_WARNING_THRESHOLDS):
        if (
            remaining <= duration * remaining_fraction
            and index not in warnings_sent
        ):
            warnings_sent.append(index)
            due.append(message)

    return due
