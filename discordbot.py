import discord
import traceback
from discord.ext import commands
from os import getenv
import openai

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# メッセージの履歴を管理するリスト
messages = [
    {"role": "system", "content": "You are a helpful assistant. The AI assistant's name is AI Qiitan."},
    {"role": "user", "content": "こんにちは。あなたは誰ですか？"},
    {"role": "assistant", "content": "私は AI アシスタントの AI Qiitan です。なにかお手伝いできることはありますか？"}
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.id in [member.id for member in message.mentions]:
        print(message.content)
        user_message = message.content.split('>')[1].lstrip() if '>' in message.content else message.content
        messages.append({"role": "user", "content": user_message})

        openai_api_key = getenv('OPENAI_API_KEY')
        openai.api_key = openai_api_key

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = response.choices[0].message['content']
            print(response_text)
            await message.channel.send(response_text)
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("エラーが発生しました。")

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
