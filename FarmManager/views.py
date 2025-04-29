import logging
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from AlertSystem.sendMesage import send_alert
from .models import (
    Cow,
    Farm,
    Message,
    Reproduction,
    Inseminator,
    Doctor,
    MedicalAssessment,  # Changed from Health
    BreedType,
    HousingType,
    FloorType,
    FeedingFrequency,
    WaterSource,
    GynecologicalStatus,
    UdderHealthStatus,
    MastitisStatus,
    GeneralHealthStatus,
    FarmerMedicalReport,
    InseminationRecord,
)
from .serializers import (
    FarmSerializer,
    CowSerializer,
    HeatSignRecordSerializer,
    MessageSerializer,
    InseminatorSerializer,
    ReproductionSerializer,
    BreedTypeSerializer,
    HousingTypeSerializer,
    FloorTypeSerializer,
    FeedingFrequencySerializer,
    WaterSourceSerializer,
    GynecologicalStatusSerializer,
    UdderHealthStatusSerializer,
    MastitisStatusSerializer,
    GeneralHealthStatusSerializer,
    FarmerMedicalReportSerializer,
    MedicalAssessmentSerializer,
    InseminationRecordSerializer,
    InseminatorAssignmentSerializer,
    DoctorAssignmentSerializer,
    MonitorPregnancySerializer,
    FarmerMedicalAssessmentSerializer,
    DoctorMedicalAssessmentSerializer,
    MonitorHeatSignSerializer,
    DoctorSerializer,
    MonitorBirthSerializer,
)

