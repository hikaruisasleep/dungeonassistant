import lavasnek_rs as Lavasnek

class EventHandler:
    async def track_start(self, _: Lavasnek.Lavalink, event: Lavasnek.TrackStart) -> None:
        print(f"Track started on guild: {event.guild_id}")

    async def track_finish(self, _: Lavasnek.Lavalink, event: Lavasnek.TrackFinish) -> None:
        print(f"Track finished on guild: {event.guild_id}")

    async def track_exception(self, lavalink: Lavasnek.Lavalink, event: Lavasnek.TrackException) -> None:
        print(f"Track exception event happened on guild: {event.guild_id}")
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)
        if skip and node:
            if not node.queue and not node.now_playing:
                await lavalink.stop(event.guild_id)


