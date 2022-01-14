from django.conf import settings
from django.db import models
from django.apps import apps
from django.db.models.signals import post_save, pre_save
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
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='mlad_teacher', null=True,
                                verbose_name="Воспитатель")

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"


######################## Познавательное развитие Младшая группа ################################

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
                                              verbose_name="Умеет группировать предметы по цвету, размеру, форме")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может составлять группы из однородных предметов и выделять один предмет из группы")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет находить в окружающей обстановке один и много одинаковых предметов ")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Правильно определяет количественное соотношение двух групп предметов, понимает конкретный смысл слов «больше», «меньше», «столько же»")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает квадрат, круг, треугольник, предметы имеющие углы и круглую форму")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает смысл обозначений: вверху-внизу, впереди-сзади, слева-справа, на, над-под, верхняя-нижняя")
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
                                              verbose_name="Называет знакомые предметы, объясняет их назначение, выделяет и называет признаки")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется в помещениях детского сада")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Называет свой город")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Знает и называет некоторые растения, животных и их детенышей")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выделяет наиболее характерные сезонные изменения в природе")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет бережное отношение к природе")
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
                                              verbose_name="Имеет первичные представления о себе: знает свое имя, возраст, пол. Имеет первичные гендерные представления")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Называет членов семьи, их имена. ")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Знает название родного города")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Знаком с некоторыми профессиями")
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
                                              verbose_name="Соблюдает правила организованного поведения в детском саду, дома, на улице. В случае проблемной ситуации обращается за помощью к взрослому")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Испытывает положительные эмоции от результатов продуктивной и познавательной деятельности")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В диалоге со взрослыми умеет услышать и понять заданный вопрос, не перебивает говорящего взрослого")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет интерес к книгам, рассматривает иллюстрации")
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
                                              verbose_name="Знает, называет и правильно использует детали строительного материала")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет располагать кирпичики, пластины вертикально")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Изменяет постройки, надстраивая или заменяя одни детали другими")
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
        verbose_name = "Познание"
        verbose_name_plural = "Познание"


class Skills(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Игровые")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Продуктивные")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Трудовые")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Комуникативные")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Двигательные")
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
                                              verbose_name="Принимает активное участие во всех видах игр")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет интерес к себе, окружающему предметному и животному миру, природе, задает вопросы взрослым, наблюдает")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Принимает активное участие в продуктивной деятельности, испытывает удовольствие от коллективных работ, просмотра спектаклей и их обсуждения")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Пытается петь, танцевать под музыку, проявляет интерес к праздникам")
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

######################## Речевое развитие Младшая группа ################################


class SpeechDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    speechactivity = models.OneToOneField('SpeechActivity', on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Речевая деятельность")
    reading = models.OneToOneField('Reading', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Чтение")
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
    param1 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES, verbose_name="Обогащение активного словаря")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Развитие связной, грамматически правильной речи")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Развитие звуковой и интонационной культуры речи, фонематического слуха")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Формирование звуковой аналитико-синтетической активности")
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
                                              verbose_name="Пересказывает содержание произведения с опорой на рисунки в книге и на вопросы воспитателя")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет произведение, прослушав отрывок из него")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может наизусть прочитать небольшое стихотворение при помощи взрослого")
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
                                              verbose_name="Отвечает на вопросы взрослого, касающиеся ближайшего окружения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует все части речи, простые нераспространенные предложения и предложения с однородными членами")
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

######################## Соц-коммуникативное развитие Младшая группа ################################


class CommunicativeDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="")
    emotional = models.OneToOneField('Emotional', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name=" Развитие социального и эмоционального интеллекта, эмоциональной отзывчивости")
    work = models.OneToOneField('Work', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Формирование готовности к совместной деятельности со сверстниками, позитивных установок к разным видам труда и творчества")
    safety = models.OneToOneField('Safety', on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Формирование основ безопасного поведения в быту, социуме, природе")
    masteringcommunicat = models.OneToOneField('MasteringCommunicat', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Овладение средствами общения и способами взаимодействия")
    behaviormanagement = models.OneToOneField('BehaviorManagement', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Становление самостоятельности, целенаправленности и саморегуляции собственных действий")
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
                                              verbose_name="Умеет проявлять доброжелательность, доброту, дружелюбие, по отношению к окружающим")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Эмоционально-заинтересованно следит за развитием действия в сказках, драматизациях и кукольных спектаклях, сопереживает персонажам")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет эмоциональную отзывчивость на произведения изобразительного искусства, красоту окружающих предметов и объектов природы")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет эмоциональную отзывчивость на доступные возрасту музыкальные произведения, различает веселые и грустные мелодии")
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
                                              verbose_name="Умеет самостоятельно одеваться и раздеваться в определенной последовательности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может помочь накрыть стол к обеду")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может ухаживать за растениями с помощью воспитателя")
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
                                              verbose_name="Соблюдает элементарные правила взаимодействия с растениями и животными")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет элементарные представления о правилах дорожного движения")
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
                                              verbose_name="Умеет в быту, в самостоятельных играх посредством речи налаживать контакты, взаимодействовать со сверстниками")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет объединяться со сверстниками для игры в группу из 2-3 человек на основе личных симпатий, выбирать роль в сюжетно-ролевой игре")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет делиться своими впечатлениями со взрослыми")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Адекватно реагирует на замечания и предложения взрослого. Обращается к воспитателю по имени и отчеству")
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
                                              verbose_name="Имеет положительный настрой на соблюдение элементарных правил поведения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет действовать совместно в подвижных играх и физических упражнениях, согласовывать движения. Готов соблюдать элементарные правила в совместных играх")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может общаться спокойно, без крика, имеет опыт правильной оценки хороших и плохих поступков. Соблюдает правила элементарной вежливости")
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
                                              verbose_name="Стремится самостоятельно выполнять элементарные поручения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может самостоятельно подобрать атрибуты для роли, дополнять игровую обстановку предметами или игрушками")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует разные способы обследования предметов, включая простейшие опыты. Способен устанавливать простейшие связи между предметами и явлениями, делать простые обобщения.")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет занимать себя игрой, самостоятельной художественной деятельностью.")
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
                                              verbose_name="Может принимать на себя роль, непродолжительно взаимодействовать со сверстниками в игре от имени героя")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет объединять несколько игровых действий в единую сюжетную линию; отражать в игре действия с предметами и взаимоотношения людей")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен придерживаться правил в дидактических играх")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен следить за развитием театрализованного действия и эмоционально на него отзываться")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Разыгрывает по просьбе взрослого и самостоятельно небольшие отрывки из знакомых сказок")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имитирует движения, мимику, интонацию изображаемых героев")
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


######################## Физическое развитие Младшая группа ################################

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
                                              verbose_name="Умеет ходить прямо, не шаркая ногами, сохраняя заданное направление")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет бегать, сохраняя равновесие, изменяя направление, темп бега в соответствии с указаниями")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сохраняет равновесие при ходьбе и беге по ограниченной плоскости при перешагивании через предметы")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может ползать на четвереньках, лазать по лесенке-стремянке, гимнастической стенке произвольным способом")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Энергично отталкивается в прыжках на двух ногах, прыгает в длину с места не менее чем на 40 см")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может катать мяч в заданном направлении с расстояния 1,5м, бросать мяч двумя руками от груди, из-за головы, ударять мячом об пол, бросать его вверх 2-3 раза подряд и ловить, метать предметы обеими руками на расстояние не менее 5 м")
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
                                              verbose_name="Приучен к опрятности (замечает непорядок в одежде, устраняет его при небольшой помощи взрослых)")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет простейшими навыками поведения во время еды, умывания ")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет доступными навыками самообслуживания")
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
                                              verbose_name="Проявляет двигательную активность, интерес к совместным играм и физическим упражнениям")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет элементарные представления о ценности здоровья, пользе закаливания, соблюдения гигиены")
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


######################## Художественное развитие Младшая группа ################################

class ArtisticDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    artisticpersonaldevelop = models.OneToOneField('ArtisticPersonalDevelop', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Художественно-личностное развитие")
    painting = models.OneToOneField('Painting', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Рисование")
    modeling = models.OneToOneField('Modeling', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Лепка")
    application = models.OneToOneField('Application', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Апликация")
    music = models.OneToOneField('Music', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Музыка")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = self.artisticpersonaldevelop.total + self.painting.total + self.modeling.total + self.application.total + self.music.total
        self.total = round(self.total / 5, 2)
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
                                              verbose_name="Изображает отдельные предметы, простые по композиции и незамысловатые по содержанию сюжеты")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Подбирает цвета соответствующие изображаемым предметам")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Правильно пользуется карандашами, фломастерами, кистью и красками")
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
                                              verbose_name="Умеет отделять от большого куска небольшие комочки, раскатывать их прямыми и круговыми движениями ладоней")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Лепит различные предметы, состоящие из 1-3 частей, используя разнообразные приёмы лепки")
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
                                              verbose_name="Создает изображение предметов из готовых фигур")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Украшает заготовки из бумаги разной формы")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет аккуратно использовать материалы")
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
                                              verbose_name="Слушает музыкальное произведение до конца")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Узнает знакомые песни")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает звуки по высоте (в пределах октавы)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Замечает изменения в звучании (тихо-громко)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Поет, не отставая и не опережая других")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выполнять танцевальные движения")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет детские музыкальные инструменты")
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


########################Диагностика психолог Старшая группа ################################

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
                                              verbose_name="Показывает и называет части тела и лица на себе и на кукл")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует право-лево, верх-низ")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспринимает простую речевую инструкцию с первого предъявления")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет части суток")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет времена года")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Собирает разрезную картинку из 3х частей.")
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
                                              verbose_name="Собирает пирамиду из 4х колец с учетом величины.")
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
                                              verbose_name="Выполняет заданные действия: всей рукой, отдельными пальцами")
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


