from adbmanager.manager import ADBmanager
from discord.ext import commands
import time


class ADBCog(commands.Cog, name="ADBKraken"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.manager = ADBmanager()

    @commands.command(help="Connects to devices (bot owner only)")
    @commands.is_owner()
    async def connect(self, ctx):
        with ctx.typing():
            await ctx.send('Connecting to devices ...')
            outputs = await self.manager.connect_all()
            message = "```diff\n"
            for device,serial,out,err in outputs:
                if 'connected' in out:
                    message += f"+ [{serial:>12}] [{device:>12}] [  OK]\n"
                else:
                    message += f"- [{serial:>12}] [{device:>12}] [DEAD]\n"
            message += "```"
            await ctx.send(message)


    @commands.command(help="Get Pogo Versions (bot owner only)")
    @commands.is_owner()
    async def pogoversion(self, ctx):
        with ctx.typing():
            await ctx.send('Fetching POGO versions ...')
            versions = self.manager.get_pogo_versions()
            await ctx.send(versions)

    @commands.command(help="Reboot device (bot owner only)")
    @commands.is_owner()
    async def reboot(self, ctx, *device_names):
        with ctx.typing():
            await ctx.send('Rebooting %s ...' % (str(device_names) if device_names is not None else 'all devices'))
            output = self.manager.reboot(device_names)
            await ctx.send(output)
