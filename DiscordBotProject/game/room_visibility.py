import discord

from game.map import ROOMS


def get_room_channel(guild: discord.Guild, room_id: str):
    """Return a room's main channel (or forum), if it is available."""
    channel_id = ROOMS[room_id]["channel_id"]
    return guild.get_channel(channel_id) or guild.get_thread(channel_id)


def get_room_command_channel(guild: discord.Guild, room_id: str):
    """Return the channel/thread where commands for a room are sent."""
    channel_id = ROOMS[room_id]["command_channel_id"]
    return guild.get_channel(channel_id) or guild.get_thread(channel_id)


async def _set_channel_visibility(channel, member: discord.Member, visible: bool):
    """Apply an overwrite only to channels that support permission overwrites."""
    if isinstance(channel, discord.abc.GuildChannel):
        await channel.set_permissions(
            member,
            view_channel=visible,
            read_message_history=False,
        )


async def _remove_from_private_threads(member: discord.Member, forum: discord.ForumChannel):
    for thread in forum.threads:
        if thread.is_private():
            try:
                await thread.remove_user(member)
            except (discord.Forbidden, discord.HTTPException):
                pass


async def reveal_forum_threads(
    member: discord.Member,
    forum: discord.ForumChannel,
    command_thread: discord.Thread | None = None,
):
    """Give a player access to this forum's active private room threads.

    Public threads inherit the forum's visibility; Discord only permits explicit
    membership changes on private threads.
    """
    threads = {thread.id: thread for thread in forum.threads}
    if command_thread is not None and command_thread.parent_id == forum.id:
        threads[command_thread.id] = command_thread

    for thread in threads.values():
        if thread.is_private() and not thread.archived:
            try:
                await thread.add_user(member)
            except (discord.Forbidden, discord.HTTPException):
                pass


async def set_player_room(guild: discord.Guild, member: discord.Member, room_id: str):
    """Hide every game room from a player, then reveal only ``room_id``."""
    if room_id not in ROOMS:
        raise ValueError(f"Unknown room: {room_id}")

    seen_channel_ids = set()
    for candidate_room in ROOMS:
        channel = get_room_channel(guild, candidate_room)
        if channel is None or channel.id in seen_channel_ids:
            continue

        seen_channel_ids.add(channel.id)
        await _set_channel_visibility(channel, member, visible=False)
        if isinstance(channel, discord.ForumChannel):
            await _remove_from_private_threads(member, channel)

    current_channel = get_room_channel(guild, room_id)
    if current_channel is None:
        return

    await _set_channel_visibility(current_channel, member, visible=True)
    if isinstance(current_channel, discord.ForumChannel):
        command_channel = get_room_command_channel(guild, room_id)
        command_thread = (
            command_channel if isinstance(command_channel, discord.Thread) else None
        )
        await reveal_forum_threads(member, current_channel, command_thread)


async def hide_all_game_rooms(guild: discord.Guild, member: discord.Member):
    """Hide game rooms from a dead player while retaining deterministic overrides."""
    seen_channel_ids = set()
    for room_id in ROOMS:
        channel = get_room_channel(guild, room_id)
        if channel is None or channel.id in seen_channel_ids:
            continue

        seen_channel_ids.add(channel.id)
        await _set_channel_visibility(channel, member, visible=False)
        if isinstance(channel, discord.ForumChannel):
            await _remove_from_private_threads(member, channel)


async def clear_player_room_visibility(guild: discord.Guild, member: discord.Member):
    """Remove all game-room overrides once a player leaves the game."""
    seen_channel_ids = set()
    for room_id in ROOMS:
        channel = get_room_channel(guild, room_id)
        if channel is None or channel.id in seen_channel_ids:
            continue

        seen_channel_ids.add(channel.id)
        if isinstance(channel, discord.abc.GuildChannel):
            await channel.set_permissions(member, overwrite=None)
        if isinstance(channel, discord.ForumChannel):
            await _remove_from_private_threads(member, channel)
