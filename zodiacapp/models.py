from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ZODIAC_CHOICES = [
        ('Avinas', 'Avinas'),
        ('Jautis', 'Jautis'),
        ('Dvyniai', 'Dvyniai'),
        ('Vėžys', 'Vėžys'),
        ('Liūtas', 'Liūtas'),
        ('Mergelė', 'Mergelė'),
        ('Svarstyklės', 'Svarstyklės'),
        ('Skorpionas', 'Skorpionas'),
        ('Šaulys', 'Šaulys'),
        ('Ožiaragis', 'Ožiaragis'),
        ('Vandenis', 'Vandenis'),
        ('Žuvys', 'Žuvys'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='images/default_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    zodiac = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class RelationshipStatus(models.Model):
    user = models.OneToOneField(User, related_name='relationship_status', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Vienišas', 'Vienišas'),
        ('Įsipareigojęs', 'Įsipareigojęs'),
        ('Susižadėjęs', 'Susižadėjęs'),
        ('Vedęs', 'Vedęs'),
        ('Komplikuota', 'Komplikuota'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Vienišas',
        help_text='Relationship status'
    )
    COLOR_CHOICES = (
        ('red', 'Raudona'),
        ('green', 'Žalia'),
        ('blue', 'Mėlyna'),
        ('yellow', 'Geltona'),
    )
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='blue',
        help_text='Color for display'
    )

    def __str__(self):
        return f"{self.user.username}'s relationship status: {self.status}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"
