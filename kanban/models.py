from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Board(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class List(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "LW", ("Low")
        MEDIUM = "MD", ("Medium")
        IMPORTANT = "IP", ("Important")
        URGENT = "UR", ("Urgent")
        IMPORTANT_URGENT = "IU", ("Important & Urgent")

    class Status(models.TextChoices):
        NOT_STARTED = "NS", ("Not Started")
        IN_PROGRESS = "IP", ("In Progress")
        COMPLETED = "CP", ("Completed")
        
    class Tag(models.TextChoices):
        NONE = "None", ('None')
        FRONT_END = "FE", ("Frontend")
        BACK_END = "BE", ("Backend")
        API = "API", ("API")
        DATABASE = "DB", ("Database")
        FRAMEWORK = "FR",("Framework")
        TESTING = "T", ("Testing")
        UI_UX = "UIUX", ('UI/UX')
    class Points(models.TextChoices):
        NONE = "None", ('None')
        ONE = "1",("1")
        TWO = "2", ("2")
        THREE = "3",("3")
        FOUR = "4",("4")
        FIVE = "5",("5")
        SIX = "6", ("6")
        SEVEN = "7",("7")
        EIGHT = "8",("8")
        NINE = "9",("9")
        TEN = "10",("10")


    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=2, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NOT_STARTED)
    tag = models.CharField(max_length=4, choices=Tag.choices, default=Tag.NONE)
    points = models.CharField(max_length=4, choices=Points.choices, default=Points.NONE)

    time_moved = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title