import os
import json
#import DiscordUtils

from keep_alive import keep_alive

import discord
from discord.ext import commands
import random

from dotenv import load_dotenv
from discord.ext.commands import has_any_role
from discord_components import DiscordComponents, InteractionType

import anilist_commands

intents = discord.Intents().default()
intents.members = True

load_dotenv()

# Load variables
if os.getenv("TESTING"):
    # If we're on testing, read testing.json
    # This file is gitignored, so it can have channel IDs and stuff from testing servers
    data_file = "testing.json"
else:
    # Otherwise read data.json
    data_file = "data.json"

with open(data_file, "r") as f:
    data = json.loads(f.read())

bot = commands.Bot(command_prefix=commands.when_mentioned_or(data["prefix"]),
                   intents=intents)
bot.remove_command("help")
#music = DiscordUtils.Music()


@bot.event
async def on_ready():
    activity = discord.Game("Sword Art Online")
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=activity)
    print("Logged in as", bot.user)
    DiscordComponents(bot)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Yuuki Asuna",
        description=
        "Vice-commander of KoB, Lightning Flash, Queen Titania, Berserk Healer, "
        + "Goddess Stacia, and Kirito's lover.",
        colour=discord.Color.blurple(),
        url="https://swordartonline.fandom.com/wiki/Yuuki_Asuna")

    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

    embed.set_image(url="https://i.imgur.com/2IuzcTL.png")
    embed.set_thumbnail(url="https://i.imgur.com/WBCCIVZ.png")

    #embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="help",
                    value=f"My command prefix is `{data['prefix']}`",
                    inline=False)
    embed.add_field(
        name="Anilist",
        value="Displays Anilist search commands on entering `,search`",
        inline=False)
    embed.add_field(
        name="Fun",
        value="Fun media commands: `,hug`,`,kiriasu`,`,kiss`,`,avatar`.",
        inline=False)
    embed.add_field(
        name="Spoiler",
        value="To send spoiler images `,spoiler` followed by the media.",
        inline=False)
    embed.add_field(name="Music",
                    value="Music commands: `,play`, `,join`,`,leave`.",
                    inline=False)
    embed.add_field(name="Mod",
                    value="Moderation commands: `,kick`, `,ban`,`,unban`.",
                    inline=False)
    embed.add_field(name="Asuna discord",
                    value="[Discord](https://discord.gg/kxWma5eUD7)",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command()
@has_any_role(*data["say_whitelist"])
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("no u")


@bot.command()
async def pick(ctx):
    response = ["Season 1", "Season 2", "Season 3", "Ordinal Scale"]
    await ctx.send(f"{random.choice(response)}")


@bot.command()
async def greet(ctx):
    await ctx.message.delete()
    await ctx.send(
        "Welcome to the guild! <:StaciaWelcome:795197458933481512>   ")


#if not os.getenv("TESTING"):

#Start webserver for uptime robot to ping
#import keep_alive
#keep_alive.keep_alive()


class Spoiler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context,
                                error: commands.CommandError):
        await ctx.send("An error occurred: {}".format(str(error)))


#image spoiler function


@bot.command()
async def spoiler(ctx):
    try:
        attachment = ctx.message.attachments[0]
    except IndexError:
        await ctx.message.delete()
        await ctx.send("Attachment not found.")
    # rename image
    attachment.filename = f"SPOILER_{attachment.filename}"
    spoiler_image = await attachment.to_file()
    await ctx.message.delete()
    await ctx.send(f"Sent by {ctx.author.name}")
    await ctx.send(file=spoiler_image)


#clear function


@bot.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


#Media fuctions


@bot.command()
async def kiss(ctx):
    response = [
        "https://i.imgur.com/3Y0oyYf.gif",
        "https://i.imgur.com/zAstcLf.gif",
        'https://i.imgur.com/LFuPdLM.gif',
        "https://i.imgur.com/HFSQlWW.gif",
        "https://i.imgur.com/JOWcJe5.gif",
    ]
    embed1 = discord.Embed(title="Recieved a kiss from Asuna",
                           color=discord.Color.blurple())
    embed1.set_image(url=random.choice(response))
    await ctx.send(embed=embed1)


@bot.command()
async def kiriasu(ctx):
    response = [
        "https://media1.tenor.com/images/4c8112155e616909833d74d1abcf9b4e/tenor.gif?itemid=18200842",
        'https://media1.tenor.com/images/edea458dd2cbc76b17b7973a0c23685c/tenor.gif?itemid=13041472',
        "https://i.imgur.com/QJPTkZn.gif", "https://i.imgur.com/R7DZ1vR.gif",
        "https://i.imgur.com/dUkmcq9.gif", 'https://i.imgur.com/3Cb0pil.gif',
        "https://i.imgur.com/7dxlB7j.gif", "https://i.imgur.com/fII9NJ2.gif",
        "https://i.imgur.com/Q6CR6P2.gif"
    ]
    embed1 = discord.Embed(title="Here is your daily dose of KiriAsu",
                           color=discord.Color.blurple())
    embed1.set_image(url=random.choice(response))
    await ctx.send(embed=embed1)


