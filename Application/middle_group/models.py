from django.conf import settings
from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

NUM_CHOICES = ((1, 1), (2, 2), (3, 3))


def get_middle_value(model):
    values = []
    for i in model._meta.get_fields():
        if 'param' in i.name or model._meta.model_name in ('cognitivedevelop',) and 'child' not in i.name:
            a = i.value_from_object(model)
            if a == None:
                return 0
            values.append(a)
    if len(values) == 0:
        return 0
    return round(sum(values) / len(values), 2)


# TODO функция для Главных таблиц, на которые ссылаются под модели, в теории должна возвращать среднее значение главной таблицы,
#  но ты можешь это попробовать это пофиксить (я не смог)
def get_middle_for_aggregate(model):
    values = []
    for i in model._meta.get_fields():
        if is_str_float(str(i)):
            values.append(float(str(i)))
    if len(values) == 0:
        return 0
    return round(sum(values) / len(values), 2)


def is_str_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Child(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    surname = models.CharField(max_length=150, verbose_name="Фамилия")
    group = models.IntegerField(verbose_name="Группа")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='mid_teacher', null=True,
                                verbose_name="Воспитатель")

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"


######################## Познавательное развитие Средняя группа ################################

# TODO названия полей, такие же как названия классов моделей, на которые ссылаются, но слитно и без заглавных букв
class CognitiveDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка", )
    math = models.OneToOneField('Math', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Развитие элементарных математических представлений")
    viewofworld = models.OneToOneField('ViewOfWorld', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Формирование целостной картины мира")
    primaryrepresent = models.OneToOneField('PrimaryRepresent', on_delete=models.CASCADE, blank=True, null=True,
                                          verbose_name="Имеет представление о себе, семье, государстве, природе, мире")
    universalprerequisite = models.OneToOneField('UniversalPrerequisite', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Овладение универсальными предпосылками учебной деятельности")
    cognition = models.OneToOneField('Cognition', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Овладение продуктивной (конструктивной) деятельностью")
    skills = models.OneToOneField('Skills', on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="Овладение необходимыми умениями и навыками")
    activities = models.OneToOneField('Activities', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Любознательный, активный")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = self.math.total + self.viewofworld.total + self.primaryrepresent.total + self.universalprerequisite.total
        self.total += self.cognition.total + self.skills.total + self.activities.total
        self.total = round(self.total / 7, 2)
        super(CognitiveDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_for_aggregate(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Познавательное развитие"
        verbose_name_plural = "Познавательное развитие"


class Math(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет считать до 5, отвечать на вопрос «Сколько всего?»")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сравнивает количество предметов в группах на основе счета, а также составления пар")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать два предмета по величине на основе приложения их друг к другу или наложения")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет круг, квадрат, треугольник, шар, куб, знает их  характерные отличия")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет положение предметов в пространстве по отношению к себе (вверху, внизу, спереди, сзади)")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет части суток")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def __str__(self):
        return str(self.middle)

    @property
    def middle(self):
        return get_middle_value(self)

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Math, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Math, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Математика"
        verbose_name_plural = "ФЭМП"


class ViewOfWorld(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет разные предметы, которые его окружают в помещениях, на участке, на улице, знает их назначение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет признаки и количество предметов")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет домашних животных и знает, какую пользу они приносят человеку")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Различает и называет некоторые растения ближайшего окружения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет времена года в правильной последовательности")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и соблюдает элементарные правила поведения в природе")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ViewOfWorld, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ViewOfWorld, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Картина мира"
        verbose_name_plural = "Картина мира"


class PrimaryRepresent(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает свои имя, фамилию, возраст, имена членов семьи")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Может рассказать о своем городе")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о Российской армии, ее роли и защите Родины. Знает некоторые военные профессии")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(PrimaryRepresent, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(PrimaryRepresent, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Первичные представления"
        verbose_name_plural = "Первичные представления"


class UniversalPrerequisite(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет индивидуальные и коллективные поручения. Показывает ответственное отношение к порученному заданию, стремится выполнить его хорошо")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен удерживать в памяти при выполнении каких – либо действий несложное условие. Способен принять установку на запоминание")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может описать предмет, картину, составить рассказ по картинке, может выучить небольшое стихотворение")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен сосредоточено действовать в течении 15 – 20 минут")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(UniversalPrerequisite, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(UniversalPrerequisite, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Универсальные предпосылки"
        verbose_name_plural = "Универсальные предпосылки"


class Cognition(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет использовать строительные детали с учетом их конструктивных свойств")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен преобразовывать постройки в соответствии с заданием")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет сгибать прямоугольный лист пополам")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Cognition, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Cognition, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Продуктивная (конструктивная) деятельность  средняя группа"
        verbose_name_plural = "Продуктивная (конструктивная) деятельность  средняя группа"


class Skills(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Игровые")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Продуктивные")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Трудовые")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Комуникативные")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Двигательные")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Познавательно - исследовательской")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Музыкально - художественной")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Skills, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Skills, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Необходимые умения и навыки"
        verbose_name_plural = "Необходимые умения и навыки"


class Activities(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет устойчивый интерес к различным видам детской деятельности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет любознательность, интерес к исследовательской деятельности, эксперементированию")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Activities, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Activities, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Любознательный, активный"
        verbose_name_plural = "Любознательный, активный"

######################## Речевое развитие Средняя группа ################################


class SpeechDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    speechactivity = models.OneToOneField('SpeechActivity', on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Речевая деятельность")
    reading = models.OneToOneField('Reading', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Знакомство с художественной литературой")
    communication = models.OneToOneField('Communication', on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Коммуникация")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = self.speechactivity.total + self.reading.total + self.communication.total
        self.total = round(self.total / 3, 2)
        super(SpeechDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_for_aggregate(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Речевое развитие"
        verbose_name_plural = "Речевое развитие"


class SpeechActivity(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Звуковая культура речи)Свистящие")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Звуковая культура речи)Шипящие")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Звуковая культура речи)Сонорные")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Фонематический слух)Место звука")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Фонематический слух)Первый и последний звук")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Фонематический слух)Количество слогов")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Словарный запас)Количество слов")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="(Словарный запас)Антонимы")
    param10 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Словарный запас)Синонимы")
    param11 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Словарный запас)Признаки предмета")
    param12 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Словарный запас)Тематические ряды")
    param13 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Грамматический строй)Предлоги")
    param14 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Грамматический строй)Несклоняемые существительные")
    param15 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Грамматический строй)Однокоренные слова")
    param16 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Грамматический строй)Притяжательные прилагательные")
    param17 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Грамматический строй)Множественное число")
    param18 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Связная речь)Рассказ по плану")
    param19 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Связная речьй)Описательный рассказ")
    param20 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Связная речь)Инсценировка")
    param21 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                               verbose_name="(Связная речь)Сложносочиненные, сложноподчиненные")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(SpeechActivity, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(SpeechActivity, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Речевая деятельность"
        verbose_name_plural = "Речевая деятельность"


class Reading(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может прочитать наизусть понравившееся стихотворение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает 1 – 2 считалки, загадки")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может назвать любимую сказку")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Рассматривает иллюстрированные издания детских книг, проявляет к ним интерес")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Драматизирует (инсценирует) с помощью взрослого небольшие сказки (отрывок из сказки)")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Reading, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Reading, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Чтение"
        verbose_name_plural = "Чтение"


class Communication(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает и употребляет слова антонимы")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет образовывать новые слова по аналогии со знакомыми словами (сахарница – сухарница)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выделять первый звук в слове")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Рассказывает о содержании сюжетной картинки")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="С помощью взрослого повторяет образцы описания игрушки")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Communication, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Communication, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Коммуникация"
        verbose_name_plural = "Коммуникация"

######################## Соц-коммуникативное развитие Средняя группа ################################


class CommunicativeDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="")
    emotional = models.OneToOneField('Emotional', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Развитие социального и эмоционального интеллекта, эмоциональной отзывчивости")
    work = models.OneToOneField('Work', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Формирование готовности к совместной деятельности со сверстниками, позитивных установок к разным видам труда и творчества")
    safety = models.OneToOneField('Safety', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Формирование основ безопасного поведения в быту, социуме, природе")
    masteringcommunicat = models.OneToOneField('MasteringCommunicat', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Овладение средствами общения и способами взаимодействия")
    behaviormanagement = models.OneToOneField('BehaviorManagement', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Становление самостоятельности, целенаправленности и саморегуляции собственных действий и поведения")
    problemsolving = models.OneToOneField('ProblemSolving', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name="Развитие способности решать интеллектуальные и личностные проблемы")
    socialization = models.OneToOneField('Socialization', on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Социализация")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = self.emotional.total + self.work.total + self.safety.total + self.masteringcommunicat.total
        self.total += self.behaviormanagement.total + self.problemsolving.total + self.socialization.total
        self.total = round(self.total / 7, 2)
        super(CommunicativeDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_for_aggregate(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Социально-коммуникативное развитие"
        verbose_name_plural = "Социально-коммуникативное развитие"


class Emotional(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Эмоционально откликается на переживания близких взрослых, детей, персонажей сказок и историй, мультфильмов и художественных фильмов, кукольных спектаклей")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает и употребляет в своей речи слова, обозначающие эмоциональные состояния, этические качества, эстетические характеристики")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Emotional, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Emotional, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Эмоцианальная отзывчивость"
        verbose_name_plural = "Эмоцианальная отзывчивость"


class Work(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Самостоятельно одевается и раздевается, складывает и убирает одежду, с помощью взрослого приводит ее в порядок")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Самостоятельно выполняет обязанности дежурного по столовой, правильно сервирует стол")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Поддерживает порядок в группе и на участке детского сада")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Самостоятельно готовит к занятиям свое рабочее место, убирает материалы по окончанию работы")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Work, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Work, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Труд"
        verbose_name_plural = "Труд"


class Safety(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соблюдает элементарные правила организованного поведения в детском саду")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соблюдает правила поведения на улице и в транспорте, правила дорожного движения")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет специальные виды транспорта, объясняет их назначение (скорая помощь. пожарная, полиция)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает значение сигналов светофора, называет некоторые дорожные знаки (пешеходный переход, Дети)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает проезжую часть, тротуар, подземный переход, пешеходный переход «Зебра»")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и соблюдает элементарные правила поведения в природе (способы безопасного взаимодействия с растениями и животными, бережного отношения к окружающей природе)")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Safety, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Safety, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Безопасность"
        verbose_name_plural = "Безопасность"


class MasteringCommunicat(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет умение объединяться с детьми для совместных игр. Согласовывает тему игры. Распределяет роли, поступает в соответствии с правилами и общим замыслом. Умеет подбирать предметы и атрибуты для сюжетно – ролевых игр")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В конструктивных играх участвует в планировании действий, договаривается, распределяет материал, согласовывает действия и совместными усилиями со сверстниками достигает результата")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Активно вступает в контакты со сверстниками (ситуативно) и взрослыми (внеситуативно)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Делает попытки решать спорные вопросы и улаживать конфликты с помощью речи: убеждать, доказывать, объяснять")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(MasteringCommunicat, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(MasteringCommunicat, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Овладение средствами общения"
        verbose_name_plural = "Овладение средствами общения"


class BehaviorManagement(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет умение объединяться с детьми для совместных игр. Согласовывает тему игры. Распределяет роли, поступает в соответствии с правилами и общим замыслом. Умеет подбирать предметы и атрибуты для сюжетно – ролевых игр")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В конструктивных играх участвует в планировании действий, договаривается, распределяет материал, согласовывает действия и совместными усилиями со сверстниками достигает результата")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Активно вступает в контакты со сверстниками (ситуативно) и взрослыми (внеситуативно)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Делает попытки решать спорные вопросы и улаживать конфликты с помощью речи: убеждать, доказывать, объяснять")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(BehaviorManagement, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(BehaviorManagement, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Управление своим поведением"
        verbose_name_plural = "Управление своим поведением"


class ProblemSolving(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет инициативу и самостоятельность в организации знакомых игр с небольшой группой детей. предпринимает попытки самостоятельного обследования предметов с опорой на все органы чувств")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен конструировать по собственному замыслу. На основе пространственного расположения объектов может сказать, что произойдет в результате из взаимодействия")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен использовать простые схематические изображения для решения несложных задач, строить по схеме, решать лабиринтные задачи")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен самостоятельно придумывать небольшую сказку на заданную тему")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ProblemSolving, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ProblemSolving, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Решение интеллектуальных задач"
        verbose_name_plural = "Решение интеллектуальных задач"


class Socialization(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Объединяясь в игре со сверстниками, может принимать на себя роль, владеет способом ролевого поведения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соблюдает ролевое соподчинение (продавец – покупатель) и ведет ролевые диалоги")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В дидактических играх противостоит трудностям, подчиняется правилам")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В настольно – печатных играх может выступать в роли ведущего, объяснять сверстникам правила игры")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В самостоятельных театрализованных играх обустраивает место для игры, воплощается в роли, используя художественные средства (интонация, мимика), атрибуты, реквизит")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет простейшее представление о профессиях")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Socialization, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Socialization, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Социализация"
        verbose_name_plural = "Социализация"


######################## Физическое развитие Средняя группа ################################

class PhysicalDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    movements = models.OneToOneField('Movements', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Развитие основных видов движения")
    hygiene = models.OneToOneField('Hygiene', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name="Здоровый образ жизни")
    health = models.OneToOneField('Health', on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="Усвоение основных культурно-гигиенических навыков")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = self.movements.total + self.hygiene.total + self.health.total
        self.total = round(self.total / 3, 2)
        super(PhysicalDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_for_aggregate(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Физическое развитие"
        verbose_name_plural = "Физическое развитие"


class Movements(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Принимает правильное исходное положение при метании, может метать предметы разными способами правой и левой рукой, отбивает мяч о землю не менее 5 раз подряд")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может ловить мяч кистями рук с расстояния до 1,5 м")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет строиться в колонну по одному, парами, в круг, в шеренгу")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может скользить самостоятельно по ледяным дорожкам (длина 5м)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ходит на лыжах скользящим шагом на расстоянии до 500м, выполняет поворот переступанием, поднимается в гору")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется в пространстве, находит левую и правую стороны")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет упражнения, демонстрируя выразительность, грациозность, пластичность движений")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Movements, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Movements, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Основные движения "
        verbose_name_plural = "Основные движения"


class Hygiene(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соблюдает элементарные правила гигиены (по мере необходимости моет руки с мылом, пользуется расческой, носовым платком, прикрывает рот при кашле)")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет доступными навыками самообслуживани")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет простейшими навыками поведения во время еды, пользуется столовыми приборами")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Пользуется салфеткой, полощет рот после еды")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Hygiene, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Hygiene, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Гигиена"
        verbose_name_plural = "Гигиена"


class Health(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Обращается к взрослым при заболевании, травме")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет интерес к участию в подвижных играх и физических упражнениях")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с понятиями «здоровье», «болезнь»")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает о пользе утренней зарядки, физических упражнений, правильном питании, закаливании, гигиене")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Health, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Health, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Здоровье"
        verbose_name_plural = "Здоровье"


######################## Художественное развитие Средняя группа ################################

class ArtisticDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    artisticpersonaldevelop = models.OneToOneField('ArtisticPersonalDevelop', on_delete=models.CASCADE, blank=True,
                                                   null=True,
                                                   verbose_name="Художественно-личностное развитие")
    painting = models.OneToOneField('Painting', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name="Рисование")
    modeling = models.OneToOneField('Modeling', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Лепка")
    application = models.OneToOneField('Application', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Аппликация")
    music = models.OneToOneField('Music', on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name="Владение навыками музыкальной деятельности")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.skillsofdrawing = round((self.painting.total + self.modeling.total + self.application.total) / 3, 2)
        self.total = round((self.artisticpersonaldevelop.total + self.skillsofdrawing + self.music.total) / 3, 2)
        super(ArtisticDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_for_aggregate(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Художественное-эстетическое развитие"
        verbose_name_plural = "Художественное-эстетическое развитие"


class ArtisticPersonalDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Становление эстетического отношения к окружающему миру")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Формирование представлений о видах искусства")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Реализация самостоятельной творческой деятельности")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ArtisticPersonalDevelop, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ArtisticPersonalDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Художественно-личное развитие"
        verbose_name_plural = "Художественно-личное развитие"


class Painting(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Изображает предметы путем создания отчетливых форм, подбора цвета, аккуратного закрашивания, использования разных материалов")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Передает несложный сюжет, объединяя в рисунке несколько предметов ")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выделяет выразительные свойства дымковской и филимоновской игрушки")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Украшает силуэты игрушек элементами дымковской и филимоновской росписи")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Painting, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Painting, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Рисование"
        verbose_name_plural = "Рисование"


class Modeling(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создает образы разных предметов и игрушек")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Объединяет предметы в коллективную композицию")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует все многообразие усвоенных приемов лепки")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Modeling, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Modeling, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Лепка"
        verbose_name_plural = "Лепка"


class Application(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Правильно держит ножницы и режет ими по прямой, по диагонали (квадрат и прямоугольник); вырезает круг из квадрата, овал из прямоугольника, плавно срезает и закругляет углы")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Аккуратно наклеивает изображение предметов, состоящее из нескольких частей")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет узоры из растительных форм и геометрических фигур")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Application, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Application, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Аппликация"
        verbose_name_plural = "Аппликация"


class Music(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Узнает песни по мелодии")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Различает звуки по высоте")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может петь протяжно, четко произносить слова; вместе с другими детьми заканчивать и начинать пение")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет движения. отвечающие характеру музыки, самостоятельно меняя их в соответствии с двухчастной формой музыкального произведения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выполнять танцевальные движения: пружинка, подскоки, движение парами по кругу, кружение по одному и в парах. Может выполнять движения с предметами")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет играть на металлофоне простейшие мелодии на одном звуке")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Music, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Music, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Музыка"
        verbose_name_plural = "Музыка"


########################Диагностика психолог Средней группа ################################

class AttentionAndMemory(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Фиксирует и удерживает взгляд на предмете, педагоге")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Способен удерживать в памяти простую инструкцию и концентрироваться на выполнении каких – либо действий")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен сосредоточено действовать в течении 5 – 7 минут")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к запоминанию небольших стихотворений, до четырех строк")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Досказывает за педагогом слова знакомой сказки.")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к кратковременному зрительному запоминанию одновременно до 4х картинок")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(AttentionAndMemory, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(AttentionAndMemory, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "внимание и память"
        verbose_name_plural = "Уровень развития внимания и памяти"


class Perception(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет геометрические фигуры и геометрические тела, соотносит с формой предмета")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Знает и различает основные цвета оттенки, соотносит с цветом предмета")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает, выделяет и сравнивает величины предметов ближайшего окружения")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Показывает и называет части тела и лица на себе и на кукле")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует право-лево")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспринимает простую речевую инструкцию с первого предъявления")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет части суток")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет времена года")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Собирает разрезную картинку из 3х частей")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Perception, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Perception, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "восприятие"
        verbose_name_plural = "Уровень развития ВОСПРИЯТИЯ"


class ThinkingAndSpeaking(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает и объясняет смысл сюжетной картинки")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Собирает пирамиду из 4х колец с учетом величины")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует понятия \"один-много\", \"больше-меньше\"")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает и обозначает в речи назначение предметов повседневного пользования")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В общении активно использует жесты, мимику")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет построить фразу для продуктивного общения")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ThinkingAndSpeaking, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(ThinkingAndSpeaking, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "мышление и речь"
        verbose_name_plural = "Уровень развития МЫШЛЕНИЯ И РЕЧИ"


