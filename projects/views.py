from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import ProjectForm, ReviewForm

# Create your views here.
def projects(request):
    projects = Project.objects.filter()

    if request.GET.get('search') != None:
        search = request.GET.get('search')
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) | 
            Q(owner__name__icontains=search) | 
            Q(tags__name__icontains=search)
        )

    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':

        if request.user.is_authenticated == False:
            messages.error(request, 'You must be logged in to review a project')
            return redirect('login')
        
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount
        
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=project.id)

    context = {'project': project, 'form': form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            form.save_m2m()
            messages.success(request, 'Project was created successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.user.profile != project.owner:
        messages.error(request, 'You are not allowed to edit other users projects')
        return redirect('projects')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project was updated successfully!')
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if request.user.profile != project.owner:
        messages.error(request, 'You are not allowed to delete other users projects')
        return redirect('projects')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project was deleted successfully!')
        return redirect('account')
    
    context = {'object': project}
    return render(request, 'delete_template.html', context)