from django import forms


class FilterForm(forms.Form):

    begraafplaats = forms.MultipleChoiceField(
        label="Locatie",
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "list--form-check-input",
                "hideLabel": True,
            }
        ),
        choices=[],
        required=False,
    )

    ordering = forms.CharField(
        widget=forms.HiddenInput(),
        initial="aangemaakt_op",
        required=False,
    )

    offset = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-check-input",
                "hideLabel": True,
            }
        ),
        required=False,
    )

    limit = forms.CharField(
        widget=forms.HiddenInput,
        initial="10",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        offset_options = kwargs.pop("offset_options", None)
        locatie_opties = kwargs.pop("locatie_opties", None)
        super().__init__(*args, **kwargs)
        self.fields["offset"].choices = offset_options
        self.fields["begraafplaats"].choices = locatie_opties
