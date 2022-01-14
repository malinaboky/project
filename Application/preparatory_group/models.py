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
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='prep_teacher', null=True,
                                verbose_name="Воспитатель")

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"


######################## Познавательное развитие Подготовительная группа ################################

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
                                              verbose_name="Самостоятельно объединяет  группы по общему признаку в единое множество и удаляет из множества отдельные его части")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Устанавливает связи и отношения между целым множеством и различными его частями, находит части целого множества и целое по известным частям")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Считает в пределах 20 (количественный и порядковый счет)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет числа в прямом и обратном порядке до 10, начиная с любого числа натурального ряда")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотносит цифру (0-9) и количество предметов")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет и решает задачи в одно действие на сложение и вычитание, пользуется цифрами и арифметическими знаками")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает величины (длину ширину, высоту), объем (вместимость), массу (вес предметов) и способы их измерения.  Измеряет с помощью условной мерки, понимает зависимость между величиной")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Math, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Math, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Математика"
        verbose_name_plural = "РЭМП"


class ViewOfWorld(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет разнообразные впечатления о предметах окружающего мира")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает герб, флаг, гимн России")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает  название родного города, страны, её столицу")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о родном крае, его достопримечательностях")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о школе, библиотеке")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает некоторых представителей животного мира (звери, птицы, пресмыкающиеся, земноводные, насекомые)")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает характерные признаки времён года и соотносит с каждым сезоном особенности жизни людей, животных, растений")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает правила поведения в природе и соблюдает их")
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
                                              verbose_name="Имеет представление о себе, собственной принадлежности и принадлежности других людей к определенному полу: о составе семьи, родственных отношениях, распределении семейных обязанностей, семейных традициях, об обществе, культурных ценностях")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Имеет представление о РФ, культурных ценностях, мире")
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
                                              verbose_name="Умеет работать по правилу и образцу")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет слушать взрослого и выполнять его инструкции")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен сосредоточенно действовать в течение 20-30 минут")
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
                                              verbose_name="Способен соотносить конструкцию предмета с его назначением")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен создавать различные конструкции одного и того же объекта")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может создавать модели из пластмассового и деревянного конструкторов по рисунку и словесной инструкции")
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
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Двигательные")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Продуктивные")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Познавательно-исследовательские")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Трудовые")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Коммуникативные")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES, verbose_name="Музыкально-художественные")
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
                                              verbose_name="Задает вопросы взрослому, любит экспериментировать, интересуется новым, активен на занятиях")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен самостоятельно действовать в повседневной жизни")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="При затруднениях обращается за помощью к взрослому")
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

######################## Речевое развитие Подготовительная группа ################################


class SpeechDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    speechactivity = models.OneToOneField('SpeechActivity', on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Речевая деятельность")
    reading = models.OneToOneField('Reading', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Чтение художественной литературы")
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
    param1 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES, verbose_name="(Звуковая культура речи)Свистящие")
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
                                              verbose_name="Знает 2-3 программных стихотворения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает 2-3 считалки, загадки")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает жанры литературных произведений")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выразительно читает стихотворение, пересказывает отрывок из сказки, рассказа")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет любимые сказки и рассказы")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет 2-3 авторов и 2-3 иллюстраторов книг")
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
        verbose_name = "Чтение художественной литературы"
        verbose_name_plural = "Чтение художественной литературы"


class Communication(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Пересказывает и драматизирует небольшие литературные произведения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет по плану и образцу рассказы о предмете")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет по плану и образцу рассказы по сюжетной картинке")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет по плану и образцу рассказы по набору картин с фабульным развитием действия")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Употребляет в речи синонимы, антонимы, сложные предложения")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает понятия «звук», «слог», «слово», «предложение»")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Находит в предложении слова с заданным звуком, определяет место звука в слове")
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

