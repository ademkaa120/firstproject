from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm


def get_user_tasks(user):
    """Return tasks belonging to the authenticated user. Admins also see orphan tasks (user=None)."""
    if user.is_superuser or user.is_staff:
        return Task.objects.filter(Q(user=user) | Q(user__isnull=True))
    return Task.objects.filter(user=user)


@login_required
def database(request):
    search_query = request.GET.get('search', '').strip()
    tasks_qs = get_user_tasks(request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', Task.PRIORITY_MEDIUM)
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                priority=priority
            )
            return redirect('todo:index')

    # Search functionality
    if search_query:
        tasks = tasks_qs.filter(
            Q(title__icontains=search_query) |
            Q(priority__icontains=search_query)
        ).order_by('-created_at')
    else:
        tasks = tasks_qs.order_by('-created_at')

    context = {
        'tasks': tasks,
        'search_query': search_query
    }
    return render(request, 'todo/base.html', context)


@login_required
def delete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect('todo:index')


@login_required
def toggle_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.completed = not task.completed
        task.save()
    return redirect('todo:index')


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', Task.PRIORITY_MEDIUM)
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                priority=priority
            )
            return redirect('todo:index')
def register(request):
    # Registration logic here (not implemented in this snippet)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        password2 = request.POST.get('password2')
        if password == password2:
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match. try again.')
    return render(request, 'todo/register.html')


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    success_url = reverse_lazy('todo:index')

    def form_valid(self, form):
        """
        Add a flash message on successful login, then continue with the normal
        LoginView flow (which logs the user in + redirects).
        """
        response = super().form_valid(form)
        messages.success(self.request, 'You have logged in successfully.')
        return response