class EmotionsAndWill(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует и называет базовые эмоциональные состояния, настроения, самочувствия")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет адекватно реагировать на эмоциональное состояние других людей, сопереживать")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к волевой регуляции своей деятельности в течение непродолжительного времени")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет желание в развитии межличностных отношений со сверстниками")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и соблюдает элементарные правила поведения в общении, на занятии, на прогулке")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Легко адаптируется после продолжительного отсутствия в связи с болезнью или отпуском")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(EmotionsAndWill, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(EmotionsAndWill, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "ЭВС"
        verbose_name_plural = "Уровень развития ЭМОЦИОНАЛЬНО-ВОЛЕВОЙ СФЕРЫ"


class MotorDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает расположение и название некоторых пальцев")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Выполняет заданные действия: всей рукой,отдельными пальцами")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен на ошупь определить свойства обследуемого предмета")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется в схеме собственного тела")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет целенаправленно выполнять движения по словесной инструкции")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(MotorDevelop, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(MotorDevelop, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "моторное развитие"
        verbose_name_plural = "Уровень развития МОТОРНОГО РАЗВИТИЯ"


########################Диагностика зрения Средняя группа ################################

class VisualPerception(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет анализировать основные признаки предметов (форма, величина, пространственное расположение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Называет цвета: красный, желтый, синий, зеленый, оранжевый, голубой, коричневый, черный, белый. Соотносит объекты по цвету: 5 оттенков основных цветов")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет различать и называть: шар, куб, кирпич, круг, квадрат, прямоугольник, треугольник")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотнесение предметов по величине: выбор одинаковых по величине предметов из множества расположенных в пространстве. Выкладывание в порядке возрастания и убывания от 3 до 5 предметов")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Анализирует форму предмета: конфигурация из двух простых форм")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать зрительно размер длину и высоту 3-4 предметов. Словесно обозначать величину предмета")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сравнивает контурные, силуэтные предметы путем наложения и приложения. Умеет изображать простейшие пути следования на рисунке")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет описывать предметы и находить их по описанию. Называет местоположение предметов в окружающей обстановке. Ориентируется в знакомых помещениях, умеет находить середину и стороны листа")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(VisualPerception, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(VisualPerception, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "зрительное восприятие"
        verbose_name_plural = "Уровень развития зрительного восприятия"


