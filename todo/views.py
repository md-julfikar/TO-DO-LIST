from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import Task
from .forms import TaskForm, UserLoginForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'todo/registration.html', {'form': form})
def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list') 
        else:
            messages.error(request, 'Invalid username or password.') 
    return render(request, 'todo/login.html', {'form': form}) 

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    response = JsonResponse({
            'title': task.title,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'details': task.description 
        })
    return response

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
        else:
            messages.error(request, 'There was an error creating the task. Please check the form.')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})


@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
        else:
            messages.error(request, 'There was an error updating the task. Please check the form.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})


@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})


@login_required
def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task.completed = data.get('completed', task.completed)
            task.save()
            return JsonResponse({'status': 'success', 'completed': task.completed})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'status': 'fail', 'message': 'Invalid data'}, status=400)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)
