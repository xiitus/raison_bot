import os
import math
from random import randint
from dotenv import load_dotenv
import discord
import subprocess
import time
from discord.ext import commands
from discord_rpc import DiscordIpcClient, Presence



load_dotenv()

token = str(os.environ["CARD_BOT_TOKEN"])
guild_id = int(os.environ["GUILD_ID"])

bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
card_2f_channel_id = int(os.environ["CARD_2F_CHANNEL_ID"])
attendance_channel_id = int(os.environ["ATTENDANCE_CHANNEL_ID"])
door_channel_id = int(os.environ["DOOR_CHANNEL_ID"])
rule_channel_id = int(os.environ["RULE_CHANNEL_ID"])
y2023_channel_id = int(os.environ["Y2023_CHANNEL_ID"])


in_role_id = int(os.environ["IN_ROLE_ID"])
card_2f_role_id = int(os.environ["CARD_2F_ROLE_ID"])
trial_joining_role_id = int(os.environ["TRIAL_JOINING_ROLE_ID"])
office_training_role_id = int(os.environ["OFFICE_TRAINING_ROLE_ID"])
cardkey_dead_role_id = int(os.environ["CARDKEY_DEAD_ROLE_ID"])

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = Client(intents=intents)

card_can_take = True



@client.event
async def on_ready():
    print(f"ロールちゃん が起動しました")
    global card_can_take
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == card_2f_role_id) and not (role.members == []):
                card_can_take = False

# def set_thread(n, ID):
#     t = time.time()
#     thread = threading.Timer(1800, my_function, args=[ID])
#     thread.start()
#     thread = threading.Timer(n, )


def is_lost(S):
    words = {"lost", "ぉst", "ｌｏｓｔ", "ぉｓｔ",
             "ろすと", "ロスト", "失", "なくし", "落", "置", "忘", "紛", "おとし", "おいてき"}
    for word in words:
        if (word in S):
            return (True)
    return (False)



@client.event
async def on_member_join(member):
    trial_joining_role = member.guild.get_role(trial_joining_role_id)
    await member.add_roles(trial_joining_role)
    lst = [f"ハーイ、<@{member.id}>！RAISON DȆTREへようこそ！\nまずは落ち着いて、**<#{y2023_channel_id}>**を確認してください……",
           f"あなたなのね、<@{member.id}>！RAISON DȆTREへおいで……\nさっそく**<#{y2023_channel_id}>**をチェックしましょう！",
           f"ドゥクシ！<@{member.id}>！RAISON DȆTREへようこそ！\nほら、**<#{y2023_channel_id}>**を見ようよ！",
           f"<@{member.id}>！ここがRAISON DȆTREさ……！\n見るんだ！**<#{y2023_channel_id}>**を！さあ！",
           f"お目にかかれて光栄です……<@{member.id}>さん。\nまずは**<#{y2023_channel_id}>**をご覧ください。",
           f"私は汎用AIのロール……RAISON DȆTREへようこそ、<@{member.id}>さん。\n説明のために、**<#{y2023_channel_id}>**をご覧ください。",
           f"ウホッウホッ！<@{member.id}>！ウホッ！！🍌🍌\nウホホ！**<#{y2023_channel_id}>**！ウホッ！🍌",
           ]
    for channel in client.get_all_channels():
        if channel.id == door_channel_id:
            idx = randint(-1, 99)
            if (idx < 0):
                idx = 6
            else:
                idx %= 6
            await channel.send(lst[idx])
            break




