import random
import string

from rest_framework import serializers
from django.db import transaction

from .models import Recipe, RecipeIngredient
from ingredient.models import Ingredient
from user.serializers import CustomUserSerializer, Base64ImageField
from core.models import FavoriteRecipe, ShoppingCart, ShortLink


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientForRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'name', 'text', 'cooking_time', 'image')

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "You need to add at least one ingredient."
            )

        ingredients_ids = [item['id'].id for item in value]
        if len(ingredients_ids) != len(set(ingredients_ids)):
            raise serializers.ValidationError("Ingredients must be unique.")

        return value

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        if ingredients_data is None or not ingredients_data:
            raise serializers.ValidationError(
                {'ingredients': [
                    'This field is required and cannot be empty.'
                ]
                }
            )
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )

        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount']
            ) for ingredient_data in ingredients_data
        ]

        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        if ingredients_data is None or not ingredients_data:
            raise serializers.ValidationError(
                {'ingredients': [
                    'This field is required and cannot be empty.'
                ]
                }
            )
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update ingredients if provided
        instance.recipe_ingredients.all().delete()
        recipe_ingredients = [
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount']
            ) for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeShortLinkSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('short-link',)

    def get_short_link(self, obj):
        request = self.context.get('request')
        host = request.get_host() if request else 'foodgram.example.org'
        protocol = 'https' if request and request.is_secure() else 'http'
        try:
            short_link = obj.short_link
        except ShortLink.DoesNotExist:
            code = ''.join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
            short_link = ShortLink.objects.create(recipe=obj, short_code=code)
        return f"{protocol}://{host}/s/{short_link.short_code}"  # noqa: E231

    def to_representation(self, instance):
        return {'short-link': self.get_short_link(instance)}
