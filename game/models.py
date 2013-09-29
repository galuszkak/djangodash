from django.contrib.auth.models import AbstractUser
from django.db import models


class MemoUser(AbstractUser):
    pass

# Create your models here.
class Game(models.Model):
    STATUS_VALUES = [
        ('WA', 'WaitingForPlayers'),
        ('PR', 'InProgress'),
        ('FI', 'Finished'),
    ]
    state = models.CharField(max_length=2, null=False, choices=STATUS_VALUES, default=STATUS_VALUES[0][0])
    comment = models.CharField(max_length=255, null=True)
    host = models.ForeignKey(MemoUser, related_name='hosted_games_set')
    players = models.ManyToManyField(MemoUser)


class Statistic(models.Model):
    STAT_TYPES = [
        ('SCO', 'Score'),
        ('TLE', 'TimeLeft'),
        ('FIN', 'FinalResult'),
        ('CTI', 'CreateTime'),
        ('STI', 'StartTime'),
        ('FTI', 'FinishTime'),
    ]
    game = models.ForeignKey(Game, null=False)
    type = models.CharField(max_length=3, null=False, choices=STAT_TYPES)
    player = models.ForeignKey(MemoUser, null=True)
    intValue = models.IntegerField(null=True)
    charValue = models.CharField(max_length=100, null=True)


class Configuration(models.Model):
    CONFIG_TYPES = [
        ('SIZ', 'Size'),
        ('MTI', 'MoveTime'),
        ('TTI', 'TotalTime'),
        ('PRI', 'Private'),
        ('PCO', 'PlayerCount'),
    ]
    game = models.ForeignKey(Game, null=False)
    type = models.CharField(max_length=3, null=False, choices=CONFIG_TYPES)
    intValue = models.IntegerField(null=True)
    charValue = models.CharField(max_length=100, null=True)