######################## Соц-коммуникативное развитие Подготовительная группа ################################


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
                                              verbose_name="Эмоционально откликается на переживания близких взрослых, детей, персонажей сказок и историй, мультфильмов и художественных фильмов, кукольных спектаклей")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Эмоционально реагирует на произведения изобразительного искусства, музыкальные и художественные произведения, мир природы")
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
                                              verbose_name="Самостоятельно ухаживает за одеждой, устраняет непорядок в своём внешнем виде")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ответственно выполняет обязанности дежурного по столовой, в уголке природы")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет трудолюбие в работе на участке детского сада")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может планировать свою трудовую деятельность, отбирать материалы, необходимые для занятий, игр")
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
                                              verbose_name="Различает и называет специальные виды транспорта, объясняет их назначение")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает значение сигналов светофоров, называет некоторые дорожные знаки")
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
                                              verbose_name="Адекватно пользуется вербальными и невербальными средствами общения, конструктивными способами взаимодействия с детьми и взрослыми")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен изменять стиль общения со взрослым и сверстником в зависимости от ситуации")
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
                                              verbose_name="Поведение регулируется требованиями взрослых и первичными ценностными ориентациями")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен планировать свои действия для достижения конкретной цели")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соблюдает правила поведения на улице, в общественных местах")
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
                                              verbose_name="Самостоятельно применяет усвоенные способы деятельности, в зависимости от ситуации изменяет способы решения задач")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен предложить собственный замысел и воплотить в рисунке, постройке, рассказе")
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
                                              verbose_name="Самостоятельно отбирает или придумывает разнообразные сюжеты игр")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Придерживается в процессе игры намеченного замысла, оставляя место для импровизации")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В дидактических играх договаривается со сверстниками об очередности ходов, проявляет себя терпимым и доброжелательным партнёром")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает образный строй спектакля: оценивает игру актёров, средства выразительности и оформление постановки")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет навыками театральной культуры: знает театральные профессии, правила поведения в театре")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Участвует в творческих группах по созданию спектаклей («режиссёры», «актёры», «костюмеры», «оформители» и т.д.)")
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
                                              verbose_name="Выполняет правильно все виды основных движений")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может прыгать и мягко приземляться с высоты до 40см, в длину с места (не менее 1м), с разбега – 1,8м, в высоту с разбега (не менее 50см), прыгать через короткую и длинную скакалку разными способами")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может перебрасывать набивные мячи (1кг), бросать предметы в цель из разных исходных положений, попадать в вертикальную и горизонтальную цель с расстояния 4-5м, метать предметы двумя руками (5-12м), метать предметы в движущую цель ")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет перестраиваться в 3-4 колонны, в 2-3 круга на ходу, в две шеренги после расчета на «первый-второй», соблюдать интервалы во время передвижения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет физические упражнения из разных исходных положений четко и ритмично, в заданном темпе")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Следит за правильной осанкой")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ходит на лыжах переменным скользящим шагом (3км), поднимается на горку и спускается с нее, тормозит при спуске")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Участвует в играх с элементами спорта")
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


class Health(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сформированы основные физические качества и потребность в двигательной активности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет сформированные представления об особенностях строения и функциями организма человека,  о рациональном питании, о значении двигательной активности в жизни человека")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет сформированные представления  о важности соблюдения режима дня, о пользе и видах закаливающих процедур, о роли солнечного света, воздуха и воды в жизни человека и их влиянии на здоровье")
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