#ユーザーがメッセージを送信したときに発動するイベントハンドラ
@client.event
async def on_message(message):
    global card_can_take

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_attendance_channel = (message.channel.id == attendance_channel_id)
    is_2f_cardkey_channel = (message.channel.id == card_2f_channel_id)

    in_role = message.guild.get_role(in_role_id)
    card_2f_role = message.guild.get_role(card_2f_role_id)
    trial_joining_role = message.guild.get_role(trial_joining_role_id)
    office_training_role = message.guild.get_role(office_training_role_id)
    cardkey_dead_role = message.guild.get_role(cardkey_dead_role_id)

    card_is_dead = False
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == cardkey_dead_role_id) and not (role.members == []):
                card_is_dead = True

    inlike_words = {"in", "いn", "un", "on", "im", "inn",
                    "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
    outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                     "おうｔ", "our", "ｏｕｔ", "あうと", "アウト", "ｱｳﾄ"}
    takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく",
                      "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
    returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                        "returm", "returb", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
    fixlike_words = {"fix", "fixed", "ふぃぇd", "ｆｉｘｅｄ", "ふぃぇｄ"}

    user_said = message.content.lower()

    if (is_attendance_channel):
        if (message.author.bot):
            return

        if (user_said in inlike_words) or (user_said[:-1] in inlike_words):
            print(f"{message.author} is in")
            await message.author.remove_roles(trial_joining_role)
            await message.author.add_roles(office_training_role)
            await message.author.add_roles(in_role)

        if (user_said in outlike_words) or (user_said[:-1] in outlike_words):
            print(f"{message.author} is out")
            await message.author.remove_roles(in_role)
        return

    if (is_2f_cardkey_channel):
        # if (is_bot_channel):
        if (message.author.bot):
            return

        if (user_said in fixlike_words):
            card_can_take = True
            await message.channel.send(f"**神聖なるカードは正位置へと戻った……この事件を忘れてはいけない。**")
            for guild in client.guilds:
                for member in guild.members:
                    if (member.id == 1073911059066396672):
                        await member.remove_roles(cardkey_dead_role)

        if (is_lost(user_said)):
            card_can_take = False
            await message.channel.send(f"**ピピピ……カードキーは *fix* コマンドが使用されるまで使用禁止になります。**")
            for guild in client.guilds:
                for member in guild.members:
                    if (member.id == 1073911059066396672):
                        await member.add_roles(cardkey_dead_role)
            await message.channel.send(f"**助けて、<@{479676924822814731}> <@{959367860734537748}> <@{493667859633930240}>!**")

        if (user_said in takelike_words) or (user_said[:-1] in takelike_words):
            if (card_is_dead):
                await message.channel.send(f"**カードキー・システムはダウン中……**")
                return
            if (card_can_take == True):
                print(f"{message.author} took")
                card_can_take = False
                await message.channel.send(f"**<@{message.author.id}> がカードキーを装備!**")
                await message.author.add_roles(card_2f_role)
            elif (card_can_take == False):
                role_member = card_2f_role.members[0].id
                await message.channel.send(f"**カードは現在 <@{role_member}> が装備中!**")

        if (user_said in returnlike_words) or (user_said[:-1] in returnlike_words):
            if (card_is_dead):
                await message.channel.send(f"**カードキー・システムはダウン中……**")
                return
            if (card_can_take == True):
                await message.channel.send(f"**カードはまだ 2F にあります!**")
            elif (card_can_take == False):
                card_can_take = True
                print(f"{message.author} returned")
                await message.channel.send(f"**<@{message.author.id}> がカードキーを返却!**")
                await message.author.remove_roles(card_2f_role)

    if (is_bot_channel):
        if (user_said == "get_in_data"):
            people = len(message.guild.get_role(in_role_id).members)
            messages = [f"**ガラ空き……ライバルをぶっちぎるチャンスだね! 世界を創る準備はできた?**",
                        f"**席にはまだまだ空きがあるよ! 競争の世界に、おいでおいで!**",
                        f"**いつもよりちょっぴりにぎやか! ライバルは今も生産してるぞ!**",
                        f"**ストイックな場所だね……これが競争の世界というわけか!**",
                        f"**ワーオ! こんなに多くの人間が励んでいるの? 最高の場所だ……!**",
                        f"**待って、待つんだ……そろそろパンクする。みみみみんな落ち着いて!😵**",
                        f"**OK……完全に満員だ、今はね。 これからオフィスに来ようとしている人は, 考え直そう……**",
                        f"**満員を超えているぞ! 一体どうやったんだ? 空間のエントロピーが高すぎる!**"
                        ]
            say = messages[math.floor(people / 6)]
            if (people == 26):
                say = messages[6]
            elif (people > 26):
                say = messages[7]
            await message.channel.send(f"**現在のin人数は{people}人!**")
            await message.channel.send(say)
        return
    return




client.run(token)


# 以下、Wi-Fi接続状態の監視
wifi_ssid = {"frourio-2.4G-WPA3", "frourio-2.4G-2F-WPA3", "frourio-2.4G-2F-sub", "frourio-2.4G-2F-WPA2", "frourio-5G-2F-sub", "frourio-5G-2F-WPA2", "frourio-5G-2F-WPA3"}  # ここに自分のWi-FiのSSIDを入力してください

#接続状態が変化した場合にhandle_wifi_connnection_changeを呼び出す
def is_wifi_connected():
    try:
        result = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        wifi_ssid = "your_wifi_ssid"  # ここに自分のWi-FiのSSIDを入力してください
        if result == wifi_ssid:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

async def on_connected(user):
    print(f"Connected to {user.name} ({user.id})")
    role_name = "in_role"  # ここに追加するロール名を入力してください
    role = discord.utils.get(guild.roles, name=role_name)
    await user.add_roles(role)
    print(f"{user.name} has been added to {role_name} role")

def on_disconnected():
    print("Disconnected from Discord")

def handle_wifi_connection_change(connected, client):
    if connected:
        if client.connected:
            presence = Presence(client)
            presence.connect()
            user = presence.get_user()
            bot.loop.create_task(on_connected(user))
            presence.close()
    else:
        if client.connected:
            client.disconnect()

CLIENT_ID = 'JUSTIN_CLIENT_ID'  # Discord Developer Portalで作成したアプリケーションのクライアントID
DISCORD_BOT_TOKEN = 'CARD_BOT_TOKEN'  # Discord Botのトークン

connected = False
client = DiscordIpcClient.for_platform(os.name)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    global guild
    print(f"Logged in as {bot.user.name}")
    guild = bot.guilds[0]

while True:
    new_connected = is_wifi_connected()
    if new_connected != connected:
        connected = new_connected
        handle_wifi_connection_change(connected, client)
    time.sleep(60)

bot.run(DISCORD_BOT_TOKEN)