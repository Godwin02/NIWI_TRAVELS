from django import forms



class CustomFileInput(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        accept = "application/pdf, image/jpeg, image/jpg, image/png"
        attrs["accept"] = accept
        context = super().get_context(name, value, attrs)
        return context
    
    
class PassengerInfoForm(forms.Form):
    passenger_name = forms.CharField(
        max_length=100,
        label='Passenger Name',
        widget=forms.TextInput(attrs={'placeholder': 'Passenger Name'})
    )
    passenger_age = forms.IntegerField(
        label='Passenger Age',
        widget=forms.TextInput(attrs={'placeholder': 'Passenger Age'})
    )
    proof_of_id = forms.FileField(
        label='Proof of ID',
        help_text='Upload a PDF file',
        widget=CustomFileInput(attrs={'placeholder': 'Upload a PDF file'})
    )



    # You can add more fields as needed for your application.
