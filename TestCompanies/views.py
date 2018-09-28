from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from TestCompanies.models import Company, Office
from TestCompanies.serializers import CompanySerializer, \
    CompanyWithHeadquarterSerializer, CompanyRentSerializer


class CompanyListViewSet(ReadOnlyModelViewSet):
    serializer_class = CompanyWithHeadquarterSerializer
    queryset = Company.objects.all()


class OfficesOfCompanyRetrieve(GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'name'


class ChangeHeadquarterViewSet(GenericViewSet, mixins.UpdateModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanyWithHeadquarterSerializer
    lookup_field = 'name'

    def partial_update(self, request, *args, **kwargs):
        name = self.kwargs['name']
        try:
            company = Company.objects.get(name=name)
            current_head = company.offices.get(is_headquarter=True)
            new_head = Office.objects.get(id=request.data['new_head_id'])
            current_head.is_headquarter = False
            new_head.is_headquarter = True
            current_head.save()
            new_head.save()
            return super().partial_update(request, args, kwargs)
        except (Company.DoesNotExist, Office.DoesNotExist):
            return NotFound("Company or offices does not exists")


class AllCompanyRentViewSet(ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyRentSerializer
