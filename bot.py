# git push -u origin main
# git pull origin main
import discord
from flask import Flask, request, jsonify
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from discord.ui import View
from pymongo import MongoClient
from discord.utils import get
from verification import get_user_discord, get_uuid, get_uuid_with_discord, get_discord_with_uuid
from hypixel_api import check_reqs_slayer, check_reqs_dungeon, get_skyblock_level, get_guild_members, get_level
from scammer import check_scammer_id
from keys import MONGO_URI, BOT_TOKEN

import asyncio
import subprocess
import sys
import os

# Constants 

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['Delerious']
users_collection = db['users']


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix='!!!!!jfadspoifj!', intents=intents)

# Views 

class ReviewView(View):
    def __init__(self, embed_user:discord.user, floor:int):
        super().__init__(timeout=None)
        self.embed_user = embed_user
        self.floor=floor

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="acceptBtn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.green() 

        role = get(self.embed_user.guild.roles, name=f"F{self.floor} Carrier")
        user = self.embed_user
        user_roles = [role.name for role in user.roles]

        if not any(role=="Carry Team" for role in user_roles):
            carry_team = get(interaction.guild.roles, name=f"Carry Team")
            await user.add_roles(carry_team) 
        try: 
            dm_embed = discord.Embed(title=f"Your dungeon floor {self.floor} application has been accepted", description="Thank you for joining our carrier program. You will be pinged when a carry service that you provide is requested!")
            dm_embed.add_field(name="Rules", value="<#990437238926110730>")
            dm_embed.add_field(name="Accepted By", value=f"{interaction.user.mention}", inline=False)

            dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            dm_embed.timestamp = interaction.created_at
            dm_embed.color=discord.Color.green() 
            await user.send(embed=dm_embed)
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
        except Exception:
            carrier_chat=interaction.guild.get_channel(990438688561463297) 
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
            await carrier_chat.send(embed=dm_embed)

            pass


    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, custom_id="rejectBtn")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        user = self.embed_user
        try:
            await user.send(f"Your dungeon floor {self.floor} application has been declined. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected by {interaction.user.mention}", ephemeral=False)
    @discord.ui.button(label="Blacklist", style=discord.ButtonStyle.gray, custom_id="blacklistBtn")
    async def blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        embed.title = f"Rejected and blacklisted {self.embed_user.display_name}"
        user = self.embed_user
        role = get(self.embed_user.guild.roles, name="Application Blacklisted")
        user = self.embed_user
        try:
            await user.send(f"Your dungeon floor {self.floor} application has been rejected and you're now application blacklisted. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await self.embed_user.add_roles(role) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected and blacklisted by {interaction.user.mention}", ephemeral=False)

class ReviewView_M(View):
    def __init__(self, embed_user:discord.user, floor:int):
        super().__init__(timeout=None)
        self.embed_user = embed_user
        self.floor=floor

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="acceptBtn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.green() 

        role = get(self.embed_user.guild.roles, name=f"M{self.floor} Carrier")
        user = self.embed_user
        user_roles = [role.name for role in user.roles]

        if not any(role=="Carry Team" for role in user_roles):
            carry_team = get(interaction.guild.roles, name=f"Carry Team")
            await user.add_roles(carry_team) 
        try: 
            dm_embed = discord.Embed(title=f"Your Mastermode floor {self.floor} application has been accepted", description="Thank you for joining our carrier program. You will be pinged when a carry service that you provide is requested!")
            dm_embed.add_field(name="Rules", value="<#990437238926110730>")
            dm_embed.add_field(name="Accepted By", value=f"{interaction.user.mention}", inline=False)

            dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            dm_embed.timestamp = interaction.created_at
            dm_embed.color=discord.Color.green() 
            await user.send(embed=dm_embed)
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
        except Exception:
            carrier_chat=interaction.guild.get_channel(990438688561463297) 
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
            await carrier_chat.send(embed=dm_embed)

            pass


    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, custom_id="rejectBtn")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        user = self.embed_user
        try:
            await user.send(f"Your Mastermode floor {self.floor} application has been declined. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected by {interaction.user.mention}", ephemeral=False)
    @discord.ui.button(label="Blacklist", style=discord.ButtonStyle.gray, custom_id="blacklistBtn")
    async def blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        embed.title = f"Rejected and blacklisted {self.embed_user.display_name}"
        user = self.embed_user
        role = get(self.embed_user.guild.roles, name="Application Blacklisted")
        user = self.embed_user
        try:
            await user.send(f"Your Mastermode floor {self.floor} application has been rejected and you're now application blacklisted. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await self.embed_user.add_roles(role) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected and blacklisted by {interaction.user.mention}", ephemeral=False)

