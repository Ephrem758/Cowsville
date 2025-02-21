from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q

from AlertSystem.sendMesage import send_alert
from .models import Cow, Farm, Message, Reproduction, Inseminator
from .serializers import FarmSerializer, CowSerializer, MessageSerializer, InseminatorSerializer
from django.utils.timezone import now


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['farm_id', 'owner_name', 'address']

    def get_queryset(self):
        queryset = Farm.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(farm_id__icontains=search_query) |
                Q(owner_name__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        return queryset

    @action(detail=True, methods=['post'])
    def change_inseminator(self, request, pk=None):
        try:
            farm = self.get_object()
            inseminator_id = request.data.get('inseminator_id')
            
            if not inseminator_id:
                return Response(
                    {'error': 'inseminator_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                new_inseminator = Inseminator.objects.get(id=inseminator_id)
            except Inseminator.DoesNotExist:
                return Response(
                    {'error': 'Inseminator not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Store old inseminator for message
            old_inseminator = farm.inseminator

            # Update farm's inseminator
            farm.inseminator = new_inseminator
            farm.save()

            # Send notifications
            if old_inseminator:
                # Notify old inseminator
                old_message = (
                    f"Notice: You have been unassigned from farm: {farm.farm_id} "
                    f"({farm.owner_name})"
                )
                send_alert(old_inseminator.phone_number, old_message)

            # Notify new inseminator
            new_message = (
                f"Notice: You have been assigned to a new farm:\n"
                f"Farm ID: {farm.farm_id}\n"
                f"Owner: {farm.owner_name}\n"
                f"Address: {farm.address}\n"
                f"Phone: {farm.telephone_number}"
            )
            send_alert(new_inseminator.phone_number, new_message)

            return Response({
                'message': 'Inseminator changed successfully',
                'farm_id': farm.farm_id,
                'new_inseminator': new_inseminator.name
            })

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cow_id', 'breed__name']

    def get_queryset(self):
        queryset = Cow.objects.all()
        farm_id = self.request.query_params.get('farm_id', None)
        search_query = self.request.query_params.get('search', None)

        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)
        
        if search_query:
            queryset = queryset.filter(
                Q(cow_id__icontains=search_query) |
                Q(breed__name__icontains=search_query)
            )
        
        return queryset

    @action(detail=False, methods=['post'])
    def record_heat_sign(self, request):
        try:
            # Get required data from request
            farm_id = request.data.get('farm_id')
            cow_id = request.data.get('cow_id')
            heat_signs = request.data.get('heat_signs', '')
            
            if not all([farm_id, cow_id]):
                return Response(
                    {'error': 'farm_id and cow_id are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                cow = Cow.objects.get(farm__farm_id=farm_id, cow_id=cow_id)
            except Cow.DoesNotExist:
                return Response(
                    {'error': 'Cow not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if farm has an assigned inseminator
            if not cow.farm.inseminator:
                return Response(
                    {'error': 'No inseminator assigned to this farm'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not cow.farm.inseminator.is_active:
                return Response(
                    {'error': 'Assigned inseminator is not active'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Record heat sign
            reproduction, created = Reproduction.objects.get_or_create(
                cow=cow,
                farm=cow.farm,
                defaults={
                    'is_cow_pregnant': False,
                    'heat_sign_start': now(),
                    'heat_signs_seen': heat_signs
                }
            )

            if not created:
                reproduction.heat_sign_start = now()
                reproduction.heat_signs_seen = heat_signs
                reproduction.save()

            # Send alert to inseminator
            inseminator_message = (
                f"🐄 Insemination Alert!\n"
                f"Farm: {cow.farm.farm_id} - {cow.farm.owner_name}\n"
                f"Address: {cow.farm.address}\n"
                f"Phone: {cow.farm.telephone_number}\n"
                f"Cow ID: {cow.cow_id}\n"
                f"Heat Signs: {heat_signs}\n"
                f"Please visit for insemination check."
            )
            
            inseminator_response = send_alert(
                cow.farm.inseminator.phone_number, 
                inseminator_message
            )

            if inseminator_response.get('status') == 'success':
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=inseminator_message,
                    message_type='inseminator_alert',
                    is_sent=True
                )

            # Send confirmation to farmer
            farmer_message = (
                f"🔔 Alert: Your inseminator ({cow.farm.inseminator.name}) "
                f"has been notified about your cow (Cow ID: {cow.cow_id}) "
                f"showing heat signs. They will visit your farm soon."
            )
            
            farmer_response = send_alert(
                cow.farm.telephone_number, 
                farmer_message
            )

            if farmer_response.get('status') == 'success':
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type='farmer_alert',
                    is_sent=True
                )

            return Response({
                'message': 'Heat sign recorded and alerts sent successfully',
                'cow_id': cow_id,
                'farm_id': farm_id,
                'heat_sign_time': reproduction.heat_sign_start,
                'alerts_sent': True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_text', 'message_type']

    def get_queryset(self):
        queryset = Message.objects.all()
        farm_id = self.request.query_params.get('farm_id', None)
        cow_id = self.request.query_params.get('cow_id', None)

        # If only cow_id is provided without farm_id, we can't uniquely identify the cow
        if cow_id and not farm_id:
            return Message.objects.none()  # Return empty queryset
        
        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
            if cow_id:
                # Now we can safely filter by cow_id since we have the farm context
                queryset = queryset.filter(cow__cow_id=cow_id)

        return queryset

class InseminatorViewSet(viewsets.ModelViewSet):
    queryset = Inseminator.objects.all()
    serializer_class = InseminatorSerializer

    @action(detail=True, methods=['post'])
    def replace_inseminator(self, request, pk=None):
        try:
            old_inseminator = self.get_object()
            new_phone = request.data.get('phone_number')
            new_name = request.data.get('name')
            new_address = request.data.get('address')
            
            if not all([new_phone, new_name, new_address]):
                return Response(
                    {'error': 'phone_number, name, and address are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update inseminator details
            old_inseminator.phone_number = new_phone
            old_inseminator.name = new_name
            old_inseminator.address = new_address
            old_inseminator.save()

            # Get all associated farms
            affected_farms = Farm.objects.filter(inseminator=old_inseminator)

            # Notify all affected farms
            for farm in affected_farms:
                message = (
                    f"Notice: Your inseminator's details have been updated:\n"
                    f"Name: {new_name}\n"
                    f"Phone: {new_phone}\n"
                    f"Address: {new_address}"
                )
                send_alert(farm.telephone_number, message)

            return Response({
                'message': 'Inseminator details updated successfully',
                'affected_farms_count': affected_farms.count(),
                'new_details': {
                    'name': new_name,
                    'phone': new_phone,
                    'address': new_address
                }
            })

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

