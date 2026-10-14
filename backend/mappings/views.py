from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__owner=self.request.user
        ).select_related("doctor")


class MappingDetailView(APIView):
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, owner=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related("doctor")
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = get_object_or_404(
            PatientDoctorMapping, pk=pk, patient__owner=request.user
        )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)