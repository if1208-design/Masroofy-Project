from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['student', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError("Amount is required!")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than ZERO!")
        
        return amount