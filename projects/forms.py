from django.forms import ModelForm
from django import forms
from .models import Project, Review, Tag

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'input'}),
            'demo_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Demo Link'}),
            'source_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Source Link'}),
            'image': forms.FileInput(attrs={'class': 'input', 'placeholder': 'Image'}),
        }

    #def __init__(self, *args, **kwargs):
        #super(ProjectForm, self).__init__(*args, **kwargs)

        #for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input'})

        #self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Title'})
        #self.fields['description'].widget.attrs.update({'class': 'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        widgets = {
            'value': forms.Select(attrs={'class': 'input'}),
            'body': forms.Textarea(attrs={'class': 'input'})
        }
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',
        }