# initiating the logger
logger = logging.getLogger(__name__)


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["farm_id", "owner_name", "address"]
    logger = logging.getLogger(__name__)

    @action(detail=True, methods=["post"])
    def change_inseminator(self, request, pk=None):
        farm = self.get_object()
        logger.info(f"Request to change inseminator for farm {farm.farm_id}")

        serializer = InseminatorAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid data for inseminator change: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Validated inseminator change request for farm {farm.farm_id}")
        return self._change_staff(
            request,
            "inseminator",
            serializer.validated_data["inseminator_id"],
            "inseminator_assignment",
        )

    @action(detail=True, methods=["post"])
    def change_doctor(self, request, pk=None):
        farm = self.get_object()
        logger.info(f"Request to change doctor for farm {farm.farm_id}")

        serializer = DoctorAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid data for doctor change: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Validated doctor change request for farm {farm.farm_id}")
        return self._change_staff(
            request,
            "doctor",
            serializer.validated_data["doctor_id"],
            "doctor_assignment",
        )

    def _change_staff(self, request, staff_type, staff_id, message_type):
        farm = self.get_object()
        logger.info(
            f"Attempting to change {staff_type} for farm {farm.farm_id} to staff ID {staff_id}"
        )

        try:
            with transaction.atomic():
                if staff_type == "inseminator":
                    StaffModel = Inseminator
                    old_staff = farm.inseminator
                    new_staff = StaffModel.objects.get(id=staff_id)
                    title = ""
                else:
                    StaffModel = Doctor
                    old_staff = farm.doctor
                    new_staff = StaffModel.objects.get(id=staff_id)
                    title = "Dr."

                logger.info(
                    f"Found new {staff_type} : {new_staff.name} (ID: {new_staff.id})"
                )

                if old_staff:
                    logger.info(
                        f"Replacing {staff_type} : {old_staff.name} (ID: {old_staff.id}) with {new_staff.name} (ID: {new_staff.id})"
                    )
                    old_staff.is_active = False
                else:
                    logger.info(f"No existing {staff_type} to replace")

                setattr(farm, staff_type, new_staff)
                farm.save(update_fields=[staff_type])

                logger.info(
                    f"Successfully updated farm {farm.farm_id} with new {staff_type}"
                )

                # send message to old staff
                if old_staff:
                    old_message = (
                        f"Notice: You have been unassigned from farm: {farm.farm_id} "
                        f"({farm.owner_name})"
                    )
                    try:
                        send_alert(old_staff.phone_number, old_message)
                        logger.info(
                            f"Notification sent to previous {staff_type} : {old_staff.name}"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to send notification to previous {staff_type} : {old_staff.name}. Error: {e}"
                        )

                # send message to new staff
                new_message = (
                    f"Notice: You have been assigned to a new farm:\n"
                    f"Farm ID: {farm.farm_id}\n"
                    f"Owner: {farm.owner_name}\n"
                    f"Address: {farm.address}\n"
                    f"Phone: {farm.telephone_number}"
                )
                try:
                    send_alert(new_staff.phone_number, new_message)
                    logger.info(
                        f"Notification sent to new {staff_type} : {new_staff.name}"
                    )
                except Exception as e:
                    logger.warning(
                        f"Failed to send notification to new {staff_type} : {new_staff.name}. Error: {e}"
                    )

                # Notify the farmer about the doctor change
                if staff_type == "doctor":
                    farmer_message = (
                        f"Notice: Your farm's doctor has been changed to {title}{new_staff.name}. "
                        f"Contact number: {new_staff.phone_number}"
                    )
                    try:
                        send_alert(farm.telephone_number, farmer_message)
                        logger.info(f"Notification sent to farmer about doctor change")
                    except Exception as e:
                        logger.warning(
                            f"Failed to send notification to farmer about doctor change. Error: {str(e)}"
                        )

                # Creating message record
                try:
                    Message.objects.create(
                        farm=farm,
                        cow=None,
                        message_text=new_message,
                        message_type=message_type,
                        is_sent=True,
                    )
                    logger.info(f"Message record created for {staff_type} change")
                except Exception as e:
                    logger.warning(
                        f"Failed to create message record for {staff_type} change. Error: {str(e)}"
                    )
                    raise

                logger.info(
                    f"Successfully compeleted the {staff_type} change process for farm {farm.farm_id}"
                )

                return Response(
                    {
                        "message": f"{staff_type} changed successfully",
                        "farm_id": farm.farm_id,
                        "new_staff_id": new_staff.id,
                        "old_staff_id": old_staff.id if old_staff else None,
                    }
                )

        except StaffModel.DoesNotExist:
            err_msg = f"{staff_type.capitalize()} with ID {staff_id} not found"
            logger.error(err_msg)

            return Response({"error": err_msg}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(
                f"An error occurred while changing {staff_type} for farm {farm.farm_id}: {str(e)}"
            )

            return Response(
                {
                    "error": f"Failed to change {staff_type} for farm {farm.farm_id}: Unexpected error"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["cow_id", "breed__name"]
    logger = logging.getLogger(__name__)
    filterset_fields = ['farm_id']

    def create(self, request, *args, **kwargs):
        """Create a new cow with logging"""
        self.logger.info(f"Received cow creation request with data: {request.data}")
        try:
            response = super().create(request, *args, **kwargs)
            self.logger.info(f"Successfully created cow with ID: {response.data.get('cow_id')}")
            return response
        except Exception as e:
            self.logger.error(f"Error creating cow: {str(e)}", exc_info=True)
            raise

    def update(self, request, *args, **kwargs):
        """Update a cow with logging"""
        self.logger.info(f"Received cow update request for cow {kwargs.get('pk')} with data: {request.data}")
        try:
            response = super().update(request, *args, **kwargs)
            self.logger.info(f"Successfully updated cow {kwargs.get('pk')}")
            return response
        except Exception as e:
            self.logger.error(f"Error updating cow {kwargs.get('pk')}: {str(e)}", exc_info=True)
            raise

    def destroy(self, request, *args, **kwargs):
        """Delete a cow with logging"""
        self.logger.info(f"Received cow deletion request for cow {kwargs.get('pk')}")
        try:
            response = super().destroy(request, *args, **kwargs)
            self.logger.info(f"Successfully deleted cow {kwargs.get('pk')}")
            return response
        except Exception as e:
            self.logger.error(f"Error deleting cow {kwargs.get('pk')}: {str(e)}", exc_info=True)
            raise

    def list(self, request, *args, **kwargs):
        """List cows with logging"""
        self.logger.info(f"Received cow list request with query params: {request.query_params}")
        try:
            response = super().list(request, *args, **kwargs)
            self.logger.info(f"Successfully retrieved {len(response.data)} cows")
            return response
        except Exception as e:
            self.logger.error(f"Error listing cows: {str(e)}", exc_info=True)
            raise

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single cow with logging"""
        self.logger.info(f"Received cow retrieve request for cow {kwargs.get('pk')}")
        try:
            response = super().retrieve(request, *args, **kwargs)
            self.logger.info(f"Successfully retrieved cow {kwargs.get('pk')}")
            return response
        except Exception as e:
            self.logger.error(f"Error retrieving cow {kwargs.get('pk')}: {str(e)}", exc_info=True)
            raise

    @action(detail=False, methods=['GET'])
    def by_farm(self, request):
        """Get all cows for a specific farm with logging"""
        farm_id = request.query_params.get('farm_id')
        self.logger.info(f"Received by_farm request for farm {farm_id}")
        
        if not farm_id:
            self.logger.warning("by_farm request missing farm_id parameter")
            return Response(
                {"error": "farm_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cows = self.get_queryset().filter(farm__farm_id=farm_id)
            serializer = self.get_serializer(cows, many=True)
            self.logger.info(f"Successfully retrieved {len(serializer.data)} cows for farm {farm_id}")
            
            return Response({
                "farm_id": farm_id,
                "total_cows": len(serializer.data),
                "cows": serializer.data
            })
        except Exception as e:
            self.logger.error(f"Error retrieving cows for farm {farm_id}: {str(e)}", exc_info=True)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        """Override perform_create to automatically create reproduction and medical assessment records"""
        try:
            with transaction.atomic():
                # Save the cow first
                cow = serializer.save()
                self.logger.info(f"Created new cow: {cow.cow_id} for farm {cow.farm.farm_id}")

                # Create reproduction record with data from the request
                Reproduction.objects.create(
                    cow=cow,
                    farm=cow.farm,
                    is_cow_pregnant=serializer.validated_data.get('is_pregnant', False),
                    pregnancy_date=serializer.validated_data.get('last_date_insemination'),
                    calving_date=serializer.validated_data.get('last_calving_date'),
                    heat_sign_start=None,
                    heat_signs_seen=None
                )
                self.logger.info(f"Created reproduction record for cow {cow.cow_id}")

                # Get default status objects
                general_health = GeneralHealthStatus.objects.get(name='Normal')
                udder_health = UdderHealthStatus.objects.get(name='4qt normal')
                mastitis = MastitisStatus.objects.get(name='Clinical mastitis')

                # Create medical assessment with data from the request
                MedicalAssessment.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    assessed_by=cow.farm.doctor,
                    is_cow_sick=False,
                    general_health=general_health,
                    udder_health=udder_health,
                    mastitis=mastitis,
                    has_lameness=serializer.validated_data.get('has_lameness', False),
                    body_condition_score=int(cow.bcs),
                    reproductive_health=serializer.validated_data.get('reproductive_health', 'Normal'),
                    metabolic_disease=serializer.validated_data.get('metabolic_disease', 'Normal'),
                    is_cow_vaccinated=serializer.validated_data.get('is_vaccinated', False),
                    vaccination_date=serializer.validated_data.get('vaccination_date'),
                    vaccination_type=serializer.validated_data.get('vaccination_type'),
                    has_deworming=serializer.validated_data.get('deworming', False),
                    deworming_date=serializer.validated_data.get('deworming_date'),
                    deworming_type=serializer.validated_data.get('deworming_type'),
                    diagnosis='',
                    treatment='',
                    prescription=''
                )
                self.logger.info(f"Created medical assessment for cow {cow.cow_id}")

        except Exception as e:
            self.logger.error(f"Error creating cow with reproduction and medical records: {str(e)}")
            raise

    @action(detail=False, methods=["post"])
    def record_heat_sign(self, request):

        self.logger.info("Received heat sign recording request")

        serializer = HeatSignRecordSerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(
                f"Invalid data for heat sign recording: {serializer.errors}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cow = serializer.validated_data["cow"]
            heat_signs = serializer.validated_data["heat_signs"]
            heat_start_time = serializer.validated_data["heat_start_time"]
            heat_sign_recorded_at = serializer.validated_data["heat_sign_recorded_at"]
            self.logger.info(
                f"Recording heat sign for cow {cow.cow_id} from farm {cow.farm.farm_id}"
            )

            # record heat sign
            reproduction = self._create_or_update_reproduction(cow, heat_signs, heat_start_time, heat_sign_recorded_at)

            # send message to farmer
            self._send_heat_sign_message(cow, heat_signs)

            self.logger.info(
                f"Successfully recorded heat sign for cow {cow.cow_id} from farm {cow.farm.farm_id}"
            )

            return Response(
                {
                    "message": "Heat sign recorded and alert sent successfully",
                    "cow_id": cow.cow_id,
                    "farm_id": cow.farm.farm_id,
                    "heat_sign_start": reproduction.heat_sign_start,
                    "heat_sign_recorded_at": reproduction.heat_sign_recorded_at,
                    "alert_sent": True,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            self.logger.error(
                f"An error occurred while recording heat sign for cow {cow.cow_id} from farm {cow.farm.farm_id}: {str(e)}"
            )

            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _create_or_update_reproduction(self, cow, heat_signs, heat_start_time, heat_sign_recorded_at=None):
        """create or update reproduction record based on heat signs"""
        self.logger.info(
            f"Creating or updating reproduction record for cow {cow.cow_id} from farm {cow.farm.farm_id}"
        )

        reproduction, created = Reproduction.objects.get_or_create(
            cow=cow,
            farm=cow.farm,
            defaults={
                "is_cow_pregnant": False,
                "heat_sign_start": heat_start_time,
                "heat_signs_seen": heat_signs,
                "heat_sign_recorded_at": heat_sign_recorded_at or now(),
            },
        )

        if not created:
            reproduction.heat_sign_start = heat_start_time
            reproduction.heat_signs_seen = heat_signs
            if heat_sign_recorded_at:
                reproduction.heat_sign_recorded_at = heat_sign_recorded_at
            reproduction.save()

        self.logger.info(
            f"Successfully created or updated reproduction record for cow {cow.cow_id} from farm {cow.farm.farm_id}"
        )

        return reproduction

    def _send_heat_sign_message(self, cow, heat_signs):
        """Send notifications to inseminator and farmer."""
        self.logger.debug(f"Sending notifications for cow {cow.cow_id}")

        # Prepare messages
        inseminator_message = (
            f"🐄 Insemination Alert!\n"
            f"Farm: {cow.farm.farm_id} - {cow.farm.owner_name}\n"
            f"Address: {cow.farm.address}\n"
            f"Phone: {cow.farm.telephone_number}\n"
            f"Cow ID: {cow.cow_id}\n"
            f"Heat Signs: {heat_signs}\n"
            f"Please visit for insemination check."
        )

        farmer_message = (
            f"🔔 Alert: Your inseminator ({cow.farm.inseminator.name}) "
            f"has been notified about your cow (Cow ID: {cow.cow_id}) "
            f"showing heat signs. They will visit your farm soon."
        )

        # send messages
        try:
            # notify inseminator
            inseminator_response = send_alert(
                "+251949911940", inseminator_message    # TODO: change to inseminator's phone number
            )
            if inseminator_response.get("status") == "success":
                self.logger.info(f"Successfully sent insemination alert to inseminator")
                self._create_message(
                    cow.farm, cow, inseminator_message, "insemination_alert"
                )
            else:
                self.logger.warning(f"Failed to send insemination alert to inseminator")

            # notify farmer
            farmer_response = send_alert("+251952137166", farmer_message)
            if farmer_response.get("status") == "success":
                self.logger.info(f"Successfully sent insemination alert to farmer")
                self._create_message(
                    cow.farm, cow, farmer_message, "insemination_alert"
                )
            else:
                self.logger.warning(f"Failed to send insemination alert to farmer")

        except Exception as e:
            self.logger.error(f"Error sending notification alert: {str(e)}")

    def _create_message(self, farm, cow, message_text, message_type):
        """Create a message record."""
        try:
            Message.objects.create(
                farm=farm,
                cow=cow,
                message_text=message_text,
                message_type=message_type,
                is_sent=True,
            )
        except Exception as e:
            self.logger.error(f"Error creating message record: {str(e)}", exc_info=True)
            raise

    @action(detail=False, methods=["post"])
    def monitor_pregnancy(self, request):
        """Monitor pregnancy status of a cow"""
        serializer = MonitorPregnancySerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(f"Invalid pregnancy monitoring data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                validated_data = serializer.validated_data
                cow = validated_data['cow']

                # Calculate expected calving date
                expected_calving_date = validated_data['pregnancy_date']

                # Update or create reproduction record
                reproduction, created = Reproduction.objects.get_or_create(
                    cow=cow,
                    farm=cow.farm,
                    defaults={
                        "is_cow_pregnant": True,
                        "pregnancy_date": validated_data['pregnancy_date'],
                        "calving_date": expected_calving_date,
                    }
                )

                if not created:
                    reproduction.is_cow_pregnant = True
                    reproduction.pregnancy_date = validated_data['pregnancy_date']
                    reproduction.calving_date = expected_calving_date
                    reproduction.save()

                # Update cow record
                cow.number_of_inseminations = validated_data['service_per_conception']
                cow.lactation_number = validated_data['lactation_number']
                cow.save()

                # Send notification
                farmer_message = (
                    f"🐄 Pregnancy Recorded!\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Pregnancy Date: {validated_data['pregnancy_date'].strftime('%Y-%m-%d')}\n"
                    f"Expected Calving Date: {expected_calving_date.strftime('%Y-%m-%d')}\n"
                    f"Services Required: {validated_data['service_per_conception']}\n"
                    f"Lactation Number: {validated_data['lactation_number']}"
                )

                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type="pregnancy_update",
                    is_sent=True
                )

                # Send alert to farmer
                send_alert(cow.farm.telephone_number, farmer_message)

                self.logger.info(f"Successfully updated pregnancy status for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Pregnancy monitoring record updated successfully",
                        "cow_id": cow.cow_id,
                        "farm_id": cow.farm.farm_id,
                        "pregnancy_date": validated_data['pregnancy_date'],
                        "expected_calving_date": expected_calving_date,
                        "service_per_conception": validated_data['service_per_conception'],
                        "lactation_number": validated_data['lactation_number']
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self.logger.error(f"Error in pregnancy monitoring: {str(e)}")
            return Response(
                {"error": "Failed to update pregnancy status"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def farmer_medical_assessment(self, request):
        """Record farmer's medical assessment"""
        serializer = FarmerMedicalAssessmentSerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(f"Invalid farmer medical assessment data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                cow = serializer.validated_data['cow']
                sickness_description = serializer.validated_data['sickness_description']

                # Create medical report
                report = FarmerMedicalReport.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    sickness_description=sickness_description
                )

                # Notify farm's doctor
                if cow.farm.doctor:
                    doctor_message = (
                        f"🚨 New Farmer Medical Report!\n"
                        f"Farm: {cow.farm.farm_id}\n"
                        f"Cow: {cow.cow_id}\n"
                        f"Reported Issue: {sickness_description}\n"
                        f"Please review this report."
                    )
                    send_alert("+251949911940", doctor_message) # TODO: change to doctor's phone number

                    Message.objects.create(
                        farm=cow.farm,
                        cow=cow,
                        message_text=doctor_message,
                        message_type="health_alert",
                        is_sent=True
                    )

                # Send confirmation to farmer
                farmer_message = (
                    f"✅ Health Issue Reported\n"
                    f"Your report about Cow {cow.cow_id} has been received.\n"
                    f"A doctor will review it soon."
                )
                send_alert("+251952137166", farmer_message) # TODO: change to farmer's phone number
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type="farmer_alert",
                    is_sent=True
                )

                self.logger.info(f"Successfully created medical report for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Medical assessment submitted successfully",
                        "report_id": report.id,
                        "farm_id": cow.farm.farm_id,
                        "cow_id": cow.cow_id,
                        "reported_date": report.reported_date
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self.logger.error(f"Error in farmer medical assessment: {str(e)}")
            return Response(
                {"error": "Failed to submit medical assessment"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def doctor_assessment(self, request):
        """Record doctor's medical assessment"""
        serializer = DoctorMedicalAssessmentSerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(f"Invalid doctor assessment data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                validated_data = serializer.validated_data
                cow = validated_data['cow']
                doctor = validated_data['doctor']

                # Create medical assessment
                assessment = MedicalAssessment.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    assessed_by=doctor,
                    **{k: v for k, v in validated_data.items() 
                       if k not in ['cow', 'doctor', 'farm_id', 'cow_id', 'doctor_id']}
                )

                # Notify farmer
                farmer_message = (
                    f"Medical Assessment Complete\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Doctor: Dr. {doctor.name}\n"
                    f"Health Status: {'Sick' if validated_data['is_cow_sick'] else 'Healthy'}\n"
                    f"Lameness: {'Yes' if validated_data.get('has_lameness', False) else 'No'}\n"
                    f"Diagnosis: {validated_data.get('diagnosis', 'N/A')}\n"
                    f"Treatment: {validated_data.get('treatment', 'N/A')}"
                )

                send_alert(cow.farm.telephone_number, farmer_message)
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type="health_alert",
                    is_sent=True
                )

                self.logger.info(f"Successfully created medical assessment for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Medical assessment recorded successfully",
                        "assessment_id": assessment.id,
                        "farm_id": cow.farm.farm_id,
                        "cow_id": cow.cow_id
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self.logger.error(f"Error in doctor assessment: {str(e)}")
            return Response(
                {"error": "Failed to record medical assessment"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def monitor_heat_sign(self, request):
        """Monitor heat signs and record insemination"""
        serializer = MonitorHeatSignSerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(f"Invalid heat sign monitoring data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                validated_data = serializer.validated_data
                cow = validated_data['cow']

                # Create insemination record
                record = InseminationRecord.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    inseminator=cow.farm.inseminator,
                    is_inseminated=validated_data['is_inseminated'],
                    insemination_count=validated_data['insemination_count'],
                    lactation_number=validated_data['lactation_number']
                )

                # Update reproduction record if cow is inseminated
                if validated_data['is_inseminated']:
                    reproduction, _ = Reproduction.objects.get_or_create(
                        cow=cow,
                        farm=cow.farm,
                        defaults={
                            'is_cow_pregnant': False,
                        }
                    )
                    reproduction.pregnancy_date = validated_data['date_of_insemination']
                    reproduction.save()

                # Notify farmer
                farmer_message = (
                    f"Heat Sign Monitoring Update\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Status: {'Inseminated' if validated_data['is_inseminated'] else 'Not inseminated'}\n"
                    f"Lactation Number: {validated_data['lactation_number']}\n"
                    f"Insemination Count: {validated_data['insemination_count']}"
                )

                if validated_data['is_inseminated']:
                    farmer_message += f"\nDate of Insemination: {validated_data['date_of_insemination'].strftime('%Y-%m-%d')}"

                send_alert("+251952137166", farmer_message) # TODO: change to farmer's phone number
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type="heat_alert",
                    is_sent=True
                )

                # Notify inseminator
                inseminator_message = (
                    f"✅ Record Received\n"
                    f"Farm: {cow.farm.farm_id}\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Status: {'Inseminated' if validated_data['is_inseminated'] else 'Not inseminated'}\n"
                    f"Lactation Number: {validated_data['lactation_number']}\n"
                    f"Insemination Count: {validated_data['insemination_count']}"
                )

                if validated_data['is_inseminated']:
                    inseminator_message += f"\nDate of Insemination: {validated_data['date_of_insemination'].strftime('%Y-%m-%d')}"

                send_alert("+251949911940", inseminator_message) # TODO: change to inseminator's phone number
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=inseminator_message,
                    message_type="inseminator_alert",
                    is_sent=True
                )

                self.logger.info(f"Successfully recorded heat sign monitoring for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Heat sign monitoring recorded successfully",
                        "record_id": record.id,
                        "farm_id": cow.farm.farm_id,
                        "cow_id": cow.cow_id
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self.logger.error(f"Error in heat sign monitoring: {str(e)}")
            return Response(
                {"error": "Failed to record heat sign monitoring"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def monitor_birth(self, request):
        """Record birth event for a cow"""
        serializer = MonitorBirthSerializer(data=request.data)
        if not serializer.is_valid():
            self.logger.warning(f"Invalid birth monitoring data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                validated_data = serializer.validated_data
                cow = validated_data['cow']

                # Check if there's an existing reproduction record
                reproduction = Reproduction.objects.filter(cow=cow, is_cow_pregnant=True).first()
                if reproduction:
                    # Update existing reproduction record
                    reproduction.is_cow_pregnant = False
                    reproduction.calving_date = validated_data['calving_date']
                    reproduction.save()

                # Update cow record
                cow.parity += 1  # Increment number of births
                cow.last_calving_date = validated_data['last_calving_date']
                cow.save()

                # Create message for farmer
                farmer_message = (
                    f"🎉 Birth Event Recorded!\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Calving Date: {validated_data['calving_date']}\n"
                    f"Last Calving Date: {validated_data['last_calving_date']}\n"
                    f"Calf Sex: {'Male' if validated_data['calf_sex'] == 'M' else 'Female'}"
                )

                # Send notifications
                send_alert(cow.farm.telephone_number, farmer_message)
                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=farmer_message,
                    message_type="birth_alert",
                    is_sent=True
                )

                self.logger.info(f"Successfully recorded birth event for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Birth event recorded successfully",
                        "cow_id": cow.cow_id,
                        "farm_id": cow.farm.farm_id,
                        "calving_date": validated_data['calving_date'],
                        "last_calving_date": validated_data['last_calving_date'],
                        "calf_sex": validated_data['calf_sex'],
                        "parity": cow.parity
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self.logger.error(f"Error in birth monitoring: {str(e)}")
            return Response(
                {"error": "Failed to record birth event"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def pregnancy_records(self, request):
        """Get pregnancy monitoring records"""
        farm_id = request.query_params.get('farm_id')
        cow_id = request.query_params.get('cow_id')
        
        if not farm_id:
            return Response(
                {"error": "farm_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = Reproduction.objects.filter(
            farm__farm_id=farm_id,
            is_cow_pregnant=True
        )
        
        if cow_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
            
        data = []
        for record in queryset:
            data.append({
                'farm_id': record.farm.farm_id,
                'cow_id': record.cow.cow_id,
                'pregnancy_date': record.pregnancy_date,
                'expected_calving_date': record.calving_date,
                'service_per_conception': record.cow.number_of_inseminations,
                'lactation_number': record.cow.lactation_number
            })
            
        return Response(data)

    @action(detail=False, methods=["get"])
    def birth_records(self, request):
        """Get birth monitoring records"""
        farm_id = request.query_params.get('farm_id')
        cow_id = request.query_params.get('cow_id')
        
        if not farm_id:
            return Response(
                {"error": "farm_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = Reproduction.objects.filter(
            farm__farm_id=farm_id,
            calving_date__isnull=False
        )
        
        if cow_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
            
        data = []
        for record in queryset:
            data.append({
                'farm_id': record.farm.farm_id,
                'cow_id': record.cow.cow_id,
                'calving_date': record.calving_date,
                'last_calving_date': record.cow.last_calving_date,
                'parity': record.cow.parity
            })
            
        return Response(data)

    @action(detail=False, methods=["get"])
    def heat_sign_records(self, request):
        """Get heat sign records from Reproduction or InseminationRecord"""
        farm_id = request.query_params.get('farm_id')
        cow_id = request.query_params.get('cow_id')
        record_type = request.query_params.get('record_type', 'all')  # Default to all

        if not farm_id:
            return Response(
                {"error": "farm_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = []

        if record_type in ['reproduction', 'all']:
            reproduction_queryset = Reproduction.objects.filter(
                farm__farm_id=farm_id,
                is_cow_pregnant=False
            ).order_by('-heat_sign_recorded_at')
            if cow_id:
                reproduction_queryset = reproduction_queryset.filter(cow__cow_id=cow_id)
            for record in reproduction_queryset:
                data.append({
                    'type': 'reproduction',
                    'farm_id': record.farm.farm_id,
                    'cow_id': record.cow.cow_id,
                    'heat_sign_start': record.heat_sign_start,
                    'heat_signs_seen': record.heat_signs_seen,
                    'heat_sign_recorded_at': record.heat_sign_recorded_at,
                })

        if record_type in ['insemination', 'all']:
            insemination_queryset = InseminationRecord.objects.filter(
                farm__farm_id=farm_id
            ).order_by('-recorded_date')
            if cow_id:
                insemination_queryset = insemination_queryset.filter(cow__cow_id=cow_id)
            for record in insemination_queryset:
                data.append({
                    'type': 'insemination',
                    'farm_id': record.farm.farm_id,
                    'cow_id': record.cow.cow_id,
                    'insemination_time': record.insemination_time,
                    'recorded_date': record.recorded_date,
                })

        return Response(data)

    @action(detail=False, methods=["get"])
    def medical_records(self, request):
        """Get medical assessment records"""
        farm_id = request.query_params.get('farm_id')
        cow_id = request.query_params.get('cow_id')
        record_type = request.query_params.get('type', 'all')  # 'farmer' or 'doctor' or 'all'
        
        if not farm_id:
            return Response(
                {"error": "farm_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        data = []
        
        # Get farmer medical reports if requested
        if record_type in ['farmer', 'all']:
            farmer_reports = FarmerMedicalReport.objects.filter(farm__farm_id=farm_id)
            if cow_id:
                farmer_reports = farmer_reports.filter(cow__cow_id=cow_id)
                
            for report in farmer_reports:
                data.append({
                    'type': 'farmer_report',
                    'farm_id': report.farm.farm_id,
                    'cow_id': report.cow.cow_id,
                    'reported_date': report.reported_date,
                    'sickness_description': report.sickness_description,
                    'is_reviewed': report.is_reviewed,
                    'reviewed_by': report.reviewed_by.name if report.reviewed_by else None,
                    'review_date': report.review_date
                })
        
        # Get doctor medical assessments if requested
        if record_type in ['doctor', 'all']:
            assessments = MedicalAssessment.objects.filter(farm__farm_id=farm_id)
            if cow_id:
                assessments = assessments.filter(cow__cow_id=cow_id)
                
            for assessment in assessments:
                data.append({
                    'type': 'doctor_assessment',
                    'farm_id': assessment.farm.farm_id,
                    'cow_id': assessment.cow.cow_id,
                    'assessment_date': assessment.assessment_date,
                    'assessed_by': assessment.assessed_by.name,
                    'is_cow_sick': assessment.is_cow_sick,
                    'sickness_type': assessment.sickness_type,
                    'general_health': assessment.general_health.name,
                    'udder_health': assessment.udder_health.name,
                    'mastitis': assessment.mastitis.name,
                    'has_lameness': assessment.has_lameness,
                    'body_condition_score': assessment.body_condition_score,
                    'reproductive_health': assessment.reproductive_health,
                    'metabolic_disease': assessment.metabolic_disease,
                    'is_cow_vaccinated': assessment.is_cow_vaccinated,
                    'vaccination_date': assessment.vaccination_date,
                    'vaccination_type': assessment.vaccination_type,
                    'has_deworming': assessment.has_deworming,
                    'deworming_date': assessment.deworming_date,
                    'deworming_type': assessment.deworming_type,
                    'diagnosis': assessment.diagnosis,
                    'treatment': assessment.treatment,
                    'prescription': assessment.prescription,
                    'next_assessment_date': assessment.next_assessment_date
                })
        
        return Response(data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_text", "message_type"]

    def get_queryset(self):
        queryset = Message.objects.all()
        farm_id = self.request.query_params.get("farm_id", None)
        cow_id = self.request.query_params.get("cow_id", None)

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

    @action(detail=True, methods=["post"])
    def replace_inseminator(self, request, pk=None):
        try:
            old_inseminator = self.get_object()
            new_phone = request.data.get("phone_number")
            new_name = request.data.get("name")
            new_address = request.data.get("address")

            if not all([new_phone, new_name, new_address]):
                return Response(
                    {"error": "phone_number, name, and address are required"},
                    status=status.HTTP_400_BAD_REQUEST,
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

            return Response(
                {
                    "message": "Inseminator details updated successfully",
                    "affected_farms_count": affected_farms.count(),
                    "new_details": {
                        "name": new_name,
                        "phone": new_phone,
                        "address": new_address,
                    },
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReproductionViewSet(viewsets.ModelViewSet):
    queryset = Reproduction.objects.all()
    serializer_class = ReproductionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["cow__cow_id", "farm__farm_id"]

    def get_queryset(self):
        queryset = Reproduction.objects.all()
        farm_id = self.request.query_params.get("farm_id", None)
        cow_id = self.request.query_params.get("cow_id", None)
        is_pregnant = self.request.query_params.get("is_pregnant", None)

        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id and farm_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
        if is_pregnant is not None:
            queryset = queryset.filter(is_cow_pregnant=is_pregnant.lower() == "true")

        return queryset


# Choice Models ViewSets (Read-only)
class BreedTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BreedType.objects.all()
    serializer_class = BreedTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "display_name"]


class HousingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HousingType.objects.all()
    serializer_class = HousingTypeSerializer
    search_fields = ["name", "display_name"]


class FloorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FloorType.objects.all()
    serializer_class = FloorTypeSerializer
    search_fields = ["name", "display_name"]


class FeedingFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedingFrequency.objects.all()
    serializer_class = FeedingFrequencySerializer
    search_fields = ["name", "display_name"]


class WaterSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WaterSource.objects.all()
    serializer_class = WaterSourceSerializer
    search_fields = ["name", "display_name"]


class GynecologicalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GynecologicalStatus.objects.all()
    serializer_class = GynecologicalStatusSerializer
    search_fields = ["name", "display_name"]


class UdderHealthStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UdderHealthStatus.objects.all()
    serializer_class = UdderHealthStatusSerializer
    search_fields = ["name", "display_name"]


class MastitisStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MastitisStatus.objects.all()
    serializer_class = MastitisStatusSerializer
    search_fields = ["name", "display_name"]


class GeneralHealthStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeneralHealthStatus.objects.all()
    serializer_class = GeneralHealthStatusSerializer
    search_fields = ["name", "display_name"]


class FarmerMedicalReportViewSet(viewsets.ModelViewSet):
    queryset = FarmerMedicalReport.objects.all()
    serializer_class = FarmerMedicalReportSerializer

    def get_queryset(self):
        queryset = FarmerMedicalReport.objects.all()
        farm_id = self.request.query_params.get("farm_id", None)
        cow_id = self.request.query_params.get("cow_id", None)
        is_reviewed = self.request.query_params.get("is_reviewed", None)

        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
        if is_reviewed is not None:
            queryset = queryset.filter(is_reviewed=is_reviewed)

        return queryset


class MedicalAssessmentViewSet(viewsets.ModelViewSet):
    queryset = MedicalAssessment.objects.all()
    serializer_class = MedicalAssessmentSerializer

    def get_queryset(self):
        queryset = MedicalAssessment.objects.all()
        farm_id = self.request.query_params.get("farm_id", None)
        cow_id = self.request.query_params.get("cow_id", None)
        doctor_id = self.request.query_params.get("doctor_id", None)
        is_cow_sick = self.request.query_params.get("is_cow_sick", None)

        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
        if doctor_id:
            queryset = queryset.filter(assessed_by_id=doctor_id)
        if is_cow_sick is not None:
            queryset = queryset.filter(is_cow_sick=is_cow_sick)

        return queryset


class InseminationRecordViewSet(viewsets.ModelViewSet):
    queryset = InseminationRecord.objects.all()
    serializer_class = InseminationRecordSerializer

    def get_queryset(self):
        queryset = InseminationRecord.objects.all()
        farm_id = self.request.query_params.get("farm_id", None)
        cow_id = self.request.query_params.get("cow_id", None)
        inseminator_id = self.request.query_params.get("inseminator_id", None)
        is_inseminated = self.request.query_params.get("is_inseminated", None)

        if farm_id:
            queryset = queryset.filter(farm__farm_id=farm_id)
        if cow_id:
            queryset = queryset.filter(cow__cow_id=cow_id)
        if inseminator_id:
            queryset = queryset.filter(inseminator_id=inseminator_id)
        if is_inseminated is not None:
            queryset = queryset.filter(is_inseminated=is_inseminated)

        return queryset


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    logger = logging.getLogger(__name__)

    def perform_create(self, serializer):
        doctor = serializer.save()
        self.logger.info(f"Created new doctor: {doctor.name} (ID: {doctor.id})")

    def perform_update(self, serializer):
        doctor = serializer.save()
        self.logger.info(f"Updated doctor: {doctor.name} (ID: {doctor.id})")