class Hygiene(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Усвоил основные культурно-гигиенические навыки (быстро и правильно умывается, насухо вытирается, пользуясь только индивидуальным полотенцем, чистит зубы, поласкает рот после еды, моет ноги перед сном, правильно пользуется носовым платком и расческой, следит за своим внешним видом, быстро раздевается и одевается, вешает одежду в определенном порядке, следит за чистотой одежды")
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


######################## Художественное развитие Подготовительная группа ################################

class ArtisticDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    artisticpersonaldevelop = models.OneToOneField('ArtisticPersonalDevelop', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Художественно-личностное развитие")
    painting = models.OneToOneField('Painting', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Рисование")
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
                                              verbose_name="Создаёт индивидуальные и коллективные рисунки, предметные  и  сюжетные композиции на темы окружающей жизни, литературных произведений")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует различные цвета и оттенки для создания выразительных образов")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет узоры по мотивам народного декоративно-прикладного искусства")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует различные материалы и способы создания изображения")
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
                                              verbose_name="Лепит различные предметы, передавая их форму, пропорции, позы, движения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создаёт сюжетные композиции из 2-3 и более изображений")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет декоративные композиции способами налепа и рельефа")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Расписывает вылепленные изделия по мотивам народного искусства")
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
                                              verbose_name="Различает виды изобразительного искусства: живопись, графика, скульптура, декоративно-прикладное и народное искусство")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет основные выразительные средства произведений искусства")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создает изображения различных предметов, используя бумагу разной фактуры и способы вырезания и обрывания")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создает сюжетные и декоративные композиции")
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
                                              verbose_name="Определяет жанр прослушанного произведения и инструмент, на котором оно исполняется")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Определяет общее настроение, характер музыкального произведения")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает части произведения (вступление, заключение, запев, припев)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может петь песни в удобном диапазоне, исполняя их выразительно, правильно передавая мелодию")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может петь индивидуально и коллективно, с сопровождением и без него")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выразительно и ритмично двигаться в соответствии с разнообразным характером музыки, музыкальными образами, передавать несложный музыкальный ритмический рисунок")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выполнять танцевальные движения (шаг с притопом, приставной шаг с приседанием, пружинящий шаг, боковой галоп, переменный шаг)")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Инсценирует игровые песни, придумывает варианты образных движений в играх и хороводах")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Исполняет сольно и в ансамбле на ударных и звуковысотных детских музыкальных инструментах несложные песни и мелодии")
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
                                              verbose_name="Способен к самостоятельной концентрации, удержанию и переключению внимания во время занятия")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Способен удерживать в памяти сложную инструкцию и концентрироваться на выполнении каких – либо действий ")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен удерживать в памяти одновременно до 2-3 простых элементов")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспроизводит стихотворения по памяти")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к кратковременному опосредованному зрительному запоминанию одновременно до 7ми картинок")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к кратковременному зрительному запоминанию одновременно до 7ти картинок")
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
                                              verbose_name="Знает и различает основные цвета спектра и оттенки, находит предметы заданного цвета в окружающей обстановке")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет величину предмета, обозначает это в речи")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует и называет изображения в затрудненном для восприятия виде")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспринимает сюжетные многоплановые изображения")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет с помощью осязания определять размер, материал, детали предметов окружения")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспринимает составную речевую инструкцию с первого предъявления")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет части суток, времена года, названия месяцев")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Собирает разрезную картинку из 6ти частей")
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
                                              verbose_name="Умеет отгадывать описательные и стихотворные загадки, решает логические задачи, при решении видит закономерности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Способен к объединению предметов и признаков во множества по заданному принципу, самостоятельно аргументирует выбор множества для предмета, признака")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к сравнению двух предметов по количеству, размеру, форме, цвету; процесс сравнения сопровождает словесным описанием")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет составить рассказ по серии сюжетных картин, видит скрытый смысл")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создание уникальных образов в процессе одного или нескольких видов творческой деятельности")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к сотрудничеству, планированию и самоконтролю; проявляет инициативу")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В общении активно использует жесты, мимику, при воспроизведении стихотворений и в играх пользуется средствами выразительности")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет построить сложную фразу для продуктивного диалога со сверстниками и педагогами, способен аргументировать свою позицию во время дискуссии на занятии")
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
                                              verbose_name="Дифференцирует и называет эмоциональные состояния, настроения, самочувтствия как свои, так и окружающих сверстников")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет адекватно реагировать на эмоциональное состояние других людей, сопереживать")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к волевой регуляции своей деятельности в течение занятия")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет поддержать диалог, заводит дружеские связи")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и соблюдает  правила поведения в общении, на занятии, на прогулке, в общественных местах")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет потребность в проявлении ответственности, настойчивости, стремлении быть аккуратным, старательным")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет подчинять свое поведение не желаниям и потребностям, а требованиям со стороны взрослых")
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
                                              verbose_name="Выполняет действия двумя руками")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Отражает в речи осязательные и тактильные восприятия")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется в схеме собственного тела, на микроплоскости, в знакомых помещениях")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет целенаправленно выполнять движения по словесной инструкции, совершает самоконтроль")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет правильно держать карандаш при письме")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Обладает достаточной моторной ловкостью для выполнения графических узоров")
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
                                              verbose_name="Умеет называть  темно-серый и светло-серый цвета. Соотносит  до 15 оттенков красного, зеленого, синего, коричневого; 7-8 оттенков оранжевого, фиолетового, желтого, голубого, 5 оттенков серого. ")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name=" Умеет описывать окраску некоторых предметов. Узнает  и называет трапецию в различных конфигурациях и модальностях. Видоизменяет геометрические фигуры, составляет  из различных фигур конфигурацию предмета из простых форм.")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает однородные предметы по различиям в конфигурации частей. Соотносит и подбирает предметы по величине на глаз без нарушения пропорций из множества разо расположенных")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выкладывает  в порядке убывания и возрастания до 7 предметов по словесному указанию")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет зрительно сравнивать длину, высоту, ширину, толщину нескольких предметов расположенных в разных направлениях.")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет в зашумленном пространстве знакомые предметы. Видит в рисунке перспективу. Составляет целое изображение из частей")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет ориентироваться в окружающей действительности  с помощью органов чувств .Умеет составлять и читать схемы пути  сточкой отсчета от себя и других предметов")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет на глаз и с помощью условной мерки размеры предметов и расстояние между ними")
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
                                              verbose_name="Умеет описывать основные признаки предмета, знает правила его использования, хранения. ")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представления о временной перспективе личности, об изменении  позиции человека с возрастом. Закреплять гендерные представления.")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представления о родном крае, Родине, государственной символике, Российской армии. воспитывать интерес и любовь к произведениям великих поэтов, композиторов и художников. знакомить с произведениями национального искусства")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представления об опасных ситуациях и способах поведения в них. Знаком с правилами ОБЖ Умеет ориентироваться  на улице с использованием сохранных анализаторов и зрения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет правила безопасного дорожного движения в качестве пешехода и пассажира транспортного средства")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представления о здоровом образе жизни, и желание сохранять и укреплять свое здоровье. ")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с конкретными видами труда взрослых. Умеет использовать знания в игровых ситуациях Самостоятельно отбирать и придумывать разнообразные сюжеты игр")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет сформированную мотивацию к учебной деятельности, осознает  себя в качестве школьника")
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
                                              verbose_name="Имеет представление об относительности пространственных направлений в процессе соотнесения парно противоположных направлений.")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет самостоятельно ориентироваться в помещениях детского сада, на территории. Обозначать в речи свой путь до различных помещений детского сада, участка.")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет  моделировать пространственные отношения между предметами.")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет передвигаться в пространстве ориентируясь по схеме и плану (маршрута) пути, обозначая в речи направления своего движения. Умеет различать пространственные признаки и отношения с помощью зрения и осязания")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет самостоятельно составлять планы различных помещений, участка")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет сравнивать, соотносить пространственные направления своего тела и стоящего напротив человека")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет и сравнивает местоположение предметов, находящихся на большом расстоянии.")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Располагает и находит предметы в реальном пространстве, ориентируясь по схеме")
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
                                              verbose_name="Знает о строении и возможностях рук, расположение,  и назначении пальцев. Умеет обследовать предметы и изображения предметов  в заданной последовательности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Знает и выделяет сенсорные эталоны формы. Умеет на ощупь различать объемные и плоскостные формы (Составь из двух частей круг. Найди в закрытой коробке все круглые, овальные и квадратные предметы)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет на ощупь характер поверхности: гладкая, шероховатая, твердая, мягкая, горячая, холодная и.т.д. ")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет на ощупь определять размер предметов, сравнивать путем наложения и приложения. С помощью условных мерок. (Узнай, где самая длинная лента)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет использовать осязание при ориентировке в окружающих предметах. (Где стекло в окне? Угадай, где ты стоишь, найди все шелковые, шерстяные, ситцевые ткани)")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Классифицирует предметы по разным осязательным признакам (все жесткие, овальные, металлические и т.д.) (Найди все мягкие предеты")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на микроплоскости стола, листа Определяет стороны листа, левый и правый углы середину, умеет размещать предметы по заданному образцу")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает строение своего тела, и других людей, выделяет характерные признаки (голова круглая, плечи покатые, руки худые и.т.д.) (Чей рост выше? У кого ноги длиннее?, Что у человека мягкое?)Умеет различать ритм ласковых, строгих, нежных, слабых, сильных движений")
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
    app_models = apps.get_app_config('preparatory_group').get_models()
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
