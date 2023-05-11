from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class MentorTags(models.Model):
    tag = models.CharField(max_length=100, blank=False, unique=True) 
    tag_auto_bio = models.CharField(max_length=100, blank=True)
    match_id = models.IntegerField(default=0)

    def __str__(self):
        return self.tag

class MenteeTags(models.Model):
    tag = models.CharField(max_length=100, blank=False, unique=True) 
    match_id = models.IntegerField(default=0)

    def __str__(self):
        return self.tag

class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mentor_first_name = models.CharField(max_length=50)
    mentor_last_name = models.CharField(max_length=50)
    mentor_email = models.EmailField(max_length=250)
    bio = models.TextField(max_length=500)
    field_of_design = models.CharField(max_length=30)
    place_of_work = models.CharField(max_length=30)
    url = models.URLField()
    social_url = models.URLField(blank=True)
    tag = models.ManyToManyField(MentorTags)
    opt_out = models.BooleanField(default=False)
    bio_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.mentor_first_name+" "+self.mentor_last_name

class MenteeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mentee_first_name = models.CharField(max_length=50, blank=True)
    mentee_last_name = models.CharField(max_length=50, blank=True)
    mentee_email = models.EmailField(max_length=250, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    field_of_design = models.CharField(max_length=30, blank=True)
    place_of_work = models.CharField(max_length=30, blank=True)
    url = models.URLField(max_length=200, blank=True)
    question1 = models.CharField(max_length=200, blank=True)
    question1_answer = models.CharField(max_length=200, blank=True)
    question2 = models.CharField(max_length=200, blank=True)
    question2_answer = models.CharField(max_length=200, blank=True)
    question3 = models.CharField(max_length=200, blank=True)
    question3_answer = models.CharField(max_length=200, blank=True)
    tag = models.ManyToManyField(MenteeTags)

    def __str__(self):
        return self.mentee_first_name+" "+self.mentee_last_name

class Appointment(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    accepted_by_mentor = models.BooleanField(default=False)
    message_by_mentee = models.CharField(max_length=200,default="")
    rejected_by_mentor = models.BooleanField(default=False)

class MentorMenteeScore(models.Model):
    score = models.IntegerField(default=0)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.score)
