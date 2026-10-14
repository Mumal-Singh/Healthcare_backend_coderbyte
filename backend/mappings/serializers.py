from rest_framework import serializers

from doctors.serializers import DoctorSerializer

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor_detail = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "doctor_detail", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_patient(self, patient):
        if patient.owner_id != self.context["request"].user.id:
            raise serializers.ValidationError("Invalid patient.")
        return patient