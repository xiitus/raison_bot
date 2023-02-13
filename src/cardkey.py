import os
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = os.environ["CARD_BOT_TOKEN"]
guild_id = int(os.environ["GUILD_ID"])
bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
card_role_id = int(os.environ["CARD_2F_ROLE_ID"])
card_2f_channel_id = int(os.environ["CARD_2F_CHANNEL_ID"])

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
            if (role.id == card_role_id) and not (role.members == []):
                card_can_take = False

@client.event
async def on_message(message):
    global card_can_take

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_2f_cardkey_channel = (message.channel.id == card_2f_channel_id)
    role = message.guild.get_role(card_role_id)

    takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく", 
                        "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
    returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                        "returm", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
    helplike_words = {"help", "ｈｅｌｐ", "へlp", "ヘｌｐ", "へるぷ", "ヘルプ", "たすけて", "ﾍﾙﾌﾟ", "助けて", "ﾀｽｹﾃ", 
                        "タスケテ", "ﾍlp", "hwkp", "hekp", "jelp", "felp", "gelp", "tasukete", "ｔａｓｕｋｅｔｅ", "本当に助けてください"}

    if (is_bot_channel) or (is_2f_cardkey_channel):
        user_said = message.content.lower()
        if (message.author.bot):
            return

        if (user_said in helplike_words) or (user_said[:-1] in helplike_words):
            await message.channel.send(f"***help***      -> このヘルプメッセージを表示\n***take***      -> カードキーを所持していることを示すロールを付与\n***return***  -> カードキー返却時に、takeコマンドで付与したロールを剥奪")

        if (user_said in takelike_words) or (user_said[:-1] in takelike_words):
            if (card_can_take == True):
                card_can_take = False
                await message.channel.send(f"**<@{message.author.id}> がカードキーを装備!**")
                await message.author.add_roles(role)
            elif (card_can_take == False):
                role_member = role.members[0].id
                await message.channel.send(f"**カードは現在 <@{role_member}> が装備中!**")

        if (user_said in returnlike_words) or (user_said[:-1] in returnlike_words):
            if (card_can_take == True):
                await message.channel.send(f"**カードはまだ 2F にあります!**")
            elif (card_can_take == False):
                card_can_take = True
                await message.channel.send(f"**<@{message.author.id}> がカードキーを返却!**")
                await message.author.remove_roles(role)

client.run(token)

