from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class OwnedPatientMixin:
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(owner=self.request.user)


class PatientListCreateView(OwnedPatientMixin, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PatientDetailView(OwnedPatientMixin, generics.RetrieveUpdateDestroyAPIView):
    pass