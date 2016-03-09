from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from lists.models import User, Position, Skill, states
from django.forms.fields import DateField, CharField, EmailField
import datetime

birth_years = ('1920', '1921', '1922', '1923', '1924', '1925','1926', '1927', '1928', '1929', 
    '1930', '1931', '1932', '1933', '1934', '1935','1936', '1937', '1938', '1939',
    '1940', '1941', '1942', '1943', '1944', '1945','1946', '1947', '1948', '1949',
    '1950', '1951', '1952', '1953', '1954', '1955','1956', '1957', '1958', '1959',
    '1960', '1961', '1962', '1963', '1964', '1965','1966', '1967', '1968', '1969',
    '1970', '1971', '1972', '1973', '1974', '1975','1976', '1977', '1978', '1979',
    '1980', '1981', '1982', '1983', '1984', '1985','1986', '1987', '1988', '1989',
    '1990', '1991', '1992', '1993', '1994', '1995','1996', '1997', '1998', '1999',
    '2000', '2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009',
    '2010', '2011', '2012', '2013', '2014', '2015','2016',   
)

class UserUpdateProfile(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    date_of_birth = DateField(widget = SelectDateWidget(years=birth_years))
    skill = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ('email', 'location_city', 'location_state', 'bio', 'age')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserUpdateProfile, self).save(commit=False)
        
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           user.skills.clear()
           for skill in self.cleaned_data['skill']:
               user.skills.add(skill)
        self.save_m2m = save_m2m        
        
        if commit:
            user.save()
            self.save_m2m()
        return user

class OrgUpdateProfile(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    class Meta:
        model = User
        fields = ('email', 'location_city', 'location_state', 'bio')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(OrgUpdateProfile, self).save(commit=False)
        if commit:
            user.save()
        return user		

class FillPosition(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    class Meta:
        model = Position
        fields = ('job_name', 'child')   

    def save(self, commit=True):
        # Save the provided password in hashed format
        jn = self.cleaned_data['job_name']
        ch = self.cleaned_data['child']
        user = Position.objects.get(job_name=jn)
        user.child = ch
        if commit:
            user.save()
        return user	

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    date_of_birth = DateField(widget = SelectDateWidget(years=birth_years))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = User
        fields = ('user_name', 'email', 'location_city', 'location_state', 'bio', 'age')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.date_of_birth = self.cleaned_data['date_of_birth']
        
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           user.skills.clear()
           for skill in self.cleaned_data['skills']:
               user.skills.add(skill)
        self.save_m2m = save_m2m
        
        if commit:
            user.save()
            self.save_m2m()
        return user

class OrgCreationForm(forms.ModelForm):
    """A form for creating new orgs. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_name', 'email', 'location_city', 'location_state', 'bio')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(OrgCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = 'ORG'
        if commit:
            user.save()
        return user

class JobCreationForm(forms.ModelForm):
    """A form for creating new positions. Includes all the required
    fields, plus a repeated password."""
    start_date = DateField(widget = SelectDateWidget())
    end_date = DateField(widget = SelectDateWidget())
    skills_required = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Position
        fields = ('job_name', 'info', 'location_city', 'location_state', 'email')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(JobCreationForm, self).save(commit=False)
        user.start_date = self.cleaned_data['start_date'] 	
        user.end_date = self.cleaned_data['end_date'] 
		
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           user.skills.clear()
           for skill in self.cleaned_data['skills_required']:
               user.skills.add(skill)
        self.save_m2m = save_m2m
		
        if commit:
            user.save()
            self.save_m2m()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating orgs. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'user_name', 'location_city', 'location_state', 'age', 'bio', 'skills', 'user_type', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class JobChangeForm(forms.ModelForm):
    """A form for updating jobs. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = Position
        fields = ('job_name', 'email', 'info', 'start_date', 'end_date', 'location_city', 'location_state', 'is_active', 'is_admin', 'skills')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_name', 'email', 'location_city', 'user_type', 'is_admin')
    list_filter = ('user_type',)
    fieldsets = (
        (None, {'fields': ('email', 'password','user_name')}),
        ('Personal info', {'fields': ('date_of_birth','location_city', 'location_state', 'age', 'bio', 'skills')}),
        ('Permissions', {'fields': ('user_type', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2','user_name', 'location_city', 'location_state', 'age', 'user_type','bio', 'skills')}
        ),
    )
    search_fields = ('email',)
    ordering = ('user_type',)
    filter_horizontal = ()

class JobAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = JobChangeForm
    add_form = JobCreationForm

    # The fields to be used in displaying the Position model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('job_name', 'start_date', 'end_date', 'location_city', 'location_state', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('job_name', 'info', 'email')}),
        ('Personal info', {'fields': ('location_city', 'location_state', 'start_date', 'end_date', 'parent', 'child', 'skills')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('job_name', 'email', 'start_date', 'end_date', 'location_city', 'location_state', 'info', 'skills')}
        ),
    )
    search_fields = ('job_name',)
    ordering = ('job_name',)
    filter_horizontal = ()

# Now register 
admin.site.register(Skill)
admin.site.register(User, UserAdmin)
admin.site.register(Position, JobAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)