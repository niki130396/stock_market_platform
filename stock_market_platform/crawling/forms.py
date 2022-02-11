from django import forms


class NormalizedFieldTreeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["name"] = self.convert_to_snake_case(
            cleaned_data["humanized_name"]
        )
        return cleaned_data

    @staticmethod
    def convert_to_snake_case(s: str):
        to_replace = {",": "", "&": "and", "'": ""}
        for k, v in to_replace.items():
            s = s.replace(k, v)
        s = s.lower().replace(" ", "_")
        return s
