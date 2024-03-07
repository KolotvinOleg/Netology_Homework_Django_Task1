from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def validate_positions(self, value):
        if not value:
            raise serializers.ValidationError('Не указаны позиции заказа')
        product_ids = [item['product'].id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('Дублируются позиции в заказе')
        return value

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock, product=position['product'], quantity=position['quantity'],
                                        price=position['price'])
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        positions_update = StockProduct.objects.filter(stock=stock)
        for position in positions:
            pos = positions_update.get(product=position['product'])
            pos.quantity = position['quantity']
            pos.price = position['price']
            pos.save()
        return stock
