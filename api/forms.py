from django import forms

# Form for letting user log in
class LoginForm(forms.Form):
    username = forms.CharField(label="Username ", required="true", max_length=100)
    password = forms.CharField(
        label="Password ", 
        max_length=100,
        required="true",
        # Adding a password widget for password 
        widget=forms.PasswordInput()
    )

# Form for letting user change password
class UpdatePassForm(forms.Form):
    username = forms.CharField(label="Username ", required="true", max_length=100)
    password = forms.CharField(
        label="New password ", 
        max_length=100,
        required="true",
        # Adding a password widget for password 
        widget=forms.PasswordInput()
    )

# Form for letting user change username 
class UpdateUserForm(forms.Form):
    current_username = forms.CharField(label="Username ", required="true", max_length=100)
    new_username = forms.CharField(
         
        max_length=100,
        required="true",
        label="New Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter new username"}),
        
    )


# Form for letting user sign up
class SignUpForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
    ]

    first_name = forms.CharField(label="First Name ", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name ", max_length=100, required=True)
    username = forms.CharField(label="Username ", max_length=100, required=True)
    email = forms.EmailField(label="Email ", required=True)
    date_of_birth = forms.DateField(
        label="Date Of Birth ",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    password = forms.CharField(
        label="Password ", required=True, max_length=100,
        widget=forms.PasswordInput()
    )
    user_type = forms.ChoiceField(label="Sign up as", choices=USER_TYPE_CHOICES, required=True)


