from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from api.models import *
from api.serializers import *

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'employees': reverse('employees', request=request, format=format),
        'departments': reverse('departments', request=request, format=format),
        'customers': reverse('customers', request=request, format=format),
        'orders': reverse('orders', request=request, format=format),
        'computers': reverse('computers', request=request, format=format)
    })

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
  queryset = Department.objects.all()
  serializer_class = DepartmentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  http_method_names = ['get', 'post', 'put']

  def get_queryset(self):
    query_set = self.queryset
    print('query params', self.request.query_params)

    # search all parameters of each customer based on the params provided
    keyword = self.request.query_params.get('q')
    if keyword is not None:
        query_set = query_set.filter(Q(firstName__icontains=keyword) | Q(lastName__icontains=keyword) | Q(street_address__icontains=keyword) | Q(city__icontains=keyword) | Q(state__icontains=keyword) | Q(zipcode__icontains=keyword) | Q(phone_number__icontains=keyword))

    return query_set


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        query_set = self.queryset
        print('query params', self.request.query_params)

        # search all parameters of each customer based on the params provided
        keyword = self.request.query_params.get('completed')
        if keyword == 'True' or keyword == 'true':
            query_set = query_set.exclude(payment_type__isnull=True)
        elif keyword == 'False' or keyword == 'false':
            query_set = query_set.exclude(payment_type__isnull=False)
        else:
          pass

        return query_set


class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer


class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer