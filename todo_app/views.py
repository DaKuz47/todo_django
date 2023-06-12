from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import List, Task
from .forms import ListForm, TaskForm


# Create your views here.
def index(request):
    """Домашняя страница"""
    return render(request, 'todo_app/index.html')


@login_required
def lists(request):
    """Страница со списком доступных списков дел"""
    users_lists = List.objects.filter(user=request.user).order_by('-date_opened')
    # расширенный список списков (добавилось количество невыполненных задач)
    extended_lists = []

    for list in users_lists:
        extended_lists.append({
            'name': list.name,
            'id': list.id,
            'tasks_count': list.task_set.filter(complete=False).count(),
        })
    context = {'lists': extended_lists}

    return render(request, 'todo_app/lists.html', context)


@login_required
def list(request, list_id):
    """Страница списка дел"""
    list = List.objects.get(id=list_id)
    check_list_owner(request.user, list)

    list.date_opened = datetime.now()
    list.save()
    tasks = list.task_set.order_by('complete', '-date_add')
    uc_count = tasks.filter(complete=False).count()
    context = {'list': list, 'tasks': tasks, 'count': uc_count}

    return render(request, 'todo_app/list.html', context)


@login_required
def task_info(request, task_id):
    """Страница с подробной информацией о задаче"""
    task = Task.objects.get(id=task_id)
    list = task.list
    check_list_owner(request.user, list)
    context = {'list': list, 'task': task}

    return render(request, 'todo_app/task_info.html', context)


@login_required
def add_list(request):
    """Форма создания списка"""

    if request.method != 'POST':
        form = ListForm()
    else:
        form = ListForm(data=request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()

            return redirect('todo_app:lists')

    context = {'form': form}
    return render(request, 'todo_app/new_list.html', context)


@login_required
def add_task(request, list_id):
    """Форма создания задачи"""
    list = List.objects.get(id=list_id)
    check_list_owner(request.user, list)

    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.list = list
            new_task.save()

            return redirect('todo_app:list', list_id)

    context = {'list': list, 'form': form}
    return render(request, 'todo_app/new_task.html', context)


@login_required
def edit_task(request, task_id):
    """Форма для редактирования задачи"""
    task = Task.objects.get(id=task_id)
    list = task.list
    check_list_owner(request.user, list)

    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_app:list', list.id)

    context = {'task': task, 'list': list, 'form': form}
    return render(request, 'todo_app/edit_task.html', context)


@login_required
def delete_task(request, task_id):
    """Удаление задачи"""
    task = Task.objects.get(id=task_id)
    list = task.list
    check_list_owner(request.user, list)

    task.delete()

    return redirect('todo_app:list', list.id)


@login_required
def delete_list(request, list_id):
    """Удаление списка"""
    list = List.objects.get(id=list_id)
    check_list_owner(request.user, list)

    list.delete()

    return redirect('todo_app:lists')


@login_required
def sts_invert(request, task_id):
    """Изменение статуса выполненности задачи"""
    task = Task.objects.get(id=task_id)
    list = task.list
    check_list_owner(request.user, list)

    # инвертирование значения
    task.complete = task.complete is not True
    task.save()

    return redirect('todo_app:list', list.id)


@login_required
def delete_completed(request, list_id):
    """Удаляет выполненные задачи"""
    list = List.objects.get(id=list_id)
    check_list_owner(request.user, list)

    list.task_set.filter(complete=True).delete()

    return redirect('todo_app:list', list_id)


def check_list_owner(user, list):
    """Проверка на владение списком"""
    if list.user != user:
        raise Http404
