import discord
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

class levelling(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def rankgen(self,message):
        # print(6)
        f = open(f"levels/{message.guild.id}.json","r")
        j = json.load(f)
        f.close()
        # print(7)
        d={}
        for i in range(len(j[str(message.guild.id)])):
            # print("o")
            d[j[str(message.guild.id)][i]['id']]=j[str(message.guild.id)][i]['xp']
            # print("p")
        # print(8)
        d = {k: v for k, v in sorted(
        d.items(), key=lambda item: item[1], reverse=True)}    
        lis = []
        # print(9)
        for p in d.keys():
            lis.append(p)
        dic = {
            str(message.guild.id):lis
        }    
        # print(10)
        f = open(f"levels/ranking/{message.guild.id}.json","w")
        json.dump(dic,f)
        # print(11)
        f.close()



    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        try:
            
            f = open(f"Moderation/{message.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            # print(1)
            c = self.bot.get_channel(json_object['levelup_channel'])
            f = open(f"levels/{message.guild.id}.json","r")
            j = json.load(f)
            # print(2)
            t=0
            for i in range(len(j[str(message.guild.id)])):
                if j[str(message.guild.id)][i]['id']==message.author.id:
                    t=i
            f.close()
            # print(3)
            d = len(message.content)
            if d>10:
                d=10
            j[str(message.guild.id)][t]["xp"]+=d
            xp = j[str(message.guild.id)][t]["xp"]
            level  = j[str(message.guild.id)][t]['level']
            
            # print(4)
            if xp>=15*level*level+15:
                j[str(message.guild.id)][t]['level']+=1
                print("level up recorded")
                level = j[str(message.guild.id)][t]['level']
                print("levels")
                # print(5)    
                print(c.id)
                # await c.send(content="1")
                # print(message.author)

                await c.send(content=f"Congratulations {message.author}!! On the lvl up !! You have advanced to {level+1} level")
                print(5)
            # print(5)
            f = open(f"levels/{message.guild.id}.json","w")
            json.dump(j,f)
            f.close()
            self.rankgen(message)
            f = open(f"levels/leveluproles/{message.guild.id}.json","r")
            data = json.load(f)
            f.close()
            m = data['count']
            index = 0
            if level % m ==0:
                index = m//10
            if(index>len(data['roles'])):
                index = len(data['roles'])
            print("p")
            print(index)
            for i in range(index):
                print("o")
                await message.author.add_roles(self.bot.get_role(data['roles'][i]))
            print("perks given")
        except:
            print("leveler not set")
    @commands.command()
    async def levels(self,ctx,userName:discord.Member=None):
        
            if userName==None:
                userName=ctx.author
            # print(1)
            f = open(f"levels/{ctx.guild.id}.json","r")
            j = json.load(f)
            f.close()
            # print(2)
            t=0
            for i in range(len(j[str(ctx.guild.id)])):
                if j[str(ctx.guild.id)][i]['id']==userName.id:
                    t=i
            # print(3)        
            xp= j[str(ctx.guild.id)][t]['xp']   
            level= j[str(ctx.guild.id)][t]['level']
            # print(4)
            embed = discord.Embed()
            embed.title=f"{userName} is on lvl {level}"
            embed.description=f"Keep grinding"
            await ctx.send(content=ctx.author.mention, embed=embed)
            # print(5)


    @commands.command()
    async def rank(self,ctx,userName:discord.Member=None):
        try:    
            # print(0)
            if userName==None:
                userName=ctx.author
            # print(1)    
            f = open(f"levels/ranking/{ctx.guild.id}.json","r")
            # print(2)
            d = json.load(f)
            # print(5)
            f.close()
            lis = d[str(ctx.guild.id)]
            
            # print(2)
            rank =1
            for i in lis:
                if (i == userName.id):
                    break
                rank+=1
            # print(3)    
            embed = discord.Embed()
            embed.title=f"{userName} is on rank {rank}"
            embed.description=f"Keep grinding"
            await ctx.send(content=ctx.author.mention, embed=embed)
        except:
            print("leveler not set")


    @commands.command()
    @has_permissions(administrator=True)
    async def setlevel(self,ctx,userName:discord.Member,count:int):
        # try:
            f = open(f"levels/{ctx.guild.id}.json","r")
            j = json.load(f)
            print(1)
            t=0
            for i in range(len(j[str(ctx.guild.id)])):
                if j[str(ctx.guild.id)][i]['id']==userName.id:
                    t=i
            
            xp= j[str(ctx.guild.id)][t]['xp']
            
            f.close()
            level= j[str(ctx.guild.id)][t]['level']
            
            j[str(ctx.guild.id)][t]['level'] = count
            level = count
            if count==0:
                j[str(ctx.guild.id)][t]['xp'] = 0
            else:        
                j[str(ctx.guild.id)][t]['xp'] = 15*level*level+15
            f = open(f"levels/{ctx.guild.id}.json","w")
            json.dump(j,f)
            f.close()
            self.rankgen(ctx)
            embed = discord.Embed()
            embed.title=f"{userName}'s level has been set to lvl {level}"
            await ctx.send(content=ctx.author.mention, embed=embed)
        
            f = open(f"levels/leveluproles/{ctx.guild.id}.json","r")
            data = json.load(f)
            f.close()
            m = data['count']
            print(m,count)
            index = count//m
            print(1)
            print(index)
            print(data['roles'])
            if(index>len(data['roles'])):
                index = len(data['roles'])
            for i in range(index):
                # print("OOO")
                role = ctx.guild.get_role(data['roles'][i])
                # print("III")
                await userName.add_roles(role)
            print(2)
            print("perks given")
        # except:
        #     print("leveler not set")

    @commands.command()
    async def leaderboard(self,ctx):
        try:
            a_file=open(f"levels/ranking/{ctx.guild.id}.json","r")
            json_object = json.load(a_file)
            a_file.close()
            t = []
            i=1
            for tl in json_object[str(ctx.guild.id)]:
                if i==6:
                    break
                t.append(int(tl))
                i+=1
            backg = Image.open("levels/ranking/caca40ca-501c-49d4-8984-338bb11ee46b.jpg")

            mid = self.bot.get_user(t[0])
            pfp = Image.open(requests.get(mid.avatar_url, stream=True).raw)
            draw = ImageDraw.Draw(backg)
            font = ImageFont.truetype("resources/KoyaSans-BoldItalic.ttf", size=36)
            pfp = pfp.resize((80, 80))
            message = str(mid)
            draw.text((290, 240), message, fill='white', font=font)
            backg.paste(pfp, (200, 220))
            # backg.show()
            # print(t)
            i = -1
            for id in t:
                i += 1
                if i == 0:
                    continue
                if i == 5:
                    break
                m = self.bot.get_user(id)
                pfp = Image.open(requests.get(m.avatar_url, stream=True).raw)
                pfp = pfp.resize((55, 55))
                message = str(m)
                font = ImageFont.truetype('resources/KoyaSans-BoldItalic.ttf', size=20)
                draw.text((280, 340+67*(i-1)), message, fill='white', font=font)
                backg.paste(pfp, (215, 320+67*(i-1)))
                # backg.show()
            backg.save("leaderboard.png")
            # backg.show()
            embed1 = discord.Embed(title="**LeaderBoard**", color=0xFF5733)
            embed1.description = "The leaderboard is as follows:-"

            await ctx.send(content=ctx.author.mention, embed=embed1, file=discord.File("leaderboard.png"))
            os.remove("leaderboard.png")    
        except:
            print("leveler not set")    

def setup(bot):
    bot.add_cog(levelling(bot))