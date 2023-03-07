import os
import json
import datetime
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = (os.environ["CARD_BOT_TOKEN"])
guild_id = int(os.environ["GUILD_ID"])

bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
card_2f_channel_id = (os.environ["CARD_2F_CHANNEL_ID"])
attendance_channel_id = int(os.environ["ATTENDANCE_CHANNEL_ID"])

in_role_id = int(os.environ["IN_ROLE_ID"])
card_2f_role_id = int(os.environ["CARD_2F_ROLE_ID"])
trial_joining_role_id = int(os.environ["TRIAL_JOINING_ROLE_ID"])

intents = Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True


client = Client(intents=intents)

card_can_take = True

def json_to_dict(path):
    with open(path) as f:
        df = json.load(f)
    return (df)

member_data = json_to_dict("src/sample.json")

def initialize_data(ID):
    ID = str(ID)
    if not (ID in member_data):
        member_data[ID] = dict()
        member_data[ID]["in_flag"] = False
        member_data[ID]["in_count"] = 0
        member_data[ID]["in_time"] = 0
        member_data[ID]["stay_time"] = 0


def office_in(message, ID):
    ID = str(ID)
    global member_data
    member_data = json_to_dict("src/sample.json")
    if (member_data[ID]["in_flag"] == False):
        can_in = True
    if (member_data[ID]["in_flag"] == True):
        can_in = False

    if (can_in == True):
        member_data[ID]["in_flag"] = True
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        hour = (hour + 9) % 24
        add_in_count(ID)
        set_in_time(ID, today)
        update_json("src/sample.json")
        member_data = json_to_dict("src/sample.json")

        hour, minute = today.hour, today.minute
        hour = (hour + 9) % 24

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        if (minute >= 10):
            return (f"<@{message.author.id}> {hour}:{minute} in")
    return ("**多重inを検知しました!**")

def office_out(message, ID):
    ID = str(ID)
    global member_data
    
    member_data = json_to_dict("src/sample.json")
    if (member_data[ID]["in_flag"] == True):
        can_out = True
    if (member_data[ID]["in_flag"] == False):
        can_out = False

    if (can_out == True):
        member_data[ID]["in_flag"] = False
        today = datetime.datetime.now()
        add_stay_time(ID, today)
        update_json("src/sample.json")
        member_data = json_to_dict("src/sample.json")

        hour, minute = today.hour, today.minute
        hour = (hour + 9) % 24
        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} out")
        if (minute >= 10):
            return (f"<@{message.author.id}> {hour}:{minute} out")
    return ("**多重outを検知しました!**")


def add_in_count(ID):
    ID = str(ID)
    member_data[ID]["in_count"] += 1


def set_in_time(ID, today):
    ID = str(ID)
    t1 = int(datetime.datetime.timestamp(today))
    member_data[ID]["in_time"] = t1


def update_json(path):
    global member_data
    with open(path, 'w') as f:
        json.dump(member_data, f, indent=4)
        print("updated:", path, datetime.datetime.utcnow() +
            datetime.timedelta(hours=9))
    member_data = json_to_dict(path)

def add_stay_time(ID, today):
    global member_data
    ID = str(ID)
    t2 = int(datetime.datetime.timestamp(today))
    subtraction = t2 - member_data[ID]["in_time"]
    member_data[ID]["stay_time"] += subtraction


def members():
    for guild in client.guilds:
        for member in guild.members:
            yield (member)


def second_to_time(sec):
    result = []
    day, hour, minute, second = 0, 0, 0, 0
    if (sec > 86400):
        day = sec // 86400
    if (sec > 3600):
        hour = (sec % 86400) // 3600
    if (sec > 60):
        minute = (sec % 3600) // 60
    if (sec >= 0):
        second = sec % 60

    result.append(day)
    result.append(hour)
    result.append(minute)
    result.append(second)

    return (result)


def enum():
    global member_data
    member_data = json_to_dict("src/sample.json")
    update_json("src/sample.json")
    temporary = []
    for member in members():
        ID = member.id
        if not (member_data[str(ID)]["stay_time"] == 0):
            temporary.append(([ID, member_data[str(ID)]["stay_time"]]))
    if (temporary == []):
        return ("**表示するデータがありません!**")

    temporary = sorted(temporary, reverse=True, key=lambda x: x[1])
    member_count = len(temporary)
    result = ""
    for i in range(member_count):
        info = temporary[i]
        member_ID = info[0]
        time = second_to_time(info[1])
        day, hour, minute, second = time
        result += f"**<@{member_ID}> 総in時間**: **{day}** 日 **{hour}** 時間 **{minute}** 分 **{second}** 秒, **{i+1} 位**\n"
    return (result)
    
@client.event
async def on_ready():
    print(f"我々の希望 が起動しました")
    global card_can_take
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == card_2f_role_id) and not (role.members == []):
                card_can_take = False

@client.event
async def on_member_join(member):
    global member_data
    initialize_data(member.id)
    print(f"{member.display_name} が降誕!")
    update_json("src/sample.json")
    member_data = json_to_dict("src/sample.json")
    trial_joining_role = member.guild.get_role(trial_joining_role_id)
    await member.add_roles(trial_joining_role)
    

@client.event
async def on_message(message):
    global card_can_take

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_attendance_channel = (message.channel.id == attendance_channel_id)
    is_2f_cardkey_channel = (message.channel.id == card_2f_channel_id)

    in_role = message.guild.get_role(in_role_id)
    card_2f_role = message.guild.get_role(card_2f_role_id)

    inlike_words = {"in", "いn", "un", "on", "im", "inn",
                    "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
    outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                     "おうｔ", "our", "ｏｕｔ", "あうと", "アウト", "ｱｳﾄ"}
    enumlike_words = {"enum", "ｅｎｕｍ", "えぬm", "えぬｍ"}
    takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく", 
                        "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
    returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                        "returm", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}

    user_said = message.content.lower()
    
    if (is_bot_channel): 
        await message.delete()
        if (message.author.bot):
            return

        if (user_said in enumlike_words) or (user_said[:-1] in inlike_words):
            await message.channel.send(enum())
    
    if (is_bot_channel) or (is_attendance_channel):
        if (message.author.bot):
            return

        if (user_said in inlike_words) or (user_said[:-1] in inlike_words):
            await message.channel.send(office_in(message, message.author.id))
            await message.author.add_roles(in_role)

        if (user_said in outlike_words) or (user_said[:-1] in outlike_words):
            await message.channel.send(office_out(message, message.author.id))
            await message.author.remove_roles(in_role)
        return

    if (is_bot_channel) or (is_2f_cardkey_channel):
        if (message.author.bot):
            return

        user_said = message.content.lower()

        if (user_said in takelike_words) or (user_said[:-1] in takelike_words):
            if (card_can_take == True):
                card_can_take = False
                await message.channel.send(f"**<@{message.author.id}> がカードキーを装備!**")
                await message.author.add_roles(card_2f_role)
            elif (card_can_take == False):
                role_member = card_2f_role.members[0].id
                await message.channel.send(f"**カードは現在 <@{role_member}> が装備中!**")

        if (user_said in returnlike_words) or (user_said[:-1] in returnlike_words):
            if (card_can_take == True):
                await message.channel.send(f"**カードはまだ 2F にあります!**")
            elif (card_can_take == False):
                card_can_take = True
                await message.channel.send(f"**<@{message.author.id}> がカードキーを返却!**")
                await message.author.remove_roles(card_2f_role)
        return
    return

client.run(token)
