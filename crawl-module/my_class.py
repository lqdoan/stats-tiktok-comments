from datetime import datetime

class User:
    def __init__(self, id, region, sec_uid, unique_id, nickname, signature, avatar, verified, secret):
        self.id = id
        self.region = region
        self.sec_uid = sec_uid
        self.unique_id = unique_id
        self.nickname = nickname
        self.signature = signature
        self.avatar = avatar
        self.verified = verified
        self.secret = secret

    def to_dict(self):
        # Convert the User object to a dictionary for easy serialization
        return {
            'id': self.id,
            'region': self.region,
            'sec_uid': self.sec_uid,
            'unique_id': self.unique_id,
            'nickname': self.nickname,
            'signature': self.signature,
            'avatar': self.avatar,
            'verified': self.verified,
            'secret': self.secret
        }

class Comment:
    def __init__(self, id, video_id, text, create_time, digg_count, reply_total, user, status):
        self.id = id
        self.video_id = video_id
        self.text = text
        self.create_time = datetime.utcfromtimestamp(create_time)  # Convert to readable datetime
        self.digg_count = digg_count
        self.reply_total = reply_total
        self.user = user  # User object
        self.status = status

    def to_dict(self):
        # Convert the Comment object to a dictionary, including its User object
        return {
            'id': self.id,
            'video_id': self.video_id,
            'text': self.text,
            'create_time': self.create_time.isoformat(),  # Convert datetime to ISO string
            'digg_count': self.digg_count,
            'reply_total': self.reply_total,
            'user': self.user.to_dict(),  # Convert user to dictionary
            'status': self.status
        }