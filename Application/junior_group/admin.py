from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import *
from django.utils.html import linebreaks


def get_model_field(model):
    return model._meta.get_fields()


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "surname",
                    "teacher",
                    "group")


# TODO возможно стоит во всех моделях снизу запретить редактирование и ручное создание записей, потому что тогда можно все сломать

######################## Познавательное развитие Младшая группа ################################

@admin.register(CognitiveDevelop)
class CognitiveDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(CognitiveDevelop) if field.name not in 'id']

    list_display = all_fields
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(Math)
class MathAdmin(admin.ModelAdmin):
    # TODO указывать названия моделей так же как и название класса этой модели, НО СЛИТНО И БЕЗ ЗАГЛАЫНХ БУКВ

    all_fields = [field.name for field in get_model_field(Math) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(ViewOfWorld)
class ViewOfWorldAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(ViewOfWorld) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(PrimaryRepresent)
class PrimaryRepresentAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(PrimaryRepresent) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(UniversalPrerequisite)
class UniversalPrerequisiteAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(UniversalPrerequisite) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Cognition)
class CognitionAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Cognition) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Skills) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Activities) if field.name not in ('id', 'cognitivedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


######################## Речевое развитие Младшая группа ################################

@admin.register(SpeechDevelop)
class SpeechDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(SpeechDevelop) if field.name not in ('id', 'speechdevelop')]

    list_display = all_fields
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(SpeechActivity)
class SpeechActivityAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(SpeechActivity) if field.name not in ('id', 'speechdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Reading) if field.name not in ('id', 'speechdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Communication) if field.name not in ('id', 'speechdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


######################## Соц-коммуникативное развитие Младшая группа ################################

@admin.register(CommunicativeDevelop)
class CommunicativeDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(CommunicativeDevelop) if
                  field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(Emotional)
class EmotionalAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Emotional) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Work) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Safety)
class SafetyAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Safety) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(MasteringCommunicat)
class MasteringCommunicatAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(MasteringCommunicat) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(BehaviorManagement)
class BehaviorManagementAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(BehaviorManagement) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(ProblemSolving)
class ProblemSolvingAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(ProblemSolving) if field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Socialization)
class SocializationAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Socialization) if
                  field.name not in ('id', 'communicativedevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


######################## Физическое развитие Младшая группа ################################

@admin.register(PhysicalDevelop)
class PhysicalDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(PhysicalDevelop) if field.name not in ('id', 'physicaldevelop')]

    list_display = all_fields
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(Movements)
class MovementsAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Movements) if field.name not in ('id', 'physicaldevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Hygiene)
class HygieneAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Hygiene) if field.name not in ('id', 'physicaldevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Health)
class HealthAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Health) if field.name not in ('id', 'physicaldevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


######################## Художественное развитие Младшая группа ################################

@admin.register(ArtisticDevelop)
class ArtisticDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(ArtisticDevelop) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    list_display_links = None

    def has_add_permission(self, request):
        return False


@admin.register(ArtisticPersonalDevelop)
class ArtisticPersonalDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(ArtisticPersonalDevelop) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Painting) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Modeling)
class ModelingAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Modeling) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Application) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Music) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(AttentionAndMemory)
class AttentionAndMemoryAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(AttentionAndMemory) if
                  field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Perception)
class PerceptionAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Perception) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(ThinkingAndSpeaking)
class ThinkingAndSpeakingAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(ThinkingAndSpeaking) if
                  field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(EmotionsAndWill)
class EmotionsAndWillAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(EmotionsAndWill) if
                  field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(MotorDevelop)
class MotorDevelopAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(MotorDevelop) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(VisualPerception)
class VisualPerceptionAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(VisualPerception) if
                  field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(SBO)
class SBOAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(SBO) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Orientation)
class OrientationAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Orientation) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False


@admin.register(Touch)
class TouchAdmin(admin.ModelAdmin):
    all_fields = [field.name for field in get_model_field(Touch) if field.name not in ('id', 'artisticdevelop')]

    list_display = all_fields
    readonly_fields = ('child', 'total')

    def has_add_permission(self, request):
        return False