########################Диагностика зрения Старшая группа ################################

class VisualPerception(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет анализировать основные признаки предметов (форма, цвет, величина, пространственное положение). группирует предметы по одному признаку")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Знает и называет цвета: красный, желтый, синий, зеленый, оранжевый, черный, белый,")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотносит объекты по цвету: 3 оттенка красного, желтого, синего, зеленого. Умеет показывать игрушки определенного цвета.")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет различать и называть:   круг, квадрат,  треугольник, прямоугольник")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выкладывает в порядке возрастания и убывания от 3 до 5 предметов")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать зрительно размер, длину и высоту 2-3 предметов,  словесно обозначать величину: большой –  маленький длинный – короткий")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сравнивает контурные, силуэтные предметы путем наложения и приложения")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет местоположение предмета в окружающей обстановке. Ориентируется в знакомых помещениях, умеет находить середину листа, сторон")
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
                                              verbose_name="Называет предметы, которые окружают его в помещении, на участке, на улице,  их количество.Знает детали предметов, их назначение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать и группировать предметы по различным признакам и наличию особенностей. Наблюдает на улице за движущимся транспортом, людьми, животными Понимает значение медленно - быстро")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и соблюдает элементарные правила поведения  Знаком с помещением детского сада. Знает  как пройти в умывальную, раздевалку, как найти кровать, шкафчик и.т.д..")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="С помощью взрослого повторяет образцы описания игрушки. Знает о труде взрослых в детском саду и своих родителей")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о здоровом образе жизни")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет наблюдать за своим внешним видом. ")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет свое имя, фамилию, возраст свой, родителей и близких родственников.")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление  об одежде, обуви, мебели, посуде, транспорте, зданиях и помещениях")
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
                                              verbose_name="Различает и правильно называет части своего тела, других детей, кукол, соотнося со своим теломЗнает детали предметов, их назначение")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет согласовывать, координировать  движения рук и ног   при ходьбе и беге. Умеет самостоятельно подниматься и спускаться по лестнице, держась за перила")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется в групповой комнате, знает расположение помещений, игрушек, мебели. Самостоятельно находит свой шкафчик, стол, кровать.")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает пространственные признаки окружающих предметов с помощью зрения. Умеет ориентироваться с помощью зрения, обоняния, осязания.")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет способом зрительно – осязательного обследования предметов и игрушек. Различает контрастные по величине предметы, обозначает соответствующими словами: большой, маленький")
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
                                              verbose_name="Знает о назначении рук и пальцев. Выполняет по показу простые действия. Умеет обследовать знакомые, крупные предметы на ощупь")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Различает на ощупь знакомые формы: круг, квадрат, треугольник")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может на ощупь определить характерные признаки предмета (твердый - мягкий, большой - маленький)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет на ощупь находить ручку на двери, стену, препятствие перед собой")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет классифицировать знакомые группы предметов ")
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
    app_models = apps.get_app_config('junior_group').get_models()
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
def my_handler(sender, instance: CognitiveDevelop, **kwargs):
    if CognitiveDevelop.objects.all().filter(id=instance.id).first() is not None:
        CognitiveDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=SpeechActivity)
@receiver(post_save, sender=Reading)
@receiver(post_save, sender=Communication)
def my_handler(sender, instance: SpeechDevelop, **kwargs):
    if SpeechDevelop.objects.all().filter(id=instance.id).first() is not None:
        SpeechDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=Emotional)
@receiver(post_save, sender=Work)
@receiver(post_save, sender=Safety)
@receiver(post_save, sender=MasteringCommunicat)
@receiver(post_save, sender=BehaviorManagement)
@receiver(post_save, sender=ProblemSolving)
@receiver(post_save, sender=Socialization)
def my_handler(sender, instance: CommunicativeDevelop, **kwargs):
    if CommunicativeDevelop.objects.all().filter(id=instance.id).first() is not None:
        CommunicativeDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=Movements)
@receiver(post_save, sender=Hygiene)
@receiver(post_save, sender=Health)
def my_handler(sender, instance: PhysicalDevelop, **kwargs):
    if PhysicalDevelop.objects.all().filter(id=instance.id).first() is not None:
        PhysicalDevelop.objects.all().filter(id=instance.id).first().save()


@receiver(post_save, sender=ArtisticPersonalDevelop)
@receiver(post_save, sender=Painting)
@receiver(post_save, sender=Modeling)
@receiver(post_save, sender=Application)
@receiver(post_save, sender=Music)
def my_handler(sender, instance: ArtisticDevelop, **kwargs):
    if ArtisticDevelop.objects.all().filter(id=instance.id).first() is not None:
        ArtisticDevelop.objects.all().filter(id=instance.id).first().save()







