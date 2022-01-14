import datetime
import xlwt

from django.http import HttpResponse
from .models import *


def pre_export_excel_cogdev(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Poznavatelnoe_razvitie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    columns_name = [field.verbose_name for field in CognitiveDevelop._meta.get_fields()[1:]]
    columns_param = [field.name for field in CognitiveDevelop._meta.get_fields()[2:] if not field.name == 'total']
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    row_num = 0

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Познавательное развитие')
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, 'Познавательное развитие', style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(row_num + 4, col_num, columns_name[col_num], style)

    rows = CognitiveDevelop.objects.order_by('child__group').values_list('child__name',
                                                'child__surname',
                                                'child__group',
                                                'math__total',
                                                'viewofworld__total',
                                                'primaryrepresent__total',
                                                'universalprerequisite__total',
                                                'cognition__total',
                                                'skills__total',
                                                'activities__total',
                                                'total')
    for row in rows:
        row_num += 1
        ws.write(row_num + 4, 0, row_num)
        ws.write(row_num + 4, 1, "{} {}".format(str(row[0]), str(row[1])))
        for col_num in range(2, len(row)):
            ws.write(row_num + 4, col_num, str(row[col_num]))

    columns_name = columns_name[3:]

    for i in range(len(columns_param)):
        get_tables(columns_param[i], columns_name[i], wb)

    wb.save(response)

    return response


def pre_export_excel_speechdev(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Rechevoe_razvitie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    columns_name = [field.verbose_name for field in SpeechDevelop._meta.get_fields()[1:]]
    columns_param = [field.name for field in SpeechDevelop._meta.get_fields()[2:] if not field.name == 'total']
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    row_num = 0

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Речевое развитие')
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, 'Речевое развитие', style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(row_num + 4, col_num, columns_name[col_num], style)

    rows = SpeechDevelop.objects.order_by('child__group').values_list('child__name',
                                                'child__surname',
                                                'child__group',
                                                'speechactivity__total',
                                                'reading__total',
                                                'communication__total',
                                                'total')
    for row in rows:
        row_num += 1
        ws.write(row_num + 4, 0, row_num)
        ws.write(row_num + 4, 1, "{} {}".format(str(row[0]), str(row[1])))
        for col_num in range(2, len(row)):
            ws.write(row_num + 4, col_num, str(row[col_num]))

    columns_name = columns_name[3:]

    for i in range(len(columns_param)):
        get_tables(columns_param[i], columns_name[i], wb)

    wb.save(response)

    return response


def pre_export_excel_comdev(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Soc_razvitie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    columns_name = [field.verbose_name for field in CommunicativeDevelop._meta.get_fields()[1:]]
    columns_param = [field.name for field in CommunicativeDevelop._meta.get_fields()[2:] if not field.name == 'total']
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    row_num = 0

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Соц-коммуникативное развитие')
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, 'Социально-коммуникативное развитие', style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(row_num + 4, col_num, columns_name[col_num], style)

    rows = CommunicativeDevelop.objects.order_by('child__group').values_list('child__name',
                                                'child__surname',
                                                'child__group',
                                                'emotional__total',
                                                'work__total',
                                                'safety__total',
                                                'masteringcommunicat__total',
                                                'behaviormanagement__total',
                                                'problemsolving__total',
                                                'socialization__total',
                                                'total')
    for row in rows:
        row_num += 1
        ws.write(row_num + 4, 0, row_num)
        ws.write(row_num + 4, 1, "{} {}".format(str(row[0]), str(row[1])))
        for col_num in range(2, len(row)):
            ws.write(row_num + 4, col_num, str(row[col_num]))

    columns_name = columns_name[3:]

    for i in range(len(columns_param)):
        get_tables(columns_param[i], columns_name[i], wb)

    wb.save(response)

    return response


def pre_export_excel_physdev(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Phyzicheskoe_razvitie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    columns_name = [field.verbose_name for field in PhysicalDevelop._meta.get_fields()[1:]]
    columns_param = [field.name for field in PhysicalDevelop._meta.get_fields()[2:] if not field.name == 'total']
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    row_num = 0

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Физическое развитие')
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, 'Физическое развитие', style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(row_num + 4, col_num, columns_name[col_num], style)

    rows = PhysicalDevelop.objects.order_by('child__group').values_list('child__name',
                                                'child__surname',
                                                'child__group',
                                                'movements__total',
                                                'hygiene__total',
                                                'health__total',
                                                'total')
    for row in rows:
        row_num += 1
        ws.write(row_num + 4, 0, row_num)
        ws.write(row_num + 4, 1, "{} {}".format(str(row[0]), str(row[1])))
        for col_num in range(2, len(row)):
            ws.write(row_num + 4, col_num, str(row[col_num]))

    columns_name = columns_name[3:]

    for i in range(len(columns_param)):
        get_tables(columns_param[i], columns_name[i], wb)

    wb.save(response)

    return response


def pre_export_excel_artdev(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Hyd_Razvitie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    columns_name = [field.verbose_name for field in ArtisticDevelop._meta.get_fields()[1:]]
    columns_param = [field.name for field in ArtisticDevelop._meta.get_fields()[2:] if not field.name == 'total']
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    row_num = 0

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Худ-эстетическое развитие')
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, 'Художественное-эстетическое развитие', style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(row_num + 4, col_num, columns_name[col_num], style)

    rows = ArtisticDevelop.objects.order_by('child__group').values_list('child__name',
                                                'child__surname',
                                                'child__group',
                                                'artisticpersonaldevelop__total',
                                                'painting__total',
                                                'modeling__total',
                                                'application__total',
                                                'music__total',
                                                'total')
    for row in rows:
        row_num += 1
        ws.write(row_num + 4, 0, row_num)
        ws.write(row_num + 4, 1, "{} {}".format(str(row[0]), str(row[1])))
        for col_num in range(2, len(row)):
            ws.write(row_num + 4, col_num, str(row[col_num]))

    columns_name = columns_name[3:]

    for i in range(len(columns_param)):
        get_tables(columns_param[i], columns_name[i], wb)

    wb.save(response)

    return response


def pre_export_excel_psycho(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Psiholog_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    wb = xlwt.Workbook(encoding='utf-8')

    for i in ['AttentionAndMemory', 'Perception', 'ThinkingAndSpeaking', 'EmotionsAndWill', 'MotorDevelop']:
        get_tables_psycho_eyes(i, wb)

    wb.save(response)

    return response


def pre_export_excel_eyes(reguest):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}{}"'.format('Zrenie_podgotov_grupa', datetime.datetime.now().date(), '.xls')

    wb = xlwt.Workbook(encoding='utf-8')

    for i in ['VisualPerception', 'SBO', 'Orientation', 'Touch']:
        get_tables_psycho_eyes(i, wb)

    wb.save(response)

    return response


def get_tables_psycho_eyes(table, main_exel):
    values_table = apps.get_app_config('preparatory_group').get_model(table)
    columns_name = [field.verbose_name for field in values_table._meta.get_fields()[1:]]
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    columns_values = ['child__name', 'child__surname', 'child__group']
    columns_values = columns_values + [field.name for field in values_table._meta.get_fields()[2:]]
    rows = [values_table.objects.order_by('child__group').values(value) for value in columns_values]

    ws = main_exel.add_sheet(values_table._meta.verbose_name)

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, values_table._meta.verbose_name_plural, style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(4, col_num, columns_name[col_num], style)

    for row in range(len(rows[0])):
        ws.write(row + 5, 0, row + 1)
        ws.write(row + 5, 1, "{} {}".format(list(rows[0][row].values())[0], list(rows[1][row].values())[0]))
        for column in range(2, len(rows)):
            ws.write(row + 5, column, list(rows[column][row].values())[0] if not list(rows[column][row].values())[0] == None else 0)


def get_tables(table, table_name, main_exel):
    values_table = apps.get_app_config('preparatory_group').get_model(table)
    columns_name = [field.verbose_name for field in values_table._meta.get_fields()[2:]]
    columns_name.insert(0, '№ п/п')
    columns_name.insert(2, 'Группа')
    columns_values = ['child__name', 'child__surname', 'child__group']
    columns_values = columns_values + [field.name for field in values_table._meta.get_fields()[3:]]
    rows = [values_table.objects.order_by('child__group').values(value) for value in columns_values]

    ws = main_exel.add_sheet(values_table._meta.verbose_name_plural[:30])

    ws.row(4).height_mismatch = True
    ws.row(4).height = 20 * 100
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    style_headline = xlwt.XFStyle()
    style_headline.font.bold = True

    ws.write(2, 1, table_name, style_headline)

    for col_num in range(len(columns_name)):
        if not col_num == 0 and not col_num == 2:
            ws.col(col_num).width = 256 * 18
        ws.write(4, col_num, columns_name[col_num], style)

    for row in range(len(rows[0])):
        ws.write(row + 5, 0, row + 1)
        ws.write(row + 5, 1, "{} {}".format(list(rows[0][row].values())[0], list(rows[1][row].values())[0]))
        for column in range(2, len(rows)):
            ws.write(row + 5, column, list(rows[column][row].values())[0] if not list(rows[column][row].values())[0] == None else 0)











