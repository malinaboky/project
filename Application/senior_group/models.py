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
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='sen_teacher', null=True,
                                verbose_name="Воспитатель")

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"


######################## Познавательное развитие Старшая группа ################################

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
                                              verbose_name="Считает (отсчитывает) в пределах 10")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Правильно пользуется количественными и порядковыми числительными (в пределах 10), отвечает на вопросы: Сколько? Который по счету?")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Уравнивает неравные группы предметов двумя способами (удаление и добавление единицы)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сравнивает предметы на глаз проверяет точность определений путем наложения или приложения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Размещает предметы различной величины (7-10) в порядке возрастания, убывания")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выражает словами местонахождение предмета по отношению к себе, другим предметам")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает некоторые характерные особенности знакомых геометрических фигур (количество углов, сторон, равенство и  неравенство сторон)")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет части суток, имеет представление об их смене")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет текущий день недели")
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
                                              verbose_name="Различает и называет виды транспорта, предметы, облегчающие труд человека в быту")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Классифицирует предметы, определяет материалы, из которых они сделаны")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает название родного города, страны, её столицу")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Называет времена года, отмечает их особенности")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает о взаимодействии человека с природой в разное время года")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает о значении солнца, воздуха и воды для человека, животных, растений")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Бережно относится к природе")
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
                                              verbose_name="Знает  и называет свое имя, фамилию, возраст, пол, имена и отчества членов семьи. Знает где работают родители, как важен для общества их труд. Знает семейные праздники. Имеет постоянные обязанности по дому")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может рассказать о своем городе, называет свою улицу")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о Российской армии, войне, Дне Победы")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о флаге, гербе, мелодии гимна РФ, знает о Москве")
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
                                              verbose_name="Проявляет ответственность в трудовых поручениях, стремиться радовать взрослых хорошими поступками")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен удерживать в памяти при выполнении каких-либо действий несложное условие. Способен принять установку на запоминание")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может выразительно, связно и последовательно рассказать небольшую сказку, может выучить небольшое стихотворение")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен сосредоточено действовать в течение 15-25 минут")
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
        verbose_name = "Овладение универсальными предпосылками учебной деятельности"
        verbose_name_plural = "Овладение универсальными предпосылками учебной деятельности"


class Cognition(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    param1 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет анализировать образец постройки")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может планировать этапы создания собственной постройки, находить конструктивные решения")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создает постройки по рисунку")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет работать коллективно")
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
        verbose_name = "ОО «Познание» продуктивная (конструктивная) деятельность старшая группа"
        verbose_name_plural = "ОО «Познание» продуктивная (конструктивная) деятельность старшая группа"


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
                                              verbose_name="Проявляет устойчивый интерес к различным видам детской деятельности, использует различные источники информации ")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Проявляет любознательность, интерес к исследовательской деятельности, экспериментированию")
    total = models.FloatField(blank=True, null=True, verbose_name='Средний итог')

    def save(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Activities, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = get_middle_value(self)
        super(Skills, self).save(*args, **kwargs)

    @property
    def middle(self):
        return get_middle_value(self)

    def __str__(self):
        return str(self.middle)

    class Meta:
        verbose_name = "Любознательный, активный"
        verbose_name_plural = "Любознательный, активный"

######################## Речевое развитие Старшая группа ################################


class SpeechDevelop(models.Model):
    child = models.OneToOneField("Child", on_delete=models.CASCADE, blank=True, null=True, verbose_name="ФИ ребенка")
    speechactivity = models.OneToOneField('SpeechActivity', on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Речевая деятельность")
    reading = models.OneToOneField('Reading', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Знакомство с книжной культурой, детской литературой")
    communication = models.OneToOneField('Communication', on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Владение речью как средством общения и культуры (коммуникация)")
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
                                              verbose_name="Знает 2-3 программных стихотворения, 2-3 считалки, загадки")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет жанр произведения")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Драматизирует небольшие сказки, читает по ролям стихотворения")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Называет любимого детского писателя, любимые сказки и рассказы")
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
                                              verbose_name="Может участвовать в беседе")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет аргументированно и доброжелательно оценивать ответ, высказывание сверстника")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Составляет по образцу рассказы по сюжетной картине, по набору картинок")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Пересказывает небольшие литературные произведения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет место звука в слове")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет подбирать к существительному несколько прилагательных")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет заменять слово другим словом со сходным значением")
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

