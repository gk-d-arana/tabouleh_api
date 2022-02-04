import json
import re
from rest_framework.views import APIView
from orders.serializers import CompDeliveryOperatorSerializer, CompleteDeliverySerializer, DeliverySerializer, OrderSerializer, SimpleOrderSerializer
from orders.models import Delivery, Order
from products.models import Cart
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from .models import *
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser


""" def admin_authenticate_view(request, token):
    admin = is_admin(token=token)
    return HttpResponse(admin)
 """

def admin_login(request):
    return render(request, 'users/login.html', {})

#  Login 
def admin_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.get(username = username)
        admin_user = Admin.objects.get(user=user)
        if user.check_password(password):
            return redirect('home/')
        else:
            return redirect('admin_login/', {'erorr' : 'wrong credential'})
    except ObjectDoesNotExist:
        return redirect('admin_login/', {'erorr' : 'wrong credential'})



@api_view(['POST'])
def customer_login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except Exception as e:
        return Response({
            'message' : 'wrong credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        user_serialized = UserSerializer(user).data
        customer = Customer.objects.get(user=user)
        customer_serialized = CustomerSerializer(customer).data
        print(customer_serialized)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            data = {
                'Customer Data' : customer_serialized,
                'token' : '{}'.format(token)
            }
            return Response(data)

        else:
            return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def delivery_login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except Exception as e:
        return Response({
            'message' : 'wrong credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        delivery_operartor = DeliveryOperator.objects.get(user=user)
        delivery_operartor_serialized = DeliveryOperatorSerializer(delivery_operartor).data
        print(delivery_operartor_serialized)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            data = {
                'Delivery Operator Data' : delivery_operartor_serialized,
                'token' : '{}'.format(token)
            }
            return Response(data)

        else:
            return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def api_admin_login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except Exception as e:
        return Response({
            'message' : 'Please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        admin = Admin.objects.get(user=user)
        admin_serialized = AdminSerializer(admin).data
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'admin' : admin_serialized,
                'token' : '{}'.format(token)
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'message' : 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)




#  Register


def admin_register(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    is_staff = True
    #profile_image = request.data['profile_image']
    #country = request.POST['country']
    country = "IQ"
    try:
        user = User.objects.get(username = username)
        if user:
            return JsonResponse({'erorr' : 'This Username Is Already Used'}) 
    except ObjectDoesNotExist:
        user = User.objects.create(username=username, password=password, email=email,
        first_name=first_name, last_name=last_name, is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        admin = Admin.objects.create(user=user, country=country)
        token = Token.objects.create(user=user)
        admin.save()
        token.save()
        return redirect('/control_panel/dashboard/')   


def cp_delivery_operator_register(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    is_staff = True
    #profile_image = request.data['profile_image']
    country = "IQ"
    try:
        user = User.objects.get(username = username)
        if user:
            return JsonResponse({'erorr' : 'This Username Is Already Used'}) 
    except ObjectDoesNotExist:
        user = User.objects.create(username=username, password=password, email=email,
        first_name=first_name, last_name=last_name, is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        admin = DeliveryOperator.objects.create(user=user, country=country)
        token = Token.objects.create(user=user)
        admin.save()
        token.save()
        return redirect('/control_panel/dashboard')   



@api_view(['POST'])
def cp_customer_register(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        is_staff = False
        country = "IQ"
        phone_number = request.POST['phone_number']
    except Exception as e:
        return Response({
            'message' : 'Please Pass Valid request.POST'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        if user:
            return Response({'erorr' : 'This Username Already Exists'}, status=status.HTTP_400_BAD_REQUEST) 
    except ObjectDoesNotExist:
        user = User.objects.create(username=username, password=password, email=email,
        first_name=first_name, last_name=last_name, is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        customer = Customer.objects.create(user=user, country=country, #profile_image=profile_image
                                            phone_number=phone_number, role=role
        )
        customer.save()
        cart, created = Cart.objects.get_or_create(cart_owner=customer)
        cart.save()
        token = Token.objects.create(user=user)
        #        token.save()
        return redirect('/control_panel/dashboard')   



@api_view(['POST'])
def customer_register(request):
    data = json.loads(request.body)
    try:
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        is_staff = False
        country = data['country']
        phone_number = data['phone_number']
    except Exception as e:
        return Response({
            'message' : 'Please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        if user:
            return Response({'erorr' : 'This Username Already Exists'}, status=status.HTTP_400_BAD_REQUEST) 
    except ObjectDoesNotExist:
        user = User.objects.create(username=username, password=password, email=email,
        first_name=first_name, last_name=last_name, is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        customer = Customer.objects.create(user=user, country=country, #profile_image=profile_image
                                            phone_number=phone_number
        )
        customer.save()
        cart, created = Cart.objects.get_or_create(cart_owner=customer)
        cart.save()
        token = Token.objects.create(user=user)
        #        token.save()
        customer_serialized = CustomerSerializer(customer).data
        data = {
                'Customer Data' : customer_serialized,
                'token' : '{}'.format(token)
            }
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def delivery_operator_register(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        is_staff = False
        #profile_image = request.data['profile_image']
        country = data['country']
        phone_number = data['phone_number']
    except Exception as e:
        return Response({
            'message' : 'Please Pass Valid Data'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username = username)
        if user:
            return Response({'message' : 'This Username Already Exists'}, status=status.HTTP_400_BAD_REQUEST) 
    except ObjectDoesNotExist:
        user = User.objects.create(username=username, password=password, email=email,
        first_name=first_name, last_name=last_name, is_staff=is_staff, phone_number=phone_number
        )
        user.set_password(password)
        user.save()
        delivery_operartor= DeliveryOperator.objects.create(user=user, country=country, #rofile_image=profile_image
        )
        delivery_operartor.save()
        token = Token.objects.create(user=user)
        delivery_operartor_serialized = FullDeliveryOperatorSerializer(delivery_operartor).data
        data = {
                'Delivery Operator Data' : delivery_operartor_serialized,
                'token' : '{}'.format(token)
            }
        token.save()
        return Response(data, status=status.HTTP_201_CREATED)



def admin_details(request):
    user = request.user
    if user:
        admin = Admin.objects.get(user=user)
        return render('users/admin_details.html', {
            admin : admin
        })
    else:
        return redirect('users/admin_register.html', {})


@api_view(['GET'])
def customer_details(request):
    try:
        token = request.headers['Authorization']
    except MultiValueDictKeyError:
        raise ValidationError('Please Pass Authorization Token')
    try:
        customer = CustomerSerializer(Customer.objects.get(user=Token.objects.get(key=token).user) ).data
        return Response(customer, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise PermissionDenied
    
@api_view(['GET'])
def view_customer_as_admin(request):
    try:
        token = request.headers['Authorization']
        admin = Admin.objects.get(user=Token.objects.get(key=token).user)
    except Exception as e:
        raise PermissionDenied
    try:
        cust = Customer.objects.get(customer_id = request.GET.get('customer_id'))
        orders = SimpleOrderSerializer(Order.objects.filter(ordered_by=cust), many=True).data
        customer = CustomerSerializer(cust).data
        return JsonResponse({
            "customer" : customer,
            'orders' : orders
            })
    except Exception as e:
        return Response({
            'message' : "Please Pass Valid Customer Id"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_delivery_operator_as_admin(request):
    try:
        token = request.headers['Authorization']
        admin = Admin.objects.get(user=Token.objects.get(key=token).user)
    except Exception as e:
        raise PermissionDenied
    #try:
    delivery_operator = DeliveryOperator.objects.get(delivery_operator_id=request.GET.get('delivery_operator_id'))
    delivery_operator_serialized = DeliveryOperatorSerializer(delivery_operator).data
    deliveries = CompleteDeliverySerializer(Delivery.objects.filter(delivery_operator=delivery_operator) ,many=True).data
    return JsonResponse({
        'delivery_operator' : delivery_operator_serialized,
        'deliveries' : deliveries
    })
    #except ObjectDoesNotExist:
    #    return JsonResponse({
    #        'message' : "Please Pass Valid Delivery Operator Id"
    #    })


@api_view(['GET'])
def delivery_operator_details(request):
    try:
        token = request.headers['Authorization']
    except MultiValueDictKeyError:
        raise ValidationError('Please Pass Authorization Token')
    try:
        delivery_operator = DeliveryOperator.objects.get(user=Token.objects.get(key=token).user)
        delivery_operator_serialized = DeliveryOperatorSerializer(DeliveryOperator.objects.get(user=Token.objects.get(key=token).user)).data
        deliveries = DeliverySerializer(Delivery.objects.filter(delivery_operator=delivery_operator) ,many=True).data
        return JsonResponse({
            'delivery_operator' : delivery_operator_serialized,
            'deliveries' : deliveries
        })
    except ObjectDoesNotExist:
        raise PermissionDenied


class ProfileView(RetrieveAPIView, UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            user = Token.objects.get(key=request.headers['Authorization']).user
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            user.first_name = first_name
            user.last_name = last_name
            try:
                phone_number = data['phone_number']
                customer = Customer.objects.get(user=user)
                customer.phone_number = phone_number
                customer.save()
            except Exception as e:
                pass
            user.email = email
            user.save()
        except Exception as e:
            pass
        try:
            password = data['password']
            new_password = data['new_password']
            if user.check_password(password):
                user.set_password(new_password)
                user.save()
                return JsonResponse({
                    'message' : 'Profile Updated Successfully'
                })
            else:
                return Response({
                'message' : "Please Pass Valid Password"
            }, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            pass
        return JsonResponse({
                            'message' : 'Profile Updated Successfully'
                        })

class UpdateProfileImageView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            profile_image = request.data['profile_image']
            customer.profile_image = profile_image
            customer.save()
            return JsonResponse({'message' : 'success'})
        except Exception as e:
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)


class CustomersListView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except ObjectDoesNotExist:
                raise PermissionDenied
        customers = CustomersListSerializer(Customer.objects.all(), many=True).data
        return Response(customers)


class CustomerDetails(RetrieveUpdateDestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except ObjectDoesNotExist:
                raise PermissionDenied
        try:
            customer = Customer.objects.get(customer_id=request.POST['customer_id'])
            customer.delete()
            return JsonResponse({'message': 'Deleted'})
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Customer Id'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except ObjectDoesNotExist:
                raise PermissionDenied
        try:
            customer = CustomerSerializer(Customer.objects.get(customer_id=request.POST['customer_id'])).data
            return Response(customer)
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Customer Id'}, status=status.HTTP_404_NOT_FOUND)
    


class DeliveryOperatorListView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except ObjectDoesNotExist:
                raise PermissionDenied
        delivery_operators = DeliveryOperatorsListSerializer(DeliveryOperator.objects.all(), many=True).data
        return Response(delivery_operators)




class DelievryOperatorDetails(RetrieveUpdateDestroyAPIView):
    def destroy(self, request, *args, **kwargs):    
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except ObjectDoesNotExist:
                raise PermissionDenied
        try:
            delivery_operator = DeliveryOperator.objects.get(delivery_operator_id=request.POST['delivery_operator_id'])
            delivery_operator.delete()
            return JsonResponse({'message': 'Deleted'})
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Delivery Operator Id'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            admin = Admin.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            print(e)
            raise PermissionDenied
        try:
            delivery_operator = CompDeliveryOperatorSerializer(DeliveryOperator.objects.get(delivery_operator_id=request.GET.get('delivery_operator_id'))).data
            return Response(delivery_operator)
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Delivery Operator Id'}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['POST', 'PUT'])
def resett_password(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        user = Token.objects.get(key=request.headers['Authorization']).user
    except Exception as e:
            raise PermissionDenied
    if request.method == "PUT":
        sent_code = int(request.POST['sent_code'])
        code = CodesForPassReset.objects.filter(id=request.POST['code_id']).last()
        if code.code == sent_code:
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            return JsonResponse({
                'message' : 'Password Edit Successfully',
            })
        return JsonResponse({
            'message' : 'Please Pass Valid Data'
        })
    import random
    string_ints = [str(int) for int in random.sample(range(0, 9), 4)]
    code  = ''.join(string_ints)
    new_code = CodesForPassReset.objects.create(user=user, code=code)
    new_code.save()
    subject = 'Your Request To Reset Your Password'
    message = f'Hi Your Confirmation Code Is {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return JsonResponse({
        'message' : 'Sent Email Successfully',
        'id' : new_code.id
    })



@api_view(['POST', 'PUT'])
def reset_password(request):
    data = json.loads(request.body)
    if request.method == "PUT":
        try:
            user=Token.objects.get(key=request.headers['Authorization']).user
        except Exception as e:
            raise PermissionDenied
        try:
            new_password = data['new_password']
            user.set_password(new_password)
            user.save()
            return JsonResponse({
                "message" : "Updated Successfully"
            })
        except Exception as e:
            return Response({"message":"Please Pass New Password"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        email = data['email']
    except Exception as e:
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)
    try:    
        user = User.objects.get(email=email)
    except Exception as e:
            return Response({"message":"This Email Did Not Match Our Records"}, status=status.HTTP_400_BAD_REQUEST)
    
    import random
    string_ints = [str(int) for int in random.sample(range(0, 9), 4)]
    code  = ''.join(string_ints)
    new_code = CodesForPassReset.objects.create(user=user, code=code)
    new_code.save()
    subject = 'Your Request To Reset Your Password'
    message = f'Hi Your Confirmation Code Is {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return JsonResponse({
        'message' : 'Sent Email Successfully',
        'id' : new_code.id
    })




@api_view(['POST'])
def check_code(request):
    try:
        data = json.loads(request.body)
        code = CodesForPassReset.objects.filter(id=data['code_id']).last()
        sent_code = int(data['sent_code'])
        if code.code == sent_code:
            return JsonResponse({
            'message' : 'success',
            'token' : "{}".format(Token.objects.get(user=code.user).key)
        })
        else:
            return Response({
                'message' : 'fail',
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"message":"Please Pass Valid Data"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_profile_image(request):
    try:
        user = Token.objects.get(key=request.headers['Authorization']).user
        try:
            admin = Admin.objects.get(user=user)
            return Response({'profile_image', f"{admin.profile_image}"})
        except Exception as e:
            pass
        try:
            customer = Customer.objects.get(user=user)
            return Response({'profile_image', f"{customer.profile_image}"})
        except Exception as e:
            pass
        try:
            delivery_operator = DeliveryOperator.objects.get(user=user)
            return Response({'profile_image', f"{delivery_operator.profile_image}"})
        except Exception as e:
            pass
            return Response({'profile_image', ""})
    except Exception as e:
        raise PermissionDenied
