#test
import discord
from datetime import datetime
from discord.ext import commands


from core import checks
from core.models import PermissionLevel

options_menu="You have provided invalid dept code.\n\n`mod` - Moderation Team\n`pt` - Partnership Team\n`events` - Events Team\n`admin` - Administration Team\n"

DEPS_DATA = {
    "mod": {
        "category_id": 1254462396031041586,
        "pretty_name": "Moderation Team",
        "reminders": "If you are reporting someone, please send their [user ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) and proof of what you are reporting.",
        "role_id": 1254463174900715632,
        "send_message_to_user": True
    },
    "pt": {
        "category_id": 1254462461482893373,
        "pretty_name": "Partnership Team",
        "reminders": "If you are partnering with our server, please make sure your ad is **at least** 150-200 characters. We recommend that your ad be longer and goes into good detail about what your server offers.",
        "role_id": 1254463282845188207,
        "send_message_to_user": True
    },
        "events": {
        "category_id": 1270840489637318829,
        "pretty_name": "Events Team",
        "reminders": "If you need a code, please provide a message link or screenshot of the use keypad command.",
        "role_id": 1258207036358004826,
        "send_message_to_user": True
    },
    "admin": {
        "category_id": 1254463580733182083,
        "pretty_name": "Administration Team",
        "reminders": "If you are reporting a staff member, please send their [user ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) and proof.",
        "role_id": 1254459655724204115,
        "send_message_to_user": True
    },
}
class HOS(commands.Cog, name="HOS Main Commands"):
    def __init__(self, bot):
        self.bot = bot
        
        
       
    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def transfer(self, ctx, *, to: str=None):
        """Command that transfers thread to other departments."""
        if to is None:
            embed = discord.Embed(title=f"Department Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Department Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        if data["send_message_to_user"]:
            mes = "You are being transferred to **`"
            mes += data["pretty_name"]
            mes += "`**.\n"
            mes += "Please remain __patient__ while we find a suitable staff member to assist in your request.\n\n"
            
            if data["reminders"] is not None:
                mes += "**__Reminders__**\n"
                mes += data["reminders"]

            msg = ctx.message
            msg.content = mes
            
            await ctx.thread.reply(msg, anonymous = False)
        
        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("<@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def stransfer(self, ctx, to: str=None):
        """Silently transfers thread"""
        if to is None:
            embed = discord.Embed(title=f"Silent Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Silent Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("Silent Transfer - <@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def id(self, ctx):
        await ctx.send(ctx.thread.id)

async def setup(bot):
    await bot.add_cog(HOS(bot))
