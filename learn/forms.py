from django.forms import ModelForm
from .models import BookImport

class BookImportForm(ModelForm):
    class Meta:
        model = BookImport
        fields = ('csv_file',)