class ReviewView_S(View):
    def __init__(self, embed_user:discord.user, slayer:str):
        super().__init__(timeout=None)
        self.embed_user = embed_user
        self.slayer=slayer

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="acceptBtn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.green() 

        role = get(self.embed_user.guild.roles, name=f"{self.slayer} Carrier")
        user = self.embed_user
        user_roles = [role.name for role in user.roles]

        if not any(role=="Carry Team" for role in user_roles):
            carry_team = get(interaction.guild.roles, name=f"Carry Team")
            await user.add_roles(carry_team) 
        try: 
            dm_embed = discord.Embed(title=f"Your {self.slayer} slayer carrier application has been accepted", description="Thank you for joining our carrier program. You will be pinged when a carry service that you provide is requested!")
            dm_embed.add_field(name="Rules", value="<#990437238926110730>")
            dm_embed.add_field(name="Accepted By", value=f"{interaction.user.mention}", inline=False)

            dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            dm_embed.timestamp = interaction.created_at
            dm_embed.color=discord.Color.green() 
            await user.send(embed=dm_embed)
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
        except Exception:
            carrier_chat=interaction.guild.get_channel(990438688561463297) 
            await interaction.message.edit(embed=embed)
            await self.embed_user.add_roles(role) 
            await interaction.response.send_message(f"{self.embed_user.mention}'s application accepted by {interaction.user.mention}", ephemeral=False)
            await carrier_chat.send(embed=dm_embed)

            pass


    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, custom_id="rejectBtn")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        user = self.embed_user
        try:
            await user.send(f"Your {self.slayer} slayer carrier application has been declined. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected by {interaction.user.mention}", ephemeral=False)
    @discord.ui.button(label="Blacklist", style=discord.ButtonStyle.gray, custom_id="blacklistBtn")
    async def blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        embed.title = f"Rejected and blacklisted {self.embed_user.display_name}"
        user = self.embed_user
        role = get(self.embed_user.guild.roles, name="Application Blacklisted")
        user = self.embed_user
        try:
            await user.send(f"Your {self.slayer} slayer carrier application has been rejected and you're now application blacklisted. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await self.embed_user.add_roles(role) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected and blacklisted by {interaction.user.mention}", ephemeral=False)



