from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def in_upload_path(instance, filename):
    """ Function to return upload path for test case input file"""
    return "/".join(["testcases", str(instance.problem.id)]) + ".in"


def out_upload_path(instance, filename):
    """ Function to return upload path for test case output file"""
    return "/".join(["testcases", str(instance.problem.id)]) + ".out"

# Model for users


class Coder(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    link = models.URLField()
    score = models.DecimalField(default=0, decimal_places=3, max_digits=100)
    rank = models.IntegerField(default=-1)
    problems_tried = models.ForeignKey(
        'Problem', null=True, related_name="problems_tried", on_delete=models.DO_NOTHING)
    problems_ac = models.ForeignKey(
        'Problem', null=True, related_name="problems_ac", on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return self.user.username

# Model for the Problems to be uploaded on the judge


class Problem(models.Model):
    # Problem name (example: life, the universe and everything)
    name = models.CharField(max_length=255)
    # Problem code (example: TEST)
    code = models.CharField(max_length=20, unique=True)
    # Problem link (example: poj.com/problems/TEST)
    link = models.URLField()
    # Problem statement
    statement = models.TextField()

    num_submissions = models.IntegerField(default=0)  # number of submissions
    # number of accepted submissions
    num_ac = models.IntegerField(default=0)
    num_wa = models.IntegerField(default=0)          # number of wrong answers
    num_re = models.IntegerField(default=0)          # number of runtime errors
    num_tle = models.IntegerField(default=0)         # number of tles
    num_ce = models.IntegerField(default=0)             # number of compilation errors
    date_added = models.DateTimeField(auto_now_add=True)  # When added
    time_limit = models.IntegerField(default=1)         # Time Limit
    source = models.CharField(max_length=255)
    num_tests = models.IntegerField(default=1)

    author = models.ForeignKey('Coder', null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.code

# Model for Test Cases


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)
    input_file = models.FileField(upload_to=in_upload_path)
    output_file = models.FileField(upload_to=out_upload_path)

    def __unicode__(self):
        return self.problem.code


LANGUAGES = (
    ("C", "GNU C"),
    ("CPP", "GNU C++"),
)

# Model for problem submissions


class Submission(models.Model):
    STATUSES = (
        ("NT", "Not tested"),
        ("CE", "Compile Error"),
        ("TL", "Time Limit Exceeded"),
        ("RE", "Runtime Error"),
        ("AC", "Accepted")
    )
    submitter = models.ForeignKey(Coder, null=True, on_delete=models.DO_NOTHING)
    problem = models.ForeignKey(Problem, default=None, null=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, default="NT", choices=STATUSES)
    lang = models.CharField(max_length=4, default="CPP", choices=LANGUAGES)
    code = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=True)


