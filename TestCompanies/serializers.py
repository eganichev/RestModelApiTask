from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from TestCompanies.models import Company, Office


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        exclude = ('company_owner', 'id')


class HeadquarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('city', 'postal_code', 'street')


class CompanySerializer(serializers.ModelSerializer):
    offices = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyWithHeadquarterSerializer(serializers.ModelSerializer):
    headquarter = SerializerMethodField()

    class Meta:
        model = Company
        fields = ('name', 'headquarter')

    def get_headquarter(self, comp):
        head_office = Office.objects.get(is_headquarter=True, company_owner=comp)
        return HeadquarterSerializer(head_office).data


class CompanyRentSerializer(serializers.ModelSerializer):
    summary_rent = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('name', 'summary_rent')

    def get_summary_rent(self, obj):
        return obj.offices.aggregate(summary_rent=Sum('monthly_rent'))