class SBO(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет различные предметы, их детали, материал, которые окружают его в помещениях, на участке, на улице, знает их назначение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать и группировать предметы по различным признакам и наличию особенностей. Называет признаки, количество и детали предметов. Называет не менее 5 домашних животных, фруктов, овощей, некоторые растения, знает, какую пользу они приносят человеку")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с помещением детского сада. Называет свое имя и возраст, а также имя и возраст своих родителей и других близких родственников")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с трудом взрослых, имеет представление о месте работы родителей и сотрудников детского сада, орудия труда, их назначение")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с правилами поведения в общественных местах, на участке детского сада, на улице и т.д. Бережно относится к природе")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Соблюдает правила ОБЖ. Умеет различать легковые и грузовые машины, трамваи, поезд, автобус и т.д., выделяет части грузового автомобиля (кабина, кузов и т.д.)")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется с опорой на зрение, слух, обоняние. Может определить по звуку далеко ли едет машина. Знает назначение сигналов светофора и правила пешеходов.")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает строение своего тела, называет части тела и их назначение. Знает элементарные правила гигиены и здорового образа жизни. Умеет строить отношения со сверстниками и сопереживать")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(SBO, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(SBO, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "СБО"
        verbose_name_plural = "Уровень развития СБО"


class Orientation(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет принимать правильную позу при самостоятельном передвижении, в различных ситуациях")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на листе бумаги, на поверхности стола, и в названных направлениях")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет навыками обследования предметов и использование этих предметов в практической деятельности")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет передвигаться в названном направлении, сохранять и менять направление движения в соответствии с инструкциями тифлопедагога")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет моделировать замкнутое пространство и пространственные отношения между предметами в нем расположенными")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о простейшем схематическом условном изображении различных предметов. Знаком с простейшей схемой")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на своем теле, знает пространственное расположение частей своего тела, использует в речи пространственные термины")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Orientation, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Orientation, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "ориентировка в пространстве"
        verbose_name_plural = "Уровень развития навыков ориентировки в пространстве"


