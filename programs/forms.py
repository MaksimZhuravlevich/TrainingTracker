# programs/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import TrainingProgram, ProgramWorkout, ProgramExercise
from exercises.models import Exercise


class TrainingProgramForm(forms.ModelForm):

    class Meta:
        model = TrainingProgram
        fields = ["name", "weeks"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Название программы"}),
            "weeks": forms.NumberInput(attrs={"min": 1}),

        }


class ProgramWorkoutForm(forms.ModelForm):

    class Meta:
        model = ProgramWorkout
        fields = ["name", "day_number", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Дополнительные заметки"})
        }


class ProgramExerciseForm(forms.ModelForm):

    class Meta:
        model = ProgramExercise
        fields = ["exercise", "sets", "reps", "rest_time", "order"]
        widgets = {
            "sets": forms.NumberInput(attrs={"min": 1}),
            "reps": forms.NumberInput(attrs={"min": 1}),
            "rest_time": forms.NumberInput(attrs={"min": 0}),
            "order": forms.NumberInput(attrs={"min": 1}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["exercise"].queryset = Exercise.objects.all()
        self.fields["exercise"].empty_label = "Выберите упражнение"


ProgramExerciseFormSet = inlineformset_factory(
    ProgramWorkout,
    ProgramExercise,
    form=ProgramExerciseForm,
    extra=3,
    can_delete=True
)