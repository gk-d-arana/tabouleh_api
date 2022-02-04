import json
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authtoken.models import Token
from django.core import exceptions
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.serializers import *
from orders.models import Order
from rest_framework import status
from .models import *
from extras.serializers import RatingSerializer, SimpleRatingSerializer
from extras.models import Rating, WishList
from .serializers import *
from django.shortcuts import redirect
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.db.models import Q



def string_to_number(str):
    if("." in str):
        try:
            res = float(str)
        except:
          res = str  
    elif(str.isdigit()):
        res = int(str)
    else:
        res = str
    return(res)



@api_view(['GET'])
def search(request, *args, **kwargs):
    in_one = False
    qs = Meal.objects.all()
    meal_rating = request.GET.get('meal_rating')
    if meal_rating is not None:
        in_one = True
        qs = Meal.objects.filter(meal_rating=string_to_number(meal_rating))
    category_id = request.GET.get('category_id')
    if category_id is not None:
        in_one = True
        try:
            meal_category = Category.objects.get(category_id=category_id)
            qs = qs.filter(meal_category=meal_category)
        except Exception as e:
            pass
    min_price = request.GET.get('min_price')
    if min_price is not None:
        in_one = True
        try:
            customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
            role = customer.role
            if role == "NormalCustomer":
                qs = qs.filter(customer_meal_price__gt=min_price)
            elif role == "SuperMarketCustomer":
                qs = qs.filter(supermarket_meal_price__gt=min_price)
            elif role == "RestaurantCustomer":
                qs = qs.filter(restaurant_meal_price__gt=min_price)
            elif role == "AgentCustomer":
                qs = qs.filter(agent_meal_price__gt=min_price)
            elif role == "CompanyCustomer":
                qs = qs.filter(company_meal_price__gt=min_price)
        except Exception as e:
            qs = qs.filter(customer_meal_price__gt=min_price)
    max_price = request.GET.get('max_price')
    if max_price is not None:
        in_one = True
        try:
            customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
            role = customer.role
            if role == "NormalCustomer":
                qs = qs.filter(customer_meal_price__lt=max_price)
            elif role == "SuperMarketCustomer":
                qs = qs.filter(supermarket_meal_price__lt=max_price)
            elif role == "RestaurantCustomer":
                qs = qs.filter(restaurant_meal_price__lt=max_price)
            elif role == "AgentCustomer":
                qs = qs.filter(agent_meal_price__lt=max_price)
            elif role == "CompanyCustomer":
                qs = qs.filter(company_meal_price__lt=max_price)
        except Exception as e:
            qs = qs.filter(customer_meal_price__lt=max_price)
    meal_name = request.GET.get('meal_name')
    if meal_name is not None:
        in_one = True
        qs = qs.filter(meal_name__contains=meal_name)
    meal_name_ar = request.GET.get('meal_name_ar')
    if meal_name_ar is not None:
        in_one = True
        qs = qs.filter(meal_name_ar__contains=meal_name_ar)
    if in_one:
        response_data = []
        for meal in qs:
            response_data.append({
                "meal" : MainMealSerializer(meal).data,
                "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
            })
        return Response(response_data)   
    else:
        return Response({"message" : "Please Pass Valid Params"}, status=status.HTTP_400_BAD_REQUEST)   
    
    
