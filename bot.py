import discord
from discord.ext import commands
import datetime
import time

client = commands.Bot(command_prefix='.')
client.remove_command('help') 
start_time = datetime.datetime.utcnow()

TOKEN = 'TOKEN'


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
    help_embed.add_field(name=';random [min][max]',
                         value='Generates a random number between the minimum and maximum values', inline=False)
    help_embed.add_field(name=';invite', value='Creates an invite link that never expires', inline=False)
    help_embed.add_field(name=';logo', value='Shows the Joyton Corporation logo', inline=False)
    help_embed.add_field(name=';members', value='Displays the amount of members present in the server', inline=False)
    help_embed.add_field(name=';call [message]', value='Allows the user to call a Joytorg Moderator', inline=False)
    help_embed.add_field(name=';uptime', value='Displays the amount of time that the bot has been on for', inline=False)
    help_embed.add_field(name=';ping', value='Shows the connection speed between the client and the bot', inline=False)
    help_embed.add_field(name=';sinfo', value='Displays general server information', inline=False)

    # Administrative Commands
    help_embed.add_field(name='---- Administrative Commands ----', value='A list of administrative commands',
                         inline=False)
    help_embed.add_field(name=';kick [@user] [reason]', value='Kicks the mentioned user', inline=False)
    help_embed.add_field(name=';ban [@user] [reason] ', value='Bans the mentioned user', inline=False)
    help_embed.add_field(name=';unban [username#tag', value='Unbans the mentioned user', inline=False)
    help_embed.add_field(name=';bans', value='Returns a list of banned users', inline=False)
    help_embed.add_field(name=';mute [@user]', value='Mutes the mentioned user', inline=False)
    help_embed.add_field(name=';unmute [@user]', value='Unmutes the mentioned user', inline=False)
    help_embed.add_field(name=';deletechannel [#channel]', value='Deletes the mentioned channel', inline=False)
    help_embed.add_field(name=';deleterole [@role]', value='Deletes the mentioned role', inline=False)
    help_embed.add_field(name=';setAnnounce [message]', value='Allows the user to set a message to send to other users',
                         inline=False)
    help_embed.add_field(name=';announce [@user]',
                         value='DMs the mentioned user the message set after using the "setAnnounce" command',
                         inline=False)
    help_embed.add_field(name=';setShout [message]',
                         value='Allows the user to set a message to post in the #announcements channel', inline=False)
    help_embed.add_field(name=';shout [#channel]',
                         value='Posts the message set after using the "setShout" command in the mentioned channel',
                         inline=False)
    help_embed.add_field(name=';purge [amount]',
                         value='Deletes a specific amount of messages found in the current channel', inline=False)
    help_embed.add_field(name='---- More questions? ----',
                         value='For more information, please contact the creator of this bot: PUT YOUR NAME HERE',
                         inline=False)

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
@commands.has_permissions(kick_members=True)
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
@commands.has_permissions(ban_members=True)
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
@commands.has_permissions(ban_members=True)
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

        if (user.name, user.discriminator) != (member_name, member_discriminator) and banned_users.index(
                ban_entry) == len(banned_users) - 1:
            await ctx.send(embed=invalid_unban_embed)
            return


# ---------------------------------------
# Bans Command
# ---------------------------------------
@client.command()
@commands.has_permissions(ban_members=True)
async def bans(ctx):
    banned_users = await ctx.guild.bans()

    bans_embed = discord.Embed(
        title="Banned users",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    no_banned_users_embed = discord.Embed(
        title="There are no banned users in this server",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )

    if len(banned_users) == 0:
        await ctx.send(embed=no_banned_users_embed)

    else:
        for banned_user in banned_users:
            user = banned_user.user
            bans_embed.add_field(name=f'{user.name}', value=f'#{user.discriminator}', inline=False)

        await ctx.send(embed=bans_embed)


# ---------------------------------------
# Announce Command
# ---------------------------------------
@client.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
    server_name = ctx.guild.name
    server_icon = ctx.guild.icon_url
    members_list = ctx.guild.members

    announce_embed = discord.Embed(
        title=f"Announcement from {server_name}",
        color=discord.Color.blurple(),
        timestamp=datetime.datetime.utcnow()
    )

    announced_embed = discord.Embed(
        title="Success",
        description="Successfully announced your message!",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.utcnow()
    )

    announce_embed.add_field(name=f'Message sent by {ctx.author}', value=f'{message}', inline=False)
    announce_embed.set_thumbnail(url=server_icon)

    for member in members_list:
        try:
            if not member.bot:
                await member.send(embed=announce_embed)
                print(f'Sent a message to {member}')
                time.sleep(1)
        except discord.errors.Forbidden:
            print(f'Could not message {member}')

    await ctx.send(embed=announced_embed)


# ---------------------------------------
# Uptime Command
# ---------------------------------------
@client.command()
async def uptime(ctx):
    current_time = datetime.datetime.utcnow()
    uptime = current_time - start_time
    uptime = str(uptime)
    uptime_index = uptime.index('.')

    if int(uptime[uptime_index + 1]) >= 5 and int(uptime[uptime_index - 1]) != 9:
        uptime_list = list(uptime)
        uptime_list[uptime_index - 1] = str(int(uptime_list[uptime_index - 1]) + 1)
        uptime = "".join(uptime_list)

    uptime = uptime[:uptime.index('.')]

    uptime_embed = discord.Embed(
        title=f"This bot has been up for {uptime} hours",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )

    await ctx.send(embed=uptime_embed)


# ---------------------------------------
# Members Command
# ---------------------------------------
@client.command()
async def members(ctx):
    members_list = ctx.guild.members
    total_members_count = len(members_list)
    online_members_count = 0
    offline_members_count = 0
    idle_members_count = 0

    for i in members_list:
        if str(i.status) == "online":
            online_members_count += 1
        elif str(i.status) == "offline":
            offline_members_count += 1
        elif str(i.status) == "idle":
            idle_members_count += 1

    members_embed = discord.Embed(
        color=discord.Color.dark_teal(),
        timestamp=datetime.datetime.utcnow()
    )

    members_embed.add_field(name='Members', value=f'{total_members_count}', inline=True)
    members_embed.add_field(name='Online', value=f'{online_members_count}', inline=True)
    members_embed.add_field(name='Offline', value=f'{offline_members_count}', inline=True)
    members_embed.add_field(name='Idle', value=f'{idle_members_count}', inline=False)

    await ctx.send(embed=members_embed)


client.run(TOKEN)