class Touch(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает о строении и возможностях рук, умеет действовать отдельными пальцами при выполнении микродинамических актов и упражнений (спрячь мизинец в кулачок другой руки)")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет с помощью осязания различать геометрические фигуры: круг, квадрат, треугольник, овал")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет различать свойства поверхности на ощупь (гладкая, мягкая, твердая)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет на ощупь определять температуру предмета (теплый, горячий, холодный)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет с помощью осязания определять размер, материал, детали предметов знакомого окружения")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Сортирует мелкие предметы по форме и величине")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на микроплоскости стола и листа. Определяет середину, левую и правую стороны. Расставляет игрушки в заданном порядке")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет обследовать себя и других людей, выделяя характерные признаки строения тела")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Touch, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Touch, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "осязание и мелкая моторика"
        verbose_name_plural = "Уровень развития осязания и мелкой моторики"


# TODO функция которая отслеживает создание в модели Child новой записи(вызова .save()), которая создает во всех моделях, запись с этим ребенком
@receiver(post_save, sender=Child)
def create_marks(sender, instance: Child, created, **kwargs):
    app_models = apps.get_app_config('middle_group').get_models()
    grades = {"child": instance}
    main_models = {}
    model_links = {}
    for model in app_models:
        model_name = model._meta.model_name
        model_fields = [field.name for field in model._meta.get_fields()]
        if model_name != "child":
            if 'param1' not in model_fields:
                model_links[model_name] = model_fields
                main_models[model_name] = model
                continue
            new_grade = model(child=instance)
            new_grade.save()
            grades[model_name] = new_grade
    for fields_set in model_links.keys():
        values = {}
        for field in model_links[fields_set]:
            if field in grades.keys():
                values[field] = grades[field]
        main_models[fields_set](**values).save()


