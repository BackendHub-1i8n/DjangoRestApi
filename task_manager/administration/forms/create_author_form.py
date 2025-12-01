from django import forms
from administration.models import Author, Person


class CreateAuthorForm(forms.ModelForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(author_profile__isnull=True).order_by('first_name'),
        label='Select Person (Author Profile)',
        empty_label="--- Select a Person to be the Author ---",
        widget=forms.Select(attrs={
            'class': 'select w-full mt-1 block rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-gray-700/50 text-light border-0'
        })
    )

    class Meta:
        model = Author
        fields = ['person', 'nacionality', 'biography']  # Reordenamos para poner Person primero
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'person' and field_name != 'biography':
                field.widget.attrs.update({
                    'class': 'input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-gray-700/50 text-light border-0'
                })