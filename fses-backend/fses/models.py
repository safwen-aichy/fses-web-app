from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Define role choices with exact values expected by frontend
    ROLE_CHOICES = (
        ('OFFICE_ASSISTANT', 'Office Assistant'),
        ('SUPERVISOR', 'Supervisor'),
        ('PROGRAM_COORDINATOR', 'Program Coordinator'),
        ('PGAM', 'PGAM'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SUPERVISOR')
    is_first_time = models.BooleanField(default=True)
    
    # Add any other fields you need

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    TITLE_CHOICES = (
        (1, 'Professor'),
        (2, 'Associate Professor'),
        (3, 'Doctor'),
    )
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.IntegerField(choices=TITLE_CHOICES)
    university = models.CharField(max_length=100)
    staff = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Student(models.Model):
    PROGRAM_CHOICES = (
        ('PHD', 'PhD'),
        ('MPHIL', 'MPhil'),
        ('DSE', 'DSE'),
    )
    
    EVALUATION_TYPE_CHOICES = (
        ('FIRST_EVALUATION', 'First Evaluation'),
        ('RE_EVALUATION', 'Re-Evaluation'),
    )
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='supervised_students')
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    evaluation_type = models.CharField(max_length=20, choices=EVALUATION_TYPE_CHOICES)
    research_title = models.CharField(max_length=255, blank=True)
    semester = models.PositiveSmallIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Nomination(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='nominations')
    examiner1 = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='examiner1_nominations', null=True, blank=True)
    examiner2 = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='examiner2_nominations', null=True, blank=True)
    examiner3 = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='examiner3_nominations', null=True, blank=True)
    # For external examiners not in the system
    examiner1_name = models.CharField(max_length=100, null=True, blank=True)
    examiner1_email = models.EmailField(null=True, blank=True)
    examiner1_university = models.CharField(max_length=100, null=True, blank=True)
    examiner2_name = models.CharField(max_length=100, null=True, blank=True)
    examiner2_email = models.EmailField(null=True, blank=True)
    examiner2_university = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Nomination for {self.student.name}"


class Postponement(models.Model):
    POSTPONEMENT_TYPE_CHOICES = (
        ('MEDICAL', 'Medical'),
        ('PERSONAL', 'Personal'),
        ('ACADEMIC', 'Academic'),
        ('OTHER', 'Other'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='postponements')
    reason = models.TextField()
    type = models.CharField(max_length=20, choices=POSTPONEMENT_TYPE_CHOICES)
    requested_date = models.DateField()
    comments = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Postponement for {self.student.name} - {self.type}"