@receiver(post_save, sender=Math)
@receiver(post_save, sender=ViewOfWorld)
@receiver(post_save, sender=PrimaryRepresent)
@receiver(post_save, sender=UniversalPrerequisite)
@receiver(post_save, sender=Cognition)
@receiver(post_save, sender=Skills)
@receiver(post_save, sender=Activities)
def my_handler(sender, instance: Math, **kwargs):
    if CognitiveDevelop.objects.all().filter(id=instance.id).first() is not None:
        CognitiveDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=SpeechActivity)
@receiver(post_save, sender=Reading)
@receiver(post_save, sender=Communication)
def my_handler(sender, instance: Math, **kwargs):
    if SpeechDevelop.objects.all().filter(id=instance.id).first() is not None:
        SpeechDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=Emotional)
@receiver(post_save, sender=Work)
@receiver(post_save, sender=Safety)
@receiver(post_save, sender=MasteringCommunicat)
@receiver(post_save, sender=BehaviorManagement)
@receiver(post_save, sender=ProblemSolving)
@receiver(post_save, sender=Socialization)
def my_handler(sender, instance: Math, **kwargs):
    if CommunicativeDevelop.objects.all().filter(id=instance.id).first() is not None:
        CommunicativeDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=Movements)
@receiver(post_save, sender=Hygiene)
@receiver(post_save, sender=Health)
def my_handler(sender, instance: Math, **kwargs):
    if PhysicalDevelop.objects.all().filter(id=instance.id).first() is not None:
        PhysicalDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=ArtisticPersonalDevelop)
@receiver(post_save, sender=Painting)
@receiver(post_save, sender=Modeling)
@receiver(post_save, sender=Application)
@receiver(post_save, sender=Music)
def my_handler(sender, instance: Math, **kwargs):
    if ArtisticDevelop.objects.all().filter(id=instance.id).first() is not None:
        ArtisticDevelop.objects.all().filter(id=instance.id).first().save()
