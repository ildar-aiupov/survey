from django import forms

from main.models import Answer


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if "variants" in kwargs:
            variants = kwargs.pop("variants")
            super().__init__(*args, **kwargs)
            self.fields["chosen_variant"] = forms.ModelChoiceField(
                queryset=variants, widget=forms.RadioSelect()
            )
        else:
            super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ["chosen_variant"]
