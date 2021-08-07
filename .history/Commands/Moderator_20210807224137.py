import discord
import datetime
from discord.ext import commands
import json
import asyncio
from PIL import ImageSequence, Image, ImageChops
# from PIL import gifmaker
# from tkinter import *
# from PIL import ImageTk,Image
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np
import os
from discord.ext.commands import has_permissions, CheckFailure

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @has_permissions(administrator=True)
    async def set_moderation(self,ctx):
        embed = discord.Embed()
        embed.color=0xFF5733
        embed.title = f"Setup Moderation for {ctx.guild.name}"
        embed.description="_react to the lower message accordingly to what u need enabled in your server_"
        await ctx.send(embed=embed,content=ctx.author.mention)
        embed = discord.Embed()
        embed.title = "Moderation Options"
        embed.add_field(name="Kick 👢",value="_react to the 👢_\nThis will enable the kick command in your server")
        mod = {}
        m = await ctx.send(embed=embed)
        await m.add_reaction('👢')
        await m.add_reaction('❎')
        valid_reactions = ['👢','❎']
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction.emoji)=='👢':
            mod['kick'] = True
        else:
            mod['kick'] = False
        embed = discord.Embed()
        embed.title = "Moderation Options"        
        embed.add_field(name="Ban ❌", value="_react to the ❌_\nThis will enable the ban command in your server")
        m = await ctx.send(embed=embed)
        await m.add_reaction('❌')
        await m.add_reaction('❎')
        valid_reactions = ['❌','❎']
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction.emoji)=='❌':
            mod['ban'] = True
        else:
            mod['ban'] = False
        embed = discord.Embed()
        embed.title = "Moderation Options"        
        
        embed.add_field(name="mute 🔇", value="_react to the 🔇_\nThis will enable the mute command in your server")
        m = await ctx.send(embed=embed)
        await m.add_reaction('🔇')
        await m.add_reaction('❎')
        valid_reactions = ['🔇','❎']
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction.emoji)=='🔇':
            mod['mute'] = True
            await ctx.send("To mute to work properly, There must be a mute role\nReply with a role u want to set as the mute role")
            def check2(m):
                return str(m.content).startswith("<@") and str(m.content).endswith(">") and m.author ==ctx.author
            msg = await self.bot.wait_for('message', check=check2)
            print(1)
            print(str(msg.content)[3:-1])
            mod['muterole_id']=int(str(msg.content)[3:-1])
            print(1)
            permissions = discord.Permissions()
            permissions.none()
            print(1)
            role = ctx.guild.get_role(mod['muterole_id'])
            print(1)
            await role.edit(permissions=permissions)

        else:
            mod['mute']=False

        
        embed = discord.Embed()
        embed.title = "Moderation Options"        
        embed.add_field(name="strikes ➖",value = "_react to the ➖_\nThis will enable the strike functionality in your server")
        m = await ctx.send(embed=embed)
        await m.add_reaction('➖')
        await m.add_reaction('❎')
        valid_reactions = ['➖','❎']
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        
        if str(reaction.emoji) == '➖':
            mod['strike'] = True
            f = open(f"strikes/{ctx.guild.id}.json","w")
            f.close()
            f = open(f"strikes/{ctx.guild.id}.json","r+")
            m=[]
            for member in ctx.guild.members:
                try:
                    m = json.load(f)
                except:
                    pass
                d = {
                    "id":member.id,
                    "strike" : 0
                }
                m.append(d)
            d = {
                str(ctx.guild.id):m
            }    
            json.dump(d,f)
            f.close()
        else:
            mod['strike'] = False        

        embed = discord.Embed()
        embed.title = "Moderation Options" 
        embed.add_field(name="levelling ✨",value ="_react to the ✨_\nThis will enable levelling of members of your server")
        m = await ctx.send(embed=embed)
        await m.add_reaction('✨')
        await m.add_reaction('❎')
        valid_reactions = ['✨','❎']
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) == '✨':
            mod['levelling'] = True
            f = open(f"levels/{ctx.guild.id}.json","w")
            f.close()
            f = open(f"levels/{ctx.guild.id}.json","r+")
            m=[]
            for member in ctx.guild.members:
                try:
                    m = json.load(f)
                except:
                    pass
                d = {
                    "id":member.id,
                    "level" : 0,
                    "xp": 0
                }
                m.append(d)
            d = {
                str(ctx.guild.id):m
            }    
            json.dump(d,f)
            f.close()
            await ctx.send("Reply with the channel you want to set for the levelling up notifications.")
            def check(m):
                return str(m.content).startswith("<#") and str(m.content).endswith('>') and m.author == ctx.author
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            print("aaaa")
            print(msg)
            msg = str(msg.content)[2:-1]
            print("2222")
            mod['levelup_channel'] = int(msg)
            print("aaaaa")
        else:
            mod['levelling'] = False

        a = open(f"Moderation/{ctx.guild.id}.json","w+")
        json.dump(mod,a)
        a.close()

        await ctx.send("Done setting up your server's Moderation :)")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            f = open(f"Moderation/{member.guild.id}.json","r")
            data = json.load(f)
            f.close()
            if(data['levelling'] == True):
                f = open(f"levels/{member.guild.id}.json","r")
                d = json.load(f)
                f.close()
                d[str(member.guild.id)].append({
                    "id":member.id,
                    "level":0,
                    "xp":0
                })
                f = open(f"levels/{member.guild.id}.json","w")
                json.dump(d,f)
                f.close()
                
            if(data['strike'] == True):
                f = open(f"strikes/{member.guild.id}.json","r")
                d = json.load(f)
                f.close()
                d[str(member.guild.id)].append({"id":member.id,"strike":0})
                f = open(f"strikes/{member.guild.id}.json","w")
                json.dump(d,f)
                f.close()
        except:
            print("Moderation not set")
    @commands.command()
    @has_permissions(administrator=True)
    async def set_punishments(self,ctx):
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        print(1)
        data  = json.load(f)
        if(data['strike'] == False):
            await ctx.send("Strikes disabled in this server, to setup strikes call `set_moderation`")
            return
        f.close()
        print(2)
        embed=discord.Embed()
        embed.title = "Strikes Punishments Setup"
        embed.add_field(name="Message Format",value="send message in format `(<number of strikes>,<punishment>)`",inline=False)
        embed.add_field(name="How to set Punishments?",value="`(2,mute 5)` -> means 2 strikes will lead to a 5 minutes mute\n`(5,kick)` -> means 5 strikes will lead to kick \n`(10,ban)` -> means 10 strikes will lead to the ban of that member",inline=False)
        embed.add_field(name="Termination",value="send `$` when u are done with the setup")
        await ctx.send(embed=embed,content=ctx.author.mention)
        flag = True
        m = {}
        i=1
        f = open(f"strikes/punishments/{ctx.guild.id}.json","w")    
        while(flag):
            duration = -1
            def check(m):
                return m.author == ctx.author
            msg = await self.bot.wait_for('message',check=check)
            if(msg.content=="$"):
                break
            try:
                message = msg.content[1:-1]
                l = message.split(',')
            except:
                ctx.send("invalid input given retry the whole process")
                return
            print(4)    
            count = int(l[0])
            punish = l[1]
            try:
                if punish[-2] == " " or punish[-3]:
                    duration = int(punish.split(" ")[1])
                    punish = "mute"
            except:
                pass            
            m[f"p{i}"] = {
                "count": count,
                "punishment": punish,
            }    
            if(duration!=-1):
                # print(duration)
                m[f"p{i}"]["duration"] = duration
                await ctx.send(f"Set {count} strikes for {punish} of {duration} minutes duration punishment")
            else:
                await ctx.send(f"Set {count} strikes for {punish} punishment")
                pass    
            i+=1  
        json.dump(m,f)
        f.close()
        await ctx.send("done setting up :)")

    @commands.command()
    @has_permissions(administrator=True)
    async def set_level_roles(self,ctx,count,*,role_ids):
        print(1)
        count=int(count)
        f = open(f"Moderation/{ctx.guild.id}.json","r")
        print(1)
        data  = json.load(f)
        if(data['levelling'] == False):
            await ctx.send("Levelling disabled in this server, to setup levelling call `,set_moderation`")
            return
        f.close()
        print(2)
        f = open(f"levels/leveluproles/{ctx.guild.id}.json","w")
        lis = []
        role_ids = role_ids.split(" ")
        for role in role_ids:
            lis.append(int(role))
        d = {
            "roles":lis,
            "count":count
        }    
        print(5)
        json.dump(d,f)
        print(6)
        f.close()
        embed = discord.Embed()
        embed.title = "Levelup Roles"
        i=1
        for role in role_ids:
            role = int(role)
            embed.add_field(name = str(count*i),value=ctx.guild.get_role(role).mention)
            i+=1

        await ctx.send(content="done setting up :)",embed=embed)
        
    @commands.command()
    @has_permissions(administrator=True)
    async def set_noxp(self,ctx,roleid:int):
        f = open(f"levels/{ctx.guild.id}noxp.txt","w")
        f.write(str(roleid))
        f.close()
        role = ctx.guild.get_role(roleid)
        await ctx.send(embed=discord.Embed(description=role.mention),content="The no xp role has been set to this")
def setup(bot):
    bot.add_cog(Moderation(bot))
