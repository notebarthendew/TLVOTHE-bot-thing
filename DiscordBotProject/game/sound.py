from collections import deque
from typing import Optional

from game.map import ROOMS
from game.player import players


def _find_direction(from_room: str, to_room: str) -> Optional[str]:
    """Find whether to_room is front/back relative to from_room on the shortest path.
    Returns 'front' or 'back' if determinable, else None.
    """
    if from_room == to_room:
        return None

    q = deque()
    # Each entry: (current_room, first_step)
    q.append((from_room, None))
    visited = {from_room}

    while q:
        room, first = q.popleft()
        # neighbors
        front = ROOMS.get(room, {}).get("front")
        back = ROOMS.get(room, {}).get("back")
        for neigh, direction in ((front, "front"), (back, "back")):
            if not neigh or neigh in visited:
                continue
            visited.add(neigh)
            nf = first if first is not None else direction
            if neigh == to_room:
                return nf
            q.append((neigh, nf))
    return None


async def notify_sound(
    guild,
    source_room: str,
    event: str = "generic",
    full_message: Optional[str] = None,
    shooter: Optional[str] = None,
    target: Optional[str] = None,
    radius: int = 1,
    exclude_ids: list | None = None,
):
    """Notify players by DM about an event happening in/near source_room.

    event: 'generic', 'gunshot', 'clatter', 'pickup', 'arrival'
    full_message: optional full textual message (used when recipient is in same room)
    shooter/target: display names for contextual messages
    radius: number of room hops sound propagates
    """
    import discord

    if exclude_ids is None:
        exclude_ids = []

    # Determine reachable rooms within radius using BFS
    if radius is None:
        reachable = set(ROOMS.keys())
    else:
        reachable = set()
        q = deque()
        q.append((source_room, 0))
        while q:
            room, dist = q.popleft()
            if room in reachable:
                continue
            reachable.add(room)
            if dist >= radius:
                continue
            front = ROOMS.get(room, {}).get("front")
            back = ROOMS.get(room, {}).get("back")
            for neigh in (front, back):
                if neigh and neigh not in reachable:
                    q.append((neigh, dist + 1))

    separator = "-.-.-.-.-.-.-"

    for user_id, pdata in players.items():
        try:
            if user_id in exclude_ids:
                continue
            if not pdata.get("alive", True):
                continue
            room = pdata.get("room")
            if room not in reachable:
                continue
            member = guild.get_member(int(user_id))
            if member is None:
                continue

            # Build contextual message
            if event == "gunshot":
                if room == source_room:
                    # same room: include full message if provided, else descriptive
                    body = full_message or (f"A gunshot rings out nearby and someone falls.")
                else:
                    # different room: directional hint only
                    direction = _find_direction(room, source_room)
                    if direction:
                        body = f"You hear a loud gunshot coming from the {direction} of the train."
                    else:
                        body = f"You hear a loud gunshot somewhere on the train."
            elif event == "clatter":
                if room == source_room:
                    body = "You hear a clatter as something hits the floor."
                else:
                    direction = _find_direction(room, source_room)
                    if direction:
                        body = f"You hear the sound of something dropping from the {direction} of the train."
                    else:
                        body = f"You hear a clatter somewhere on the train."
            elif event == "arrival":
                # arrival: if same room, send full_message (arrival text), else small hint
                if room == source_room:
                    body = full_message or f"Someone arrives here."
                else:
                    direction = _find_direction(room, source_room)
                    if direction:
                        body = f"You hear footsteps arriving from the {direction} of the train."
                    else:
                        body = f"You hear footsteps somewhere on the train."
            elif event == "pickup":
                if room == source_room:
                    body = full_message or f"You hear someone handling something here."
                else:
                    direction = _find_direction(room, source_room)
                    if direction:
                        body = f"You hear a small sound coming from the {direction} of the train."
                    else:
                        body = f"You hear a small sound somewhere on the train."
            else:
                # generic
                if room == source_room:
                    body = full_message or "You notice activity nearby."
                else:
                    direction = _find_direction(room, source_room)
                    if direction:
                        body = f"You notice activity coming from the {direction} of the train."
                    else:
                        body = f"You notice some activity elsewhere on the train."

            dm_text = f"{separator}\n{body}"

            try:
                await member.send(dm_text)
            except (discord.Forbidden, discord.HTTPException):
                pass
        except Exception:
            pass


async def notify_global(guild, message: str):
    """Notify every alive player in the game via DM."""
    import discord
    separator = "-.-.-.-.-.-.-"
    for user_id, pdata in players.items():
        try:
            if not pdata.get("alive", True):
                continue
            member = guild.get_member(int(user_id))
            if member is None:
                continue
            try:
                await member.send(f"{separator}\n# [Announcement] {message}")
            except (discord.Forbidden, discord.HTTPException):
                pass
        except Exception:
            pass
