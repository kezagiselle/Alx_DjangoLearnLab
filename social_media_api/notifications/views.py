from rest_framework import generics, permissions, serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    target = serializers.StringRelatedField() # Simple string representation

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp', 'read']

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
