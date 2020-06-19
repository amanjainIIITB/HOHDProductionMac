from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    author = models.CharField(max_length=50, null=True)
    shopID = models.CharField(max_length=10, default='S1')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:10]

    def get_all_messages(shop_id):
        return Message.objects.filter(shopID=shop_id).order_by('timestamp').all()