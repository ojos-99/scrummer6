from django import forms
from .models import Task, Board, List

class TaskForm(forms.ModelForm):
    list = forms.ModelChoiceField(queryset=List.objects.all().order_by('order'), empty_label="---------", required=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'list', 'assignee', 'priority', 'status','tag', 'points']
   
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title']

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'board', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].disabled = True