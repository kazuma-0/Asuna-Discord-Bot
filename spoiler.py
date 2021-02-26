import discord
from discord.ext import commands

class Spoiler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command()
    async def spoiler(self, ctx):
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
