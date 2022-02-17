from django import forms

from stock_market_platform.crawling.models import NormalizedFieldTree


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


#  TODO maybe I will make it usable in the future
class FinancialStatementFieldInlineFormset(forms.BaseInlineFormSet):
    pass
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     normalized_field_maps = self.get_normalized_field_maps()
    #     for row in cleaned_data:
    #         normalized_field = self.match_source_field_to_normalized_field(
    #             row["name"],
    #             str(row["statement_type"]),
    #             normalized_field_maps
    #         )
    #         if normalized_field:
    #             row.update({"normalized_field": normalized_field})
    #     return cleaned_data

    @staticmethod
    def match_source_field_to_normalized_field(
        source_field, statement_type, normalized_field_maps
    ):
        source_field = source_field.lower()
        if source_field in normalized_field_maps[statement_type]:
            return normalized_field_maps[statement_type][source_field]

    @staticmethod
    def get_normalized_field_maps():
        output = {}

        for statement_type in ("income_statement", "balance_sheet", "cash_flow"):
            statement_fields = NormalizedFieldTree.objects.filter(
                statement_type=statement_type
            ).values_list("humanized_name", "name")
            values = {}
            for value, normalized_value in statement_fields:
                value = value.lower()
                values[value] = normalized_value
            output[statement_type] = values
        return output
