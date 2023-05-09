from django import forms

BEHANDEL_OPTIES = (
    ("ja", "Ja"),
    ("in_behandeling", "Nog niet, de melding is in behandeling."),
    ("nee", "Nee, het probleem kan niet worden opgelost."),
)


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
    afhandel_reden = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        label="Is het probleem opgelost?",
        choices=(BEHANDEL_OPTIES),
    )

    tekst_extern = forms.CharField(
        label="Bericht voor de melder",
        help_text="Je kunt deze tekst aanpassen of eigen tekst toevoegen.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "message",
                "rows": "4",
                "data-incidentHandleForm-target": "externalText",
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

    tekst_intern = forms.CharField(
        label="Interne opmerking",
        help_text="Je kunt deze tekst aanpassen of eigen tekst toevoegen.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "information",
                "rows": "4",
                "data-incidentHandleForm-target": "internalText",
            }
        ),
        required=False,
    )

    # def __init__(self, *args, **kwargs):
    # afhandel_reden_opties = kwargs.pop("afhandel_reden_opties", None)
    # afhandel_reden_opties = (
    #     ("ja", "Ja"),
    #     ("in_behandeling", "Nog niet, de melding is in behandeling."),
    #     ("nee", "Nee, het probleem kan niet worden opgelost."),
    # )
    # super().__init__(*args, **kwargs)
    # self.fields["afhandel_reden"].choices = afhandel_reden_opties

    # def terugsturen(self, data):
    #     if data.get("afhandel_reden") == ""


class HandleForm(forms.Form):

    handle_choice = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
                "data-action": "change->handleForm#onHandledChange",
                "data-request-target": "handledField",
            }
        ),
        label="Is het probleem opgelost?",
        choices=(
            ("ja", "Ja"),
            ("in_behandeling", "Nog niet, de melding is in behandeling."),
            ("nee", "Nee, het probleem kan niet worden opgelost."),
        ),
        required=True,
    )

    # handle_choice = forms.ChoiceField(
    #     label="Is het probleem opgelost?",
    #     widget=RadioSelect(attrs={"class": "list--form-check-input"}),
    #     choices=[[x, HANDLED_OPTIONS[x][1]] for x in range(len(HANDLED_OPTIONS))],
    #     initial=0,
    # )

    def __init__(self, *args, **kwargs):
        # handled_type = kwargs.pop("handled_type", None)
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        # if handled_type == "handled":
        #     self.fields["handle_choice"].widget = forms.HiddenInput()
        #     self.fields["external_text"].initial = HANDLED_OPTIONS[0][2]
        # else:
        #     self.fields["handle_choice"].choices = [
        #         [x, HANDLED_OPTIONS[x][1]]
        #         for x in range(len(HANDLED_OPTIONS))
        #         if HANDLED_OPTIONS[x][0] == "N"
        #     ]

        # if self.data.get("handle_choice", False) == "3":
        #     self.fields["external_text"].widget = forms.HiddenInput()
        #     self.fields["external_text"].required = False
