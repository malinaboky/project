from django.urls import path, include

from . import sources
from .views import *

urlpatterns = [
    # получение информации о детях
    path('', ChildAllView.as_view()),  # получение всех детей
    path('groups/', GroupView.as_view()),  # получение списка групп
    path('group/<int:group>', ChildGroupAllView.as_view()),  # получение всех детей в одной группе
    # получение информации, математика
    path('math/child/<int:id>', MathChildView.as_view()),  # получение инфы по конкретному ребенку
    path('math/update/', UpdateMathAPIView.as_view()),  # обновление информации по конкретному ребенку
    path('math/group/<int:group>', MathGroupAllView.as_view()),  # получение инфы по группе
    path('math/all', MathAllView.as_view()),  # получение инфы по всем группам
    # получение информации, познавательное развитие
    path('cogdev/child/<int:id>', CognitiveDevelopChildView.as_view()),
    path('cogdev/group/<int:id>', CognitiveDevelopGroupView.as_view()),
    path('cogdev/all', CognitiveDevelopAllView.as_view()),
    # получение информации, картина мира
    path('viewofworld/child/<int:id>', ViewOfWorldChildView.as_view()),
    path('viewofworld/update/', UpdateViewOfWorldView.as_view()),
    path('viewofworld/group/<int:id>', ViewOfWorldGroupAllView.as_view()),
    path('viewofworld/all', ViewOfWorldAllView.as_view()),
    # получение информации, первичные представления
    path('primrep/child/<int:id>', PrimaryRepresentChildView.as_view()),
    path('primrep/update/', UpdatePrimaryRepresentView.as_view()),
    path('primrep/group/<int:id>', PrimaryRepresentGroupAllView.as_view()),
    path('primrep/all', PrimaryRepresentAllView.as_view()),
    # получение информации, универсальные предпосылки
    path('univers/child/<int:id>', UniversalPrerequisiteChildView.as_view()),
    path('univers/update/', UpdateUniversalPrerequisiteView.as_view()),
    path('univers/group/<int:id>', UniversalPrerequisiteGroupAllView.as_view()),
    path('univers/all', UniversalPrerequisiteAllView.as_view()),
    # получение информации, познание
    path('cognition/child/<int:id>', CognitionChildView.as_view()),
    path('cognition/update/', UpdateCognitionView.as_view()),
    path('cognition/group/<int:id>', CognitiveDevelopGroupView.as_view()),
    path('cognition/all', CognitionAllView.as_view()),
    # получение информации, необходимые умения и навыки
    path('skills/child/<int:id>', SkillsChildView.as_view()),
    path('skills/update/', UpdateSkillsView.as_view()),
    path('skills/group/<int:id>', SkillsGroupAllView.as_view()),
    path('skills/all', SkillsAllView.as_view()),
    # получение информации, любознательный и активный
    path('activities/child/<int:id>', ActivitiesChildView.as_view()),
    path('activities/update/', UpdateActivitiesView.as_view()),
    path('activities/group/<int:id>', ActivitiesGroupAllView.as_view()),
    path('activities/all', ActivitiesAllView.as_view()),
    # получение информации, речевое развитие
    path('speechdev/child/<int:id>', SpeechDevelopChildView.as_view()),
    path('speechdev/group/<int:id>', SpeechDevelopGroupView.as_view()),
    path('speechdev/all', SpeechDevelopAllView.as_view()),
    # получение информации, речевая активность
    path('speechactivity/child/<int:id>', SpeechActivityChildView.as_view()),
    path('speechactivity/update/', UpdateSpeechActivityView.as_view()),
    path('speechactivity/group/<int:id>', SpeechActivityGroupAllView.as_view()),
    path('speechactivity/all', SpeechDevelopAllView.as_view()),
    # получение информации, чтение
    path('reading/child/<int:id>', ReadingChildView.as_view()),
    path('reading/update/', UpdateReadingView.as_view()),
    path('reading/group/<int:id>', ReadingGroupAllView.as_view()),
    path('reading/all', ReadingAllView.as_view()),
    # получение информации, коммуникация
    path('communication/child/<int:id>', CommunicationChildView.as_view()),
    path('communication/update/', UpdateCommunicationView.as_view()),
    path('communication/group/<int:id>', CommunicationGroupAllView.as_view()),
    path('communication/all', CommunicationAllView.as_view()),
    # получение информации, социально-коммуникационное развитие
    path('communicativedevelop/child/<int:id>', CommunicativeDevelopChildView.as_view()),
    path('communicativedevelop/group/<int:id>', CommunicativeDevelopGroupView.as_view()),
    path('communicativedevelop/all', CommunicativeDevelopAllView.as_view()),
    # получение информации, эмоциональная отзывчивость
    path('emotional/child/<int:id>', EmotionalChildView.as_view()),
    path('emotional/update/', UpdateEmotionalView.as_view()),
    path('emotional/group/<int:id>', EmotionalGroupAllView.as_view()),
    path('emotional/all', EmotionalAllView.as_view()),
    # получение информации, труд
    path('work/child/<int:id>', WorkChildView.as_view()),
    path('work/update/', UpdateWorkView.as_view()),
    path('work/group/<int:id>', WorkGroupAllView.as_view()),
    path('work/all', WorkAllView.as_view()),
    # получение информации, безопасность
    path('safety/child/<int:id>', SafetyChildView.as_view()),
    path('safety/update/', UpdateSafetyView.as_view()),
    path('safety/group/<int:id>', SafetyGroupAllView.as_view()),
    path('safety/all', SafetyAllView.as_view()),
    # получение информации, овладение средствами общения
    path('mastercom/child/<int:id>', MasteringCommunicatChildView.as_view()),
    path('mastercom/update/', UpdateMasteringCommunicatView.as_view()),
    path('mastercom/group/<int:id>', MasteringCommunicatGroupAllView.as_view()),
    path('mastercom/all', MasteringCommunicatAllView.as_view()),
    # получение информации, Управление своим поведением
    path('behaveman/child/<int:id>', BehaviorManagementChildView.as_view()),
    path('behaveman/update/', UpdateBehaviorManagementView.as_view()),
    path('behaveman/group/<int:id>', BehaviorManagementGroupAllView.as_view()),
    path('behaveman/all', BehaviorManagementAllView.as_view()),
    # получение информации, Решение интеллектуальных задач
    path('problemsolv/child/<int:id>', ProblemSolvingChildView.as_view()),
    path('problemsolv/update/', UpdateProblemSolvingView.as_view()),
    path('problemsolv/group/<int:id>', ProblemSolvingGroupAllView.as_view()),
    path('problemsolv/all', ProblemSolvingAllView.as_view()),
    # получение информации, Социализация
    path('social/child/<int:id>', SocializationChildView.as_view()),
    path('social/update/', UpdateSocializationView.as_view()),
    path('social/group/<int:id>', SocializationGroupAllView.as_view()),
    path('social/all', SocializationAllView.as_view()),
    # получение информации, Физическое развитие
    path('physicdev/child/<int:id>', PhysicalDevelopChildView.as_view()),
    path('physicdev/group/<int:id>', PhysicalDevelopGroupView.as_view()),
    path('physicdev/all', PhysicalDevelopAllView.as_view()),
    # получение информации, Основные движения
    path('move/child/<int:id>', MovementsChildView.as_view()),
    path('move/update/', UpdateMovementsView.as_view()),
    path('move/group/<int:id>', MovementsGroupAllView.as_view()),
    path('move/all', MovementsAllView.as_view()),
    # получение информации, Гигиена
    path('hygiene/child/<int:id>', HygieneChildView.as_view()),
    path('hygiene/update/', UpdateHygieneView.as_view()),
    path('hygiene/group/<int:id>', HygieneGroupAllView.as_view()),
    path('hygiene/all', HygieneAllView.as_view()),
    # получение информации, Здоровье
    path('health/child/<int:id>', HealthChildView.as_view()),
    path('health/update/', UpdateHealthView.as_view()),
    path('health/group/<int:id>', HealthGroupAllView.as_view()),
    path('health/all', HealthAllView.as_view()),
    # получение информации, Художественное-эстетическое развитие
    path('artdev/child/<int:id>', ArtisticDevelopChildView.as_view()),
    path('artdev/group/<int:id>', ArtisticDevelopGroupView.as_view()),
    path('artdev/all', ArtisticDevelopAllView.as_view()),
    # получение информации, Художественно-личное развитие
    path('personaldev/child/<int:id>', ArtisticDevelopChildView.as_view()),
    path('personaldev/update/', UpdateArtisticPersonalDevelopView.as_view()),
    path('personaldev/group/<int:id>', ArtisticPersonalDevelopGroupAllView.as_view()),
    path('personaldev/all', ArtisticPersonalDevelopAllView.as_view()),
    # получение информации, Рисование
    path('painting/child/<int:id>', PaintingChildView.as_view()),
    path('painting/update/', UpdatePaintingView.as_view()),
    path('painting/group/<int:id>', PaintingGroupAllView.as_view()),
    path('painting/all', PaintingAllView.as_view()),
    # получение информации, Лепка
    path('modeling/child/<int:id>', ModelingChildView.as_view()),
    path('modeling/update/', UpdateModelingView.as_view()),
    path('modeling/group/<int:id>', ModelingGroupAllView.as_view()),
    path('modeling/all', ModelingAllView.as_view()),
    # получение информации, Аппликация
    path('application/child/<int:id>', ApplicationChildView.as_view()),
    path('application/update/', UpdateApplicationView.as_view()),
    path('application/group/<int:id>', ApplicationGroupAllView.as_view()),
    path('application/all', ApplicationAllView.as_view()),
    # получение информации, Музыка
    path('music/child/<int:id>', MusicChildView.as_view()),
    path('music/update/', UpdateMusicView.as_view()),
    path('music/group/<int:id>', MusicGroupAllView.as_view()),
    path('music/all', MusicAllView.as_view()),
    # получение информации, Уровень развития внимания и памяти
    path('attentionmemory/child/<int:id>', AttentionAndMemoryChildView.as_view()),
    path('attentionmemory/update/', UpdateAttentionAndMemoryView.as_view()),
    path('attentionmemory/group/<int:id>', AttentionAndMemoryGroupAllView.as_view()),
    path('attentionmemory/all', AttentionAndMemoryAllView.as_view()),
    # получение информации, Уровень развития ВОСПРИЯТИЯ
    path('perception/child/<int:id>', PerceptionChildView.as_view()),
    path('perception/update/', UpdatePerceptionView.as_view()),
    path('perception/group/<int:id>', PerceptionGroupAllView.as_view()),
    path('perception/all', PerceptionAllView.as_view()),
    # получение информации, Уровень развития МЫШЛЕНИЯ И РЕЧИ
    path('thinkspeak/child/<int:id>', ThinkingAndSpeakingChildView.as_view()),
    path('thinkspeak/update/', UpdateThinkingAndSpeakingView.as_view()),
    path('thinkspeak/group/<int:id>', ThinkingAndSpeakingGroupAllView.as_view()),
    path('thinkspeak/all', ThinkingAndSpeakingAllView.as_view()),
    # получение информации, Уровень развития ЭМОЦИОНАЛЬНО-ВОЛЕВОЙ СФЕРЫ
    path('emotionswill/child/<int:id>', EmotionsAndWillChildView.as_view()),
    path('emotionswill/update/', UpdateEmotionsAndWillView.as_view()),
    path('emotionswill/group/<int:id>', EmotionsAndWillGroupAllView.as_view()),
    path('emotionswill/all', EmotionsAndWillAllView.as_view()),
    # получение информации, Уровень развития МОТОРНОГО РАЗВИТИЯ
    path('motordev/child/<int:id>', MotorDevelopChildView.as_view()),
    path('motordev/update/', UpdateMotorDevelopView.as_view()),
    path('motordev/group/<int:id>', MotorDevelopGroupAllView.as_view()),
    path('motordev/all', MotorDevelopAllView.as_view()),
    # получение информации, Уровень развития зрительного восприятия
    path('visper/child/<int:id>', VisualPerceptionChildView.as_view()),
    path('visper/update/', UpdateVisualPerceptionView.as_view()),
    path('visper/group/<int:id>', VisualPerceptionGroupAllView.as_view()),
    path('visper/all', VisualPerceptionAllView.as_view()),
    # получение информации, Уровень развития СБО
    path('sbo/child/<int:id>', SBOChildView.as_view()),
    path('sbo/update/', UpdateSBOView.as_view()),
    path('sbo/group/<int:id>', SBOGroupAllView.as_view()),
    path('sbo/all', SBOAllView.as_view()),
    # получение информации, Уровень развития навыков ориентировки в пространстве
    path('orientation/child/<int:id>', OrientationChildView.as_view()),
    path('orientation/update/', UpdateOrientationView.as_view()),
    path('orientation/group/<int:id>', OrientationGroupAllView.as_view()),
    path('orientation/all', OrientationAllView.as_view()),
    # получение информации, Уровень развития осязания и мелкой моторики
    path('touch/child/<int:id>', TouchChildView.as_view()),
    path('touch/update/', UpdateTouchView.as_view()),
    path('touch/group/<int:id>', TouchGroupAllView.as_view()),
    path('touch/all', TouchAllView.as_view()),
    path('sen_export_excel_cogdev', sources.sen_export_excel_cogdev, name='sen_export_excel_cogdev'),
    path('sen_export_excel_speechdev', sources.sen_export_excel_speechdev, name='sen_export_excel_speechdev'),
    path('sen_export_excel_comdev', sources.sen_export_excel_comdev, name='sen_export_excel_comdev'),
    path('sen_export_excel_physdev', sources.sen_export_excel_physdev, name='sen_export_excel_physdev'),
    path('sen_export_excel_artdev', sources.sen_export_excel_artdev, name='sen_export_excel_artdev'),
    path('sen_export_excel_psycho', sources.sen_export_excel_psycho, name='sen_export_excel_psycho'),
    path('sen_export_excel_eyes', sources.sen_export_excel_eyes, name='sen_export_excel_eyes'),
]
