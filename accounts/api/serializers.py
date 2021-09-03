from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class LoginSerializer(serializers.Serializer):
    # 这里的变量名会作为前端显示的要填写的内容
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer):
    # 用modelSerializer是为了最后点save时，可以把这个实例创建出来
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        # 表示创建user的时候，只会填以下几部分
        fields = ('username', 'email', 'password')

    # will be called when is_valid is called
    def valid(self, data):
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username = username,
            email=email,
            password=password
        )
        return user