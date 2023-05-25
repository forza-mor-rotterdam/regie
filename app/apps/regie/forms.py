from django import forms

BEHANDEL_OPTIES = (
    (
        "ja",
        "Ja",
        "We zijn met uw melding aan de slag gegaan en hebben het probleem opgelost.",
        "afgehandeld",
        "opgelost",
    ),
    (
        "in_behandeling",
        "Nog niet, de melding is in behandeling.",
        "We zijn met uw melding aan de slag gegaan maar deze kan niet direct worden opgelost. Want...",
        None,
        None,
    ),
    (
        "nee",
        "Nee, het probleem kan niet worden opgelost.",
        "We zijn met uw melding aan de slag gegaan, maar konden het probleem helaas niet oplossen. Want...",
        "afgehandeld",
        None,
    ),
)

BEHANDEL_STATUS = {bo[0]: bo[3] for bo in BEHANDEL_OPTIES}
BEHANDEL_RESOLUTIE = {bo[0]: bo[4] for bo in BEHANDEL_OPTIES}


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


class InformatieToevoegenForm(forms.Form):
    opmerking = forms.CharField(
        label="Voeg een opmerking toe",
        widget=forms.Textarea(
            attrs={"class": "form-control", "data-testid": "information", "rows": "4"}
        ),
        required=False,
    )

    bijlagen_extra = forms.FileField(
        widget=forms.widgets.FileInput(
            attrs={
                "accept": ".jpg, .jpeg, .png, .heic",
                "data-action": "change->bijlagen#updateImageDisplay",
            }
        ),
        label="Voeg één of meerdere foto's toe",
        required=False,
    )


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
        required=False,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def terugsturen(self, data):
    #     if data.get("afhandel_reden") == ""
