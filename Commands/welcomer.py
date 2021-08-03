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
# intents = discord.Intents.all()
#   # client = discord.Client(intents=intents)

# bot = commands.Bot(command_prefix=',', intents=intents)
class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            
            f = open(f"resources/welcomeSet{member.guild.name}.json","r")
            data = json.load(f)
            f.close()
            l = data
            channel = self.bot.get_channel(int(l['channel']))
            # await channel.send("hello")
            message = str(l['message'])
            back = l['backgroundPath']
            message = message.format(username=member.mention,server=member.guild.name,count=len(member.guild.members))
            fp = self.welcome(member.avatar_url,back,member)            
            await channel.send(file=discord.File(fp),content=str(message))
            print(7)
            os.remove(fp)

        except:
            print("welcomer not set")

    @commands.command()
    @has_permissions(administrator=True)
    async def set_welcomer(self,ctx):
        embed = discord.Embed(title=f"{self.bot.user} welcomer Settings")
        embed.add_field(name="Welcome Channel",value="send the welcome channel as`welcome|<channel id>` ")
        await ctx.send(content=ctx.author.mention,embed=embed)
        def check(m):
            return (str(m.content)).startswith("welcome") and m.author == ctx.author
        msg = await self.bot.wait_for('message',check=check)
        # print(1)
        try:
            cid=msg.content.split("|")[1]
            # print(cid)
            await ctx.send(f"<#{cid}>")
        except:
            await ctx.send("invalid input given, retry the whole process")
            return    
        embed = discord.Embed(title=f"{self.bot.user} welcomer Settings")
        embed.add_field(name="back Image",value="send the url as `welcome|<url of gif/image>` ")
        await ctx.send(content=ctx.author.mention,embed=embed)

        def check(m):
            return (str(m.content)).startswith("welcome") and m.author == ctx.author
        msg = await self.bot.wait_for('message',check=check)
        
        try:
            # print(2)
            url = msg.content.split("|")[1]
            # print(2)
            await ctx.send(content = "The Set Background picture is:-"+url)
        except:
            await ctx.send("invalid url was sent\nretry the whole process")
            return    
        
        embed = discord.Embed(title=f"{self.bot.user} welcomer Settings")
        embed.add_field(inline=False,name="Welcome Message",value="send the contents as `welcome|<content>`")
        embed.add_field(inline=False,name = "addons", value="{username} to mention the new member\n{server} to mention the name of the server\n{count} to give the count since the member has joined.")
        await ctx.send(content=ctx.author.mention,embed=embed)
        def check2(m):
            return (str(m.content)).startswith("welcome") and m.author ==ctx.author
        msg = await self.bot.wait_for('message', check=check2)
        try:
            content = msg.content.split("|")[1]
            await ctx.send(content=content)
        except:
            await ctx.send("invalid content, retry the whole process. ;(")
        
        b = Image.open(requests.get(url, stream=True).raw)
        back = []
        for frame in ImageSequence.Iterator(b):
                frame = frame.convert('RGBA')
                back.append(frame)
        back[0].save(f'resources/welcomeBack/{ctx.guild.id}.gif', format='GIF',
                        append_images=back[1:],
                        save_all=True,
                        duration=10, loop=0)        
        back = f'resources/welcomeBack/{ctx.guild.id}.gif'
        fp = self.welcome(self.bot.user.avatar_url,url,self.bot.user)
        # print(1)
        await ctx.send(file=discord.File(fp),content=content)    
        
        os.remove(fp)
        await ctx.send("The Above is a preview\n_if u agree reply `yes`_\n_if u don't agree reply `no` to call off_")
        def check2(m):
            return ((str(m.content)).lower() == "yes" or (str(m.content)).lower() =="no") and m.author ==ctx.author
        msg = await self.bot.wait_for('message', check=check2)
        if msg.content.lower() == "no":
            os.remove(back)
            await ctx.send("Sorry to disappoint")
            return
        await ctx.send("setting things up...")
        print(1)

        # print(1)
        temp = {
            "channel" : cid,
            "message" : content,
            "backgroundPath" : back
        }
        # print(2)
        f=open(f"resources/welcomeSet{ctx.guild.name}.json","w+")
        json.dump(temp,f)
        f.close()
        # print(3)
        await ctx.send(":thumbs_up: -_-")







    def border(self,im, size, color='white'):
        img = Image.new("RGB", (60, 60), 'white')
        dr = ImageDraw.Draw(img)
        dr = ImageDraw.Draw(img)
        dr.ellipse((0, 0, 60, 60), 'white')
        # crop_to_circle(img)
        basewidth = 300
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        # img1 = Image.open("/home/luto_login/Documents/my_bot/backg_welc.jpg")
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        h, w = img.size
        size = (size[0]+12, size[1]+12)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        h, w = output.size
        h1, w1 = im.size
        output.paste(im, (h//2-h1//2, w//2-w1//2), im)
        return output

    def crop_to_circle(self,img2, s):
            basewidth = 300
            wpercent = (basewidth / float(img2.size[0]))
            hsize = int((float(img2.size[1]) * float(wpercent)))
            # img1 = Image.open("/home/luto_login/Documents/my_bot/backg_welc.jpg")
            img2 = img2.resize((basewidth, hsize), Image.ANTIALIAS)
            h, w = img2.size
            size = s
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            output = ImageOps.fit(img2, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output = self.border(output, size)
            return output
        # count the number of frames

    def getPFP(self,url, size):
            pfp = Image.open(requests.get(url, stream=True).raw)
            pfpf = []
            for frame in ImageSequence.Iterator(pfp):
                frame = self.crop_to_circle(frame.convert('RGBA'), size)
                # display(frame)
                pfpf.append(frame)
            return pfpf
        # display(pfpf[0])

    def getBackg(self,url):
            print(19)
            try:
                backg = Image.open(requests.get(url, stream=True).raw)
            except:
                print(url)
                backg = Image.open(url)
            print(20)
            back = []
            for frame in ImageSequence.Iterator(backg):
                frame = frame.convert('RGBA')
                back.append(frame)
            return back

    def text(self,img1, p, member):
            # print(2)
            draw = ImageDraw.Draw(img1)
            font = ImageFont.truetype(
                'resources/KoyaSans-BoldItalic.ttf', size=36)
            fontb = ImageFont.truetype(
                'resources/KoyaSans-BoldItalic.ttf', size=39)
            (x, y) = img1.size
            # print(2)
            x = x//2
            y = y-54
            message = "WELCOME"
            color = 'rgb(255, 255, 2555)'  # black color
            w, h = fontb.getsize(message)
            draw.text((x-w/2, y-h/2), message, fill='black', font=fontb)
            w, h = font.getsize(message)

            draw.text((x-w/2, y-h/2), message, fill=color, font=font)
            message = f"{member}"
            font = ImageFont.truetype(
                'resources/KoyaSans-BoldItalic.ttf', size=18)
            fontb = ImageFont.truetype(
                'resources/KoyaSans-BoldItalic.ttf', size=20)
            # w, h = fontb.getsize(message)
            # draw.text((x-w/2, y+36-h/2), message, font=font, fill="black")
            w, h = font.getsize(message)
            draw.text((x-w/2, y+36-h/2), message, font=font, fill="white")
            return img1

    def pfp_paste(self,pfpf, back, member, p):
            h, w = back[0].size
            h1, w1 = pfpf[0].size
            # display(pfpf[0])
            if(p == (0, 0)):
                p = (h//2-h1//2, w//2-w1//2-25)
            if(len(pfpf) > len(back)):
                j = 0
                while(len(pfpf) > len(back)):
                    if(j >= len(back)):
                        j = 0
                    back.append(back[j])
                    j += 1
                # print(len(back), len(pfpf))
                for i in range(len(back)):
                    back[i].paste(pfpf[i], p, pfpf[i])
                    # print("o")
                    back[i] = self.text(back[i], p, member)
                    # print("p")
            else:
                j = 0
                while(len(back) > len(pfpf)):
                    if(j >= len(pfpf)):
                        j = 0
                    pfpf.append(pfpf[j])
                    j += 1
                # display(pfpf[0])
                for i in range(len(back)):
                    back[i].paste(pfpf[i], p, pfpf[i])
                    back[i] = self.text(back[i], p, member)
            # display(back[0])
            # print("fine")
            return back

    def welcome(self,url, fp, member, size=(0, 0), position=(0, 0)):
            # print(1)
            back = self.getBackg(fp)
            # print(1)
            if(size == (0, 0)):
                t = back[0]
                size = (t.size[0]//3, t.size[0]//3)
            pfpf = self.getPFP(url, size)
            back = self.pfp_paste(pfpf, back, member, position)
            # print("fine")
            back[0].save("resources/welCfile.gif", format='GIF',
                        append_images=back[1:],
                        save_all=True,
                        duration=10, loop=0)
            # print(1)
            return "resources/welCfile.gif"

def setup(bot):
    bot.add_cog(Welcome(bot))
