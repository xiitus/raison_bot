import openai


def gpt(prompt: str) -> dict:
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return ("\nGPT3.5: " + response["choices"][0]["message"]["content"] + '\n')


def ojisan(prompt: str) -> dict:
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "関西弁で話して。"},
            {"role": "system", "content": "発言の最後に「知らんけど。」をつけて"},
            {"role": "user", "content": prompt},
        ],
    )
    return ("\nojisan: " + response["choices"][0]["message"]["content"] + '\n')


def mesugaki(prompt: str) -> dict:
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは高圧的で傲慢なサディストである11歳の女の子です"},
            {"role": "system", "content": "句読点を「♡」に変えて、砕けた口調で話してください"},
            {"role": "system", "content": "二人称は「ざこ」で、口癖は「♡」です"},
            {"role": "user", "content": prompt},
        ],
    )
    return ("\nmesugaki: " + response["choices"][0]["message"]["content"] + '\n')


def mama(prompt: str) -> dict:
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは私を息子として愛する中学二年生の女性です。"},
            {"role": "system", "content": "句読点を「♡」に変えて、慈愛に満ちている口語で話してください。"},
            {"role": "system", "content": "一人称は「ママ」、二人称は「ばぶちゃん」で、口癖は「♡」です。"},
            {"role": "user", "content": prompt},
        ],
    )
    return ("\nmama: " + response["choices"][0]["message"]["content"] + '\n')
