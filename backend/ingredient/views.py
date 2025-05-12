from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            # Search for ingredients that start with the provided name
            queryset = queryset.filter(name__istartswith=name)
        return queryset 