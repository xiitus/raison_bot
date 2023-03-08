import os
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = str(os.environ["CARD_BOT_TOKEN"])
guild_id = int(os.environ["GUILD_ID"])

bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
card_2f_channel_id = int(os.environ["CARD_2F_CHANNEL_ID"])
attendance_channel_id = int(os.environ["ATTENDANCE_CHANNEL_ID"])

in_role_id = int(os.environ["IN_ROLE_ID"])
card_2f_role_id = int(os.environ["CARD_2F_ROLE_ID"])
trial_joining_role_id = int(os.environ["TRIAL_JOINING_ROLE_ID"])

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = Client(intents=intents)

card_can_take = True

@client.event
async def on_ready():
    print(f"カードキーちゃん が起動しました")
    global card_can_take
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == card_2f_role_id) and not (role.members == []):
                card_can_take = False

@client.event
async def on_member_join(member):
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
    takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく", 
                        "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
    returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                        "returm", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
    helplike_words = {"help", "ｈｅｌｐ", "へlp", "ヘｌｐ", "へるぷ", "ヘルプ", "たすけて", "ﾍﾙﾌﾟ", "助けて", "ﾀｽｹﾃ", 
                        "タスケテ", "ﾍlp", "hwkp", "hekp", "jelp", "felp", "gelp", "tasukete", "ｔａｓｕｋｅｔｅ", "本当に助けてください"}
    
    if (is_bot_channel) or (is_attendance_channel):
        if (message.author.bot):
            return

        user_said = message.content.lower()

        if (user_said in inlike_words) or (user_said[:-1] in inlike_words):
            print("add in")
            await message.author.add_roles(in_role)

        if (user_said in outlike_words) or (user_said[:-1] in outlike_words):
            print("remove in")
            await message.author.remove_roles(in_role)
        return

    if (is_bot_channel) or (is_2f_cardkey_channel):
        print("help/take/return")
        if (message.author.bot):
            return

        user_said = message.content.lower()

        if (user_said in helplike_words) or (user_said[:-1] in helplike_words):
            print("help")
            await message.channel.send(f"***help***      -> このヘルプメッセージを表示\n***take***      -> カードキーを所持していることを示すロールを付与\n***return***  -> カードキー返却時に、takeコマンドで付与したロールを剥奪")

        if (user_said in takelike_words) or (user_said[:-1] in takelike_words):
            if (card_can_take == True):
                card_can_take = False
                print("add card")
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
                print("remove card")
                await message.channel.send(f"**<@{message.author.id}> がカードキーを返却!**")
                await message.author.remove_roles(card_2f_role)
        return
    return

client.run(token)