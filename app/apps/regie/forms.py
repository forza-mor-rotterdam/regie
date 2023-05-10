import base64

from django import forms
from django.core.files.storage import default_storage

BEHANDEL_OPTIES = (
    (
        "ja",
        "Ja",
        "Tekst bij Ja",
        "afgehandeld",
    ),
    (
        "in_behandeling",
        "Nog niet, de melding is in behandeling.",
        "Tekst bij In behandeling",
        None,
    ),
    (
        "nee",
        "Nee, het probleem kan niet worden opgelost.",
        "Tekst bij Nee",
        "geannuleerd",
    ),
)

BEHANDEL_STATUS = {bo[0]: bo[3] for bo in BEHANDEL_OPTIES}


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


class LoginForm(forms.Form):
    username = forms.CharField(label="Personeelsnummer", widget=forms.TextInput())
    password = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput())


class RadioSelect(forms.RadioSelect):
    option_template_name = "widgets/radio_option.html"


class MeldingAfhandelenForm(forms.Form):
    status = forms.ChoiceField(
        widget=RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        label="Is het probleem opgelost?",
        choices=[[x[0], x[1]] for x in BEHANDEL_OPTIES],
    )

    omschrijving_extern = forms.CharField(
        label="Bericht voor de melder",
        help_text="Je kunt deze tekst aanpassen of eigen tekst toevoegen.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "message",
                "rows": "4",
                "data-meldingbehandelformulier-target": "externalText",
            }
        ),
        required=True,
    )

    bijlagen = forms.FileField(
        widget=forms.widgets.FileInput(
            attrs={
                "accept": ".jpg, .jpeg, .png, .heic",
                "data-action": "change->bijlagen#updateImageDisplay",
            }
        ),
        label="Foto's",
        required=False,
    )

    omschrijving_intern = forms.CharField(
        label="Interne opmerking",
        help_text="Je kunt deze tekst aanpassen of eigen tekst toevoegen.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "information",
                "rows": "4",
                "data-meldingbehandelformulier-target": "internalText",
            }
        ),
        required=False,
    )

    def _to_base64(self, file):
        binary_file = default_storage.open(file)
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode("utf-8")
        return base64_message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def terugsturen(self, data):
    #     if data.get("afhandel_reden") == ""
