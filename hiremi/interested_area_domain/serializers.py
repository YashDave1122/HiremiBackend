# from rest_framework import serializers
# from .models import SelectedDomain

# class SelectedDomainSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SelectedDomain
#         fields = ['id', 'register', 'items']
#         extra_kwargs = {
#             'register': {'required': True}
#         }

#     def create(self, validated_data):
#         # Ensure items are stored as comma-separated string
#         items = validated_data.get('items', '')
#         if isinstance(items, list):
#             validated_data['items'] = ','.join(items)
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # Handle list to string conversion during update
#         items = validated_data.get('items', instance.items)
#         if isinstance(items, list):
#             validated_data['items'] = ','.join(items)
#         return super().update(instance, validated_data)


from rest_framework import serializers
from .models import SelectedDomain

class SelectedDomainSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.CharField(max_length=255), 
        write_only=True  # Ensures proper input
    )
    selected_domains = serializers.SerializerMethodField()  # For readable output

    class Meta:
        model = SelectedDomain
        fields = ['id', 'register', 'items', 'selected_domains']
        extra_kwargs = {
            'register': {'required': True, 'read_only': True}  # Prevents user from manually setting it
        }

    def get_selected_domains(self, obj):
        """Convert stored string back to a list for readability"""
        return obj.items.split(',') if obj.items else []

    def validate_items(self, value):
        """Ensure no more than 5 domains are selected"""
        if len(value) > 5:
            raise serializers.ValidationError("You can select at most 5 domains.")
        return value

    def create(self, validated_data):
        """Convert list to comma-separated string before saving"""
        validated_data['items'] = ','.join(validated_data.pop('items'))
        validated_data['register'] = self.context['request'].user  # Ensure register is current user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Convert list to string for storage"""
        items = validated_data.pop('items', instance.items.split(','))
        instance.items = ','.join(items)
        instance.save()
        return instance