class GuildView(View):
    def __init__(self, embed_user:discord.user, ign:str):
        super().__init__(timeout=None)
        self.embed_user = embed_user
        self.ign=ign

    @discord.ui.button(label="Invited", style=discord.ButtonStyle.success, custom_id="acceptBtn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.green() 

        user = self.embed_user

        try: 
            dm_embed = discord.Embed(title=f"A guild invite has been sent! Please accept as soon as you log on", description="Thank you for choosing a Delerious guild!")
            dm_embed.add_field(name="Guild Giveaways", value="<#979728051321577492>")
            dm_embed.add_field(name="Invitation sent by", value=f"{interaction.user.mention}", inline=False)

            dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            dm_embed.timestamp = interaction.created_at
            dm_embed.color=discord.Color.green() 
            await user.send(embed=dm_embed)
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(f"{self.embed_user.mention}'s invitation sent by {interaction.user.mention}", ephemeral=False)
        except Exception:
            bot_commands=interaction.guild.get_channel(855570105857867816) 
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(f"{self.embed_user.mention}'s invitation sent by {interaction.user.mention}", ephemeral=False)
            await bot_commands.send(embed=dm_embed)

            pass


    @discord.ui.button(label="Invite Failed", style=discord.ButtonStyle.danger, custom_id="rejectBtn")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        user = self.embed_user
        try:
            await user.send(f"We are currently unable to invite you to join our guilds, as you are **already in another guild** or you need to change your settings. Feel free to apply again once you've made these changes.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await interaction.response.send_message(f"{self.embed_user.mention} has been notified to leave their current guild or change their settings.", ephemeral=False)

    @discord.ui.button(label="Blacklist", style=discord.ButtonStyle.gray, custom_id="blacklistBtn")
    async def blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]  
        embed.color = discord.Color.red() 
        embed.title = f"Rejected and blacklisted {self.embed_user.display_name}"
        user = self.embed_user
        role = get(self.embed_user.guild.roles, name="Application Blacklisted")
        user = self.embed_user
        try:
            await user.send(f"Your guild application has been rejected and you're now application blacklisted. If you have any questions regarding this decision, feel free to make a support ticket.")
        except Exception as e:
            pass
        await interaction.message.edit(embed=embed) 
        await self.embed_user.add_roles(role) 
        await interaction.response.send_message(f"{self.embed_user.mention}'s application rejected and blacklisted by {interaction.user.mention}", ephemeral=False)





class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  

    @discord.ui.button(label="F1", style=discord.ButtonStyle.primary, custom_id="f1")
    async def f1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await apply_dungeon(interaction, 1)
    @discord.ui.button(label="F2", style=discord.ButtonStyle.primary, custom_id="f2")
    async def f2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await apply_dungeon(interaction, 2)
    @discord.ui.button(label="F3", style=discord.ButtonStyle.primary, custom_id="f3")
    async def f3_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await apply_dungeon(interaction, 3)
    # @discord.ui.button(label="F4", style=discord.ButtonStyle.primary, custom_id="f4")
    # async def f4_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await apply_dungeon(interaction, 4)
    # @discord.ui.button(label="F5", style=discord.ButtonStyle.primary, custom_id="f5")
    # async def f5_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await apply_dungeon(interaction, 5)
    # @discord.ui.button(label="F6", style=discord.ButtonStyle.primary, custom_id="f6")
    # async def f6_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await apply_dungeon(interaction, 6)

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  

    @discord.ui.button(label="Spruce Guild", style=discord.ButtonStyle.primary, custom_id="spruce")
    async def spruce_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await apply_guild(interaction, "spruce")
    # @discord.ui.button(label="Legend Guild", style=discord.ButtonStyle.primary, custom_id="legend")
    # async def legend_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await apply_dungeon(interaction, 2)


# Bot

@client.event
async def on_ready():
    await client.tree.sync(guild=discord.Object(id=732620946300600331))
    print(f'Logged in as {client.user}')
    print("Wait a moment, syncing guilds...")
    view = MyView()
    client.add_view(view)
    client.loop.create_task(sync_guilds())




def start_bot():
    client.run(BOT_TOKEN)

@client.tree.command(
    name="sync",
    description="Sync bot to latest branch",
    guild=discord.Object(id=732620946300600331)
)
async def sync(interaction: discord.Interaction):
    user_roles = [role.name for role in interaction.user.roles] if isinstance(interaction.user, discord.Member) else []
    
    if any(role == "Owner" for role in user_roles):
        try:
            await interaction.response.defer(ephemeral=True)  
            
            result = subprocess.run(
                ['git', '-C', '/home/skylier/Documents/bot', 'pull', 'origin', 'main'],
                capture_output=True,
                text=True
            )
            output = result.stdout or result.stderr or "No output"
            await interaction.followup.send(f'```\n{output}\n```', ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(f'Error: {e}', ephemeral=True)

    else:
        await interaction.response.send_message(".-. Go away please", ephemeral=True)

@client.tree.command(
    name="restart",
    description="Restart the bot",
    guild=discord.Object(id=732620946300600331)
)
async def sync(interaction: discord.Interaction):
    user_roles = [role.name for role in interaction.user.roles] if isinstance(interaction.user, discord.Member) else []
    
    if any(role == "Owner" for role in user_roles):
        try:
            await interaction.response.send_message("Restarting...", ephemeral=True)
            python = sys.executable
            os.execv(python, [python] + sys.argv)

        
        except Exception as e:
            await interaction.followup.send(f'Error: {e}', ephemeral=True)

    else:
        await interaction.response.send_message(".-. Go away please", ephemeral=True)


async def sync_guilds():
    await client.wait_until_ready()
    guild_channel = client.get_channel(1374415191378235606)
    loop = asyncio.get_running_loop()
    while not client.is_closed():
        guild = client.get_guild(732620946300600331) 
        role = discord.utils.get(guild.roles, name="Spruce Guild")

        if role is None:
            await guild_channel.send("Role 'Spruce Guild' not found.")
            return
        
        members = role.members

        guild_members = await loop.run_in_executor(None, get_guild_members, "Spruce")
        guild_embed = discord.Embed(title=f"Daily guild stats refreshed", description=f"Total members: {len(guild_members)}")
        guild_embed.color=discord.Color.green()

        left = await refresh_guild_roles(members, guild_members)
        while left == False:
            left = await refresh_guild_roles(members, guild_members)

        guild_embed.add_field(name="Removed members: ", value=left)

        await guild_channel.send(embed=guild_embed)
        print("Guilds synced")
        print("Bot is ready.")

        await asyncio.sleep(43200)
        

async def refresh_guild_roles(members, guild_members):
    guild = client.get_guild(732620946300600331) 
    role = discord.utils.get(guild.roles, name="Spruce Guild")
    member_role = discord.utils.get(guild.roles, name="Guild Member")


    i = 0 
    for member in members:
        uuid = get_uuid_with_discord(member.id)
        if uuid not in guild_members:

            i = i+1
            await member.remove_roles(role)
            await member.remove_roles(member_role)
        else:
            guild_members.remove(uuid)

    for uuid in guild_members:
        try:
            discord_id=get_discord_with_uuid(uuid)
            user = client.get_user(discord_id)
            user.add_roles(role)
            user.add_roles(member_role)
        except AttributeError:
            pass
    if i==0:
        return "N/A"
    else:
        return str(i) + " members removed"

    
@client.tree.command(
    name="guild_embed",
    description="Test",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe()
async def carrier_embed(interaction):
    app_embed = discord.Embed(title=f"Guild Applications", description="""
Spruce Guild
Entry requirement: None

[ C ] Commander
➥ Level: 150
➥ Can stay in Spruce or move up to higher guilds

[ G ] General
➥ Level: 100

[ E ] Elite Member
➥ Level: 50

Inactivity Prune: 7 Days+ Offline

""")

    app_embed.timestamp = interaction.created_at
    app_embed.color=discord.Color.green() 

    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Owner" for role in user_roles):
        channel = interaction.guild.get_channel(990437238926110730)  
        await channel.send(embed=app_embed, view=MyView())
        await interaction.response.send_message("Success!", ephemeral=True)
    else:
        await interaction.response.send_message("You are not Sky lil bro")
    



@client.tree.command(
    name="carrier_embed",
    description="Test",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe()
async def carrier_embed(interaction):
    app_embed = discord.Embed(title=f"Carrier Applications", description="""
Here are the requirements to be a Delerious Carrier:

**Dungeon Carrier Bypass Requirements:**

Floor 3 Carrier --> Cata 24

Floor 2 Carrier --> Cata 21

Floor 1 Carrier --> Cata 19

""")
    app_embed.add_field(name="If you do not meet the bypass the requirements", value="Please follow the instructions in https://discord.com/channels/732620946300600331/1054358545728028782 to apply normally")
    app_embed.add_field(name="To remove your roles", value="Please open a support ticket in https://discord.com/channels/732620946300600331/833547393097400381")



    app_embed.timestamp = interaction.created_at
    app_embed.color=discord.Color.green() 

    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Owner" for role in user_roles):
        channel = interaction.guild.get_channel(990437238926110730)  
        await channel.send(embed=app_embed, view=MyView())
        await interaction.response.send_message("Success!", ephemeral=True)
    else:
        await interaction.response.send_message("You are not Sky lil bro")
    



@client.tree.command(
    name="verify",
    description="Link your Hypixel account!",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe(username="Your Minecraft in game name")
async def verify(interaction, username: str):
    discord_tag_given_old = f"{interaction.user.name}#{interaction.user.discriminator}"
    discord_tag_given_new = f"{interaction.user.name}"
    discord_tag_from_acc = get_user_discord(username)
    uuid=get_uuid(username)
    if not discord_tag_from_acc: 
        await interaction.response.send_message("You have not yet link this account on Hypixel, please follow the tutorial in <#1054358545728028782> to link your account!")
        return
    await interaction.response.defer(ephemeral=True)
    if discord_tag_from_acc.lower() == discord_tag_given_old.lower() or discord_tag_from_acc.lower() == discord_tag_given_new.lower():
        user_data = {
            'id': interaction.user.id,
            'discord_tag': discord_tag_from_acc,
            'username': username,
            'uuid': uuid
        }

        result = users_collection.update_one(
            {'id': interaction.user.id},  
            {'$set': user_data}, 
            upsert=True  
        )

        role = get(interaction.user.guild.roles, name="Verified")
        await interaction.user.add_roles(role) 
        await interaction.followup.send("You are now verified! You now have access to carrier applications!", ephemeral=True)
    else:
        await interaction.followup.send("Make sure that you have set the correct Discord handler on Hypixel! Because it doesn't match right now!", ephemeral=True)


async def apply_dungeon(interaction, floor: int, evidence: discord.Attachment=None):
    if floor <= 0 or floor>7:
        await interaction.response.send_message(f"Hey! Troll applications will result in an application blacklist if done repeatedly!", ephemeral=True)
        return
    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Application Blacklisted" for role in user_roles):
        await interaction.response.send_message("You're application blacklisted. If you'd wish to appeal open a support ticket.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)

    
    carrier_log=interaction.guild.get_channel(1298550693870829579) 

    if check_scammer_id(interaction.user.id):
        await interaction.followup.send("You're found in SBZ scammer database. If you'd wish to appeal please contact SBZ staff.", ephemeral=True)
        embed = discord.Embed(title=f"Auto Declined: {username}'s floor {floor} application ({interaction.user})")
        embed.add_field(name="Scammer identified", value="Using SBZ Scammer Database/discord.gg/sbz", inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at
        embed.color=discord.Color.red() 
        await carrier_log.send(embed=embed)
        return

    id = interaction.user.id
    verified_user = users_collection.find_one({'id':id})
    if not verified_user:
        await interaction.followup.send("It appears that you're not verified yet. Please verify using the `/verify` command before applying!", ephemeral=True)
        return
    username = verified_user['username']


    if any(role==f"F{floor} Carrier" for role in user_roles):
        await interaction.followup.send(f"You're already a floor {floor} carrier.", ephemeral=True)
        return

    bypass, level=check_reqs_dungeon(username, floor)

    if bypass:
        role = get(interaction.guild.roles, name=f"F{floor} Carrier")

        embed = discord.Embed(title=f"Auto Accepted: {username}'s floor {floor} application ({interaction.user})")
        embed.add_field(name="Cata Level", value=level, inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at
        embed.set_footer(text="Not scammer in SBZ database")
        embed.color=discord.Color.green() 
        
        if not any(role=="Carry Team" for role in user_roles):
            carry_team = get(interaction.guild.roles, name=f"Carry Team")
            await interaction.user.add_roles(carry_team)

        dm_embed = discord.Embed(title=f"Your dungeon floor {floor} application has been accepted", description="Thank you for joining our carrier program. You will be pinged when a carry service that you provide is requested!")
        dm_embed.add_field(name="Rules", value="<#990437238926110730>")
        dm_embed.add_field(name="Accepted By", value=f"Automatic", inline=False)

        dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        dm_embed.timestamp = interaction.created_at
        dm_embed.color=discord.Color.green() 
        try:
            await interaction.user.send(embed=dm_embed) 
        except: 
            pass
        await interaction.user.add_roles(role) 
        await interaction.followup.send(f"You meet the evidence bypass requirement, and your application is automatically accepted!", ephemeral=True)
        await carrier_log.send(embed=embed)
    elif evidence != None:


        embed = discord.Embed(title=f"{username}'s floor {floor} application", description=f"Cata Level: {level}")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at

        # embed.add_field(name="Status", value="Pending", inline=False)
        evidence_url = evidence.url

        embed.set_footer(text="Not scammer in SBZ database")

        embed.set_image(url=evidence_url)

        view = ReviewView(embed_user=interaction.user, floor=floor)
        await carrier_log.send(embed=embed, view=view)
        await carrier_log.send("<@&732620946350800896> please review this application")

        await interaction.followup.send(f"Your application for floor {floor} carrier has been sent to our moderation team. It will be reviewed within 24 hours!", ephemeral=True)
    else: 
        await interaction.followup.send(f"You do not meet the bypass requirements for this dungeon slayer. Please submit a screenshot of a completion run as evidence.", ephemeral=True)
    

async def apply_master(interaction, floor: int, evidence: discord.Attachment=None):
    if floor <= 0 or floor>3:
        await interaction.response.send_message(f"We only accept mastermode floor 1-3 applications right now!", ephemeral=True)
        return
    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Application Blacklisted" for role in user_roles):
        await interaction.response.send_message("You're application blacklisted. If you'd wish to appeal open a support ticket.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)

    
    carrier_log=interaction.guild.get_channel(1298550693870829579) 

    if check_scammer_id(interaction.user.id):
        await interaction.followup.send("You're found in SBZ scammer database. If you'd wish to appeal please contact SBZ staff.", ephemeral=True)
        embed = discord.Embed(title=f"Auto Declined: {username}'s floor {floor} application ({interaction.user})")
        embed.add_field(name="Scammer identified", value="Using SBZ Scammer Database/discord.gg/sbz", inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at
        embed.color=discord.Color.red() 
        await carrier_log.send(embed=embed)
        return

    id = interaction.user.id
    verified_user = users_collection.find_one({'id':id})
    if not verified_user:
        await interaction.followup.send("It appears that you're not verified yet. Please verify using the `/verify` command before applying!", ephemeral=True)
        return
    username = verified_user['username']
    level = get_level(username)


    if any(role==f"M{floor} Carrier" for role in user_roles):
        await interaction.followup.send(f"You're already a M{floor} carrier.", ephemeral=True)
        return

    embed = discord.Embed(title=f"{username}'s **MASTERMODE** floor {floor} application", description=f"Cata Level: {level}")
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.timestamp = interaction.created_at

    # embed.add_field(name="Status", value="Pending", inline=False)
    evidence_url = evidence.url

    embed.set_footer(text="Not scammer in SBZ database")

    embed.set_image(url=evidence_url)

    view = ReviewView_M(embed_user=interaction.user, floor=floor)
    await carrier_log.send(embed=embed, view=view)
    await carrier_log.send("<@&732620946350800896> please review this application")

    await interaction.followup.send(f"Your application for Mastermode floor {floor} carrier has been sent to our moderation team. It will be reviewed within 24 hours!", ephemeral=True)


@client.tree.command(
    name="apply_dungeon_carrier",
    description="Apply to be a Delerious dungeon carrier",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe(floor="Integer; e.g. 5", evidence="The screenshot of completion of the floor you are applying to")
async def apply_dungeon_carrier(interaction, floor: int, evidence: discord.Attachment=None):
    await apply_dungeon(interaction, floor, evidence)

@client.tree.command(
    name="apply_mastermode_carrier",
    description="Apply to be a Delerious mastermode dungeon carrier",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe(floor="Integer; e.g. 5", evidence="The screenshot of completion of the floor you are applying to")
async def apply_mastermode_carrier(interaction, floor: int, evidence: discord.Attachment):
    await apply_master(interaction, floor, evidence)


@client.tree.command(
    name="apply_slayer_carrier",
    description="Apply to be a Delerious slayer carrier",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe(slayer="The slayer you're applying for", evidence="The screenshot of completion of the slayer you are applying to")
@app_commands.choices(
    slayer = [
        Choice(name = "Revenant Horror", value = "Revenant"),
        Choice(name = "Tarantula Broodfather", value = "Tarantula"),
        Choice(name = "Sven Packmaster", value = "Sven"),
        Choice(name = "Voidgloom Seraph", value = "Voidgloom"),
    ]
)
async def apply_slayer_carrier(interaction, slayer: Choice[str], evidence: discord.Attachment=None):
    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Application Blacklisted" for role in user_roles):
        await interaction.response.send_message("You're application blacklisted. If you'd wish to appeal open a support ticket.")
        return
    slayer_choice=slayer.value
    id = interaction.user.id
    verified_user = users_collection.find_one({'id':id})
    if not verified_user:
        await interaction.response.send_message("It appears that you're not verified yet. Please verify using the `/verify` command before applying!", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    
    if check_scammer_id(interaction.user.id):
        await interaction.followup.send("You are found as a scammer in the SkyBlockZ database, this check was provided by discord.gg/skyblock", ephemeral=True)
        embed = discord.Embed(title=f"Auto Declined: {username}'s {slayer_choice} carrier application ({interaction.user})")
        embed.add_field(name="Scammer identified", value="Using SBZ Scammer Database", inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at
        embed.color=discord.Color.red() 
        await carrier_log.send(embed=embed)
        return

    carrier_log=interaction.guild.get_channel(1298550693870829579) 
    username = verified_user['username']
    role_name = ""

    can_bypass = False
    if slayer_choice=="Revenant":
        role_name = "Revenant Carrier"
    elif slayer_choice=="Tarantula":
        role_name= "Tarantula Carrier"
    elif slayer_choice=="Sven":
        role_name="Sven Carrier"
        can_bypass = True
    elif slayer_choice=="Voidgloom":
        role_name="Voidgloom Carrier"
    if any(role==role_name for role in user_roles):
        await interaction.followup.send(f"You're already a {slayer_choice} carrier.")
        return


    meet_req, xp=check_reqs_slayer(username, slayer_choice)
    if meet_req:
        if can_bypass:
            role = get(interaction.guild.roles, name=role_name)
            
            embed = discord.Embed(title=f"Auto Accepted: {username}'s {role_name} application ({interaction.user})")
            embed.add_field(name="Slayer XP", value=xp, inline=False)
            embed.set_footer(text="Not scammer in SBZ database")

            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.timestamp = interaction.created_at
            embed.color=discord.Color.green() 
            if not any(role=="Carry Team" for role in user_roles):
                carry_team = get(interaction.guild.roles, name=f"Carry Team")
                await interaction.user.add_roles(carry_team) 
            await interaction.user.add_roles(role) 
            dm_embed = discord.Embed(title=f"Your slayer carrier application has been accepted", description="Thank you for joining our carrier program. You will be pinged when a carry service that you provide is requested!")
            dm_embed.add_field(name="Rules", value="<#990437238926110730>")
            dm_embed.add_field(name="Accepted By", value=f"Automatic", inline=False)

            dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            dm_embed.timestamp = interaction.created_at
            dm_embed.color=discord.Color.green() 
            try: 
                await interaction.user.send(embed=dm_embed) 
            except Exception:
                pass
            await interaction.followup.send(f"Your application is automatically accepted!", ephemeral=True)
            await carrier_log.send(embed=embed)
        else:
            if evidence == None:
                await interaction.followup.send(f"You meet the requirements for {slayer_choice} slayer carrier, but since this slayer doesn't have a bypass, please submit a screenshot of a slayer completion run as evidence.", ephemeral=True)
                return
            else:
                embed = discord.Embed(title=f"{username}'s {slayer_choice} carrier application", description=f"Slayer XP: {xp}")
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.timestamp = interaction.created_at

                # embed.add_field(name="Status", value="Pending", inline=False)
                evidence_url = evidence.url

                embed.set_footer(text="Not scammer in SBZ database")

                embed.set_image(url=evidence_url)

                view = ReviewView_S(embed_user=interaction.user, slayer=slayer_choice)
                await carrier_log.send(embed=embed, view=view)
                await carrier_log.send("<@&732620946350800896> please review this application")

                await interaction.followup.send(f"Your application for {slayer_choice} slayer carrier has been sent to our moderation team. It will be reviewed within 24 hours!", ephemeral=True)


    else:
        await interaction.followup.send(f"Your slayer carrier application has been declined as you don't meet the requirements!")




@client.tree.command(
    name="apply_guild",
    description="Apply for a Delerious guild",
    guild=discord.Object(id=732620946300600331)
)
@app_commands.describe(guild="The guild you're applying for")
@app_commands.choices(
    guild = [
        Choice(name = "Skys Guild", value = "sky"),
        Choice(name = "Spruce", value = "spruce"),

    ]
)
async def apply_guild(interaction, guild: Choice[str]):
    user_roles = [role.name for role in interaction.user.roles]
    if any(role=="Application Blacklisted" for role in user_roles):
        await interaction.response.send_message("You're application blacklisted. If you'd wish to appeal open a support ticket.")
        return
    guild_choice=guild.value 
    id = interaction.user.id
    verified_user = users_collection.find_one({'id':id})
    if not verified_user:
        await interaction.response.send_message("It appears that you're not verified yet. Please verify using the `/verify` command before applying!", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    guild_log=interaction.guild.get_channel(1376121292108861450) 
    
    if check_scammer_id(interaction.user.id):
        await interaction.followup.send("You are found as a scammer in the SkyBlockZ database, this check was provided by discord.gg/skyblock", ephemeral=True)
        embed = discord.Embed(title=f"Auto Declined: {username}'s {guild_choice} guild application ({interaction.user})")
        embed.add_field(name="Scammer identified", value="Using SBZ Scammer Database", inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at
        embed.color=discord.Color.red() 

        await guild_log.send(embed=embed)
        return

    username = verified_user['username']
    role_name = ""
    member_role = get(interaction.guild.roles, name="Guild Member")

    level = get_skyblock_level(username)
    if guild_choice == "spruce":
        role_name = "Spruce Guild"
        role = get(interaction.guild.roles, name=role_name)
        
        embed = discord.Embed(title=f"New Applicant {username}'s {role_name} application ({interaction.user})")
        embed.add_field(name="Skyblock Level", value=level, inline=False)
        embed.set_footer(text="Not scammer in SBZ database")

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at

        await interaction.user.add_roles(member_role) 
        await interaction.user.add_roles(role) 

        dm_embed = discord.Embed(title=f"Your guild application has been accepted", description="Thank you for joining a Delerious guild! Welcome to the family! \n An invitation will be send by one of our staff within the next 24 hours!")
        dm_embed.add_field(name="Guild Announcements", value="<#979237342541934652>")
        dm_embed.add_field(name="Guild Giveaways", value="<#979728051321577492>", inline=False)

        dm_embed.add_field(name="Approved By", value=f"Automatic", inline=False)

        dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        dm_embed.timestamp = interaction.created_at
        dm_embed.color=discord.Color.green() 
        try: 
            await interaction.user.send(embed=dm_embed) 
        except Exception:
            pass
        await interaction.followup.send(f"Your application is automatically accepted!", ephemeral=True)
        view = GuildView(embed_user=interaction.user, ign="")

        await guild_log.send(f"<@&1376123270583160913> Please invite new member ASAP! ```/g invite {username}```",embed=embed, view=view)
    elif guild_choice == "sky" and level >=200 and False:  # Future update
        role_name = "Sky Guild" # NEED TO BE CHANGED
        role = get(interaction.guild.roles, name=role_name)
        
        embed = discord.Embed(title=f"New Applicant {username}'s {role_name} application ({interaction.user})")
        embed.add_field(name="Skyblock Level", value=level, inline=False)
        embed.set_footer(text="Not scammer in SBZ database")

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.timestamp = interaction.created_at

        await interaction.user.add_roles(member_role) 
        await interaction.user.add_roles(role) 

        dm_embed = discord.Embed(title=f"Your guild application has been accepted", description="Thank you for joining a Delerious guild! Welcome to the family! \n An invitation will be send by one of our staff within the next 24 hours!")
        dm_embed.add_field(name="Guild Announcements", value="<#979237342541934652>")
        dm_embed.add_field(name="Guild Giveaways", value="<#979728051321577492>", inline=False)

        dm_embed.add_field(name="Approved By", value=f"Automatic", inline=False)

        dm_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        dm_embed.timestamp = interaction.created_at
        dm_embed.color=discord.Color.green() 
        try: 
            await interaction.user.send(embed=dm_embed) 
        except Exception:
            pass
        await interaction.followup.send(f"Your application is automatically accepted!", ephemeral=True)
        view = GuildView(embed_user=interaction.user, ign="")

        await guild_log.send(f"<@&1376123270583160913> Please invite new member ASAP! ```/g invite {username}```",embed=embed, view=view)
    else:
        await interaction.followup.send(f"Your guild application has been declined as you don't meet the requirements!")



    

if __name__ == "__main__":
    start_bot()