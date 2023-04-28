import os
from dotenv import load_dotenv
from discord import Intents, Client, Game, Status

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

inlike_words = {"in", "いn", "un", "on", "im", "inn",
                "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                 "おうｔ", "our", "ｏｕｔ", "oup", "あうと", "アウト", "ｱｳﾄ"}
takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく",
                  "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                    "returm", "returb", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
fixlike_words = {"fix", "fixed", "ふぃぇd", "ｆｉｘｅｄ", "ふぃぇｄ"}


