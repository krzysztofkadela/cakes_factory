from django.db import models

# Create your models here.
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # Add active field

    def get_status_display(self):
        return "Active" if self.active else "Inactive"

    def __str__(self):
        return f"{self.email} - {'Active' if self.active else 'Inactive'}"
