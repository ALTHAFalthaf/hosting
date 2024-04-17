from django import forms

class VaccinePurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class CompletePurchaseForm(forms.Form):
    confirm_purchase = forms.BooleanField(required=True)


from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16, required=True)
    expiry_month = forms.CharField(label='Expiry Month', max_length=2, required=True)
    expiry_year = forms.CharField(label='Expiry Year', max_length=4, required=True)
    cvv = forms.CharField(label='CVV', max_length=3, required=True)
