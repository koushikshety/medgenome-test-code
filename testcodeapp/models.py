from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TestCode(models.Model):
    mgm_code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='test_codes')
    status = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Not Normal', 'Not Normal')])
    documents = models.ManyToManyField(Document, blank=True, related_name='test_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mgm_code


class PreData(models.Model):
    mgm_code = models.CharField(max_length=100, default="mgm#", unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pre_data', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Not Normal', 'Not Normal')], default='Not Normal')
    documents = models.ManyToManyField(Document, blank=True, related_name='pre_data')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mgm_code


class Log(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.message[:50]}"


class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LockCode(models.Model):
    code = models.CharField(max_length=6, default='000000')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Lock Code"

