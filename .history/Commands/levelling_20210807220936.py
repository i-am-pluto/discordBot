import matplotlib.pyplot as plt
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
        f = open(f"levels/{message.guild.id}.json","r")
        j = json.load(f)
        f.close()
        d={}
        for i in range(len(j[str(message.guild.id)])):
            d[j[str(message.guild.id)][i]['id']]=j[str(message.guild.id)][i]['xp']
        d = {k: v for k, v in sorted(
        d.items(), key=lambda item: item[1], reverse=True)}    
        lis = []
        for p in d.keys():
            lis.append(p)
        dic = {
            str(message.guild.id):lis
        }    
        f = open(f"levels/ranking/{message.guild.id}.json","w")
        json.dump(dic,f)
        f.close()



    @commands.Cog.listener()
    async def on_message(self,message):
            if message.author.bot:
                return
            try:    
                f = open(f"levels/{message.guild.id}noxp.txt","r")
                roleid = int(f.read())
                f.close()
                role = message.guild.get_role(roleid)
                if role in message.author.roles  :
                    return  
            except:
                pass    


            f = open(f"Moderation/{message.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            if(json_object['levelling']==False):
                print("Levelling Not set")
                return

            c = self.bot.get_channel(json_object['levelup_channel'])
            f = open(f"levels/{message.guild.id}.json","r")
            j = json.load(f)

            t=0
            for i in range(len(j[str(message.guild.id)])):
                if j[str(message.guild.id)][i]['id']==message.author.id:
                    t=i
            f.close()

            d = len(message.content)
            if d>10:
                d=10
            j[str(message.guild.id)][t]["xp"]+=d
            xp = j[str(message.guild.id)][t]["xp"]
            level  = j[str(message.guild.id)][t]['level']
            if xp>=100*level*level*level+100:
                # j[str(message.guild.id)][t]['xp']=0
                j[str(message.guild.id)][t]['level']+=1
                print("level up recorded")
                level = j[str(message.guild.id)][t]['level']
                print("levels")
                print(c.id)

                msg = await c.send(embed = discord.Embed(title=f"Congratulations!! On the lvl up !! You have advanced to {level} level"),content=message.author)
                await msg.add_reaction('👍')

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
            try:
                for i in range(index):
                    print("o")
                    await message.author.add_roles(self.bot.get_role(data['roles'][i]))
                print("perks given")
            except:
                pass

    @commands.command()
    async def levels(self,ctx,userName:discord.Member=None):
            f = open(f"Moderation/{ctx.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            if(json_object['levelling']==False):
                print("Levelling Not set")
                return
            if userName==None:
                userName=ctx.author
            f = open(f"levels/{ctx.guild.id}.json","r")
            j = json.load(f)
            f.close()
            t=0
            for i in range(len(j[str(ctx.guild.id)])):
                if j[str(ctx.guild.id)][i]['id']==userName.id:
                    t=i
            xp= j[str(ctx.guild.id)][t]['xp']   
            level= j[str(ctx.guild.id)][t]['level']
            limit  =100*level*level*level+100
            percentage = (xp//limit)*100
            embed = discord.Embed()
            embed.title=f"{userName[:-5]} is on lvl {level}"
            embed.description=f"{userName.mention} keep grinding.."
            labels= ['Progress',""]
            color=['purple','pink']
            sizes= [40, 40]
            print(1)
            fig = plt.figure(figsize=(5,5))
            plt.pie(sizes,labels=labels,shadow=True,colors=color,explode=(0.1,0.1))
            plt.title('{level}')
            plt.axis('equal')
            print(1)
            fig.savefig(f"{ctx.author.id}.png")
            await ctx.send(content=ctx.author.mention, file = discord.File(f"{ctx.author.id}.png"),embed=embed)
            os.remove(f"{ctx.author.id}.png")


    @commands.command()
    async def rank(self,ctx,userName:discord.Member=None):
            f = open(f"Moderation/{ctx.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            if(json_object['levelling']==False):
                print("Levelling Not set")
                return
            if userName==None:
                userName=ctx.author
            f = open(f"levels/ranking/{ctx.guild.id}.json","r")
            d = json.load(f)
            f.close()
            lis = d[str(ctx.guild.id)]
            rank =1
            for i in lis:
                if (i == userName.id):
                    break
                rank+=1
            embed = discord.Embed()
            embed.title=f"{userName} is on rank {rank}"
            embed.description=f"Keep grinding"
            await ctx.send(content=ctx.author.mention, embed=embed)


    @commands.command()
    @has_permissions(administrator=True)
    async def setlevel(self,ctx,userName:discord.Member,count:int):
            f = open(f"Moderation/{ctx.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            if(json_object['levelling']==False):
                print("Levelling Not set")
                return
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
                j[str(ctx.guild.id)][t]['xp'] = 100*(level-1)*(level-1)*(level-1)+100
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
            index = count//m
            print(data['roles'])
            if(index>len(data['roles'])):
                index = len(data['roles'])
            for i in range(index):
                role = ctx.guild.get_role(data['roles'][i])
                await userName.add_roles(role)

    @commands.command()
    async def leaderboard(self,ctx):
            f = open(f"Moderation/{ctx.guild.id}.json","r")
            json_object=json.load(f)
            f.close()
            if(json_object['levelling']==False):
                print("Levelling Not set")
                return
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

def setup(bot):
    bot.add_cog(levelling(bot))