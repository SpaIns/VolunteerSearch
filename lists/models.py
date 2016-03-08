#Created 2-6-15 Steffan
#Edited 2-14-16 to create first new models
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save

#thoughts; for location, add zip/require zip?

states = (
    ('AL','ALABAMA'),
    ('AK','ALASKA'), 
    ('AZ','ARIZONA'),
    ('AR','ARKANSAS'),
    ('CA','CALIFORNIA'),
    ('CO','COLORADO'),
    ('CT','CONNECTICUT'),
    ('DE','DELAWARE'),
    ('FL','FLORIDA'),
    ('GA','GEORGIA'),
    ('HI','HAWAII'),
    ('ID','IDAHO'),
    ('IL','ILLINOIS'),
    ('IN','INDIANA'),
    ('IA','IOWA'),
    ('KS','KANSAS'),
    ('KY','KENTUCKY'),
    ('LA','LOUISIANA'),
    ('ME','MAINE'),
    ('MD','MARYLAND'),
    ('MA','MASSACHUSETTS'),
    ('MI','MICHIGAN'),
    ('MN','MINNESOTA'),
    ('MS','MISSISSIPPI'),
    ('MO','MISSOURI'),
    ('MT','MONTANA'),
    ('NE','NEBRASKA'),
    ('NV','NEVADA'),
    ('NH','NEW HAMPSHIRE'),
    ('NJ','NEW JERSEY'),
    ('NM','NEW MEXICO'),
    ('NY','NEW YORK'),
    ('NC','NORTH CAROLINA'),
    ('ND','NORTH DAKOTA'),
    ('OH','OHIO'),
    ('OK','OKLAHOMA'),
    ('OR','OREGON'),
    ('PA','PENNSYLVANIA'),
    ('RI','RHODE ISLAND'),
    ('SC','SOUTH CAROLINA'),
    ('SD','SOUTH DAKOTA'),
    ('TN','TENNESSEE'),
    ('TX','TEXAS'),
    ('UT','UTAH'),
    ('VT','VERMONT'),
    ('VA','VIRGINIA'),
    ('WA','WASHINGTON'),
    ('WV','WEST VIRGINIA'),
    ('WI','WISCONSIN'),
    ('WY','WYOMING')
)
    
class Skill(models.Model):
    skill = models.CharField(max_length=30)

    def __str__(self):
        return self.skill

    class Meta:
        ordering = ('skill',)

class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not user_name:
            raise ValueError('Users must have a user name')

        user = self.model(
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(user_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user    

class User(AbstractBaseUser):
    skills_choices = (
        ('ms_office', 'MS Office'),
        ('coding', 'Programming'),
        ('senior_help', 'Senior Help'),
        ('grooming', 'Pet Grooming'),
        ('walking', 'Dog Walking'),
        ('training', 'Pet Training'),
        ('tutoring', 'Tutoring'),
        ('construction', 'Construction'),
        ('restoration', 'Restoration'),
        ('landscaping', 'Landscaping'),
        ('heavy_lifting', 'Heavy Lifting')
    )
    
    user_type_choices = (
        ('USER', 'USER'),
        ('ORG', 'ORG'),
    )

    age_range_choices = (
        ('NA', '-'),
        ('MINOR', '18 and under'),
        ('U25', '19-25'),
        ('U40', '25-39'),
        ('MDA', '40-64'),
        ('SNR', '65+'),
    )
    
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(default='1990-04-04')
    user_name = models.CharField(max_length=20,verbose_name='Name', unique=True)
    location_city = models.CharField(max_length=50, verbose_name='City')
    location_state = models.CharField(max_length=20, verbose_name='State', choices=states, default='WA')
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    age=models.CharField(max_length=5, choices=age_range_choices, default='NA')
    #will have to fix the below to cap at a certain length eventually for security reasons
    bio = models.TextField()
    skills = models.ManyToManyField(Skill)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user_type=models.CharField(max_length=4, choices=user_type_choices, default='USER')
    
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their user name
        return self.user_name

    def get_short_name(self):
        # The user is identified by their user name
        return self.user_name

    def __str__(self):              # __unicode__ on Python 2
        return self.user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Position(models.Model):
    job_name = models.CharField(max_length=20,unique=True)
    info = models.TextField()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default='2016-01-01')
    end_date = models.DateField(auto_now=False, auto_now_add=False, default='2016-01-01')
    location_city = models.CharField(max_length=50)
    location_state = models.CharField(max_length=20, choices=states, default='WA')
    parent = models.ForeignKey(User, blank=True, null=True, related_name='parent')
    child = models.ForeignKey(User, blank=True, null=True, verbose_name='Volunteer', related_name='child')
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    email = models.EmailField(
        max_length=255,
        verbose_name='Contact Email',
    )
	
    objects = UserManager()

    USERNAME_FIELD = 'job_name'
    REQUIRED_FIELDS = []