class CategoryListView(ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        data = []
        for category in queryset:
            meals_count = Meal.objects.filter(meal_category=category).count()
            data.append({
                "category" : CategorySerializer(category).data,
                "meals_count" : meals_count
            })            
        return Response(data)



class MealListView(ListAPIView):
    queryset = Meal.objects.all()
    serializer_class = MainMealSerializer


class CatregoryMealsListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(category_id=request.POST['category_id'])
        except Exception as e:
            return JsonResponse({'message' : 'Please Pass Valid Category Id'})
        meals = Meal.objects.filter(meal_category=category)
        data = []
        for meal in meals:
            _meal = MainMealSerializer(meal).data
            meal_image = MealImageSerializer(MealImage.objects.filter(meal=meal).first()).data
            data.append({
                'meal' : _meal,
                "meal_image" : meal_image
            })
        return JsonResponse({
            'data' : data
        })



class HomeView(ListAPIView):
    def list(self, request, *args, **kwargs):
        categries = CategorySerializer(Category.objects.all().order_by('?'), many=True).data
        _meals = Meal.objects.order_by('-meal_rating')[:12]
        meals = []
        for meal in _meals:
            meals.append({
                "meal" : MealSerializer(meal).data,
                "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
            })
        offers = OfferSerializer(Offer.objects.all().order_by('?')[:4], many=True).data
        ratings = SimpleRatingSerializer(Rating.objects.order_by('?')[:6], many=True).data
        return JsonResponse({
            'categories' : categries, 
            'meals' : meals, 
            'ratings' : ratings,
            'offers' : offers
        })




class OfferMangmentView(CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    def create(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            offer_name = request.POST['offer_name']
            offer_name_ar = request.POST['offer_name_ar']
            normal_customer_offer_price = int(request.POST['normal_customer_offer_price'])
            supermarket_customer_offer_price = int(request.POST['supermarket_customer_offer_price'])
            agent_customer_offer_price = int(request.POST['agent_customer_offer_price'])
            company_customer_offer_price = int(request.POST['company_customer_offer_price'])
            restuarant_customer_offer_price = int(request.POST['restuarant_customer_offer_price'])
            normal_customer_offer_description = request.POST['normal_customer_offer_description']
            supermarket_customer_offer_description = request.POST['supermarket_customer_offer_description']
            agent_customer_offer_description = request.POST['agent_customer_offer_description']
            company_customer_offer_description = request.POST['company_customer_offer_description']
            restuarant_customer_offer_description = request.POST['restuarant_customer_offer_description']
            normal_customer_offer_description_ar = request.POST['normal_customer_offer_description_ar']
            supermarket_customer_offer_description_ar = request.POST['supermarket_customer_offer_description_ar']
            agent_customer_offer_description_ar = request.POST['agent_customer_offer_description_ar']
            company_customer_offer_description_ar = request.POST['company_customer_offer_description_ar']
            restuarant_customer_offer_description_ar = request.POST['restuarant_customer_offer_description_ar']
            offer_image = request.data['offer_image']
            meal = Meal.objects.get(meal_id=request.POST['meal_id'])
        except Exception as e:
            print(e)
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        offer = Offer.objects.create(
            offer_name = offer_name, offer_name_ar=offer_name_ar, normal_customer_offer_price = normal_customer_offer_price,
            supermarket_customer_offer_price = supermarket_customer_offer_price, agent_customer_offer_price = agent_customer_offer_price,
            company_customer_offer_price = company_customer_offer_price, restuarant_customer_offer_price = restuarant_customer_offer_price,
            normal_customer_offer_description = normal_customer_offer_description, supermarket_customer_offer_description = supermarket_customer_offer_description,
            agent_customer_offer_description = agent_customer_offer_description, company_customer_offer_description = company_customer_offer_description,
            restuarant_customer_offer_description = restuarant_customer_offer_description, offer_image = offer_image, normal_customer_offer_description_ar =normal_customer_offer_description_ar,
            supermarket_customer_offer_description_ar = supermarket_customer_offer_description_ar, agent_customer_offer_description_ar = agent_customer_offer_description_ar,
            company_customer_offer_description_ar = company_customer_offer_description_ar, restuarant_customer_offer_description_ar = restuarant_customer_offer_description_ar,
            meal=meal
        )
        offer.save()
        meal.offers.add(offer)
        meal.save()
        return Response({
            'message' : 'Offer Created Successfully',
            "offer_id" : offer.offer_id,
            "offer_image" : "{}".format(offer.offer_image)
        }, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            offer_name = request.POST['offer_name']
            offer_name_ar = request.POST['offer_name_ar']
            normal_customer_offer_price = int(request.POST['normal_customer_offer_price'])
            supermarket_customer_offer_price = int(request.POST['supermarket_customer_offer_price'])
            agent_customer_offer_price = int(request.POST['agent_customer_offer_price'])
            company_customer_offer_price = int(request.POST['company_customer_offer_price'])
            restuarant_customer_offer_price = int(request.POST['restuarant_customer_offer_price'])
            normal_customer_offer_description = request.POST['normal_customer_offer_description']
            supermarket_customer_offer_description = request.POST['supermarket_customer_offer_description']
            agent_customer_offer_description = request.POST['agent_customer_offer_description']
            company_customer_offer_description = request.POST['company_customer_offer_description']
            restuarant_customer_offer_description = request.POST['restuarant_customer_offer_description']
            normal_customer_offer_description_ar = request.POST['normal_customer_offer_description_ar']
            supermarket_customer_offer_description_ar = request.POST['supermarket_customer_offer_description_ar']
            agent_customer_offer_description_ar = request.POST['agent_customer_offer_description_ar']
            company_customer_offer_description_ar = request.POST['company_customer_offer_description_ar']
            restuarant_customer_offer_description_ar = request.POST['restuarant_customer_offer_description_ar']
            offer_image = request.data['offer_image']
            meal = Meal.objects.get(meal_id=request.POST['meal_id'])
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        offer = Offer.objects.create(
            offer_name = offer_name,offer_name_ar=offer_name_ar, normal_customer_offer_price = normal_customer_offer_price,
            supermarket_customer_offer_price = supermarket_customer_offer_price, agent_customer_offer_price = agent_customer_offer_price,
            company_customer_offer_price = company_customer_offer_price, restuarant_customer_offer_price = restuarant_customer_offer_price,
            normal_customer_offer_description = normal_customer_offer_description, supermarket_customer_offer_description = supermarket_customer_offer_description,
            agent_customer_offer_description = agent_customer_offer_description, company_customer_offer_description = company_customer_offer_description,
            restuarant_customer_offer_description = restuarant_customer_offer_description, offer_image = offer_image, normal_customer_offer_description_ar =normal_customer_offer_description_ar,
            supermarket_customer_offer_description_ar = supermarket_customer_offer_description_ar, agent_customer_offer_description_ar = agent_customer_offer_description_ar,
            company_customer_offer_description_ar = company_customer_offer_description_ar, restuarant_customer_offer_description_ar = restuarant_customer_offer_description_ar,
            meal=meal
        )
        offer.save()
        return JsonResponse({
            'message' : 'Offer Updated Successfully'
        })
    def destroy(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            offer = Offer.objects.get(offer_id=data['offer_id'])
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Id'
            }, status=status.HTTP_404_NOT_FOUND)
        offer.delete()
        return JsonResponse({
            'message' : 'Offer Deleted Successfully'
        })
    def list(self, request, *args, **kwargs):
        queryset = Offer.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = OfferSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)



class MealDetailsView(RetrieveAPIView):
    def get(self, request, meal_id, *args, **kwargs):
        try: 
            meal = Meal.objects.get(meal_id=meal_id)
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Meal Id'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = MealSerializer(meal).data
            ratings = SimpleRatingSerializer(Rating.objects.filter(meal_rated=meal), many=True).data
            meal_images = MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
            return JsonResponse({
                'meal' : serializer,
                'ratings' : ratings,
                'meal_images' : meal_images
            })
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Meal Id'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_all_categories(request):
    try:
        admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    Category.objects.all().delete()
    return JsonResponse(
        {"message" : "Categories Deleted Successfully"}
    )


class MealManagmentView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    def create(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try: 
            meal_name = request.POST['meal_name']
            meal_name_ar = request.POST['meal_name_ar']
            meal_points = string_to_number(request.POST['meal_points'])
            meal_description = request.POST['meal_description']
            meal_description_ar = request.POST['meal_description_ar']
            category_id = request.POST['category_id']
            meal_main_image = request.data['meal_main_image']
            customer_meal_price = int(request.POST['customer_meal_price'])
            supermarket_meal_price = int(request.POST['supermarket_meal_price'])
            agent_meal_price = int(request.POST['agent_meal_price'])
            restaurant_meal_price = int(request.POST['restaurant_meal_price'])
            company_meal_price = int(request.POST['company_meal_price'])
            meal_images = request.data.getlist('meal_image')
            print(meal_images)
            meal_category = Category.objects.get(category_id=category_id)
            ingredients = request.POST.getlist('ingredients')
            
            #offers_ids  = request.POST.getlist('offers')
            #except Exception as e:
            #    return Response({
            #        'message' : 'Please Pass Valid Data'
            #    }, status=status.HTTP_400_BAD_REQUEST)
            meal = Meal.objects.create(meal_name=meal_name, meal_description=meal_description, 
            meal_main_image=meal_main_image,
            customer_meal_price=customer_meal_price, supermarket_meal_price = supermarket_meal_price,
            agent_meal_price = agent_meal_price ,restaurant_meal_price = restaurant_meal_price,
            company_meal_price =company_meal_price, meal_category=meal_category, meal_points=meal_points,meal_name_ar = meal_name_ar,
            meal_description_ar = meal_description_ar
            )
            meal.save()
            meal_category.meals_count += 1
            meal_category.save()
            for ingredient in ingredients:
                ingre = Ingredient.objects.create(ingredient_name=ingredient)
                ingre.save()
                meal.meal_ingredients.add(ingre)
                meal.save()
            #for offer_id in offers_ids:
            #    try:
            #        offer = Offer.objects.get(offer_id=offer_id)
            #    except Exception as e:
            #        return Response({
            #            "message" : "Please Pass Valid Offer Id"
            #        }, status=status.HTTP_404_NOT_FOUND)
            #       meal.meal_properties.add(offer)
            if len(meal_images) == 1:
                meal_image = MealImage.objects.create(meal=meal, image=meal_images[0])
                meal_image.save()     
            else:
                for image in meal_images:
                    meal_image = MealImage.objects.create(meal=meal, image=image)
                    meal_image.save()
            return Response({
                'message' : 'Meal Created Successfully',
                "meal_id" : "{}".format(meal.meal_id),
                "meal_main_image" : "{}".format(meal.meal_main_image)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                "message" : "Please Pass Valid Data"
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def update(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        
        try:
            data = json.loads(request.body)
            meal_id = data['meal_id']
            meal = Meal.objects.get(meal_id=meal_id)
            meal_name = data['meal_name']
            meal_name_ar = data['meal_name_ar']
            meal_description = data['meal_description']
            meal_description_ar = data['meal_description_ar']
            meal_points = string_to_number(data['meal_points'])
            category_id = data['category_id']
            customer_meal_price = int(data['customer_meal_price'])
            supermarket_meal_price = int(data['supermarket_meal_price'])
            agent_meal_price = int(data['agent_meal_price'])
            restaurant_meal_price = int(data['restaurant_meal_price'])
            company_meal_price = int(data['company_meal_price'])
            meal_category = Category.objects.get(category_id=category_id)
            meal.meal_name=meal_name
            meal.meal_name_ar=meal_name_ar
            meal.meal_points=meal_points
            meal.meal_description=meal_description
            meal.meal_description_ar=meal_description_ar
            meal.customer_meal_price=customer_meal_price
            meal.supermarket_meal_price = supermarket_meal_price
            meal.agent_meal_price = agent_meal_price 
            meal.restaurant_meal_price = restaurant_meal_price
            meal.company_meal_price = company_meal_price 
            meal.meal_category=meal_category
            meal.save()
        except Exception as e:
            """ return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST) """
            pass
        try:
            meal_images = request.FILES.getlist('meal_image')
            if len(meal_images) == 1:
                meal_image = MealImage.objects.create(meal=meal, image=meal_images[0])
                meal_image.save()     
            else:
                for image in meal_images:
                    meal_image = MealImage.objects.create(meal=meal, image=image)
                    meal_image.save() 
        except Exception as e:
            pass
            try:
                ingredients = data['ingredients']
                for ingredient in ingredients:
                    ingre, created = Ingredient.objects.get_or_create(ingredient_name=ingredient)
                    ingre.save()
                    meal.meal_ingredients.add(ingre)
            except Exception as e:
                pass
            """             try:
                offers_ids  = request.POST.getlist('offers_ids')
                for offer_id in offers_ids:
                    try:
                        offer = Offer.objects.get(offer_id=offer_id)
                    except Exception as e:
                        return Response({
                            "message" : "Please Pass Valid Offer Id"
                        }, status=status.HTTP_404_NOT_FOUND)
                    meal.meal_properties.add(offer)
            except Exception as e:      
                pass """
        
        return Response({
            'message' : 'Meal Updated Successfully'
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            meal = Meal.objects.get(meal_id=data['meal_id'])
            meal.meal_category.meals_count += 1
            meal.meal_category.save()
            meal.delete()
            return JsonResponse({
                'message' : "Meal Deleted Successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Id'
            }, status=status.HTTP_404_NOT_FOUND)



class CategoryManagmentView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    def create(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            category_name_ar = request.POST['category_name_ar']
            category_name = request.POST['category_name']
            category_image = request.FILES.get('category_image')
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        category = Category.objects.create(
            category_image = category_image,
            category_name=category_name, 
            category_name_ar = category_name_ar
        )
        category.save()
        return Response({
            'message' : 'Category Created Successfully',
            "category_id" : category.category_id
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            try:
                category = Category.objects.get(category_id=data['category_id'])
                category.category_name_ar = data['category_name_ar']
                category.category_name = data['category_name']
                category.save()
                return JsonResponse({
                'message' : 'Category Updated Successfully'
                })
            except Exception as e:
                return Response({
                    'message' : 'Please Pass Valid Data'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            pass
        
        try:
            category_name_ar = request.POST['category_name_ar']
            category_name = request.POST['category_name']
            category = Category.objects.get(category_id=request.POST['category_id'])
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            category_image = request.FILES.get('category_image')
            category.category_image = category_image
        except Exception as e:
            pass
        category.category_name = category_name
        category.category_name_ar = category_name_ar
        category.save()
        return JsonResponse({
            'message' : 'Category Updated Successfully'
        })

    def destroy(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        try:
            data = json.loads(request.body)
            category = Category.objects.get(category_id=data['category_id'])
            category.delete()
            return JsonResponse({
                'message' : "Category Deleted Successfully"
            })
        except Exception as e:
            return Response({
                'message' : 'Please Pass Valid Data'
            }, status=status.HTTP_404_NOT_FOUND)



class CartView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
        except Exception as e:
            raise PermissionDenied
        cart, created = Cart.objects.get_or_create(cart_owner = customer)
        #cart_ = CartSerializer(cart).data
        wishlist, created = WishList.objects.get_or_create(customer=customer)
        wishlist.save()
        returned_data = []
        for cart_item in cart.cart_items.all():
            if cart_item.meal in wishlist.meals.all():
                returned_data.append({
                    "cart_item" : CartItemSerializer(cart_item).data,
                    "in_wishlist" : True
                })
            else:
                returned_data.append({
                    "cart_item" : CartItemSerializer(cart_item).data,
                    "in_wishlist" : False
                })
        return Response(returned_data)






@api_view(['POST'])
def add_to_cart(request):
    try:
        token = request.headers['Authorization']
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meal = Meal.objects.get(meal_id = data['meal_id'])
        cart_item ,created = CartItem.objects.get_or_create(meal=meal, cart_item_owner= customer)
        cart_item.save()
        cart, created = Cart.objects.get_or_create(cart_owner=customer)
        if cart_item in cart.cart_items.all():
            return Response({'message' : 'Meal Is In Cart Already'}, status=status.HTTP_204_NO_CONTENT)
        else:
            cart.cart_items.add(cart_item)
            cart.save()
        return Response({'message' : 'Meal Added To Cart Successfuly'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "message" : "Please Pass Valid Data"
        }, status=status.HTTP_404_NOT_FOUND)





@api_view(['DELETE'])
def remove_from_cart(request):
    try:
        token = request.headers['Authorization']
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except Exception as e:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meal = Meal.objects.get(meal_id = data['meal_id'])
    except Exception as e:
        return Response({"message":'No Such Meal'}, status=status.HTTP_404_NOT_FOUND)
    try:
        cart_item = CartItem.objects.get(meal=meal, cart_item_owner= customer)
        cart, created = Cart.objects.get_or_create(cart_owner=customer)
        if cart_item in cart.cart_items.all():
            cart.cart_items.remove(cart_item)
            cart.save()
            return Response({'message' : 'Meal Removed From Cart Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Meal Not In Cart'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'message' : 'Meal Not In Cart'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def increase_meal_amount(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except ObjectDoesNotExist:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meal = Meal.objects.get(meal_id = data['meal_id'])
    except exceptions.ValidationError:
        return Response({"message":'No Such Meal In Cart'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart_item = CartItem.objects.get(meal=meal, cart_item_owner= customer)
        cart_item.quantity += 1
        cart_item.save()
        return Response({'message' : 'Increased Amount'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message' : 'Meal Not In Cart'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def decrease_meal_amount(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        raise PermissionDenied
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=token).user) 
    except ObjectDoesNotExist:
        raise PermissionDenied
    try:
        data = json.loads(request.body)
        meal = Meal.objects.get(meal_id = data['meal_id'])
    except Exception as e :
        return Response({"message":'No Such Meal In The Cart'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart_item = CartItem.objects.get(meal=meal, cart_item_owner= customer)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({'message' : 'Decreased Amount'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Decreased Amount Level Reached'} ,status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        return Response({'message' : 'Meal Not In Cart'}, status=status.HTTP_204_NO_CONTENT)




""" @api_view(['POST'])
def edit_category(request):
    try:
        category_name = request.POST['category_name']
        operation = int(request.POST['operation_id']) # 1 for remove
    except MultiValueDictKeyError:
        return redirect('users/add_meal.html', {'error' : 'please pass requried info'})
    category, created = Category.objects.get_or_create(category_name=category_name)
    try:
        category_image = request.POST['category_image']
        category.category_image = category_image
    except Exception as e:
        pass
    if operation == 0:
        category.category_name = category_name
        return JsonResponse({'message': 'Success'})
    elif operation == 1:
        category.delete()
    return JsonResponse({'message': 'Category Deleted'})
 """
""" 
class SearchView(ListAPIView):
    def list(self, request, *args, **kwargs):
        try:
            min_price = int(request.GET.get('min_price'))
            max_price = int(request.GET.get('max_price'))
            if min_price is not None and max_price is not None:
                try:
                    customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
                    role = customer.role
                    if role == "NormalCustomer":
                        queryset = Meal.objects.filter(customer_meal_price__gt=min_price, customer_meal_price__lt=max_price)
                    elif role == "SuperMarketCustomer":
                        queryset = Meal.objects.filter(supermarket_meal_price__gt=min_price, supermarket_meal_price__lt=max_price)
                    elif role == "RestaurantCustomer":
                        queryset = Meal.objects.filter(restaurant_meal_price__gt=min_price, restaurant_meal_price__lt=max_price)
                    elif role == "AgentCustomer":
                        queryset = Meal.objects.filter(agent_meal_price__gt=min_price, agent_meal_price__lt=max_price)
                    elif role == "CompanyCustomer":
                        queryset = Meal.objects.filter(company_meal_price__gt=min_price, company_meal_price__lt=max_price)
                except Exception as e:
                    queryset = Meal.objects.filter(customer_meal_price__gt=min_price, customer_meal_price__lt=max_price)
                meal_rating  = float(request.GET.get('meal_rating'))
                if meal_rating is not None:
                    queryset = queryset.filter(meal_rating=meal_rating)
                category_id = request.GET.get['category_id']
                try:
                    meal_category = Category.objects.get(category_id=category_id)
                    queryset = queryset.filter(meal_category=meal_category)
                except Exception as e:
                    pass
                response_data = []
                for meal in queryset:
                    response_data.append({
                        "meal" : MainMealSerializer(meal).data,
                        "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
                    })
                return Response(response_data)
        except Exception as e:
            pass
        try:
            rating  = float(request.GET.get('meal_rating'))
            if rating is not None:
                queryset = Meal.objects.filter(meal_rating=rating)
                try:
                    meal_category = Category.objects.get(category_id=category_id)
                    queryset = queryset.filter(meal_category=meal_category)
                except Exception as e:
                    pass
                response_data = []
                for meal in queryset:
                    response_data.append({
                        "meal" : MainMealSerializer(meal).data,
                        "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
                    })
                return Response(response_data)
        except Exception as e:
            pass
        category_id=request.GET.get('category_id')
        if category_id is not None:
                category = Category.objects.get(category_id=category_id)
                queryset = Meal.objects.filter(meal_category=category)
                response_data = []
                for meal in queryset:
                    response_data.append({
                        "meal" : MainMealSerializer(meal).data,
                        "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
                    })
                return Response(response_data)

        meal_name = request.GET.get('meal_name')
        if meal_name is not None:
                queryset = Meal.objects.filter(meal_name=meal_name)
                response_data = []
                for meal in queryset:
                    response_data.append({
                        "meal" : MainMealSerializer(meal).data,
                        "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
                    })
                return Response(response_data)

        meal_name_ar = request.GET.get('meal_name_ar')
        if meal_name_ar is not None:
                queryset = Meal.objects.filter(meal_name_ar=meal_name_ar)
                response_data = []
                for meal in queryset:
                    response_data.append({
                        "meal" : MainMealSerializer(meal).data,
                        "meal_images" : MealImageSerializer(MealImage.objects.filter(meal=meal), many=True).data
                    })
                return Response(response_data)
    
        return Response({'message': 'Please Pass Valid Parametres'}, status=status.HTTP_400_BAD_REQUEST)
 """

#For Admin Panel


def add_meal(request):
    try:
        meal_name = request.POST['meal_name']
        meal_description = request.POST['meal_description']
        category_id = request.POST['category_id']
        meal_price = int(request.POST['meal_price'])
        meal_images = request.POST['meal_images']
    except MultiValueDictKeyError:
        return redirect('products/add_meal.html', {'error' : 'please pass requried info'})
    try:
        meal_category = Category.objects.get(category_id=category_id)
    except ObjectDoesNotExist:
        return redirect('products/add_meal.html', {'error' : 'please pass Correct Category'})
    meal = Meal.objects.create(meal_name=meal_name, meal_description=meal_description, 
    meal_price=meal_price, meal_category=meal_category
    )
    meal.save()
    meal = Meal.objects.create()
    for image in meal_images:
        meal_image = MealImage.objects.create(meal=meal, image=image)
        meal_image.save()
    return redirect('home.html', {})


def add_category(request):
    try:
        category_name = request.POST['category_name']
    except MultiValueDictKeyError:
        return redirect('users/add_meal.html', {'error' : 'please pass requried info'})
    try:
        category = Category.objects.get(category_name=category_name)
        if category:
            return redirect('products/add_category.html', {'error' : 'Category Already There'})
    except ObjectDoesNotExist:
        category = Category.objects.create(category_name=category_name)
        category.save()
    return redirect('home.html', {})


''' 
def add_property(request):
    try:
        property_name = request.POST['property_name']
        meal_id = request.POST['meal_id']
    except MultiValueDictKeyError:
        return redirect('users/add_property.html', {'error' : 'please pass requried info'})
    try:
        property = Offer.objects.get(property_name=property_name)
        if property:
            return redirect('products/add_property.html', {'error' : 'Property Already There'})
    except ObjectDoesNotExist:
        try:
            meal = Meal.objects.get(meal_id=meal_id)
        except exceptions.ValidationError:
            return redirect('products/add_property.html', {'error' : 'Please Pass Valid Meal'})
        property = Offer.objects.create(property_name=property_name, meal=meal)
        property.save()
    return redirect('home.html', {})

 '''

@api_view(['GET'])
def customer_points(request):
    try:
        customer = Customer.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
    except Exception as e:
        raise PermissionDenied
    orders = OrderSerializer(Order.objects.filter(ordered_by=customer),many=True).data
    return JsonResponse({
        'orders' : orders
    })