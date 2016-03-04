from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.widgets import CheckboxSelectMultiple
from lists.models import User, Position, Skill

class UserUpdateProfile(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    skill = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'location_city', 'location_state', 'age', 'bio')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserUpdateProfile, self).save(commit=False)
        
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           user.skill.clear()
           for skill in self.cleaned_data['skill']:
               user.skill.add(skill)
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
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ('user_name', 'email', 'date_of_birth', 'location_city', 'location_state', 'age', 'bio')
        
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
    class Meta:
        model = Position
        fields = ('job_name', 'info', 'start_date', 'end_date', 'location_city', 'location_state')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(JobCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating orgs. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'user_name', 'location_city', 'location_state', 'age', 'bio', 'user_type', 'is_active', 'is_admin')

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
        fields = ('job_name', 'info', 'start_date', 'end_date', 'location_city', 'location_state', 'is_active', 'is_admin')

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
        ('Personal info', {'fields': ('date_of_birth','location_city', 'location_state', 'age', 'bio', 'skill')}),
        ('Permissions', {'fields': ('user_type', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2','user_name', 'location_city', 'location_state', 'age', 'user_type','bio', 'skill')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
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
        (None, {'fields': ('job_name', 'info')}),
        ('Personal info', {'fields': ('location_city', 'location_state', 'start_date', 'end_date', 'parent', 'child')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('job_name', 'start_date', 'end_date', 'location_city', 'location_state', 'info')}
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