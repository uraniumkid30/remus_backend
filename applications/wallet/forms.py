from django import forms
from . import models


class WalletForm(forms.Form):
    amount = forms.FloatField(label="Amount")
    card_number = forms.CharField(
        label="Card Number",
        widget=forms.TextInput(attrs={"placeholder": "4084084084084081"}),
    )
    cvv = forms.IntegerField(
        label="CVV", widget=forms.TextInput(attrs={"placeholder": "408"})
    )
    expiry_month = forms.IntegerField(
        widget=forms.TextInput(attrs={"placeholder": "12"})
    )
    expiry_year = forms.IntegerField(
        widget=forms.TextInput(attrs={"placeholder": "25"})
    )


class WalletAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Wallet
        fields = "__all__"


class SubWalletAdminForm(forms.ModelForm):

    class Meta:
        model = models.Wallet
        fields = "__all__"
    readonly_fields = (
        "user",
        "restaurant",
        "amount",
        "bonus_balance",
        "status",
        "currency",
        "overdraft_limit",
        "overdraft",
        "allow_overdraft",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            for _field in self.readonly_fields:
                try:
                    self.fields[_field].required = False
                    self.fields[_field].disabled = True
                except:
                    pass
