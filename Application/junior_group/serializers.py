from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('id', 'name', 'surname', 'group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('group',)


class CognitiveDevelopSerializer(serializers.ModelSerializer):
    math = serializers.IntegerField(source='math.total')
    viewofworld = serializers.ReadOnlyField(source='viewofworld.total')
    primaryrepresent = serializers.ReadOnlyField(source='primaryrepresent.total')
    universalprerequisite = serializers.ReadOnlyField(source='universalprerequisite.total')
    cognition = serializers.ReadOnlyField(source='cognition.total')
    skills = serializers.ReadOnlyField(source='skills.total')
    activities = serializers.ReadOnlyField(source='activities.total')

    class Meta:
        model = CognitiveDevelop
        exclude = ('id',)


class MathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Math
        exclude = ('id', )


class UpdateMathSerializer(serializers.ModelSerializer):
    def update(self, instance: Math, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = Math
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class ViewOfWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewOfWorld
        exclude = ('id',)


class UpdateViewOfWorldSerializer(serializers.ModelSerializer):
    def update(self, instance: ViewOfWorld, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = ViewOfWorld
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class PrimaryRepresentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryRepresent
        # exclude = ('id',)
        fields = '__all__'


class UpdatePrimaryRepresentSerializer(serializers.ModelSerializer):
    def update(self, instance: PrimaryRepresent, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = PrimaryRepresent
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class UniversalPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversalPrerequisite
        exclude = ('id',)


class UpdateUniversalPrerequisiteSerializer(serializers.ModelSerializer):
    def update(self, instance: UniversalPrerequisite, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = UniversalPrerequisite
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class CognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cognition
        exclude = ('id',)


class UpdateCognitionSerializer(serializers.ModelSerializer):
    def update(self, instance: Cognition, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Cognition
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        exclude = ('id',)


class UpdateSkillsSerializer(serializers.ModelSerializer):
    def update(self, instance: Skills, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)

        instance.save()
        return instance

    class Meta:
        model = Skills
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5')


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        exclude = ('id',)


class UpdateActivitiesSerializer(serializers.ModelSerializer):
    def update(self, instance: Activities, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = Activities
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class SpeechDevelopSerializer(serializers.ModelSerializer):
    speechactivity = serializers.ReadOnlyField(source='speechactivity.total')
    reading = serializers.ReadOnlyField(source='reading.total')
    communication = serializers.ReadOnlyField(source='communication.total')


    class Meta:
        model = SpeechDevelop
        exclude = ('id',)


class SpeechActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechActivity
        exclude = ('id',)


class UpdateSpeechActivitySerializer(serializers.ModelSerializer):
    def update(self, instance: SpeechActivity, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = SpeechActivity
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        exclude = ('id',)


class UpdateReadingSerializer(serializers.ModelSerializer):
    def update(self, instance: Reading, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Reading
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        exclude = ('id',)


class UpdateCommunicationSerializer(serializers.ModelSerializer):
    def update(self, instance: Communication, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)

        instance.save()
        return instance

    class Meta:
        model = Communication
        fields = ('child',
                  'param1',
                  'param2')


class CommunicativeDevelopSerializer(serializers.ModelSerializer):
    emotional = serializers.ReadOnlyField(source='emotional.total')
    work = serializers.ReadOnlyField(source='work.total')
    safety = serializers.ReadOnlyField(source='safety.total')
    masteringcommunicat = serializers.ReadOnlyField(source='masteringcommunicat.total')
    behaviormanagement = serializers.ReadOnlyField(source='behaviormanagement.total')
    problemsolving = serializers.ReadOnlyField(source='problemsolving.total')
    socialization = serializers.ReadOnlyField(source='socialization.total')


    class Meta:
        model = CommunicativeDevelop
        exclude = ('id',)


class EmotionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotional
        exclude = ('id',)


class UpdateEmotionalSerializer(serializers.ModelSerializer):
    def update(self, instance: Emotional, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = Emotional
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        exclude = ('id',)


class UpdateWorkSerializer(serializers.ModelSerializer):
    def update(self, instance: Work, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Work
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = Safety
        exclude = ('id',)


class UpdateSafetySerializer(serializers.ModelSerializer):
    def update(self, instance: Safety, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Safety
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class MasteringCommunicatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasteringCommunicat
        exclude = ('id',)


class UpdateMasteringCommunicatSerializer(serializers.ModelSerializer):
    def update(self, instance: MasteringCommunicat, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = MasteringCommunicat
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class BehaviorManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorManagement
        exclude = ('id',)


class UpdateBehaviorManagementSerializer(serializers.ModelSerializer):
    def update(self, instance: BehaviorManagement, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = MasteringCommunicat
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class ProblemSolvingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemSolving
        exclude = ('id',)


class UpdateProblemSolvingSerializer(serializers.ModelSerializer):
    def update(self, instance: ProblemSolving, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)

        instance.save()
        return instance

    class Meta:
        model = ProblemSolving
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4')


class SocializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socialization
        exclude = ('id',)


class UpdateSocializationSerializer(serializers.ModelSerializer):
    def update(self, instance: Socialization, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = Socialization
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class PhysicalDevelopSerializer(serializers.ModelSerializer):
    movements = serializers.ReadOnlyField(source='movements.total')
    hygiene = serializers.ReadOnlyField(source='hygiene.total')
    health = serializers.ReadOnlyField(source='health.total')

    class Meta:
        model = CommunicativeDevelop
        exclude = ('id',)


class MovementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movements
        exclude = ('id',)


class UpdateMovementsSerializer(serializers.ModelSerializer):
    def update(self, instance: Movements, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = Movements
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class HygieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hygiene
        exclude = ('id',)


class UpdateHygieneSerializer(serializers.ModelSerializer):
    def update(self, instance: Hygiene, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Hygiene
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        exclude = ('id',)


class UpdateHealthSerializer(serializers.ModelSerializer):
    def update(self, instance: Health, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)

        instance.save()
        return instance

    class Meta:
        model = Health
        fields = ('child',
                  'param1',
                  'param2')


class ArtisticDevelopSerializer(serializers.ModelSerializer):
    artisticpersonaldevelop = serializers.ReadOnlyField(source='artisticpersonaldevelop.total')
    painting = serializers.ReadOnlyField(source='painting.total')
    modeling = serializers.ReadOnlyField(source='modeling.total')
    application = serializers.ReadOnlyField(source='application.total')
    music = serializers.ReadOnlyField(source='music.total')

    class Meta:
        model = ArtisticDevelop
        exclude = ('id',)


class ArtisticPersonalDevelopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisticPersonalDevelop
        exclude = ('id',)


class UpdateArtisticPersonalDevelopSerializer(serializers.ModelSerializer):
    def update(self, instance: ArtisticPersonalDevelop, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = ArtisticPersonalDevelop
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class PaintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        exclude = ('id',)


class UpdatePaintingSerializer(serializers.ModelSerializer):
    def update(self, instance: Painting, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Painting
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class ModelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modeling
        exclude = ('id',)


class UpdateModelingSerializer(serializers.ModelSerializer):
    def update(self, instance: Modeling, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)

        instance.save()
        return instance

    class Meta:
        model = Modeling
        fields = ('child',
                  'param1',
                  'param2')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('id',)


class UpdateApplicationSerializer(serializers.ModelSerializer):
    def update(self, instance: Application, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)

        instance.save()
        return instance

    class Meta:
        model = Application
        fields = ('child',
                  'param1',
                  'param2',
                  'param3')


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        exclude = ('id',)


class UpdateMusicSerializer(serializers.ModelSerializer):
    def update(self, instance: Music, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)
        instance.param7 = validated_data.get('param7', instance.param7)

        instance.save()
        return instance

    class Meta:
        model = Music
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6',
                  'param7')


class AttentionAndMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttentionAndMemory
        exclude = ('id',)


class UpdateAttentionAndMemorySerializer(serializers.ModelSerializer):
    def update(self, instance: AttentionAndMemory, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = AttentionAndMemory
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class PerceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perception
        exclude = ('id',)


class UpdatePerceptionSerializer(serializers.ModelSerializer):
    def update(self, instance: Perception, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)
        instance.param7 = validated_data.get('param7', instance.param7)
        instance.param8 = validated_data.get('param8', instance.param8)
        instance.param9 = validated_data.get('param9', instance.param9)

        instance.save()
        return instance

    class Meta:
        model = Perception
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6',
                  'param7',
                  'param8',
                  'param9')


class ThinkingAndSpeakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThinkingAndSpeaking
        exclude = ('id',)


class UpdateThinkingAndSpeakingSerializer(serializers.ModelSerializer):
    def update(self, instance: ThinkingAndSpeaking, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = ThinkingAndSpeaking
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class EmotionsAndWillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionsAndWill
        exclude = ('id',)


class UpdateEmotionsAndWillSerializer(serializers.ModelSerializer):
    def update(self, instance: EmotionsAndWill, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)

        instance.save()
        return instance

    class Meta:
        model = EmotionsAndWill
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6')


class MotorDevelopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorDevelop
        exclude = ('id',)


class UpdateMotorDevelopSerializer(serializers.ModelSerializer):
    def update(self, instance: MotorDevelop, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)

        instance.save()
        return instance

    class Meta:
        model = MotorDevelop
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5')


class VisualPerceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualPerception
        exclude = ('id',)


class UpdateVisualPerceptionSerializer(serializers.ModelSerializer):
    def update(self, instance: VisualPerception, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)
        instance.param7 = validated_data.get('param7', instance.param7)
        instance.param8 = validated_data.get('param8', instance.param8)

        instance.save()
        return instance

    class Meta:
        model = VisualPerception
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6',
                  'param7',
                  'param8')


class SBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SBO
        exclude = ('id',)


class UpdateSBOSerializer(serializers.ModelSerializer):
    def update(self, instance: SBO, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)
        instance.param6 = validated_data.get('param6', instance.param6)
        instance.param7 = validated_data.get('param7', instance.param7)
        instance.param8 = validated_data.get('param8', instance.param8)

        instance.save()
        return instance

    class Meta:
        model = SBO
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5',
                  'param6',
                  'param7',
                  'param8')


class OrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        exclude = ('id',)


class UpdateOrientationSerializer(serializers.ModelSerializer):
    def update(self, instance: Orientation, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)

        instance.save()
        return instance

    class Meta:
        model = Orientation
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5')


class TouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Touch
        exclude = ('id',)


class UpdateTouchSerializer(serializers.ModelSerializer):
    def update(self, instance: Touch, validated_data):
        instance.param1 = validated_data.get('param1', instance.param1)
        instance.param2 = validated_data.get('param2', instance.param2)
        instance.param3 = validated_data.get('param3', instance.param3)
        instance.param4 = validated_data.get('param4', instance.param4)
        instance.param5 = validated_data.get('param5', instance.param5)

        instance.save()
        return instance

    class Meta:
        model = Touch
        fields = ('child',
                  'param1',
                  'param2',
                  'param3',
                  'param4',
                  'param5')
