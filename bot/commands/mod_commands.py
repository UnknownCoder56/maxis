"""
Moderation slash commands
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from bot.helper import get_random_color, warn_map, refresh_warns
from bot.objects.warn import Warn


def _get_main():
    """Lazy import Main to avoid circular imports during bot startup."""
    from bot.main import Main  # type: ignore

    return Main


def setup_mod_commands(bot: commands.Bot):
    """Setup moderation slash commands"""
    Main = _get_main()

    @bot.tree.command(name="kick", description="Kicks the mentioned user")
    @app_commands.describe(
        user="The user to kick", reason="The reason for kicking (optional)"
    )
    @app_commands.default_permissions(kick_members=True)
    async def kick(
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None,
    ):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            await interaction.guild.kick(user, reason=reason)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully kicked user {user}."
                + (f" Reason: {reason}" if reason else ""),
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I can't kick that user! Reasons - No kick permission, lower role or lower position.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(name="ban", description="Bans the mentioned user")
    @app_commands.describe(
        user="The user to ban", reason="The reason for banning (optional)"
    )
    @app_commands.default_permissions(ban_members=True)
    async def ban(
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None,
    ):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            await interaction.guild.ban(user, reason=reason)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully banned user {user}."
                + (f" Reason: {reason}" if reason else ""),
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I can't ban that user! Reasons - No ban permission, lower role or lower position.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(name="unban", description="Unbans the mentioned user")
    @app_commands.describe(user="The user to unban")
    @app_commands.default_permissions(ban_members=True)
    async def unban(interaction: discord.Interaction, user: discord.User):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            await interaction.guild.unban(user)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully unbanned user {user}.",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I can't unban that user! Reasons - No unban permission.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(
        name="mute", description="Mutes the mentioned user (Mute = Disable chat and VC)"
    )
    @app_commands.describe(user="The user to mute")
    @app_commands.default_permissions(moderate_members=True)
    async def mute(interaction: discord.Interaction, user: discord.Member):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            await user.edit(mute=True, deafen=True)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully muted user {user}.",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I can't mute that user! Reasons - No mute permission, lower role or lower position.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(
        name="unmute",
        description="Unmutes the mentioned user (Mute = Enable chat and VC)",
    )
    @app_commands.describe(user="The user to unmute")
    @app_commands.default_permissions(moderate_members=True)
    async def unmute(interaction: discord.Interaction, user: discord.Member):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            await user.edit(mute=False, deafen=False)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully unmuted user {user}.",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I can't unmute that user! Reasons - No unmute permission.",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(name="warn", description="Warns a user")
    @app_commands.describe(user="The user to warn", cause="The reason for the warning")
    @app_commands.default_permissions(moderate_members=True)
    async def warn(interaction: discord.Interaction, user: discord.Member, cause: str):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        server_id = interaction.guild.id

        if server_id not in warn_map:
            warn_map[server_id] = {}

        if user.id not in warn_map[server_id]:
            warn = Warn(cause, user.id)
            warn_map[server_id][user.id] = warn
        else:
            warn_map[server_id][user.id].new_warn(cause)

        warn = warn_map[server_id][user.id]

        embed = discord.Embed(
            title="Success!",
            description=f"Successfully warned {user} for cause:\n{cause}\n"
            f"They now have {warn.warns} warn(s).",
            color=get_random_color(),
        )
        await interaction.response.send_message(embed=embed)

        # Try to DM user
        try:
            dm_embed = discord.Embed(
                title="Alert!",
                description=f"You have been warned in **{interaction.guild.name}** for reason: **{cause}**. "
                f"You now have **{warn.warns}** warn(s) in that server.",
                color=get_random_color(),
            )
            await user.send(embed=dm_embed)
        except:
            pass

        refresh_warns(Main.CONNSTR)

    @bot.tree.command(name="clearwarns", description="Clear all warns for a user")
    @app_commands.describe(user="The user to clear warns for")
    @app_commands.default_permissions(moderate_members=True)
    async def clear_warn(interaction: discord.Interaction, user: discord.Member):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        server_id = interaction.guild.id

        if server_id in warn_map and user.id in warn_map[server_id]:
            del warn_map[server_id][user.id]
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully removed all warnings for {user}!",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="No warns were found for this user!",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed)

        refresh_warns(Main.CONNSTR)

    @bot.tree.command(name="getwarns", description="Gets all warns for a user")
    @app_commands.describe(user="The user to get warns for")
    @app_commands.default_permissions(moderate_members=True)
    async def get_warns(interaction: discord.Interaction, user: discord.Member):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        server_id = interaction.guild.id

        if server_id in warn_map and user.id in warn_map[server_id]:
            warn = warn_map[server_id][user.id]
            causes = (
                "\n".join(warn.warn_causes)
                if warn.warn_causes
                else "No warns were found for this user!"
            )
        else:
            causes = "No warns were found for this user!"

        embed = discord.Embed(
            title=f"Warns for {user}:-", description=causes, color=get_random_color()
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="clear", description="Clears specified number of messages")
    @app_commands.describe(amount="The number of messages to clear")
    @app_commands.default_permissions(manage_messages=True)
    async def clear_messages(interaction: discord.Interaction, amount: int):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if type(interaction.channel) is not discord.TextChannel:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if amount <= 0 or amount > 100:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="Amount must be between 1 and 100!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        try:
            deleted = await interaction.channel.purge(limit=amount)
            embed = discord.Embed(
                title="Success!",
                description=f"{interaction.user.name} cleared {len(deleted)} message(s) in: {interaction.channel.mention}",
                color=get_random_color(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I don't have permission to manage messages!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )

    @bot.tree.command(name="nuke", description="Cleans everything in a channel")
    @app_commands.default_permissions(manage_channels=True)
    async def nuke(interaction: discord.Interaction):
        if type(interaction.user) is discord.User:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in servers!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:  # type: ignore
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="You don't have admin perms, so you cannot use mod commands!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="This command only works in text channels!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
            return

        channel = interaction.channel
        channel_name = channel.name
        channel_category = channel.category
        channel_topic = channel.topic
        channel_slowmode = channel.slowmode_delay
        channel_nsfw = channel.is_nsfw()
        channel_auto_archive_duration = channel.default_auto_archive_duration
        channel_default_thread_slowmode_delay = channel.default_thread_slowmode_delay
        channel_news = channel.is_news()
        channel_overwrites = channel.overwrites
        channel_position = channel.position

        try:
            # Delete channel
            await channel.delete()

            # Recreate channel
            new_channel = await channel.guild.create_text_channel(
                name=channel_name,
                category=channel_category,
                topic=channel_topic if channel_topic else "",
                slowmode_delay=channel_slowmode,
                nsfw=channel_nsfw,
                default_auto_archive_duration=channel_auto_archive_duration,
                default_thread_slowmode_delay=channel_default_thread_slowmode_delay,
                news=channel_news,
                overwrites=channel_overwrites,
                position=channel_position,
                reason=f"Nuked by {interaction.user.name}",
            )

            embed = discord.Embed(
                title="Success!",
                description=f"Successfully nuked this channel (Nuked By: {interaction.user.name}).",
                color=get_random_color(),
            )
            await new_channel.send(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error!",
                    description="I don't have permission to manage channels!",
                    color=get_random_color(),
                ),
                ephemeral=True,
            )
