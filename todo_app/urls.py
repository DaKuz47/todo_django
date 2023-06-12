"""URL структура нашего приложения"""

from django.urls import path
from . import views


app_name="todo_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('lists/', views.lists, name='lists'),
    path('lists/<int:list_id>', views.list, name='list'),
    path('lists/del_completed/<int:list_id>', views.delete_completed, name='delete_completed'),
    path('lists/tasks/<int:task_id>', views.task_info, name='task_info'),
    path('lists/add_list', views.add_list, name='add_list'),
    path('lists/del_list/<int:list_id>', views.delete_list, name='delete_list'),
    path('lists/tasks/add_task/<int:list_id>', views.add_task, name='add_task'),
    path('lists/tasks/edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('lists/tasks/del_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('lists/tasks/status_invert/<int:task_id>', views.sts_invert, name="sts_invert"),
]
