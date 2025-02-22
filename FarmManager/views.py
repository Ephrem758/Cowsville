from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now, timezone

from AlertSystem.sendMesage import send_alert
from .models import Cow, Farm, Message, Reproduction, Inseminator, Doctor, Health, BreedType, HousingType, FloorType, FeedingFrequency, WaterSource, GynecologicalStatus, UdderHealthStatus, MastitisStatus, GeneralHealthStatus, FarmerMedicalReport, MedicalAssessment, InseminationRecord
from .serializers import FarmSerializer, CowSerializer, MessageSerializer, InseminatorSerializer, HealthSerializer, ReproductionSerializer, BreedTypeSerializer, HousingTypeSerializer, FloorTypeSerializer, FeedingFrequencySerializer, WaterSourceSerializer, GynecologicalStatusSerializer, UdderHealthStatusSerializer, MastitisStatusSerializer, GeneralHealthStatusSerializer


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

            # Similar update needed for inseminator assignment
            Message.objects.create(
                farm=farm,
                cow=None,  # Yes, cow field is nullable based on the model definition
                message_text=new_message,
                message_type='inseminator_assignment',
                is_sent=True
            )

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

    @action(detail=True, methods=['post'])
    def change_doctor(self, request, pk=None):
        try:
            farm = self.get_object()
            doctor_id = request.data.get('doctor_id')
            
            if not doctor_id:
                return Response(
                    {'error': 'doctor_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                new_doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                return Response(
                    {'error': 'Doctor not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            if not new_doctor.is_active:
                return Response(
                    {'error': 'Selected doctor is not active'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Store old doctor for message
            old_doctor = farm.doctor

            # Update farm's doctor
            farm.doctor = new_doctor
            farm.save()

            # Send notifications
            if old_doctor:
                # Notify old doctor
                old_message = (
                    f"Notice: You have been unassigned from farm: {farm.farm_id} "
                    f"({farm.owner_name})"
                )
                send_alert(old_doctor.phone_number, old_message)

            # Notify new doctor
            new_message = (
                f"Notice: You have been assigned to a new farm:\n"
                f"Farm ID: {farm.farm_id}\n"
                f"Owner: {farm.owner_name}\n"
                f"Address: {farm.address}\n"
                f"Phone: {farm.telephone_number}"
            )
            send_alert(new_doctor.phone_number, new_message)

            # Notify farmer
            farmer_message = (
                f"Notice: Your farm's doctor has been changed to Dr. {new_doctor.name}. "
                f"Contact number: {new_doctor.phone_number}"
            )
            send_alert(farm.telephone_number, farmer_message)

            # Create message record
            Message.objects.create(
                farm=farm,
                cow=None,
                message_text=old_message,
                message_type='doctor_assignment',
                is_sent=True
            )

            return Response({
                'message': 'Doctor changed successfully',
                'farm_id': farm.farm_id,
                'new_doctor': new_doctor.name
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

    @action(detail=False, methods=['post'])
    def monitor_pregnancy(self, request):
        try:
            # Get data from request
            farm_id = request.data.get('farm_id')
            cow_id = request.data.get('cow_id')
            is_pregnant = request.data.get('is_pregnant')
            lactation_number = request.data.get('lactation_number')

            # Validate required fields
            if not all([farm_id, cow_id, is_pregnant is not None]):
                return Response(
                    {'error': 'farm_id, cow_id, and pregnancy status are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the cow
            try:
                cow = Cow.objects.get(farm__farm_id=farm_id, cow_id=cow_id)
            except Cow.DoesNotExist:
                return Response(
                    {'error': 'Cow not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Update or create reproduction record
            reproduction, created = Reproduction.objects.get_or_create(
                cow=cow,
                farm=cow.farm,
                defaults={
                    'is_cow_pregnant': is_pregnant,
                    'lactation_number': lactation_number
                }
            )

            if not created:
                reproduction.is_cow_pregnant = is_pregnant
                if lactation_number:
                    reproduction.lactation_number = lactation_number
                reproduction.save()

            # Send notifications if pregnancy status changed
            if reproduction.is_cow_pregnant:
                # Notify farmer about confirmed pregnancy
                message_text = (
                    f"Pregnancy Confirmed: Cow {cow_id} from Farm {farm_id} "
                    f"is pregnant. Lactation number: {lactation_number}"
                )
            else:
                message_text = (
                    f"Pregnancy Status Update: Cow {cow_id} from Farm {farm_id} "
                    f"is not pregnant. Lactation number: {lactation_number}"
                )

            # Create message record
            Message.objects.create(
                farm=cow.farm,
                cow=cow,
                message_text=message_text,
                message_type='pregnancy_update',
                is_sent=True
            )

            # Send alert to farmer
            send_alert(cow.farm.telephone_number, message_text)

            return Response({
                'message': 'Pregnancy monitoring record updated successfully',
                'cow_id': cow_id,
                'farm_id': farm_id,
                'is_pregnant': is_pregnant,
                'lactation_number': lactation_number
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def farmer_medical_assessment(self, request):
        try:
            # Get required data from request
            farm_id = request.data.get('farm_id')
            cow_id = request.data.get('cow_id')
            sickness_description = request.data.get('sickness_description')

            # Validate required fields
            if not all([farm_id, cow_id, sickness_description]):
                return Response(
                    {'error': 'farm_id, cow_id, and sickness_description are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                cow = Cow.objects.get(farm__farm_id=farm_id, cow_id=cow_id)
            except Cow.DoesNotExist:
                return Response(
                    {'error': 'Cow not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create farmer medical report
            report = FarmerMedicalReport.objects.create(
                farm=cow.farm,
                cow=cow,
                sickness_description=sickness_description
            )

            # Notify farm's doctor if assigned
            if cow.farm.doctor:
                doctor_message = (
                    f"🚨 New Farmer Medical Report!\n"
                    f"Farm: {farm_id}\n"
                    f"Cow: {cow_id}\n"
                    f"Reported Issue: {sickness_description}\n"
                    f"Please review this report."
                )
                send_alert(cow.farm.doctor.phone_number, doctor_message)

                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=doctor_message,
                    message_type='health_alert',
                    is_sent=True
                )

            return Response({
                'message': 'Medical assessment submitted successfully',
                'report_id': report.id,
                'farm_id': farm_id,
                'cow_id': cow_id,
                'reported_date': report.reported_date
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def doctor_assessment(self, request):
        try:
            # Get required data from request
            farm_id = request.data.get('farm_id')
            cow_id = request.data.get('cow_id')
            doctor_id = request.data.get('doctor_id')
            
            # Health status data
            is_cow_sick = request.data.get('is_cow_sick')
            sickness_type = request.data.get('sickness_type')
            general_health_id = request.data.get('general_health')
            udder_health_id = request.data.get('udder_health')
            mastitis_id = request.data.get('mastitis')
            body_condition_score = request.data.get('body_condition_score')
            reproductive_health = request.data.get('reproductive_health')
            metabolic_disease = request.data.get('metabolic_disease')
            
            # Vaccination data
            is_vaccinated = request.data.get('is_cow_vaccinated')
            vaccination_date = request.data.get('vaccination_date')
            vaccination_type = request.data.get('vaccination_type')
            
            # Deworming data
            has_deworming = request.data.get('has_deworming')
            deworming_date = request.data.get('deworming_date')
            deworming_type = request.data.get('deworming_type')
            
            # Assessment details
            diagnosis = request.data.get('diagnosis')
            treatment = request.data.get('treatment')
            prescription = request.data.get('prescription')
            next_assessment = request.data.get('next_assessment_date')
            notes = request.data.get('notes')

            # Validate required fields
            required_fields = {
                'farm_id': farm_id,
                'cow_id': cow_id,
                'doctor_id': doctor_id,
                'is_cow_sick': is_cow_sick is not None,
                'general_health': general_health_id,
                'udder_health': udder_health_id,
                'mastitis': mastitis_id,
                'body_condition_score': body_condition_score,
                'reproductive_health': reproductive_health
            }

            missing_fields = [k for k, v in required_fields.items() if not v]
            if missing_fields:
                return Response(
                    {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate sickness type if cow is sick
            if is_cow_sick and not sickness_type:
                return Response(
                    {'error': 'Sickness type is required when cow is sick'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get required objects
            try:
                cow = Cow.objects.get(farm__farm_id=farm_id, cow_id=cow_id)
                doctor = Doctor.objects.get(id=doctor_id)
            except (Cow.DoesNotExist, Doctor.DoesNotExist):
                return Response(
                    {'error': 'Cow or Doctor not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create medical assessment
            assessment = MedicalAssessment.objects.create(
                farm=cow.farm,
                cow=cow,
                assessed_by=doctor,
                is_cow_sick=is_cow_sick,
                sickness_type=sickness_type,
                general_health_id=general_health_id,
                udder_health_id=udder_health_id,
                mastitis_id=mastitis_id,
                body_condition_score=body_condition_score,
                reproductive_health=reproductive_health,
                metabolic_disease=metabolic_disease,
                is_cow_vaccinated=is_vaccinated,
                vaccination_date=vaccination_date,
                vaccination_type=vaccination_type,
                has_deworming=has_deworming,
                deworming_date=deworming_date,
                deworming_type=deworming_type,
                diagnosis=diagnosis,
                treatment=treatment,
                prescription=prescription,
                next_assessment_date=next_assessment,
                notes=notes
            )

            # Notify farmer
            farmer_message = (
                f"Medical Assessment Complete\n"
                f"Cow: {cow_id}\n"
                f"Doctor: Dr. {doctor.name}\n"
                f"Health Status: {'Sick' if is_cow_sick else 'Healthy'}\n"
                f"Body Condition Score: {body_condition_score}\n"
                f"Diagnosis: {diagnosis}\n"
                f"Treatment: {treatment}\n"
                f"Next Assessment: {next_assessment}"
            )
            
            send_alert(cow.farm.telephone_number, farmer_message)
            
            Message.objects.create(
                farm=cow.farm,
                cow=cow,
                message_text=farmer_message,
                message_type='health_alert',
                is_sent=True
            )

            return Response({
                'message': 'Medical assessment recorded successfully',
                'assessment_id': assessment.id,
                'farm_id': farm_id,
                'cow_id': cow_id,
                'assessment_date': assessment.assessment_date,
                'next_assessment_date': next_assessment
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def monitor_heat_sign(self, request):
        try:
            # Get required data from request
            farm_id = request.data.get('farm_id')
            cow_id = request.data.get('cow_id')
            is_inseminated = request.data.get('is_inseminated')
            insemination_time = request.data.get('insemination_time')  # format: "HH:mm"
            insemination_count = request.data.get('insemination_count')
            lactation_number = request.data.get('lactation_number')

            # Validate required fields
            if not all([farm_id, cow_id, is_inseminated is not None, 
                       lactation_number is not None]):
                return Response(
                    {'error': 'farm_id, cow_id, is_inseminated, and lactation_number are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # If inseminated, time is required
            if is_inseminated and not insemination_time:
                return Response(
                    {'error': 'insemination_time is required when cow is inseminated'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                cow = Cow.objects.get(farm__farm_id=farm_id, cow_id=cow_id)
            except Cow.DoesNotExist:
                return Response(
                    {'error': 'Cow not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get the inseminator from the farm
            inseminator = cow.farm.inseminator
            if not inseminator:
                return Response(
                    {'error': 'No inseminator assigned to this farm'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create insemination record
            record = InseminationRecord.objects.create(
                farm=cow.farm,
                cow=cow,
                inseminator=inseminator,
                is_inseminated=is_inseminated,
                insemination_time=insemination_time if is_inseminated else None,
                insemination_count=insemination_count or 0,
                lactation_number=lactation_number
            )

            # Update cow's reproduction record
            reproduction, created = Reproduction.objects.get_or_create(
                cow=cow,
                farm=cow.farm
            )
            
            if is_inseminated:
                reproduction.last_insemination_date = timezone.now()
                reproduction.insemination_count = insemination_count or 0
                reproduction.save()

            # Send notifications
            if is_inseminated:
                farmer_message = (
                    f"Insemination Complete!\n"
                    f"Cow: {cow_id}\n"
                    f"Time: {insemination_time}\n"
                    f"Insemination Count: {insemination_count}\n"
                    f"Lactation Number: {lactation_number}"
                )
            else:
                farmer_message = (
                    f"Heat Sign Monitored\n"
                    f"Cow: {cow_id}\n"
                    f"Status: Not inseminated\n"
                    f"Lactation Number: {lactation_number}"
                )

            send_alert(cow.farm.telephone_number, farmer_message)
            
            Message.objects.create(
                farm=cow.farm,
                cow=cow,
                message_text=farmer_message,
                message_type='inseminator_alert',
                is_sent=True
            )

            return Response({
                'message': 'Heat sign monitoring recorded successfully',
                'record_id': record.id,
                'farm_id': farm_id,
                'cow_id': cow_id,
                'is_inseminated': is_inseminated,
                'insemination_time': insemination_time,
                'lactation_number': lactation_number
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

class HealthViewSet(viewsets.ModelViewSet):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cow__cow_id', 'farm__farm_id']

    def get_queryset(self):
        queryset = Health.objects.all()
        farm_id = self.request.query_params.get('farm_id', None)
        cow_id = self.request.query_params.get('cow_id', None)
        
        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id and farm_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
            
        return queryset

class ReproductionViewSet(viewsets.ModelViewSet):
    queryset = Reproduction.objects.all()
    serializer_class = ReproductionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cow__cow_id', 'farm__farm_id']

    def get_queryset(self):
        queryset = Reproduction.objects.all()
        farm_id = self.request.query_params.get('farm_id', None)
        cow_id = self.request.query_params.get('cow_id', None)
        is_pregnant = self.request.query_params.get('is_pregnant', None)
        
        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id and farm_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
        if is_pregnant is not None:
            queryset = queryset.filter(is_cow_pregnant=is_pregnant.lower() == 'true')
            
        return queryset

# Choice Models ViewSets (Read-only)
class BreedTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BreedType.objects.all()
    serializer_class = BreedTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'display_name']

class HousingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HousingType.objects.all()
    serializer_class = HousingTypeSerializer
    search_fields = ['name', 'display_name']

class FloorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FloorType.objects.all()
    serializer_class = FloorTypeSerializer
    search_fields = ['name', 'display_name']

class FeedingFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedingFrequency.objects.all()
    serializer_class = FeedingFrequencySerializer
    search_fields = ['name', 'display_name']

class WaterSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WaterSource.objects.all()
    serializer_class = WaterSourceSerializer
    search_fields = ['name', 'display_name']

class GynecologicalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GynecologicalStatus.objects.all()
    serializer_class = GynecologicalStatusSerializer
    search_fields = ['name', 'display_name']

class UdderHealthStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UdderHealthStatus.objects.all()
    serializer_class = UdderHealthStatusSerializer
    search_fields = ['name', 'display_name']

class MastitisStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MastitisStatus.objects.all()
    serializer_class = MastitisStatusSerializer
    search_fields = ['name', 'display_name']

class GeneralHealthStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeneralHealthStatus.objects.all()
    serializer_class = GeneralHealthStatusSerializer
    search_fields = ['name', 'display_name']

