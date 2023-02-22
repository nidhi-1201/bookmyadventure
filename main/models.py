from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class activity(models.Model):
    activityId = models.CharField(default=None, max_length=30)
    ATTRACTION_TYPE = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Thrilling'),
    ]
    attraction_type = models.CharField(max_length=20, choices=ATTRACTION_TYPE, null=False)
    price = models.PositiveIntegerField(default=None, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Activity'
        ordering = ['activityId']

    def __str__(self):
        return self.activityId


class Reservation(models.Model):
    bookingID = models.CharField(default=None, max_length=30)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)

    user_booked = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    # no_rooms = models.IntegerField(    null=True, blank=True)
    activity_allocated = models.ForeignKey(activity, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    waiting = models.BooleanField(default=False)
    ATTRACTION_TYPE = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Thrilling'),
    ]
    attraction_type = models.CharField(max_length=20, choices=ATTRACTION_TYPE, null=False)
    booktime = models.DateField(null=False)

    class Meta:
        ordering = ['-booktime']

    def __str__(self):
        return self.bookingID


class PreReservation(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    # no_rooms = models.IntegerField(null=True, blank=True)
    activity = models.ForeignKey(activity, on_delete=models.CASCADE, null=True, blank=True)
    ATTRACTION_TYPE = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Thrilling'),
    ]
    attraction_type = models.CharField(max_length=20, choices=ATTRACTION_TYPE, null=False)

    def __str__(self):
        return str(self.activity) + ' || ' + str(self.start_date) + ' - ' + str(self.end_date)


class Visitor(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Visitors'

    def __str__(self):
        return self.first_name


class Feedback(models.Model):
    feedbackID = models.CharField(default=None, max_length=100)
    user_of = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    time = models.DateField(default=timezone.now, null=False)
    feed = models.TextField(default=None)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.feedbackID


class WaitingOn(models.Model):
    resID = models.ForeignKey('Reservation', on_delete=models.CASCADE, null=False, blank=False)
    date_booked = models.DateField(default=timezone.now, null=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'WaitingOn'