@bot.command()
async def hug(ctx):
    response = [
        "https://i.imgur.com/pOwuQvD.gif", 'https://i.imgur.com/h5UmDP7.gif',
        "https://i.imgur.com/KhbncbD.gif", "https://i.imgur.com/YniZ5n0.gif",
        "https://i.imgur.com/DN3RtQM.gif", "https://i.imgur.com/jNiBxd2.gif"
    ]
    embed1 = discord.Embed(title="Recieved a hug from Asuna",
                           color=discord.Color.blurple())
    embed1.set_image(url=random.choice(response))
    await ctx.send(embed=embed1)


@bot.command()
async def avatar(ctx):
    response = [
        "https://cdn.discordapp.com/attachments/794837349628117021/847548986616840212/575.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548977477058600/562.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548972528566282/545.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548972063260702/559.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548964621778974/544.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548958402150460/543.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548949971206224/542.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548946669764628/532.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548930094268426/524.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548928832045056/522.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548922935115846/523.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548913480630293/521.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548908900319342/517.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548902323388426/510.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548884381204500/498.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548876038471730/497.png"
        "https://cdn.discordapp.com/attachments/794837349628117021/847548873852846110/496.png"
        "https://cdn.discordapp.com/attachments/794837349628117021/847548865335132200/495.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548858727661658/477.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548847193849896/473.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548835584540712/473.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548816081420318/450.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548803498377216/443.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548790055501874/419.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548777866723418/418.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548765560897556/417.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548755548307506/416.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548747066900510/412.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548735495733305/410.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548726717186058/409.jpg",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548717418151966/385.png",
        "https://cdn.discordapp.com/attachments/794837349628117021/847548705728626688/226.jpg"
    ]
    embed1 = discord.Embed(title="Here is your Asuna avatar",
                           color=discord.Color.blurple())
    embed1.set_image(url=random.choice(response))
    await ctx.send(embed=embed1)


#poll fucntion
@bot.command()
async def poll(ctx, *, message):
    embed = discord.Embed(title="Poll",
                          description=f"{message}",
                          colour=discord.Color.red())
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('⬆')
    await msg.add_reaction('⬇')


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(790857658856898560)  #GUILD ID
    welcome_channel = guild.get_channel(790857658856898566)  #CHANNEL ID
    role = guild.get_role(794458597706039338)  #ROLE ID
    if member.guild.id == 790857658856898560:
        await welcome_channel.send(
            f"**A new member has registered to Asuna's guild, everyone welcome** {member.mention}!"
        )
        embed = discord.Embed(
            colour=15158332,
            description=
            f"""You are the **{guild.member_count}th** member of the guild. **Asuna** wants you to have a sandwich! Once you are done with her delicious snack, please check these channels  <#790857658856898562>, <#794928177423974400>, <#794928219077607424> to grab some roles and gain more information on the guild. Enjoy your stay!
            
            **NOTE:** In order to be able to send messages you will have to **react to the emoji** in <#790857658856898562>!"""
        )
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_image(url="https://i.imgur.com/t9lI56U.gif")
        embed.set_author(name="Welcome to Asuna's Guild",
                         icon_url=guild.icon_url)

        await welcome_channel.send(embed=embed)
        await member.add_roles(role)
        #await welcome_channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !')

    #kick function


@bot.command()
@has_any_role(*data["say_whitelist"])
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked from the server, reason: {reason}")


#unban function


@bot.command()
@has_any_role(*data["say_whitelist"])
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_tag = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.tag) == (member_name, member_tag):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.tag}')


#music function


@bot.command()
async def join(ctx):
    voiceTrue = ctx.author.voice
    if voiceTrue is None:
        return await ctx.send(
            "You currently aren't connected to a voice channel.")
    await ctx.author.voice.channel.connect()
    await ctx.send('Joined the voice chanel.')


@bot.command()
async def leave(ctx):
    voiceTrue = ctx.author.voice
    myvoiceTrue = ctx.guild.me.voice
    if voiceTrue is None:
        return await ctx.send(
            "You currently aren't connected to a voice channel.")
    if myvoiceTrue is None:
        return await ctx.send("I'm not currently connected to a voice channel."
                              )
    await ctx.voice_client.disconnect()
    await ctx.send('Left the voice chanel.')


@bot.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f'I have started playing `{song.name}`')
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f'`{song.name}` has been added to the playlist')


#queue function
@bot.command
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(
        f"{','.join([song.name for song in player.current_queue()])}")


#pause function
@bot.command
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f'Paused {song.name} successfully!')


#resume function
@bot.command
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f'Resumed {song.name} successfully!')


keep_alive()
# Add the anilist cog
bot.add_cog(anilist_commands.AniList(bot))
# Start the bot
bot.run(os.getenv("TOKEN"))
