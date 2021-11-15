from rest_framework import serializers
from chat.models import MessageModel
from users.models import CustomUser
import random
from django.utils import timezone


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageModel
        fields = ['id', 'user', 'recipient', 'created_at', 'updated_at', 'message', 'seen_at', 'deleted_by_user', 'deleted_by_recipient']

    def create(self, validated_data):
        user = validated_data.get('user')
        instance = self.Meta.model(**validated_data)
        admin_users = CustomUser.objects.all().filter(user_type=1, is_active=True, is_superuser=False).values_list('id')
        admin_users = [x[0] for x in admin_users]
        if user not in admin_users:
            random_admin_id = random.choice(admin_users)
            random_admin_id = CustomUser.objects.get(pk=random_admin_id)
            instance.recipient = random_admin_id
            instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.message = validated_data.pop('message', instance.message)
        instance.seen_at = validated_data.pop('seen_at', instance.seen_at)
        instance.deleted_by_user = validated_data.pop('deleted_by_user', instance.deleted_by_user)
        instance.deleted_by_recipient = validated_data.pop('deleted_by_recipient', instance.deleted_by_recipient)
        instance.save()
        return instance
