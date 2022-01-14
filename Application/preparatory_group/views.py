from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class ChildGroupAllView(generics.ListAPIView):
    serializer_class = ChildSerializer

    def get_queryset(self):
        return Child.objects.filter(group=self.kwargs['group'])


class ChildAllView(generics.ListAPIView):
    serializer_class = ChildSerializer

    def get_queryset(self):
        return Child.objects.all()


class GroupView(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Child.objects.values('group').distinct()


class CognitiveDevelopGroupView(generics.ListAPIView):
    serializer_class = CognitiveDevelopSerializer

    def get_queryset(self):
        return CognitiveDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class CognitiveDevelopAllView(generics.ListAPIView):
    serializer_class = CognitiveDevelopSerializer

    def get_queryset(self):
        return CognitiveDevelop.objects.all()


class CognitiveDevelopChildView(generics.ListAPIView):
    serializer_class = CognitiveDevelopSerializer

    def get_queryset(self):
        return CognitiveDevelop.objects.filter(pk=self.kwargs['id'])


class MathChildView(generics.ListAPIView):
    serializer_class = MathSerializer

    def get_queryset(self):
        return Math.objects.filter(pk=self.kwargs['id'])


class MathGroupAllView(generics.ListAPIView):
    serializer_class = MathSerializer

    def get_queryset(self):
        return Math.objects.select_related('child').filter(child__group=self.kwargs['group'])


class UpdateMathAPIView(APIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateMathSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Math.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MathAllView(generics.ListAPIView):
    serializer_class = MathSerializer

    def get_queryset(self):
        return Math.objects.all()


class UpdateViewOfWorldView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateViewOfWorldSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = ViewOfWorld.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ViewOfWorldGroupAllView(generics.ListAPIView):
    serializer_class = ViewOfWorldSerializer

    def get_queryset(self):
        return ViewOfWorld.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ViewOfWorldAllView(generics.ListAPIView):
    serializer_class = ViewOfWorldSerializer

    def get_queryset(self):
        return ViewOfWorld.objects.all()


class ViewOfWorldChildView(generics.ListAPIView):
    serializer_class = ViewOfWorldSerializer

    def get_queryset(self):
        return ViewOfWorld.objects.filter(pk=self.kwargs['id'])


class PrimaryRepresentChildView(generics.ListAPIView):
    serializer_class = PrimaryRepresentSerializer

    def get_queryset(self):
        return PrimaryRepresent.objects.filter(pk=self.kwargs['id'])


class PrimaryRepresentGroupAllView(generics.ListAPIView):
    serializer_class = PrimaryRepresentSerializer

    def get_queryset(self):
        return PrimaryRepresent.objects.select_related('child').filter(child__group=self.kwargs['id'])


class PrimaryRepresentAllView(generics.ListAPIView):
    serializer_class = PrimaryRepresentSerializer

    def get_queryset(self):
        return PrimaryRepresent.objects.all()


class UpdatePrimaryRepresentView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdatePrimaryRepresentSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = PrimaryRepresent.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UniversalPrerequisiteChildView(generics.ListAPIView):
    serializer_class = UniversalPrerequisiteSerializer

    def get_queryset(self):
        return UniversalPrerequisite.objects.filter(pk=self.kwargs['id'])


class UniversalPrerequisiteGroupAllView(generics.ListAPIView):
    serializer_class = UniversalPrerequisiteSerializer

    def get_queryset(self):
        return UniversalPrerequisite.objects.select_related('child').filter(child__group=self.kwargs['id'])


class UniversalPrerequisiteAllView(generics.ListAPIView):
    serializer_class = UniversalPrerequisiteSerializer

    def get_queryset(self):
        return UniversalPrerequisite.objects.all()


class UpdateUniversalPrerequisiteView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateUniversalPrerequisiteSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = UniversalPrerequisite.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CognitionChildView(generics.RetrieveUpdateAPIView):
    serializer_class = CognitionSerializer

    def get_queryset(self):
        return Cognition.objects.filter(pk=self.kwargs['id'])


class CognitionGroupAllView(generics.ListAPIView):
    serializer_class = CognitionSerializer

    def get_queryset(self):
        return Cognition.objects.select_related('child').filter(child__group=self.kwargs['id'])


class CognitionAllView(generics.ListAPIView):
    serializer_class = CognitionSerializer

    def get_queryset(self):
        return Cognition.objects.all()


class UpdateCognitionView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateCognitionSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Cognition.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SkillsChildView(generics.ListAPIView):
    serializer_class = SkillsSerializer

    def get_queryset(self):
        return Skills.objects.filter(pk=self.kwargs['id'])


class SkillsGroupAllView(generics.ListAPIView):
    serializer_class = SkillsSerializer

    def get_queryset(self):
        return Skills.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SkillsAllView(generics.ListAPIView):
    serializer_class = SkillsSerializer

    def get_queryset(self):
        return Skills.objects.all()


class UpdateSkillsView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateSkillsSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Skills.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ActivitiesChildView(generics.ListAPIView):
    serializer_class = ActivitiesSerializer

    def get_queryset(self):
        return Activities.objects.filter(pk=self.kwargs['id'])


class ActivitiesGroupAllView(generics.ListAPIView):
    serializer_class = ActivitiesSerializer

    def get_queryset(self):
        return Activities.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ActivitiesAllView(generics.ListAPIView):
    serializer_class = ActivitiesSerializer

    def get_queryset(self):
        return Activities.objects.all()


class UpdateActivitiesView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateActivitiesSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Activities.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SpeechDevelopGroupView(generics.ListAPIView):
    serializer_class = SpeechDevelopSerializer

    def get_queryset(self):
        return SpeechDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SpeechDevelopAllView(generics.ListAPIView):
    serializer_class = SpeechDevelopSerializer

    def get_queryset(self):
        return SpeechDevelop.objects.all()


class SpeechDevelopChildView(generics.ListAPIView):
    serializer_class = SpeechDevelopSerializer

    def get_queryset(self):
        return SpeechDevelop.objects.filter(pk=self.kwargs['id'])


class SpeechActivityChildView(generics.RetrieveUpdateAPIView):
    serializer_class = SpeechActivitySerializer

    def get_queryset(self):
        return SpeechActivity.objects.filter(pk=self.kwargs['id'])


class SpeechActivityGroupAllView(generics.ListAPIView):
    serializer_class = SpeechActivitySerializer

    def get_queryset(self):
        return SpeechActivity.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SpeechActivityAllView(generics.ListAPIView):
    serializer_class = SpeechActivitySerializer

    def get_queryset(self):
        return SpeechActivity.objects.all()


class UpdateSpeechActivityView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateSpeechActivitySerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = SpeechActivity.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ReadingChildView(generics.ListAPIView):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        return Reading.objects.filter(pk=self.kwargs['id'])


class ReadingGroupAllView(generics.ListAPIView):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        return Reading.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ReadingAllView(generics.ListAPIView):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        return Reading.objects.all()


class UpdateReadingView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateReadingSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Reading.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CommunicationChildView(generics.ListAPIView):
    serializer_class = CommunicationSerializer

    def get_queryset(self):
        return Communication.objects.filter(pk=self.kwargs['id'])


class CommunicationGroupAllView(generics.ListAPIView):
    serializer_class = CommunicationSerializer

    def get_queryset(self):
        return Communication.objects.select_related('child').filter(child__group=self.kwargs['id'])


class CommunicationAllView(generics.ListAPIView):
    serializer_class = CommunicationSerializer

    def get_queryset(self):
        return Communication.objects.all()


class UpdateCommunicationView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateCommunicationSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Communication.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CommunicativeDevelopGroupView(generics.ListAPIView):
    serializer_class = CommunicativeDevelopSerializer

    def get_queryset(self):
        return CommunicativeDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class CommunicativeDevelopAllView(generics.ListAPIView):
    serializer_class = CommunicativeDevelopSerializer

    def get_queryset(self):
        return CommunicativeDevelop.objects.all()


class CommunicativeDevelopChildView(generics.ListAPIView):
    serializer_class = CommunicativeDevelopSerializer

    def get_queryset(self):
        return CommunicativeDevelop.objects.filter(pk=self.kwargs['id'])


class EmotionalChildView(generics.ListAPIView):
    serializer_class = EmotionalSerializer

    def get_queryset(self):
        return Emotional.objects.filter(pk=self.kwargs['id'])


class EmotionalGroupAllView(generics.ListAPIView):
    serializer_class = EmotionalSerializer

    def get_queryset(self):
        return Emotional.objects.select_related('child').filter(child__group=self.kwargs['id'])


class EmotionalAllView(generics.ListAPIView):
    serializer_class = EmotionalSerializer

    def get_queryset(self):
        return Emotional.objects.all()


class UpdateEmotionalView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateEmotionalSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Emotional.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class WorkChildView(generics.ListAPIView):
    serializer_class = WorkSerializer

    def get_queryset(self):
        return Work.objects.filter(pk=self.kwargs['id'])


class WorkGroupAllView(generics.ListAPIView):
    serializer_class = WorkSerializer

    def get_queryset(self):
        return Work.objects.select_related('child').filter(child__group=self.kwargs['id'])


class WorkAllView(generics.ListAPIView):
    serializer_class = WorkSerializer

    def get_queryset(self):
        return Work.objects.all()


class UpdateWorkView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateWorkSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Work.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SafetyChildView(generics.ListAPIView):
    serializer_class = SafetySerializer

    def get_queryset(self):
        return Safety.objects.filter(pk=self.kwargs['id'])


class SafetyGroupAllView(generics.ListAPIView):
    serializer_class = SafetySerializer

    def get_queryset(self):
        return Safety.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SafetyAllView(generics.ListAPIView):
    serializer_class = SafetySerializer

    def get_queryset(self):
        return Safety.objects.all()


class UpdateSafetyView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateSafetySerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Safety.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MasteringCommunicatChildView(generics.ListAPIView):
    serializer_class = MasteringCommunicatSerializer

    def get_queryset(self):
        return MasteringCommunicat.objects.filter(pk=self.kwargs['id'])


class MasteringCommunicatGroupAllView(generics.ListAPIView):
    serializer_class = MasteringCommunicatSerializer

    def get_queryset(self):
        return MasteringCommunicat.objects.select_related('child').filter(child__group=self.kwargs['id'])


class MasteringCommunicatAllView(generics.ListAPIView):
    serializer_class = MasteringCommunicatSerializer

    def get_queryset(self):
        return MasteringCommunicat.objects.all()


class UpdateMasteringCommunicatView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateMasteringCommunicatSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = MasteringCommunicat.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class BehaviorManagementChildView(generics.ListAPIView):
    serializer_class = BehaviorManagementSerializer

    def get_queryset(self):
        return BehaviorManagement.objects.filter(pk=self.kwargs['id'])


class BehaviorManagementGroupAllView(generics.ListAPIView):
    serializer_class = BehaviorManagementSerializer

    def get_queryset(self):
        return BehaviorManagement.objects.select_related('child').filter(child__group=self.kwargs['id'])


class BehaviorManagementAllView(generics.ListAPIView):
    serializer_class = BehaviorManagementSerializer

    def get_queryset(self):
        return BehaviorManagement.objects.all()


class UpdateBehaviorManagementView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateBehaviorManagementSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = BehaviorManagement.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ProblemSolvingChildView(generics.ListAPIView):
    serializer_class = ProblemSolvingSerializer

    def get_queryset(self):
        return ProblemSolving.objects.filter(pk=self.kwargs['id'])


class ProblemSolvingGroupAllView(generics.ListAPIView):
    serializer_class = ProblemSolvingSerializer

    def get_queryset(self):
        return ProblemSolving.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ProblemSolvingAllView(generics.ListAPIView):
    serializer_class = ProblemSolvingSerializer

    def get_queryset(self):
        return ProblemSolving.objects.all()


class UpdateProblemSolvingView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateProblemSolvingSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = ProblemSolving.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SocializationChildView(generics.ListAPIView):
    serializer_class = SocializationSerializer

    def get_queryset(self):
        return Socialization.objects.filter(pk=self.kwargs['id'])


class SocializationGroupAllView(generics.ListAPIView):
    serializer_class = SocializationSerializer

    def get_queryset(self):
        return Socialization.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SocializationAllView(generics.ListAPIView):
    serializer_class = SocializationSerializer

    def get_queryset(self):
        return Socialization.objects.all()


class UpdateSocializationView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateSocializationSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Socialization.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class PhysicalDevelopGroupView(generics.ListAPIView):
    serializer_class = PhysicalDevelopSerializer

    def get_queryset(self):
        return PhysicalDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class PhysicalDevelopAllView(generics.ListAPIView):
    serializer_class = PhysicalDevelopSerializer

    def get_queryset(self):
        return PhysicalDevelop.objects.all()


class PhysicalDevelopChildView(generics.ListAPIView):
    serializer_class = PhysicalDevelopSerializer

    def get_queryset(self):
        return PhysicalDevelop.objects.filter(pk=self.kwargs['id'])


class MovementsChildView(generics.ListAPIView):
    serializer_class = MovementsSerializer

    def get_queryset(self):
        return Movements.objects.filter(pk=self.kwargs['id'])


class MovementsGroupAllView(generics.ListAPIView):
    serializer_class = MovementsSerializer

    def get_queryset(self):
        return Movements.objects.select_related('child').filter(child__group=self.kwargs['id'])


class MovementsAllView(generics.ListAPIView):
    serializer_class = MovementsSerializer

    def get_queryset(self):
        return Movements.objects.all()


class UpdateMovementsView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateMovementsSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Movements.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class HygieneChildView(generics.ListAPIView):
    serializer_class = HygieneSerializer

    def get_queryset(self):
        return Hygiene.objects.filter(pk=self.kwargs['id'])


class HygieneGroupAllView(generics.ListAPIView):
    serializer_class = HygieneSerializer

    def get_queryset(self):
        return Hygiene.objects.select_related('child').filter(child__group=self.kwargs['id'])


class HygieneAllView(generics.ListAPIView):
    serializer_class = HygieneSerializer

    def get_queryset(self):
        return Hygiene.objects.all()


class UpdateHygieneView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateHygieneSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Hygiene.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class HealthChildView(generics.ListAPIView):
    serializer_class = HealthSerializer

    def get_queryset(self):
        return Health.objects.filter(pk=self.kwargs['id'])


class HealthGroupAllView(generics.ListAPIView):
    serializer_class = HealthSerializer

    def get_queryset(self):
        return Health.objects.select_related('child').filter(child__group=self.kwargs['id'])


class HealthAllView(generics.ListAPIView):
    serializer_class = HealthSerializer

    def get_queryset(self):
        return Health.objects.all()


class UpdateHealthView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateHealthSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Health.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ArtisticDevelopGroupView(generics.ListAPIView):
    serializer_class = ArtisticDevelopSerializer

    def get_queryset(self):
        return ArtisticDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ArtisticDevelopAllView(generics.ListAPIView):
    serializer_class = ArtisticDevelopSerializer

    def get_queryset(self):
        return ArtisticDevelop.objects.all()


class ArtisticDevelopChildView(generics.ListAPIView):
    serializer_class = ArtisticDevelopSerializer

    def get_queryset(self):
        return ArtisticDevelop.objects.filter(pk=self.kwargs['id'])


class ArtisticPersonalDevelopChildView(generics.ListAPIView):
    serializer_class = ArtisticPersonalDevelopSerializer

    def get_queryset(self):
        return ArtisticPersonalDevelop.objects.filter(pk=self.kwargs['id'])


class ArtisticPersonalDevelopGroupAllView(generics.ListAPIView):
    serializer_class = ArtisticPersonalDevelopSerializer

    def get_queryset(self):
        return ArtisticPersonalDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ArtisticPersonalDevelopAllView(generics.ListAPIView):
    serializer_class = ArtisticPersonalDevelopSerializer

    def get_queryset(self):
        return ArtisticPersonalDevelop.objects.all()


class UpdateArtisticPersonalDevelopView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateArtisticPersonalDevelopSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = ArtisticPersonalDevelop.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class PaintingChildView(generics.ListAPIView):
    serializer_class = PaintingSerializer

    def get_queryset(self):
        return Painting.objects.filter(pk=self.kwargs['id'])


class PaintingGroupAllView(generics.ListAPIView):
    serializer_class = PaintingSerializer

    def get_queryset(self):
        return Painting.objects.select_related('child').filter(child__group=self.kwargs['id'])


class PaintingAllView(generics.ListAPIView):
    serializer_class = PaintingSerializer

    def get_queryset(self):
        return Painting.objects.all()


class UpdatePaintingView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdatePaintingSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Painting.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ModelingChildView(generics.ListAPIView):
    serializer_class = ModelingSerializer

    def get_queryset(self):
        return Modeling.objects.filter(pk=self.kwargs['id'])


class ModelingGroupAllView(generics.ListAPIView):
    serializer_class = ModelingSerializer

    def get_queryset(self):
        return Modeling.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ModelingAllView(generics.ListAPIView):
    serializer_class = ModelingSerializer

    def get_queryset(self):
        return Modeling.objects.all()


class UpdateModelingView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateModelingSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Modeling.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ApplicationChildView(generics.ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(pk=self.kwargs['id'])


class ApplicationGroupAllView(generics.ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ApplicationAllView(generics.ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.all()


class UpdateApplicationView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateApplicationSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Application.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MusicChildView(generics.ListAPIView):
    serializer_class = MusicSerializer

    def get_queryset(self):
        return Music.objects.filter(pk=self.kwargs['id'])


class MusicGroupAllView(generics.ListAPIView):
    serializer_class = MusicSerializer

    def get_queryset(self):
        return Music.objects.select_related('child').filter(child__group=self.kwargs['id'])


class MusicAllView(generics.ListAPIView):
    serializer_class = MusicSerializer

    def get_queryset(self):
        return Music.objects.all()


class UpdateMusicView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateMusicSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Music.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AttentionAndMemoryChildView(generics.ListAPIView):
    serializer_class = AttentionAndMemorySerializer

    def get_queryset(self):
        return AttentionAndMemory.objects.filter(pk=self.kwargs['id'])


class AttentionAndMemoryGroupAllView(generics.ListAPIView):
    serializer_class = AttentionAndMemorySerializer

    def get_queryset(self):
        return AttentionAndMemory.objects.select_related('child').filter(child__group=self.kwargs['id'])


class AttentionAndMemoryAllView(generics.ListAPIView):
    serializer_class = AttentionAndMemorySerializer

    def get_queryset(self):
        return AttentionAndMemory.objects.all()


class UpdateAttentionAndMemoryView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateAttentionAndMemorySerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = AttentionAndMemory.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class PerceptionChildView(generics.ListAPIView):
    serializer_class = Perception

    def get_queryset(self):
        return Perception.objects.filter(pk=self.kwargs['id'])


class PerceptionGroupAllView(generics.ListAPIView):
    serializer_class = PerceptionSerializer

    def get_queryset(self):
        return Perception.objects.select_related('child').filter(child__group=self.kwargs['id'])


class PerceptionAllView(generics.ListAPIView):
    serializer_class = PerceptionSerializer

    def get_queryset(self):
        return Perception.objects.all()


class UpdatePerceptionView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdatePerceptionSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Perception.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ThinkingAndSpeakingChildView(generics.ListAPIView):
    serializer_class = ThinkingAndSpeakingSerializer

    def get_queryset(self):
        return ThinkingAndSpeaking.objects.filter(pk=self.kwargs['id'])


class ThinkingAndSpeakingGroupAllView(generics.ListAPIView):
    serializer_class = ThinkingAndSpeakingSerializer

    def get_queryset(self):
        return ThinkingAndSpeaking.objects.select_related('child').filter(child__group=self.kwargs['id'])


class ThinkingAndSpeakingAllView(generics.ListAPIView):
    serializer_class = ThinkingAndSpeakingSerializer

    def get_queryset(self):
        return ThinkingAndSpeaking.objects.all()


class UpdateThinkingAndSpeakingView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateThinkingAndSpeakingSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = ThinkingAndSpeaking.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class EmotionsAndWillChildView(generics.ListAPIView):
    serializer_class = EmotionsAndWillSerializer

    def get_queryset(self):
        return EmotionsAndWill.objects.filter(pk=self.kwargs['id'])


class EmotionsAndWillGroupAllView(generics.ListAPIView):
    serializer_class = EmotionsAndWillSerializer

    def get_queryset(self):
        return EmotionsAndWill.objects.select_related('child').filter(child__group=self.kwargs['id'])


class EmotionsAndWillAllView(generics.ListAPIView):
    serializer_class = EmotionsAndWill

    def get_queryset(self):
        return EmotionsAndWill.objects.all()


class UpdateEmotionsAndWillView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateEmotionsAndWillSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = EmotionsAndWill.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MotorDevelopChildView(generics.ListAPIView):
    serializer_class = MotorDevelopSerializer

    def get_queryset(self):
        return MotorDevelop.objects.filter(pk=self.kwargs['id'])


class MotorDevelopGroupAllView(generics.ListAPIView):
    serializer_class = MotorDevelopSerializer

    def get_queryset(self):
        return MotorDevelop.objects.select_related('child').filter(child__group=self.kwargs['id'])


class MotorDevelopAllView(generics.ListAPIView):
    serializer_class = MotorDevelopSerializer

    def get_queryset(self):
        return MotorDevelop.objects.all()


class UpdateMotorDevelopView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateMotorDevelopSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = MotorDevelop.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class VisualPerceptionChildView(generics.ListAPIView):
    serializer_class = VisualPerceptionSerializer

    def get_queryset(self):
        return VisualPerception.objects.filter(pk=self.kwargs['id'])


class VisualPerceptionGroupAllView(generics.ListAPIView):
    serializer_class = VisualPerceptionSerializer

    def get_queryset(self):
        return VisualPerception.objects.select_related('child').filter(child__group=self.kwargs['id'])


class VisualPerceptionAllView(generics.ListAPIView):
    serializer_class = VisualPerceptionSerializer

    def get_queryset(self):
        return VisualPerception.objects.all()


class UpdateVisualPerceptionView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateVisualPerceptionSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = VisualPerception.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SBOChildView(generics.ListAPIView):
    serializer_class = SBOSerializer

    def get_queryset(self):
        return SBO.objects.filter(pk=self.kwargs['id'])


class SBOGroupAllView(generics.ListAPIView):
    serializer_class = SBOSerializer

    def get_queryset(self):
        return SBO.objects.select_related('child').filter(child__group=self.kwargs['id'])


class SBOAllView(generics.ListAPIView):
    serializer_class = SBOSerializer

    def get_queryset(self):
        return SBO.objects.all()


class UpdateSBOView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateSBOSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = SBO.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class OrientationChildView(generics.ListAPIView):
    serializer_class = OrientationSerializer

    def get_queryset(self):
        return Orientation.objects.filter(pk=self.kwargs['id'])


class OrientationGroupAllView(generics.ListAPIView):
    serializer_class = OrientationSerializer

    def get_queryset(self):
        return Orientation.objects.select_related('child').filter(child__group=self.kwargs['id'])


class OrientationAllView(generics.ListAPIView):
    serializer_class = OrientationSerializer

    def get_queryset(self):
        return Orientation.objects.all()


class UpdateOrientationView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateOrientationSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Orientation.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class TouchChildView(generics.ListAPIView):
    serializer_class = TouchSerializer

    def get_queryset(self):
        return Touch.objects.filter(pk=self.kwargs['id'])


class TouchGroupAllView(generics.ListAPIView):
    serializer_class = TouchSerializer

    def get_queryset(self):
        return Touch.objects.select_related('child').filter(child__group=self.kwargs['id'])


class TouchAllView(generics.ListAPIView):
    serializer_class = TouchSerializer

    def get_queryset(self):
        return Touch.objects.all()


class UpdateTouchView(generics.RetrieveUpdateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UpdateTouchSerializer

    def post(self, request, *args, **kwargs):
        grade = request.data.get('grade', {})
        if "child" not in grade.keys():
            raise ValidationError('Обязательное поле child')
        instance_grade = Touch.objects.filter(child=grade['child']).first()
        serializer = self.serializer_class(instance_grade, data=grade)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
