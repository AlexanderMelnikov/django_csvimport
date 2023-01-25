# обычные модули для панели администрирования
from django.contrib import admin
from .models import Book, BookImport

# обслуживание импорта
import csv
from .forms import BookImportForm, BookImport
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

# модель для просмотра импортируемых файлов
@admin.register(BookImport)
class BookImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')

# вывод основной модели, кнопки "Импорт" и реализация самого импорта
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publish_date',)

    # метод, который расширит urlpatterns добавив путь
    # на страницу с формой и привязывает url к методу
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = BookImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['name', 'author', 'publish_date']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Book.objects.update_or_create(
                            name=row[0],
                            author=row[1],
                            publish_date=row[2]
                        )
                # конец обработки файлы
                # перенаправляем пользователя на главную страницу
                # с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = BookImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})
