from django.contrib.auth.models import User
from rest_framework import serializers\


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({"error": "Both passwords must be same"})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user