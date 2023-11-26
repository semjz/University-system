from django.test import TestCase
from management.factories import StudentFactory
from management.models import Student
from management.filtersets import StudentFilterSet


class StudentFilterSetTest(TestCase):
    def setUp(self):

        StudentFactory.create(name="Test 1")
        StudentFactory.create(name="Test 2")
        StudentFactory.create(name="Other name")

    def test_name_filter(self):
        data = {'name': 'Test'}
        queryset = Student.objects.all()
        filter_set = StudentFilterSet(data, queryset=queryset)
        filtered_queryset = filter_set.qs

        self.assertEqual(filtered_queryset.count(), 2)
        self.assertEqual(filtered_queryset.first().name, 'Test 1')
        self.assertEqual(filtered_queryset.last().name, 'Test 2')