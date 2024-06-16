
users = {
    "1234": {"reffer_id": "5165396993", "flag": True, "user_realy_name": "bot"},
    "1357": {"reffer_id": "5165396993", "flag": True, "user_realy_name": "bot"},
    "5678": {"reffer_id": None, "flag": True, "user_realy_name": "bot"},
    "1479": {"reffer_id": "5165396993", "flag": True, "user_realy_name": "bot"},
    "3154": {"reffer_id": "5678", "flag": True, "user_realy_name": "bot"},
    "6234": {"reffer_id": "5678", "flag": True, "user_realy_name": "bot"},
    "2244": {"reffer_id": "1234", "flag": True, "user_realy_name": "bot"},
}
def get_user_ball(user_id):
        ball = 0
        for user in users.values():
            if user_id == user['reffer_id'] and user['flag']: ball += 1
        return ball

