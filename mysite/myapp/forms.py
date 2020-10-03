import datetime
from django import forms

# for client registration
class clientRegForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=120)
    contactNumber = forms.CharField(max_length=15)
    pwd= forms.CharField(max_length=80)

# for client login
class clientLoginForm(forms.Form):
    email=forms.CharField(max_length = 80)
    pwd= forms.CharField(max_length=80)

#for student login
class studenLoginForm(forms.Form):
    email = forms.CharField(max_length=120)
    password = forms.CharField(max_length=50)

#for student registration
class studentRegForm(forms.Form):
    email = forms.CharField(max_length=120)
    name = forms.CharField(max_length=100)
    rollno = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    client = forms.CharField(max_length=50)

# for saving test detials
class saveTestDetails(forms.Form):
    testtitle = forms.CharField(max_length=100)
    testduration = forms.CharField(max_length=10)

#for submitting marks
class saveMarks(forms.Form):
    totalmarks = forms.CharField(max_length=20)

# for validating test ID
class testIdVal(forms.Form):
    test_id=forms.CharField(max_length = 250)
