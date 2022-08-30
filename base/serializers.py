from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import *
# from rest_auth.serializers import ChangePasswordSerializer

class UserSerializer(serializers.ModelSerializer):
    name= serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = ['id','_id','username','email','name','isAdmin']

    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

    def get_name(self,obj):
        name = obj.first_name
        if name=="":
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =User
        fields = ['id','_id','username','email','name','isAdmin','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    image = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



# class AddImgSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AddImg
#         fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Product 
        fields = '__all__'

    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    User = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self,obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items,many=True)
        return serializer.data

    def get_shippingAddress(self,obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress,many=False).data
        except:
            address = False
        return address

    def get_User(self,obj):
        items = obj.user
        serializer = UserSerializer(items,many=False)
        return serializer.data

    


# class CustomPasswordResetSerializer(PasswordResetSerializer):
#     email = serializers.EmailField()
#     password_reset_form_class = ResetPasswordForm

#     def validate_email(self, value):
#         # Create PasswordResetForm with the serializer
#         self.reset_form = self.password_reset_form_class(data=self.initial_data)
#         if not self.reset_form.is_valid():
#             raise serializers.ValidationError(self.reset_form.errors)

#         ###### FILTER YOUR USER MODEL ######
#         if not get_user_model().objects.filter(email=value).exists():
#             raise serializers.ValidationError(_('Invalid e-mail address'))

#         return value

#     def save(self):
#         request = self.context.get('request')
#         # Set some values to trigger the send_email method.
#         opts = {
#             'use_https': request.is_secure(),
#             'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
#             'request': request,
#         }
#         opts.update(self.get_email_options())
#         self.reset_form.save(**opts)




# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
    
#     class Meta:
#         model = User
#         fields = '__all__'


