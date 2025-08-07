from .models import Notification

def create_notification(recipient, sender, notification_type, project=None, message=""):
    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        project=project,
        message=message
    )