######################## Соц-коммуникативное развитие Старшая группа ################################


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
                                              verbose_name="Понимает и употребляет в своей речи слова, обозначающие эмоциональные состояния, этические качества, эстетические характеристики")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Понимает скрытые мотивы поступков героев литературных произведений")
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
                                              verbose_name="Самостоятельно одевается и раздевается, сушит мокрые вещи, ухаживает за обувью")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет обязанности дежурного по столовой, правильно сервирует стол")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Поддерживает порядок в группе и на участке детского сада")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет поручения по уходу за животными и растениями в уголке природы")
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
                                              verbose_name="Распределяет роли в игре, исполняет роль, сопровождает действия речью, содержательно и интонационно")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сочиняет оригинальные и последовательно разворачивающиеся истории, использует все части речи, словотворчество")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет делиться со взрослыми и детьми разнообразными впечатлениями")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Поддерживает беседу, высказывает свою точку зрения, согласие и несогласие")
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
                                              verbose_name="Договаривается со сверстниками в коллективной работе, распределяет роли, при конфликте убеждает, объясняет, доказывает")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Оценивает свои поступки, понимает необходимость заботы о младших")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Самостоятельно использует в общении вежливые слова, соблюдает правила поведения на улице и в детском саду")
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
                                              verbose_name="Ориентируется в пространстве и времени (вчера, сегодня, завтра; сначала - потом)")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен конструировать по собственному замыслу. Способен использовать простые схематические изображения для решения несложных задач, строить по схеме, решать лабиринтовые задачи")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен рассуждать и давать адекватные причинные объяснения")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен самостоятельно придумать небольшую сказку на заданную тему")
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
                                              verbose_name="Договаривается с партнёрами, во что играть, кто кем будет в игре, подчиняется правилам игры")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В дидактических играх оценивает свои возможности и без обиды воспринимает проигрыш")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Объясняет правила игры сверстникам")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="После просмотра спектакля может оценить игру актёров, используемые средства художественной выразительности и элементы оформления постановки")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет в творческом опыте несколько ролей, сыгранных в спектаклях в детском саду и домашнем театре")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет оформлять свой спектакль, используя разнообразные материалы (атрибуты, подручный материал, поделки)")
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


######################## Физическое развитие Старшая группа ################################

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
                                              verbose_name="Умеет ходить и бегать легко, ритмично, сохраняя правильную осанку, направление и темп")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет лазать по гимнастической стенке (высота 2,5м) с изменением темпа")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может прыгать на мягкое покрытие (высота 20 см), прыгать в обозначенное место с высоты 30см, прыгать в длину с места (не менее 80см), с разбега (не менее 1м), в высоту с разбега (не менее 40см), прыгать через короткую скакалку")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет метать предметы обеими руками на расстоянии 5-9м, в вертикальную и горизонтальную цель с расстояния 3-4м, бросать мяч вверх, о землю и ловить его одной рукой, отбивать мяч на месте не менее 10 раз, в ходьбе (расстояние 6м)")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет упражнения на статическое и динамическое равновесие")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет перестраиваться в колонну по трое, четверо, равняться, размыкаться в колонне, шеренге, выполнять повороты направо, налево, кругом")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ходит на лыжах скользящим шагом на расстоянии около 2 км, ухаживает за лыжами")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет кататься на самокате")
    param9 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Участвует в упражнениях с элементами спортивных игр")
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
                                              verbose_name="Развитие основных физических качеств и потребности в двигательной активности")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о составляющих здорового образа жизни (правильное питание, движение, сон) и факторах, разрушающих здоровье")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает о значении для здоровья человека ежедневной утренней гимнастики, заваливания организма, соблюдения режима дня")
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
                                              verbose_name="Умеет быстро, аккуратно одеваться и раздеваться, соблюдать порядок в своём шкафу")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Имеет навыки опрятности (замечает непорядок в одежде, устраняет его при небольшой помощи взрослых)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Сформированы навыки личной гигиены (моет руки перед едой, при кашле и чихании закрывает рот и нос платком)")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет простейшими навыками поведения во время еды, пользуется столовыми приборами")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
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


