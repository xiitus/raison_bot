import os
import math
from random import randint
from dotenv import load_dotenv
from discord import Intents, Client, Game, Status
from datetime import datetime, timezone

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
newby_role_id = int(os.environ["NEWBY_ROLE_ID"])

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = Client(intents=intents)

card_can_take = True

inlike_words = {"in", "いn", "un", "on", "im", "inn",
                "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                 "おうｔ", "our", "ｏｕｔ", "あうと", "アウト", "ｱｳﾄ"}
takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく",
                  "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                    "returm", "returb", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
fixlike_words = {"fix", "fixed", "ふぃぇd", "ｆｉｘｅｄ", "ふぃぇｄ"}


@client.event
async def on_ready():
    guild = client.get_guild(guild_id)
    print(f"ロールちゃん が起動しました")
    global card_can_take
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == card_2f_role_id) and not (role.members == []):
                card_can_take = False

    people = len(guild.get_role(in_role_id).members)
    game = Game(f"{people}人が RAISON DÊTRE")
    await client.change_presence(status=Status.idle, activity=game)


def is_lost(S):
    words = {"lost", "ぉst", "ｌｏｓｔ", "ぉｓｔ",
             "ろすと", "ロスト", "失", "なくし", "落", "置", "忘", "紛", "おとし", "おいてき"}
    for word in words:
        if (word in S):
            return (True)
    return (False)


def subtime(unix_time1: float, unix_time2: float) -> tuple:
    diff = (unix_time2 - unix_time1)
    hour, minute = (diff//3600 + 24) % 24, (diff//60 + 60) % 60
    return (hour, minute)


@client.event
async def on_member_join(member):
    newby_role = member.guild.get_role(newby_role_id)
    trial_joining_role = member.guild.get_role(trial_joining_role_id)
    await member.add_roles(newby_role)
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


async def get_newby_rank(after_date, before_date):
    server = client.get_guild(guild_id)
    channel = server.get_channel(attendance_channel_id)
    newby_role = server.get_role(newby_role_id)

    tmp = dict()
    names = set()

    async for message in channel.history(limit=None):
        if (after_date.replace(tzinfo=timezone.utc) <= message.created_at.replace(tzinfo=timezone.utc) <= before_date.replace(tzinfo=timezone.utc)):
            person = message.author.id
            msg = message.content
            time = message.created_at.timestamp()
            roles = message.author.roles
            if (msg.lower() in outlike_words) and (newby_role in roles):
                if not (person in tmp):
                    names.add(person)
                    tmp[person] = ([], [])
                tmp[person][1].append(time)
        else:
            break

    async for message in channel.history(limit=None):
        if (after_date.replace(tzinfo=timezone.utc) <= message.created_at.replace(tzinfo=timezone.utc) <= before_date.replace(tzinfo=timezone.utc)):
            person = message.author.id
            msg = message.content
            time = message.created_at.timestamp()
            roles = message.author.roles
            if (msg.lower() in inlike_words) and (newby_role in roles):
                if not (person in tmp):
                    tmp[person] = ([], [])
                tmp[person][0].append(time)
        else:
            break

    ans = dict()
    for n in names:
        ans[n] = [0, 0]
        length = min(len(tmp[n][0]), len(tmp[n][1]))
        ans[n].append(length)
        for i in range(length):
            t = subtime(tmp[n][0][i], tmp[n][1][i])
            ans[n][0] += t[0]
            ans[n][1] += t[1]
        ans[n][0] += ans[n][1] // 60
        ans[n][1] %= 60

    ans2 = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    print(ans2)

    channel = server.get_channel(bot_channel_id)
    await channel.send(f"***Ranking of newby:\n{after_date} ~ {before_date}***")
    i = 1
    for a in ans2:
        await channel.send(f"{i}位: <@{a[0]}> - {int(a[1][0])}h {int(a[1][1])}m (in回数 {a[1][2]}回)\n")
        i += 1
    return ans2


async def get_all_rank(after_date, before_date):
    server = client.get_guild(guild_id)
    channel = server.get_channel(attendance_channel_id)

    tmp = dict()
    names = set()

    async for message in channel.history(limit=None):
        if (after_date.replace(tzinfo=timezone.utc) <= message.created_at.replace(tzinfo=timezone.utc) <= before_date.replace(tzinfo=timezone.utc)):
            person = message.author.id
            msg = message.content
            time = message.created_at.timestamp()
            if (msg.lower() in outlike_words):
                if not (person in tmp):
                    names.add(person)
                    tmp[person] = ([], [])
                tmp[person][1].append(time)
        else:
            break

    async for message in channel.history(limit=None):
        if (after_date.replace(tzinfo=timezone.utc) <= message.created_at.replace(tzinfo=timezone.utc) <= before_date.replace(tzinfo=timezone.utc)):
            person = message.author.id
            msg = message.content
            time = message.created_at.timestamp()
            if (msg.lower() in inlike_words):
                if not (person in tmp):
                    tmp[person] = ([], [])
                tmp[person][0].append(time)
        else:
            break

    ans = dict()
    for n in names:
        ans[n] = [0, 0]
        length = min(len(tmp[n][0]), len(tmp[n][1]))
        ans[n].append(length)
        for i in range(length):
            t = subtime(tmp[n][0][i], tmp[n][1][i])
            ans[n][0] += t[0]
            ans[n][1] += t[1]
        ans[n][0] += ans[n][1] // 60
        ans[n][1] %= 60

    ans2 = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    print(ans2)

    channel = server.get_channel(bot_channel_id)
    await channel.send(f"***{after_date} ~ {before_date} Ranking of newby:***")
    await channel.send('\n')
    i = 1
    for a in ans2:
        await channel.send(f"{i}位: <@{a[0]}> - {int(a[1][0])}h {int(a[1][1])}m (in回数 {a[1][2]}回)\n")
        i += 1
    return ans2


@ client.event
async def on_message(message):
    global card_can_take

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_attendance_channel = (message.channel.id == attendance_channel_id)
    is_2f_cardkey_channel = (message.channel.id == card_2f_channel_id)

    in_role = message.guild.get_role(in_role_id)
    card_2f_role = message.guild.get_role(card_2f_role_id)
    cardkey_dead_role = message.guild.get_role(cardkey_dead_role_id)
    trial_joining_role = message.guild.get_role(trial_joining_role_id)
    office_training_role = message.guild.get_role(office_training_role_id)

    card_is_dead = False
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == cardkey_dead_role_id) and not (role.members == []):
                card_is_dead = True

    user_said = message.content.lower()

    people = len(message.guild.get_role(in_role_id).members)
    game = Game(f"{people}人が RAISON DÊTRE")
    await client.change_presence(status=Status.idle, activity=game)

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
        if (user_said == "newby_ranking_plz"):
            d1 = datetime(2023, 4, 9, tzinfo=timezone.utc)
            d2 = datetime(2023, 4, 30, tzinfo=timezone.utc)
            await get_newby_rank(after_date=d1, before_date=d2)
            return

        if (user_said == "all_ranking_plz"):
            d1 = datetime(2023, 4, 9, tzinfo=timezone.utc)
            d2 = datetime(2023, 4, 30, tzinfo=timezone.utc)
            await get_newby_rank(after_date=d1, before_date=d2)
            await get_all_rank(after_date=d1, before_date=d2)
            return

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
