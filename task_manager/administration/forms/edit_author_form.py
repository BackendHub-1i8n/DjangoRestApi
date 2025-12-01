from django import forms
from administration.models import Author  # Asegúrate de importar Author


class EditAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['nacionality', 'biography']

        widgets = {
            'biography': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter a brief biography for the author.',
                'class': 'textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-gray-700/50 text-light border-0'
            }),
            'nacionality': forms.TextInput(attrs={
                'placeholder': 'e.g., Bolivian, Mexican, Spanish, etc.',
                'class': 'input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-gray-700/50 text-light border-0'
            }),
        }
        labels = {
            'nacionality': 'Nationality',
            'biography': 'Biography',
        }

    def clean_nacionality(self):
        nacionality = self.cleaned_data.get('nacionality')
        if not nacionality.replace(" ", "").isalpha():
            raise forms.ValidationError("Nationality should only contain letters and spaces.")
        return nacionality.capitalize()