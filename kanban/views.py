from django.contrib.auth.decorators import login_required
from .models import Board, Task, List
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, BoardForm, ListForm
import json
from django.utils import timezone
from .filters import TaskFilter


@login_required(login_url="/login/")
def index(request):
    """View function for home page of site."""
    boards = Board.objects.all()
    tasks = Task.objects.filter(list=None)

    context = {"boards": boards, "tasks": tasks}

    return render(request, "kanban/index.html", context)

@login_required(login_url="/login/")
def single_board(request, board_id):
    lists = List.objects.filter(board=board_id)
    tasks = Task.objects.all()
    board = Board.objects.get(pk=board_id)

    taskFilter = TaskFilter(request.GET, queryset=tasks)
    tasks = taskFilter.qs
    # group tasks by lists
    list_to_task = {l: sorted(tasks.filter(list=l), key=lambda t: t.time_moved, reverse=False) for l in lists}

    context = {"list_to_task": list_to_task, "board": board, 'taskFilter': taskFilter}

    return render(request, "kanban/single_board.html", context)

@login_required(login_url="/login/")
def single_board_settings(request, board_id):
    lists = List.objects.filter(board=board_id)
    tasks = Task.objects.all()
    board = Board.objects.get(pk=board_id)

    # group tasks by lists
    list_to_task = {l: sorted(tasks.filter(list=l), key=lambda t: t.time_moved, reverse=False) for l in lists}

    context = {"list_to_task": list_to_task, "board": board}

    return render(request, "kanban/single_board.html", context)

@login_required(login_url="/login/")
def create_board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BoardForm()
    return render(request, 'kanban/board_form.html', {'form': form, 'new': True})

@login_required(login_url="/login/")
def edit_board(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BoardForm(instance=board)
       
    return render(request, 'kanban/board_form.html', {'form': form, 'new': False, 'board': board})

@login_required(login_url="/login/")
def delete_board(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == "POST":
        board.delete()
        return redirect('index')
    return render(request, 'kanban/delete_board.html', {'board': board})

@login_required(login_url="/login/")
def create_list(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    order = get_next_order(board)
    if request.method == "POST":
        form = ListForm(request.POST, initial={'current_board': board, 'order': order})
        if form.is_valid():
            list_instance = form.save(commit=False) ##
            list_instance.board = board  # Set the board for the list
            list_instance.save()
            return redirect('single_board', board_id=board_id)
    else:
        form = ListForm(initial={'current_board': board, 'order': order})

    return render(request, 'kanban/list_form.html', {'form': form, 'new': True, 'board': board})

@login_required(login_url="/login/")
def task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {"task": task}
    return render(request, "kanban/task.html", context)

@login_required(login_url="/login/")
def create_task(request, board_id=None):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.board_id = board_id
            task.save()
            
            if board_id is None:
                return redirect('index')
            return redirect('single_board', board_id=board_id)
        
    else:
        form = TaskForm()

        form.fields['list'].empty_label = "---------"

    return render(request, 'kanban/task_form.html', {'form': form, 'new': True, 'board_id': board_id})

@login_required(login_url="/login/")
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if task.list:
                board_id = task.list.board.id
                return redirect('single_board', board_id=board_id)
            return redirect('index')
    else:
        form = TaskForm(instance=task)

        formFields = []
        formFields.append((None, "None"))

        for board in Board.objects.all().order_by('id'):
            formFields.append(
                (board.title,
                [
                    (list.id, list.title) for list in List.objects.filter(board=board).order_by('id')
                ])
            )
        
        form.fields['list'].choices = formFields
        
    return render(request, 'kanban/task_form.html', {'form': form, 'new': False, 'task': task})

@login_required(login_url="/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        if task.list:
            board_id = task.list.board.id
            task.delete()
            return redirect('single_board', board_id=board_id)
        return redirect('index')
    return render(request, 'kanban/delete_task.html', {'task': task})

def update_task_list(request, task_id):
    if request.method == "POST":
        requestBody = json.loads(request.body)

        listName = requestBody.get("listName")

        task = get_object_or_404(Task, pk=task_id)
        list = List.objects.get(title=listName)
        task.list = list
        task.time_moved = timezone.now()
        task.save()

    return redirect("index")







def get_next_order(board):
    board_lists = List.objects.filter(board=board)
    if board_lists:
        return board_lists.latest('order').order + 1
    return 1 # first in board



def board_view(request):
    view_mode = request.GET.get('view_mode', 'kanban')  # Default to 'kanban' view
    # Fetch your tasks and boards as before
    return render(request, 'index.html', {'tasks': tasks, 'boards': boards, 'view_mode': view_mode})


















"""""
def index(request):
    """#View function for home page of site.
"""
    # Redirect user to login page if they haven't logged in yet
    if not request.user.is_authenticated:
        return redirect("login/")

    boards = Board.objects.all()
    tasks = Task.objects.all()

    # group tasks by boards
    board_to_task = {b: sorted(tasks.filter(board=b), key=lambda t: t.time_moved, reverse=False) for b in boards}

    context = {"board_to_task": board_to_task}

    return render(request, "kanban/index.html", context)


@login_required(login_url="/login/")
def task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {"task": task}
    return render(request, "kanban/task.html", context)

@login_required(login_url="/login/")
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'kanban/create_task.html', {'form': form})

@login_required(login_url="/login/")
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'kanban/edit_task.html', {'form': form})

@login_required(login_url="/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('index')
    return render(request, 'kanban/delete_task.html', {'task': task})

def update_task_board(request, task_id):
    if request.method == "POST":
        
        requestBody = json.loads(request.body)

        boardName = requestBody.get("boardName")

        task = get_object_or_404(Task, pk=task_id)
        board = Board.objects.get(title=boardName)
        task.board = board
        task.time_moved = timezone.now()
        task.save()

    return redirect("index")

#</form> class="form__container">
"""""