######################## Художественное развитие Старшая группа ################################

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
    skillsofdrawing = models.FloatField(blank=True, null=True,
                                            verbose_name="Владение навыками изобразительной деятельности (лепка, аппликация, рисование)")
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
                                              verbose_name="Создаёт изображение предметов (с натуры, по представлению), сюжетные изображения")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует разнообразные композиционные решения, изобразительные материалы")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Использует различные цвета и оттенки для создания выразительных образов")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выполняет узоры по мотивам народного декоративно-прикладного искусства")
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
                                              verbose_name="Лепит предметы разной формы, используя усвоенные приёмы и способы")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создаёт небольшие сюжетные композиции, передавая пропорции, позы и движения фигур")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создаёт изображения по мотивам народных игрушек")
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
                                              verbose_name="Различает произведения изобразительного искусства (живопись, книжная графика, народное декоративное искусство, скульптура)")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выделяет выразительные средства в разных видах искусства (форма, цвет, колорит, композиция)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает особенности изобразительных материалов")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Изображает предметы и создает несложные сюжетные композиции, используя разнообразные приемы вырезания, обрывания бумаги")
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
                                              verbose_name="Различает жанры музыкальных произведений")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Различает высокие и низкие звуки (в пределах квинты)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может петь без напряжения, плавно, легким звуком, отчетливо произносить слова, своевременно начинать и заканчивать песню, петь в сопровождении музыкального инструмента")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Может ритмично двигаться в соответствии с характером и динамикой музыки")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет выполнять танцевальные движения (поочередное выбрасывание ног вперед в прыжке, полуприседание с выставлением ноги на пятку, шаг на всей ступне на месте, с продвижением вперед и в кружении)")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Самостоятельно инсценирует содержание песен, хороводов, действует не подражая другим детям")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет играть на металлофоне по одному и в небольшой группе детей")
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
                                              verbose_name="Способен сосредоточено действовать в течении 10-15 минут")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспроизводит простые стихотворения по памяти")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к кратковременному опосредованному зрительному запоминанию одновременно до 6ти картинок")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к кратковременному зрительному запоминанию одновременно до 6ти картинок")
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
                                              verbose_name=" Знает и различает основные цвета оттенки, соотносит с цветом предмета")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Определяет величину предмета, обозначает это в речи")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Дифференцирует и называет изображения в затрудненном для восприятия виде")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет с помощью осязания определять размер, материал, детали предметов окружения")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воспринимает сложную речевую инструкцию с первого предъявления")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает и называет части суток, времена года, названия месяцев")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Собирает разрезную картинку из 5ти частей")
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
                                              verbose_name="Способен к объединению предметов и признаков во множества по заданному принципу")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к сравнению двух предметов по количеству, размеру, форме, цвету")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет составить рассказ по серии сюжетных картин")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Создание уникальных образов в процессе одного или нескольких видов творческой деятельности")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Способен к сотрудничеству, планированию и самоконтролю; проявляет инициативу")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="В общении активно использует жесты, мимику")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет построить фразу для продуктивного диалога со сверстниками и педагогами")
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
                                              verbose_name="Подчинять свое поведение не желаниям и потребностям, а требованиям со стороны взрослых")
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
                                              verbose_name="Узнает  и называет фиолетовый и  розовый цвета. Соотносит объекты по цвету: 8 оттенков красного синего, зеленого, коричневого; 5 оттенков фиолетового, оранжевого, желтого голубого.  Умеет описывать окраску некоторых предметов.")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Узнает  и называет конус, призму, овал, ромб, цилиндр. Анализирует форму предмета: (конфигурация из 3-4 разнородных простых форм), знает  составные части заданной конфигурации")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотносит предметы  по величине: находит одинаковые из множества ( 5-7 предметов) по заданной величине ")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотносит величину частей целого объекта")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Выкладывает в порядке убывания и возрастания 5-7 предметов. Умеет сравнивать зрительно длину, высоту, ширину, толщину 5-7 предметов вблизи, 4-5 на расстоянии")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет словесно обозначать: длинный – короткий, высокий - низкий, широкий – узкий, тонкий - толстый")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет обозначать простейшие пути следования на рисунке, сличать действительное расположение предметов и расположение их в зеркале")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Анализирует сложные формы предметов с помощью вписывания сенсорных эталонов. Умеет описывать предметы, находить взаимосвязь между предметами по величине")
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
                                              verbose_name="Называет и выделяет основные признаки предметов, опираясь при этом на полисенсорный механизм восприятия. Устанавливает логические связи, между внешним обликом предмета, материалом и его функциональным назначением.")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о труде взрослых, результатах труда, его общественной значимости.  Бережно относится  к тому, что сделано руками человека. Знаком с трудом людей творческих профессий и результатом их труда.")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Воссоздает в ходе игры трудовые действия, характерные для некоторых профессий")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знаком с работой службой спасения, навыками безопасного поведения в быту. и на дороге умеет обращаться за помощью к взрослым")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Четко знает личные данные свои и близких людей, домашний адрес. Осознает свой статус в семье и обществе.")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Имеет представление о возможностях своего организма, о замене зрительной информации слуховой при ориентировке в пространстве, о здоровом образе жизни, охране и использования зрения")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Знает различные общественные учреждения, их назначение. Умеет  развивать сюжет на основе полученного опыта")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Владеет  понятиями  Родина, родной край, родной город, название страны ,столицы, города в котором живет, их характерными особенностями (размер, климат, животный и растительный мир)")
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
                                              verbose_name="Владеет навыками ориентировки на поверхности листа бумаги, тетради, альбомного листа, фланелеграфа, стола. Умеет располагать предметы в названных направлениях микропространства")
    param2 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Владеет навыками моделирования замкнутого пространства и пространственных отношений между предметами в нем расположенными, по инструкции тифлопедагога, по представлению")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет  ориентироваться по плану в замкнутом пространстве, Ориентируется по  схеме маршрута передвижения в помещениях детского сада")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет составлять простейшие схемы, пути в направлениях из группы в кабинет врача и т.д.")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Принимает правильные позы и жесты при обследовании предметов")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Умеет обозначать в речи пространственное расположение частей своего тела. Определяет и словесно обозначает пространственное расположении игрушек с точкой отсчета от себя. Определяет стороны предмета")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет показывать направление движения. ориентируется в процессе движения на цветовые, звуковые, световые ориентиры")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Соотносит форму предметов с соответствующими геометрическими эталонами, используя зрение и осязание правильной позы и жеста при обследовании предметов")
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
                                              verbose_name="Знает и выделяет сенсорные эталоны формы Умеет на ощупь различать объемные и плоскостные формы  круг – шар, квадрат – куб , треугольник - призма(Вложи в прорези соответствующие фигуры)")
    param3 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Различает и называет на ощупь характер поверхности: гладкая, шероховатая, твердая, мягкая, горячая, холодная и.т.д. ")
    param4 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет на ощупь определять размер предметов, сравнивать путем наложения и приложения")
    param5 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Умеет на ощупь ориентироваться в знакомом пространстве. Знает, где дверь, ручка, окно, шкаф")
    param6 = models.PositiveSmallIntegerField(blank=True, null=True,  choices=NUM_CHOICES,
                                              verbose_name="Классифицирует предметы по разным осязательным признакам (все жесткие, овальные, металлические и т.д.) (Найди все мягкие предеты")
    param7 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на микроплоскости стола, листа Определяет стороны листа, левый и правый углы середину, умеет размещать предметы по заданному образцу")
    param8 = models.PositiveSmallIntegerField(blank=True, null=True, choices=NUM_CHOICES,
                                              verbose_name="Ориентируется на ощупь в  строении своего тела, и других людей выделяет характерные признаки (голова вверху, ноги внизу,. Рассказывает какие у него волосы, руки, ноги. т.д.")
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
    app_models = apps.get_app_config('senior_group').get_models()
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
