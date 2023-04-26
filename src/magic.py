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
