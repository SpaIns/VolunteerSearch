#Created 2-6-15 Steffan
#Edited 2-14-16 to create first new models
from django.db import models

#thoughts; for location, add zip/require zip?
    
class Person(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	location_city = models.CharField(max_length=50)
	location_state = models.CharField(max_length=20)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	#how to make an age range? choice probably?
	MINOR = 'MNR'
	UNDER_25 = 'U25'
	UNDER_40 = 'U40'
	MIDDLE_AGE = 'MDA'
	SENIOR = 'SNR'
	age_range_choices = (
		(MINOR, "18 and under"),
		(UNDER_25, "Test1"),
		(UNDER_40, "25-39"),
		(MIDDLE_AGE, '40-64'),
		(SENIOR, '65+'),
	)
	age=models.CharField(max_length=3, choices=age_range_choices, default=UNDER_25)
	#will have to fix the below to cap at a certain length eventually for security reasons
	bio = models.TextField()
	#another choice for transit
	has_transportation = models.BooleanField()
	email = models.EmailField(max_length=254)


class Organization(models.Model):
	org_name = models.CharField(max_length=50)
	#Link org contact to a person object?
	location_city = models.CharField(max_length=50)
	location_state = models.CharField(max_length=20)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	#ensure it's less than or equal to 4 digits?
	age = models.IntegerField()
	#will have to fix the below to cap at a certain length eventually for security reasons
	bio = models.TextField()
	#needs job category link
	


class Jobs(models.Model):
	#job category link
	info = models.TextField()
	duration = models.DurationField()
	location_city = models.CharField(max_length=50)
	#contact = link to person
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	start_date = models.DateField(auto_now=False, auto_now_add=False)


#this one will have to auto-create skills when people add their own
#class SkillSets(models.Model):


#same as above
#class Categories(models.Model):


#To do later for ratings
#class Ratings(models.Model):