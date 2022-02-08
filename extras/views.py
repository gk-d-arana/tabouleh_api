import json
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http.response import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from products.serializers import MainMealSerializer
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from user_roles.models import Customer
from products.models import Cart, CartItem, Meal
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status

""" @api_view(['POST'])
def add_rating(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except ObjectDoesNotExist:
        raise PermissionDenied
    rating_content = request.POST['rating_content']
    rating_value = float(request.POST['rating_value'])
    try:
        meal_rated = Meal.objects.get(meal_id = request.POST['meal_rated'])
        rating = Rating.objects.create(customer=customer, rating_content=rating_content, 
        rating_value=rating_value, meal_rated=meal_rated
        )
        rating.save()
        ratings = Rating.objects.filter(meal_rated=meal_rated)
        if len(ratings) != 0 : 
            meal_rated.meal_rating = (meal_rated.meal_rating + rating_value) / len(ratings)
        else : 
            meal_rated.meal_rating = (meal_rated.meal_rating + rating_value)
        meal_rated.save()
        return JsonResponse({'message' : 'Rating Added Successfully'})
    except ValidationError:
        return JsonResponse({'message':'No Such Product'})
 """


class RatingView(CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            raise PermissionDenied
        return Response(RatingListSerializer(Rating.objects.filter(customer=customer), many=True).data)

    def create(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            raise PermissionDenied
        try: 
            data = json.loads(request.body)
            rating_content = data['rating_content']
            rating_value = float(data['rating_value'])
            meal_id = data['meal_id']
        except Exception as e :
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            meal_rated = Meal.objects.get(meal_id=meal_id)
            rating = Rating.objects.create(customer=customer, rating_content=rating_content, 
            rating_value=rating_value, meal_rated=meal_rated
            )
            rating.save()
            ratings = Rating.objects.filter(meal_rated=meal_rated)
            if len(ratings) != 0 : 
                meal_rated.meal_rating = (meal_rated.meal_rating + rating_value) / len(ratings)
            else : 
                meal_rated.meal_rating = (meal_rated.meal_rating + rating_value)
            meal_rated.save()
            return Response({'message' : 'Rating Added Successfully', "rating_id" : rating.rating_id}, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({'message':'No Such Product'}, status=status.HTTP_404_NOT_FOUND)
    
        return super().update(request, *args, **kwargs)
   
    def update(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            print(e)
            raise PermissionDenied
        try: 
            data = json.loads(request.body)
            rating_content = data['rating_content']
            rating_value = float(data['rating_value'])
            rating_id = data['rating_id']
            rating = Rating.objects.get(rating_id=rating_id)
            meal_rated = rating.meal_rated
        except Exception as e :
            print(e)
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            if rating.customer != customer:
                print(rating.customer, customer)
                raise PermissionDenied
            rating.rating_content=rating_content
            rating.rating_value=rating_value
            rating.save()
            ratings = Rating.objects.filter(meal_rated=meal_rated)
            new_rating = 0
            for rating in ratings:
                new_rating += rating.rating_value
            meal_rated.meal_rating = new_rating / len(ratings)
            meal_rated.save()
            return JsonResponse({'message' : 'Rating Updated Successfully'})
        except ValidationError:
            return Response({'message':'No Such Product'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):  
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            raise PermissionDenied
        try: 
            data = json.loads(request.body)
            rating_id = data['rating_id']
            rating = Rating.objects.get(rating_id=rating_id)
            meal_rated = rating.meal_rated
        except Exception as e :
            return Response({
                'message' : 'Please Pass Valid Id'
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            if rating.customer != customer:
                raise PermissionDenied
            rating.delete()
            ratings = Rating.objects.filter(meal_rated=meal_rated)
            new_rating = 0
            for rating in ratings:
                new_rating += rating.rating_value
            meal_rated.meal_rating = new_rating / len(ratings)
            meal_rated.save()
            return Response({'message' : 'Rating Deleted Successfully'}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({'message':'No Such Product'}, status=status.HTTP_404_NOT_FOUND)


class MealRatings(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            meal_id = data['meal_id']
        except MultiValueDictKeyError or exceptions.ValidationError:
            return JsonResponse({'message':'Please Pass Valid Meal Id'})
        try:
            meal = Meal.objects.get(meal_id=meal_id)
            ratings = RatingSerializer(Rating.objects.filter(meal_rated=meal), many=True).data
            return Response(ratings)
        except ValidationError:
            return JsonResponse({'message':'No Such Meal'})


@api_view(['POST', 'DELETE'])
def edit_wishlist(request):
    try:
        token = request.headers['Authorization']
        customer= Customer.objects.get(user=Token.objects.get(key=token).user)
    except Exception as e :
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meal = Meal.objects.get(meal_id=data['meal_id'])
    except Exception as e:
        return Response({'message' : 'Please Pass Valid Meal Id'}, status=status.HTTP_404_NOT_FOUND)
    wishlist ,created = WishList.objects.get_or_create(customer=customer)
    if request.method == "POST":
        if meal in wishlist.meals.all():
            return Response({'message' : 'Already In Wishlist'}, status=status.HTTP_204_NO_CONTENT)
        else:
            wishlist.meals.add(meal)
            wishlist.save()
        return Response({'message' : 'Added To Wishlist'}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if meal in wishlist.meals.all():
            wishlist.meals.remove(meal)
            wishlist.save()
            return Response({'message' : 'Removed From Wishlist'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Not In Wishlist'}, status=status.HTTP_204_NO_CONTENT)


class WishListView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            raise PermissionDenied
        try:
            wishlist, created = WishList.objects.get_or_create(customer=customer)
            cart ,created = Cart.objects.get_or_create(cart_owner=customer)
            cart.save()
            wishlist.save()
            returned_data = []
            for meal in wishlist.meals.all():
                try:
                    cart_item = CartItem.objects.get(meal=meal)
                    if cart_item in cart.cart_items.all():
                        returned_data.append({
                            "meal" : MainMealSerializer(meal).data,
                            "in_cart" : True
                        })
                    else:
                        returned_data.append({
                            "meal" : MainMealSerializer(meal).data,
                            "in_cart" : False
                        })
                except :
                    returned_data.append({
                            "meal" : MainMealSerializer(meal).data,
                            "in_cart" : False
                        })
            return Response(returned_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message" : "error"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except KeyError:
            raise PermissionDenied
        try:
            meal = Meal.objects.get(meal_id=request.POST['meal_id'])
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Meal Id'})
        wishlist ,created = WishList.objects.get_or_create(customer=customer)
        if meal in wishlist.meals.all():
            return JsonResponse({'message' : 'Already In Wishlist'})
        else:
            wishlist.meals.add(meal)
        return JsonResponse({'message' : 'Added To Wishlist'})

    def destroy(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except KeyError:
            raise PermissionDenied
        try:
            meal = Meal.objects.get(meal_id=request.POST['meal_id'])
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Meal Id'})
        wishlist ,created = WishList.objects.get_or_create(customer=customer)
        if meal in wishlist.meals.all():
            wishlist.meals.remove(meal)
            wishlist.save()
            return JsonResponse({'message' : 'Removed From Wishlist'})
        else:
            return JsonResponse({'message' : 'Not In Wishlist'})



class ManagePayment(ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    def list(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            raise PermissionDenied
        try:
            payments = PaymentTypeSerializer(PaymentType.objects.filter(customer=customer), many=True).data
            return Response(payments)
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid WishList Id'})
    def create(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            payment = PaymentType.objects.create(payment_provider = data['payment_provider'], first_name = data[''],
                                        customer=customer, card_number=data['card_number'],
                                        card_expire_date=data['card_expire_date'], card_cvc=data['card_cvc']
                                                 )
            payment.save()
            return Response({'message' : 'success', 'payment_id':payment.payment_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
      

    def update(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            payment = PaymentType.objects.get(payment_id=data['payment_id'])
            payment.card_number = data['card_number']
            payment.card_cvc = data['card_cvc']
            payment.card_expire_date = data['card_expire_date']
            payment.payment_provider = data['payment_provider']
            payment.save()
            return JsonResponse({'message' : 'Payment Updated'})
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Data'}, status=status.HTTP_400_BAD_REQUEST)
      

    def destroy(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer= Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            payment = PaymentType.objects.get(payment_id=data['payment_id'])
            payment.delete()
            return JsonResponse(
                {"message" : "Payment Deleted"}
            )
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Id'}, status=status.HTTP_404_NOT_FOUND)
      

@api_view(['POST', 'DELETE', 'PUT'])
def manage_addresses(request):
    data = json.loads(request.body)
    try:
        token = request.headers['Authorization']
    except Exception as e:
        raise PermissionDenied
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except Exception as e:
        raise PermissionDenied
    if request.method == "DELETE":
        try:
            address = Address.objects.get(id=data['address_id'])
        except Exception as e:
            return Response({'message' : 'please pass valid id'}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({'message' : 'Address Deleted Successfully'}, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        try:
            area_name = data['area_name']
            street = data['street']
            building_no = data['building_no']
            phone_no = data['phone_no']
            address = Address.objects.create(customer=customer)
            address.area_name = area_name
            address.street = street
            address.building_no = building_no
            address.phone_no = phone_no
            address.save()
            customer.addresses.add(address)
            customer.save()
            return Response({
                'message' : 'Address Saved Successfully',
                'address_id' : address.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message' : 'please pass required data'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        try:
            address = Address.objects.get(id=int(data["address_id"]))
        except Exception as e:
            return Response({'message' : 'Please Pass Valid Id'}, status=status.HTTP_404_NOT_FOUND)
        try:
            area_name = data['area_name']
            street = data['street']
            building_no = data['building_no']
            phone_no = data['phone_no']
            address.area_name = area_name
            address.street = street
            address.building_no = building_no
            address.phone_no = phone_no
            address.save()
            return Response({
                'message' : 'Address Updated Successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message' : 'please pass required data'}, status=status.HTTP_400_BAD_REQUEST)


class AddressListView(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user)
        except Exception as e:
                raise PermissionDenied
        addresses = AddressSerializer(Address.objects.filter(customer=customer), many=True).data
        return Response(addresses, status=status.HTTP_200_OK)


@api_view(['GET'])
def about_view(request):
    return Response(AboutSerializer(About.objects.first()).data)


@api_view(['GET'])
def services_view(request):
    return Response(ServiceSerializer(Service.objects.first()).data)

@api_view(['GET'])
def agencies_view(request):
    return Response(AgencySerializer(Agency.objects.all(), many=True).data)



@api_view(['GET'])
def main_values(request):
    return Response(MainValueSerializer(MainValue.objects.all(), many=True).data)
