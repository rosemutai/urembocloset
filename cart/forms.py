from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        widget=forms.NumberInput(attrs={
            "class":(
                "w-14 h-8 border border-navy/15 rounded text-navy outline-0 focus:border-navy/55 "
                "hover:border-transparent hover:shadow hover:shadow-navy/15 hover:transition-all "
                "duration-150 focus:shadow-transparent p-1"
            ),
            "min": 1
        })
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
