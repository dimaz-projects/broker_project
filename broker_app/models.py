from django.db import models

class clients(models.Model):
    name=models.CharField(max_length=200)
    birthday=models.DateField('birthday')
    phone_number=models.CharField(max_length=11)
    email=models.CharField(max_length=200)
    contract_date=models.DateField('contract date')

class companies_sites(models.Model):
    company_name=models.CharField(max_length=200)
    link=models.CharField(max_length=200)
    report_link = models.CharField(max_length=200)

class useful_sites(models.Model):
    site_name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    link=models.CharField(max_length=200)


class notes(models.Model):
    topic=models.CharField(max_length=100)
    description=models.CharField(max_length=300)
    date=models.DateTimeField('date of creation')
