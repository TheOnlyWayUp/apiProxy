import discord, asyncio, aiohttp, jishaku
from discord.ext import commands

# set the profix to h! and !!
bot = commands.Bot(command_prefix=["h!", "!!"], intents=discord.Intents.all())
bot.load_extension("jishaku")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Error handler.
    Args:
        ctx (commands.Context): Provided by system.
        error (commands.CommandError): The error object.
    Raises:
        error: Raises error if undocumented.
    """
    # raise error
    # Command not found
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction("⁉️")
        message = "Command not found."
    # On cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.message.add_reaction("❌")
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    # User doesn't have permissions
    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction("🔐")
        message = "No permissions."
    elif isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction("🤏")
        message = "Bad argument."
    # Not enough args
    elif isinstance(error, commands.UserInputError):
        await ctx.message.add_reaction("🤏")
        message = f"Not all required arguments were passed, do `{bot.command_prefix[0]}help {ctx.message.content[2:]}`"
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction("🤏")
        message = f"Not all required arguments were passed, do `{bot.command_prefix[0]}help {ctx.message.content[2:]}`"
    # Mentioned member not found
    elif isinstance(error, commands.MemberNotFound):
        await ctx.message.add_reaction("🤷‍♂️")
        message = "Couldn't find that member."
    # Bot doesn't have permissions
    elif isinstance(error.original, discord.errors.Forbidden):
        await ctx.message.add_reaction("📛")
        message = "Bot doesn't have the permissions needed."
    else:
        message = "This is an undocumented error, it has been reported and will be patched in the next update."
        raise error
    await ctx.send(embed=discord.Embed(title=message, color=0x992D22))


async def newHwid(hwid):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/addHwid",
            headers={"Authorisation": "mcStalkerBased", "hwid": hwid},
        ) as resp:
            return await resp.json()


@bot.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        if before.id == 505713760124665867:
            await after.edit(nick="_T1MPy_ (very cool)")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(help="Add a HWID to the database.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def add(ctx, hwid, owner: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/addHwid",
            headers={
                "Authorisation": "mcStalkerBased",
                "hwid": hwid,
                "owner": str(owner.id),
            },
        ) as resp:
            if resp.status == 200:
                await ctx.send("HWID added to database.")
                return
    await ctx.send("Failed.")


@bot.command(help="Check if a HWID is valid.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def check(ctx, hwid):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/checkHwidAuth",
            headers={"Authorisation": "mcStalkerBased", "hwid": hwid},
        ) as resp:
            if await resp.text() == "true":
                await ctx.send(f"HWID is valid. {await resp.text()}")
                return
    await ctx.send("HWID is invalid.")


@bot.command(help="Ping grief request.")
@commands.has_any_role(919324337171988561, 930464825446891580)
async def griefReq(ctx):
    await ctx.send(
        content="<@&919324310378790992>",
        embed=discord.Embed(
            title="Grief request",
            description=f"Sent by {ctx.author.mention}.",
            color=0x992D22,
        ),
    )


@bot.command(help="Show Illegitimate HWIDs.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def illegal(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/returnIllegitimateHwids",
            headers={"Authorisation": "mcStalkerBased"},
        ) as resp:
            text = await resp.json()
            em = discord.Embed(title="Illegitimate HWIDs")
            for d in text:
                ipList = ", ".join(d[list(d.keys())[0]]["ip"])
                em.add_field(
                    name=list(d.keys())[0],
                    value=f"Owner - {d[list(d.keys())[0]]['id']}.\nIPs - {ipList}",
                )
            await ctx.send(embed=em)
            return


@bot.command(help="Revoke a HWID.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def revoke(ctx, hwid):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/revokeHWID",
            headers={"Authorisation": "mcStalkerBased", "hwid": hwid},
        ) as resp:
            await ctx.send(f"HWID status -. {await resp.text()}")
            return


@bot.command(help="Show all HWIDs.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def all(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/returnAllHwids",
            headers={"Authorisation": "mcStalkerBased"},
        ) as resp:
            text = await resp.json()
            em = discord.Embed(title="All HWIDs", description="\n".join(text["list"]))
            for key in text.keys():
                if key != "list":
                    try:
                        mention = bot.get_user(int(text[key]["id"])).mention
                    except:
                        mention = "Not a Discord Member."
                    em.add_field(
                        name=key,
                        value=f'Owner - {text[key]["id"]} - {mention}.\nIPs - {", ".join(text[key]["ip"])}',
                    )

    await ctx.send(embed=em)


@bot.command(help="Change the version.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def changeVersion(
    ctx, version: str, downloadUrl: str, authorisedBy: discord.Member
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/changeVersion",
            headers={
                "Authorisation": "mcStalkerBased",
                "version": version,
                "downloadUrl": downloadUrl,
                "authorisedBy": str(authorisedBy.id),
            },
        ) as resp:
            await ctx.send(f"Version status - {await resp.text()}")
            return


@bot.command(help="Show the version.")
@commands.has_any_role(919327476742750208, 924233487643451402)
async def version(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://uhhimactuallyoutheretouhhgetacupcake.mcson.top/mod/showVersion",
            headers={"Authorisation": "mcStalkerBased"},
        ) as resp:
            data = await resp.json()
            try:
                mention = bot.get_user(int(data["authorisedBy"])).mention
            except:
                mention = "Not a Discord Member."
            em = discord.Embed(
                title=f"Version {data['versionString']}",
                description=f"Download URL - {data['downloadUrl']}\nAuthorised By - {data['authorisedBy']} - {mention}",
            )
            await ctx.send(embed=em)
            return


token = "OTE5NTYzMDQ0NjEzNDAyNjI1.YbXn0g.Xk5wgPMJnQ1N9cUpRFqKrmUTgzs"
bot.run(token)
