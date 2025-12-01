from django import forms
from books.models import Book
from administration.models import Author

# Clase base para el estilo de los inputs
INPUT_CLASSES = 'mt-1 block w-full rounded-md shadow-sm focus:border-primary focus:ring-primary bg-gray-700/50 text-white border border-gray-700 p-3'


class BookForm(forms.ModelForm):
    # Definición explícita para el ManyToManyField con estilos
    author = forms.ModelMultipleChoiceField(
        queryset=Author.objects.select_related('person').order_by('person__last_name'),
        widget=forms.SelectMultiple(attrs={
            'class': INPUT_CLASSES,
            'size': 6,  # Muestra 6 líneas de opciones de autores
        }),
        required=True,
        label="Authors"
    )

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'pages', 'amount', 'language', 'published_date', 'author']

        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Book Title'}),
            'isbn': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'ISBN (13 digits)'}),
            'pages': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Number of pages'}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Initial stock amount'}),
            'language': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., Spanish, English'}),
            # Usar type='date' para un control de fecha nativo en HTML5
            'published_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
        }