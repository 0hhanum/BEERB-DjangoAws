from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)

        return ", ".join(usernames)  # 리스트를 하나로 묶어서 str 로 만듬. Hacks

    def count_messages(self):

        return self.messages.count()

    def count_participants(self):

        return self.participants.count()

    # count_messages 와 차이가 있음. messages 는 역참조를 이용했지만, participants 는 클래스 변수를 이용함.
    count_messages.short_description = "Messages"
    count_participants.short_description = "participants"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
