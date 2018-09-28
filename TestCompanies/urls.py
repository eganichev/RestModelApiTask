from rest_framework import routers
from TestCompanies.views import CompanyListViewSet, OfficesOfCompanyRetrieve, \
    ChangeHeadquarterViewSet, AllCompanyRentViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyListViewSet, base_name='company')
router.register(r'company_offices', OfficesOfCompanyRetrieve, base_name='company_offices')
router.register(r'change_headquarter', ChangeHeadquarterViewSet, base_name='change_headquarter')
router.register(r'all_rent', AllCompanyRentViewSet, base_name='all_rent')