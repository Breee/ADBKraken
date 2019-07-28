from adbmanager.manager import ADBmanager
from discord.ext import commands
import time


class ADBCog(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.manager = ADBmanager()

    @commands.command(help="Connects to devices")
    @commands.is_owner()
    async def connect(self, ctx):
        with ctx.typing():
            await ctx.send('Connecting to devices ...')
            outputs = self.manager.connect_all()
            await ctx.send(outputs)

    @commands.command(help="Shows Devices")
    @commands.is_owner()
    async def devices(self, ctx):
        with ctx.typing():
            await ctx.send('Fetching devices ...')
            devices = self.manager.get_devices()
            await ctx.send(devices)

    @commands.command(help="Get Pogo Versions")
    @commands.is_owner()
    async def pogoversion(self, ctx):
        with ctx.typing():
            await ctx.send('Fetching POGO versions ...')
            versions = self.manager.get_pogo_versions()
            await ctx.send(versions)

    @commands.command(help="Reboot device")
    @commands.is_owner()
    async def reboot(self, ctx, device=None):
        with ctx.typing():
            await ctx.send('Rebooting %s ...' % (device if device is not None else 'all devices'))
            output = self.manager.reboot(device)
            await ctx.send(output)
