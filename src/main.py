import discord
from discord.ext import commands
from pynput.keyboard import Controller, Key
import mss
import os
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

keyboard = Controller()

class KeyPressView(discord.ui.View):
    async def take_screenshot(self):
        screenshot_file = "screenshot.png"
        
        # Take a screenshot
        with mss.mss() as sct:
            sct.shot(output=screenshot_file)

        return screenshot_file

    async def update_screenshot(self, interaction: discord.Interaction):
        screenshot_file = await self.take_screenshot()

        file = discord.File(screenshot_file, filename="screenshot.png")
        embed = discord.Embed(title="Screen")
        embed.set_image(url="attachment://screenshot.png")

        await interaction.message.edit(embed=embed, attachments=[file])

        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)

    async def press_key(self, key, duration=1.0):
        keyboard.press(key)
        await asyncio.sleep(duration)
        keyboard.release(key)
        
    @discord.ui.button(label="←", style=discord.ButtonStyle.primary, custom_id="left_arrow")
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key('a', duration=1.0)
        await interaction.response.defer()
        await self.update_screenshot(interaction)

    @discord.ui.button(label="↑", style=discord.ButtonStyle.primary, custom_id="up")
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key('w', duration=1.0)
        await interaction.response.defer()
        await self.update_screenshot(interaction)

    @discord.ui.button(label="↓", style=discord.ButtonStyle.primary, custom_id="down")
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key('s', duration=1.0)
        await interaction.response.defer()
        await self.update_screenshot(interaction)

    @discord.ui.button(label="→", style=discord.ButtonStyle.primary, custom_id="right_arrow")
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key('d', duration=1.0)
        await interaction.response.defer()
        await self.update_screenshot(interaction)

    @discord.ui.button(label="Jump", style=discord.ButtonStyle.grey, custom_id="space")
    async def space_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key(Key.space, duration=1.0)
        await interaction.response.defer()
        await self.update_screenshot(interaction)

    @discord.ui.button(label="<--", style=discord.ButtonStyle.success, custom_id="left_key")
    async def left_arrow_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key(Key.left, duration=0.5)
        await interaction.response.defer()
        await self.update_screenshot(interaction)
            
    @discord.ui.button(label="-->", style=discord.ButtonStyle.success, custom_id="right_key")
    async def right_arrow_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key(Key.right, duration=0.5)
        await interaction.response.defer()
        await self.update_screenshot(interaction)
    
    
    @discord.ui.button(label="Reset", style=discord.ButtonStyle.red, custom_id="reset")
    async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key(Key.esc)
        time.sleep(0.2)
        await self.press_key('r')
        time.sleep(0.1)
        await self.press_key(Key.enter)
        await interaction.response.defer()
        await self.update_screenshot(interaction)
        
    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red, custom_id="leave")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key(Key.esc)
        time.sleep(0.2)
        await self.press_key('l')
        time.sleep(0.1)
        await self.press_key(Key.enter)
        await interaction.response.defer()
        await self.update_screenshot(interaction)
        
    @discord.ui.button(label="Chat", style=discord.ButtonStyle.green, custom_id="chat")
    async def chat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.press_key('/')
        await interaction.response.defer()
        await self.update_screenshot(interaction)

@bot.command()
async def play(ctx):
    screenshot_file = "screenshot.png"
    
    with mss.mss() as sct:
        sct.shot(output=screenshot_file)
    
    if not os.path.exists(screenshot_file):
        await ctx.send("Failed to take a screenshot!")
        return

    file = discord.File(screenshot_file, filename="screenshot.png")
    embed = discord.Embed(title="Control Panel")
    embed.set_image(url="attachment://screenshot.png")
    view = KeyPressView()

    await ctx.send(file=file, embed=embed, view=view)
    
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)
    
bot.run('TOKEN') #your bot token
