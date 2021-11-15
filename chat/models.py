from django.db import models
from users.models import CustomUser

# Create your models here.

class MessageModel(models.Model):

    # TEXT = 1
    # DOC = 2
    # IMAGE = 3
    # AUDIO = 4
    # VIDEO = 5

    # MESSAGE_TYPE_CHOICES = (
    #     (TEXT, 'text'),
    #     (DOC, 'doc'),
    #     (IMAGE, 'image'),
    #     (AUDIO, 'audio'),
    #     (VIDEO, 'video'),
    # )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user', related_name='from_user', db_index=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='recipient', related_name='to_user', db_index=True)
    created_at = models.DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField('timestamp', auto_now=True)
    message = models.TextField()
    # message_type = models.PositiveSmallIntegerField(choices=MESSAGE_TYPE_CHOICES)
    # attachment_file = models.FileField(upload_to='media/message_attachments', blank=True, null=True) 
    seen_at = models.DateTimeField('timestamp', default=None, blank=True, null=True)
    deleted_by_user = models.DateTimeField('timestamp', default=None, blank=True, null=True)
    deleted_by_recipient = models.DateTimeField('timestamp', default=None, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.message)

    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-created_at',)


class MessageAttachmentsModel(models.Model):

    TEXT = 1
    DOC = 2
    IMAGE = 3
    AUDIO = 4
    VIDEO = 5

    ATTACHMENT_TYPE_CHOICES = (
        (TEXT, 'text'),
        (DOC, 'doc'),
        (IMAGE, 'image'),
        (AUDIO, 'audio'),
        (VIDEO, 'video'),
    )

    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE, related_name='message_id', db_index=True)
    attachment_type = models.PositiveSmallIntegerField(choices=ATTACHMENT_TYPE_CHOICES)
    attachment_file = models.FileField(upload_to='message_attachments')

    class Meta:
        app_label = 'chat'
        verbose_name = 'message_attachment'
        verbose_name_plural = 'message_attachments'