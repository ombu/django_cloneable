from datetime import date
from django.test import TestCase

from .models import ModelWithCustomPK
from .models import ModelWithFields
from .models import RelatedModel
from .models import ModelWithFK


class CloneableTests(TestCase):
    def test_cloning_generates_a_new_instance(self):
        i1 = ModelWithFields.objects.create(
            char='custom value',
            integer=23,
            date=date(2015, 12, 31))

        i2 = i1.clone()

        assert i2.pk is not None
        assert i1.pk != i2.pk
        assert i1.char == i2.char
        assert i1.integer == i2.integer
        assert i1.date == i2.date

    def test_must_provide_new_pk_if_its_custom_field(self):
        i1 = ModelWithCustomPK.objects.create(key='foo', value=42)
        i2 = i1.clone(attrs={'key': 'bar'})

        assert i2.pk == 'bar'
        assert i1.pk != i2.pk
        assert i2.value == 42

    def test_cloning_object_allows_overwriting_fk_reference(self):
        i1 = ModelWithFK.objects.create()
        i1.related = RelatedModel.objects.create()
        i1.save()

        i2 = i1.clone()
        i2.related = RelatedModel.objects.create()
        i2.save()
        assert i1.related != i2.related