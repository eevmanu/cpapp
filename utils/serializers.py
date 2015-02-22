from rest_framework import serializers


class CPBaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super(CPBaseSerializer, self).__init__(*args, **kwargs)

        if fields:
            existing = set(self.fields.keys())
            allowed = set(fields)
            # Intersect lists
            to_pop = list(existing - allowed)
            for field_name in to_pop:
                self.fields.pop(field_name)

        if exclude:
            existing = set(self.fields.keys())
            disallowed = set(exclude)
            # Substract list from list
            to_pop = list(existing & disallowed)
            for field_name in disallowed:
                self.fields.pop(field_name)
