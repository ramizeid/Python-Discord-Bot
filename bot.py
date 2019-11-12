import discord
from discord.ext import commands
import datetime

client = commands.Bot(command_prefix='.')
client.remove_command('help')

TOKEN = 'PUT YOUR TOKEN HERE!'


# ---------------------------------------
# Bot Initialization
# ---------------------------------------
@client.event
async def on_ready():
    print('Bot is ready.')


# ---------------------------------------
# Help Command
# ---------------------------------------
@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title="Help is here!",
        color=discord.Color.dark_green(),
        timestamp=datetime.datetime.utcnow()
    )

    # Public Commands
    help_embed.add_field(name='---- Public Commands ----', value='A list of public commands', inline=False)
    help_embed.add_field(name=';help', value='Lists available commands', inline=False)
    help_embed.add_field(name=';random [min][max]', value='Generates a random number between the minimum and maximum values', inline=False)
    help_embed.add_field(name=';invite', value='Creates an invite link that never expires', inline=False)
    help_embed.add_field(name=';logo', value='Shows the Joyton Corporation logo', inline=False)
    help_embed.add_field(name=';members', value='Displays the amount of members present in the server', inline=False)
    help_embed.add_field(name=';call [message]', value='Allows the user to call a Joytorg Moderator', inline=False)
    help_embed.add_field(name=';uptime', value='Displays the amount of time that the bot has been on for', inline=False)
    help_embed.add_field(name=';ping', value='Shows the connection speed between the client and the bot', inline=False)
    help_embed.add_field(name=';sinfo', value='Displays general server information', inline=False)

    # Administrative Commands
    help_embed.add_field(name='---- Administrative Commands ----', value='A list of administrative commands', inline=False)
    help_embed.add_field(name=';kick [@user] [reason]', value='Kicks the mentioned user', inline=False)
    help_embed.add_field(name=';ban [@user] [reason] ', value='Bans the mentioned user', inline=False)
    help_embed.add_field(name=';unban [username#tag', value='Unbans the mentioned user', inline=False)
    help_embed.add_field(name=';bans', value='Returns a list of banned users', inline=False)
    help_embed.add_field(name=';mute [@user]', value='Mutes the mentioned user', inline=False)
    help_embed.add_field(name=';unmute [@user]', value='Unmutes the mentioned user', inline=False)
    help_embed.add_field(name=';deletechannel [#channel]', value='Deletes the mentioned channel', inline=False)
    help_embed.add_field(name=';deleterole [@role]', value='Deletes the mentioned role', inline=False)
    help_embed.add_field(name=';setAnnounce [message]', value='Allows the user to set a message to send to other users', inline=False)
    help_embed.add_field(name=';announce [@user]', value='DMs the mentioned user the message set after using the "setAnnounce" command', inline=False)
    help_embed.add_field(name=';setShout [message]', value='Allows the user to set a message to post in the #announcements channel', inline=False)
    help_embed.add_field(name=';shout [#channel]', value='Posts the message set after using the "setShout" command in the mentioned channel', inline=False)
    help_embed.add_field(name=';purge [amount]', value='Deletes a specific amount of messages found in the current channel', inline=False)
    help_embed.add_field(name='---- More questions? ----', value='For more information, please contact the creator of this bot: PUT YOUR NAME HERE', inline=False)

    await ctx.author.send(embed=help_embed)
    await ctx.send(f'A list of available commands has been sent to you by DMs. {ctx.author.mention}')


# ---------------------------------------
# Ping Command
# ---------------------------------------
@client.command()
async def ping(ctx):
    bot_ping = client.latency

    ping_embed = discord.Embed(
        title="Ping",
        description=f"{round(bot_ping * 1000)} ms",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )

    await ctx.send(embed=ping_embed)


# ---------------------------------------
# Kick Command
# ---------------------------------------
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    kick_embed = discord.Embed(
        title="User kicked",
        description=f"Successfully kicked {member.mention}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    await member.kick(reason=reason)
    await ctx.send(embed=kick_embed)


# ---------------------------------------
# Ban Command
# ---------------------------------------
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    ban_embed = discord.Embed(
        title="User banned",
        description=f"Successfully banned {member.mention}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    await member.ban(reason=reason)
    await ctx.send(embed=ban_embed)


# ---------------------------------------
# Unban Command
# ---------------------------------------
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    valid_unban_embed = discord.Embed(
        title="User unbanned",
        description=f"Successfully unbanned {member}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    invalid_unban_embed = discord.Embed(
        title="User is not banned!",
        description=f"{member} is not banned",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(embed=valid_unban_embed)
            return

        if (user.name, user.discriminator) != (member_name, member_discriminator) and banned_users.index(ban_entry) == len(banned_users) - 1:
            await ctx.send(embed=invalid_unban_embed)
            return


# ---------------------------------------
# Bans Command
# ---------------------------------------
@client.command()
async def bans(ctx):
    banned_users = await ctx.guild.bans()

    bans_embed = discord.Embed(
        title="Banned users",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    for banned_user in banned_users:
        user = banned_user.user

        bans_embed.add_field(name=f'{user.name}', value=f'#{user.discriminator}', inline=False)

    await ctx.send(embed=bans_embed)


client.run(TOKEN)
