import json
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from extras.models import Address, PaymentType
from orders.models import Delivery, Order, OrderReview
from products.models import Cart, CartItem, Meal
from rest_framework.authtoken.models import Token
from user_roles.models import Admin, Customer, DeliveryOperator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from .serializers import DeliverySerializer, OrderReviewSerializer, OrderSerializer, SemiCompleteDeliverySerializer, SimpleDeliverySerializer ,SimpleOrderSerializer, MyOrderDeliverySerializer
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

@api_view(['POST'])
def submit_order(request):
    try:
        token = request.headers['Authorization']
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        # Those Are The Address The Customer Chooses
        order_lang   = data['order_lang']
        order_lat = data['order_lat']
        order_address = Address.objects.get(id=int(data['address_id'])) 
    except Exception as e:
        return Response({'message' : 'please pass location details'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        cart ,created = Cart.objects.get_or_create(cart_owner= customer)
        order = Order.objects.create(ordered_by=customer)
        bill = cart.get_customer_total_price()
        order.bill = bill
        order.save()
    except Exception as e:
        raise PermissionDenied
    try:
        _payment = int(data['payment_type'])
        order_note = data['order_note']
        order.order_note = order_note
        if _payment == 0:
            order.pay_home = True        
        else:
            payment_type  = PaymentType.objects.get(payment_id=data['payment_id'])
            order.payment_type = payment_type
        delivery, created = Delivery.objects.get_or_create(order=order)
        delivery.save()
        order.lang = order_lang   
        order.lat = order_lat
        order.order_address=order_address
        order.delivery = delivery        
        order.save()  
        points = 0
        for cart_item in cart.cart_items.all():
            points += cart_item.meal.meal_points
            cart_item.meal.meal_order_times += cart_item.quantity
            order.cart_items.add(cart_item)
            cart.cart_items.remove(cart_item)
            cart_item.meal.save()
        cart.save()
        order.points = points
        order.save()
        delivery.save()
    except Exception as e:
        return Response({'message':'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message' : 'order submitted successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def submit_single_order(request):
    try:    
        token = request.headers['Authorization']
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        # Those Are The Address The Customer Chooses
        order_lang   = data['order_lang']
        order_lat = data['order_lat']
        order_address = Address.objects.get(id=int(data['address_id'])) 
    except Exception as e:
        return Response({'message' : 'please pass location details'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        cart,created = Cart.objects.get_or_create(cart_owner=customer)
        cart.save()
    except Exception as e:
        raise PermissionDenied
    try:
        order_note = data['order_note']
        try:
            cart_item, created =  CartItem.objects.get_or_create(meal=Meal.objects.get(meal_id = data['meal_id']), cart_item_owner=customer)
            if cart_item in cart.cart_items.all():
                cart.cart_items.remove(cart_item)
                cart.save()
        except Exception as e:
            return Response({'message' : 'Please Pass Valid id'}, status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(
            ordered_by = customer, order_note = order_note,
            lang=order_lang , lat=order_lat,
            order_address=order_address
        )
        order.cart_items.add(cart_item)
        order.save()
        _payment = int(data['payment_type'])
        if _payment == 0:
            order.pay_home = True
        else:
            payment_type  = PaymentType.objects.get(payment_id=data['payment_id'])
            order.payment_type = payment_type
        order.save()
        delivery, created = Delivery.objects.get_or_create(order=order)
        delivery.save()
        order.delivery= delivery
        order.bill = cart_item.get_customer_meal_item_total_price()
        order.points = cart_item.meal.meal_points
        cart_item.meal.meal_order_times += cart_item.quantity
        order.save()
        cart_item.meal.save()

    except Exception as e:
        return Response({'message':'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message' : 'order submitted successfully'}, status=status.HTTP_201_CREATED)




class UnoccupiedDeliveries(GenericViewSet):
    def list(self, request):
        queryset = Delivery.objects.filter(is_delivered=False, is_being_delivered=False, delivery_report="Some Problem Occured", delivery_problem_report_choice="")
        page = self.paginate_queryset(queryset)
        serializer = SemiCompleteDeliverySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    
class MyDeliveries(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
        except ObjectDoesNotExist:
            raise PermissionDenied
        queryset = Delivery.objects.filter(delivery_operator=delivery_operator)
        page = self.paginate_queryset(queryset)
        serializer = SemiCompleteDeliverySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)




class MyOrders(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
        except ObjectDoesNotExist:
            raise PermissionDenied
        queryset = Delivery.objects.filter(Q(order__ordered_by=customer))     
        page = self.paginate_queryset(queryset)
        serializer = MyOrderDeliverySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)



class OrderRetrieveView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            token = request.headers['Authorization']
        except KeyError:
            raise PermissionDenied
        try:
            delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user) 
        except ObjectDoesNotExist:
            raise PermissionDenied
        try:
            order_id = data['order_id']
        except MultiValueDictKeyError:
            return Response({'message' : 'Please Pass Order Id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = OrderSerializer(Order.objects.get(order_id=order_id)).data
            return Response(order)
        except ObjectDoesNotExist:
            return Response({'message':'wrong order id'}, status= status.HTTP_404_NOT_FOUND)


 


class AdminOrderRetrieveView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user) 
        except KeyError:
            raise PermissionDenied
        try:
            order_id = request.POST['order_id']
            order = OrderSerializer(Order.objects.get(id=order_id)).data
            return Response(order)
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Order Id'})


class CustomerOrderRetrieveView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            raise PermissionDenied
        try:
            order_id = request.POST['order_id']
            order = OrderSerializer(Order.objects.get(id=order_id)).data
            return Response(order)
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Order Id'})



class DeliveryRetrieveView(RetrieveAPIView):
    def get(self, request,delivery_id, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e :
            raise PermissionDenied
        try:
            delivery = Delivery.objects.get(delivery_id=delivery_id)
            delivery_serialized = DeliverySerializer(delivery).data
            order = OrderBackup.objects.get(order=Order.objects.get(delivery=delivery)) 
            order_serialized = OrderBackupSerializer(order).data
            return JsonResponse({
                "delivery" : delivery_serialized,
                "order_backup" : order_serialized,
            })   
        except Exception as e:
           return Response({'message' : 'Please Pass Valid Delivery Id'} ,status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def start_delivery(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user) 
        if delivery_operator.delivering:
            return JsonResponse({'message' : 'Delivery Operator Is Delivering The Order'})
    except ObjectDoesNotExist:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        delivery_id = data['delivery_id']
    except Exception as e :
        return JsonResponse({'message' : 'Please Pass Delivery Id'})
    try:
        delivery = Delivery.objects.get(delivery_id=delivery_id)
        delivery.is_being_delivered = True
        delivery.delivery_operator = delivery_operator
        delivery.save()
        delivery_operator.delivering = True
        delivery_operator.save()
        return JsonResponse({'message' : 'started delivery session'})
    except ObjectDoesNotExist:
        return Response({'message':'wrong order id'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def end_delivery(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user) 
    except ObjectDoesNotExist:
        raise PermissionDenied
    data = json.loads(request.body)
    try:
        delivery_id = data['delivery_id']
        delivery_report = data['delivery_report']
    except Exception as e:
        return Response({'message' : 'Please Pass Required Info'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        delivery = Delivery.objects.get(delivery_id=delivery_id)
        if delivery_report == 'success':
            print('in')
            delivery_recieved_money = int(data['recieved_money'])
            delivery_operator.Deliveries.add(delivery)
            delivery_operator.save()
            delivery.is_delivered = True
            delivery.is_being_delivered = False
            delivery_operator.delivering = False
            delivery.order.ordered_by.points += delivery.order.points
            delivery.delivery_report = "SUCCESS"
            delivery.save()
            delivery.order.ordered_by.save()
            delivery.order.save()
            delivery_operator.save()
            return JsonResponse({'message' : 'ended delivery session', "money_recieved" : delivery_recieved_money})
        else:
            try:
                delivery_choice = data['delivery_choice']
                delivery.delivery_problem_report_choice = delivery_choice
                delivery.delivery_report = delivery_report
                delivery.save()
                delivery_operator.delivering = False
                delivery.is_delivered = False
                delivery.is_being_delivered = False
                delivery_operator.Deliveries.add(delivery)
                delivery_operator.save()
                delivery.delivery_operator = delivery_operator
                delivery.save()
                return JsonResponse({'message' : 'ended delivery session', "delivery_report_choice" : delivery_choice})
            except Exception as e:
                return Response({'message' : 'Please Pass Required Info'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message':'wrong order id'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['POST'])
def update_location(request):
    try:
        token = request.headers['Authorization']
        delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user) 
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        delivery = Delivery.objects.get(is_being_delivered = True ,delivery_operator = delivery_operator)
        delivery.lang = int(data['lang'])
        delivery.lat = int(data['lat'])
        delivery.save()
        return JsonResponse({'message' : 'updated'})
    except Exception as e:
        return JsonResponse({'message' : 'updated'})


# https://www.upidev.com/tutoriels/send-a-push-notification-with-firebase-django/  For Sending Notification

@api_view(['POST'])
def admin_start_delivery(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=token).user) 
    except ObjectDoesNotExist:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        delivery_operator = DeliveryOperator.objects.get(delivery_operator_id = data['delivery_operator_id']) 
        if delivery_operator.delivering:
            return JsonResponse({'message' : 'Delivery Operator Is Delivering An Order'})
    except Exception as e:
        return Response({'message' : 'Please Pass Delivery Operator Id'}, status=status.HTTP_404_NOT_FOUND)
    try:
        delivery_id = request.POST['delivery_id']
        delivery = Delivery.objects.get(delivery_id=delivery_id)
    except MultiValueDictKeyError:
        return Response({'message' : 'Please Pass Valid Delivery Id'}, status=status.HTTP_404_NOT_FOUND)
    try:       
        delivery_operator.delivering = True
        delivery_operator.save()
        delivery.is_being_delivered = True
        delivery.delivery_operator = delivery_operator
        delivery.save()
        return JsonResponse({'message' : 'started delivery session'})
    except ObjectDoesNotExist:
        return Response({'message':'wrong order id'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['POST'])
def add_order_review(request):
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
    except Exception as e:
        raise PermissionDenied
    
    try:
        data = json.loads(request.body)
        order = Order.objects.get(id=data['order_id'])
        package_review =  float(data['package_review'])        
        delivery_review = float(data['delivery_review'])
        comment = data['comment']
        order_review = OrderReview.objects.create(
            order=order,
            package_review=package_review,
            delivery_review=delivery_review,
            comment=comment
        )
        order_review.save()
        try:
            delivery = Delivery.objects.get(order=order)
            delivery.is_reviewed = True
            delivery.save()
        except Exception as e:
            return Response({
            "message" : "Please Pass Valid Order Id"
        }, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"message" : "Order Review Submited Successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "message" : "Please Pass Valid Data"
        }, status=status.HTTP_400_BAD_REQUEST)
        
        


@api_view(['GET'])
def my_orders_reviews(request):
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user) 
    except Exception as e:
        raise PermissionDenied
    return Response(OrderReviewSerializer(OrderReview.objects.filter(order__ordered_by=customer), many=True).data)
    