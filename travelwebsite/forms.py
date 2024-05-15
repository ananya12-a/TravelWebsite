from django import forms

from django.contrib.auth.models import User
from travelwebsite.models import Profile, Trip, Activity
from django.contrib.auth import authenticate
from django.forms import ModelForm
import csv

LIST_OF_DICT = []
MAX_UPLOAD_SIZE = 2500000


csv_file_path = 'travelwebsite/airports.csv'
data = dict() #(code:name)

# Read the CSV file and extract data from the desired columns
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        airport_name = row['Goroka Airport']  # Replace 'airport_name' with the actual column name for airport names
        airport_code = row['GKA']  # Replace 'airport_code' with the actual column name for airport codes
        data[airport_code] = airport_name
# print(list(data.keys()))
        
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'border w-full text-base px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-600',
            'placeholder': 'Username',
            'required': True})
    )
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={
            'class': 'border w-full text-base px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-600',
            'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password! Try again!")
        return cleaned_data
    
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('picture',)
#         # widgets settings: changes the id
#         widgets = {
#             # can specify the dimensions of the text area
#             # 'bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':'3'}), 
#             'picture': forms.FileInput(attrs={'id':'id_profile_picture'})
#         }
#         labels = {
#             # 'bio':"",
#             'picture': "Upload image"
#         }
    
#     def clean_picture(self):
#         picture = self.cleaned_data['picture']
#         if not picture or not hasattr(picture, 'content_type'):
#             raise forms.ValidationError('You must upload a picture')
#         if not picture.content_type or not picture.content_type.startswith('image'):
#             raise forms.ValidationError('File type is not image')
#         if picture.size > MAX_UPLOAD_SIZE:
#             raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
#         return picture

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-400 py-1 px-2',
            'placeholder': 'First name'}) 
    )
    last_name  = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-400 py-1 px-2',
            'placeholder': 'Last name'}) 
    )

    username   = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full',
            'placeholder': 'Username'}) 
    )

    password  = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full',
            'placeholder': 'Password'})
    )
    confirm_password  = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full',
            'placeholder': 'Confirm Password'})
    )
    email      = forms.CharField(
        max_length=50,
        widget = forms.EmailInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full',
            'placeholder': 'Email'})
    )
   

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match! Try again!")

        #print("REGISTRATIONFORM cleaned_data", cleaned_data)
        # We must return the cleaned data we got from our parent.
        #LIST_OF_DICT.append(cleaned_data)
        print("cleaned_data", cleaned_data)
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
    
class DateInput(forms.DateInput):
    input_type = 'date'
    
class TripForm(forms.Form):    
    # flights  = forms.CharField(max_length=200,
    #                              label='Flights')
    
    start_date = forms.DateTimeField(
        widget=DateInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-2/3 rounded-md my-3', 
            'type': 'date'
        }), 
        label='Start Date'
    )

    end_date = forms.DateTimeField(
        widget=DateInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-2/3 rounded-md my-3', 
            'type': 'date'
        }), 
        label='End Date'
    )
    
    origin_airport = forms.ChoiceField(choices=data.items(), initial='EWR')

    destination_airport = forms.ChoiceField(choices=data.items(), initial='EWR')

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-400 w-2/3 text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-3',
            'required': True})
    )

    print("location", location)

    cost = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="cost",
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-400 w-2/3 text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-2',
            'required': True})
    )

    print("cost", cost)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        origin_airport = cleaned_data.get('origin_airport')
        destination_airport = cleaned_data.get('destination_airport')
        location = cleaned_data.get('location')
        cost = cleaned_data.get('cost')

        print("------ cleaned_data", cleaned_data)

        return cleaned_data
    # def clean_picture(self):
    #     picture = self.cleaned_data['picture']
    #     if not picture or not hasattr(picture, 'content_type'):
    #         raise forms.ValidationError('You must upload a picture')
    #     if not picture.content_type or not picture.content_type.startswith('image'):
    #         raise forms.ValidationError('File type is not image')
    #     if picture.size > MAX_UPLOAD_SIZE:
    #         raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
    #     return picture

class EditForm(forms.Form):
    start_date = forms.DateTimeField(
        widget=DateInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3', 
            'type': 'date'
        }), 
        label='Start Date'
    )

    end_date = forms.DateTimeField(
        widget=DateInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3', 
            'type': 'date'
        }), 
        label='End Date'
    )
    
    origin_airport = forms.ChoiceField(choices=data.items(), initial='EWR')

    destination_airport = forms.ChoiceField(choices=data.items(), initial='EWR')

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-600 w-full text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-3',
            'required': True})
    )

    print("location", location)

    cost = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="cost",
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-600 w-full text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-2',
            'required': True})
    )

    print("cost", cost)


    class Meta:
        model = Trip
        exclude = (
            'person',
            'updated_by',
        )
        widgets = {
            'start_date': forms.DateTimeField(widget=DateInput, label='Start Date'),
            'end_date': forms.DateTimeField(widget=DateInput,label='End Date'),
            'location': forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'class': 'border border-gray-600 w-1/6 text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-3',
                        'required': True})
                ),
            # 'flights': forms.CharField(max_length=200, label='Flights'),
            'cost': forms.DecimalField(
                    max_digits=10, 
                    decimal_places=2, 
                    label="cost",
                    widget=forms.NumberInput(attrs={
                        'class': 'border border-gray-600 w-1/6 text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-2',
                        'required': True})
                ),
        }

class ActivityForm(forms.Form):
    #activity_type  = forms.ChoiceField(choices=Activity.choices, initial=Activity.SKIING_SNOWBOARDING)
    
    activity_type = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3'
            }) 
    )
    # start_date = forms.DateField(label='Start Date')
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3',
            'placeholder': 'Start Time',
            'type': 'time'  # Ensure the input type is set to 'time'
        })
    )

    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3',
            'placeholder': 'End Time',
            'type': 'time'  # Ensure the input type is set to 'time'
        })
    )

    date = forms.DateTimeField(
        widget=DateInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full rounded-md my-3', 
            'type': 'date'
        }), 
        label='Date'
    )

    """ datetime_local = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'border border-gray-400 py-1 px-2 w-full',
            'type': 'datetime-local',
            'placeholder': 'Select Date and Time',
            'input_type': 'datetime-local'  # Ensure the input type is set to 'datetime-local'
        })
    ) """

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-600 w-full text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-3',
            'required': True})
    )

    cost = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="cost",
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-600 w-full text-sm px-2 py-1 focus:outline-none focus:ring-0 focus:border-gray-700 rounded-md my-2',
            'required': True})
    )


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        #print("REGISTRATIONFORM cleaned_data", cleaned_data)
        # We must return the cleaned data we got from our parent.
        #LIST_OF_DICT.append(cleaned_data)
        # print("00000000000 cleaned_data", cleaned_data)
        # print("cleaned_data[start_date]", cleaned_data.get('start_date'))
        return cleaned_data