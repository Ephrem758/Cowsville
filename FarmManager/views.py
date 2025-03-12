import logging
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now, timezone

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
    filter_backends = [filters.SearchFilter]
    search_fields = ["cow_id", "breed__name"]
    logger = logging.getLogger(__name__)

    def perform_create(self, serializer):
        """Override perform_create to automatically create reproduction record"""
        try:
            with transaction.atomic():
                # Save the cow first
                cow = serializer.save()
                self.logger.info(f"Created new cow: {cow.cow_id} for farm {cow.farm.farm_id}")

                # Create default reproduction record
                Reproduction.objects.create(
                    cow=cow,
                    farm=cow.farm,
                    is_cow_pregnant=False,
                    heat_sign_start=None,
                    heat_signs_seen=None
                )
                self.logger.info(f"Created default reproduction record for cow {cow.cow_id}")

        except Exception as e:
            self.logger.error(f"Error creating cow with reproduction record: {str(e)}")
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
            self.logger.info(
                f"Recording heat sign for cow {cow.cow_id} from farm {cow.farm.farm_id}"
            )

            # record heat sign
            reproduction = self._create_or_update_reproduction(cow, heat_signs)

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

    def _create_or_update_reproduction(self, cow, heat_signs):
        """create or update reproduction record based on heat signs"""
        self.logger.info(
            f"Creating or updating reproduction record for cow {cow.cow_id} from farm {cow.farm.farm_id}"
        )

        reproduction, created = Reproduction.objects.get_or_create(
            cow=cow,
            farm=cow.farm,
            defaults={
                "is_cow_pregnant": False,
                "heat_sign_start": now(),
                "heat_signs_seen": heat_signs,
            },
        )

        if not created:
            reproduction.heat_sign_start = now()
            reproduction.heat_signs_seen = heat_signs
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
                cow = serializer.validated_data['cow']
                is_pregnant = serializer.validated_data['is_pregnant']
                lactation_number = serializer.validated_data['lactation_number']

                # Update or create reproduction record
                reproduction, created = Reproduction.objects.get_or_create(
                    cow=cow,
                    farm=cow.farm,
                    defaults={
                        "is_cow_pregnant": is_pregnant,
                        "lactation_number": lactation_number
                    }
                )

                if not created:
                    reproduction.is_cow_pregnant = is_pregnant
                    reproduction.lactation_number = lactation_number
                    reproduction.save()

                # Send notification
                message_text = (
                    f"Pregnancy Confirmed: Cow {cow.cow_id} "
                    if is_pregnant
                    else f"Pregnancy Status Update: Cow {cow.cow_id} is not pregnant"
                )
                message_text += f". Lactation number: {lactation_number}"

                Message.objects.create(
                    farm=cow.farm,
                    cow=cow,
                    message_text=message_text,
                    message_type="pregnancy_update",
                    is_sent=True
                )

                # Send alert to farmer
                send_alert("+251949911940", message_text) # TODO: change to farmer's phone number

                self.logger.info(f"Successfully updated pregnancy status for cow {cow.cow_id}")
                return Response(
                    {
                        "message": "Pregnancy monitoring record updated successfully",
                        "cow_id": cow.cow_id,
                        "farm_id": cow.farm.farm_id,
                        "is_pregnant": is_pregnant,
                        "lactation_number": lactation_number
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
                    insemination_time=validated_data.get('insemination_time'),
                    insemination_count=validated_data.get('insemination_count', 0),
                    lactation_number=validated_data['lactation_number']
                )

                # Notify farmer
                farmer_message = (
                    f"Heat Sign Monitoring Update\n"
                    f"Cow: {cow.cow_id}\n"
                    f"Status: {'Inseminated' if validated_data['is_inseminated'] else 'Not inseminated'}\n"
                    f"Lactation Number: {validated_data['lactation_number']}"
                )

                if validated_data['is_inseminated']:
                    farmer_message += f"\nInsemination Time: {validated_data['insemination_time']}"

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
                    f"Lactation Number: {validated_data['lactation_number']}"
                )

                if validated_data['is_inseminated']:
                    inseminator_message += f"\nInsemination Time: {validated_data['insemination_time']}"

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
