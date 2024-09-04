from django import forms
class CreateForm(forms.Form):
    title = forms.CharField(label="Title",max_length=100, required=True, error_messages={
        "required": "This field is required"
    })
    description = forms.CharField(label="Description",max_length=100, required=True, error_messages={
        "required": "This field is required"
    })
    starting_bid = forms.FloatField(label="Starting bid",required=True, error_messages={
        "required": "This field is required"
    })
    image_url = forms.URLField(label="Image url(optional)",max_length=1500, required=False, error_messages={
        "required": "This field is required"
    })

class BidForm(forms.Form):
    bid = forms.FloatField(required=True, error_messages={
        "required": "This field is required"
    })