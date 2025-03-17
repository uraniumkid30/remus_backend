from django import forms
from . import models


class OrderAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Order
        fields = "__all__"


class SubOrderAdminForm(forms.ModelForm):
    # total = forms.DecimalField()
    # total_wait_time = forms.DecimalField()
    # order_number = forms.CharField()

    class Meta:
        model = models.Order
        fields = "__all__"
    readonly_fields = (
        "customer",
        "device",
        "table",
        # "total",
        # "total_wait_time",
        #"order_number",
        "order_note",
        "tax",
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
