from django import forms
from users.models import CustomUser
from exercises.models import Exercise


class UserPhysicalDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_age', 'user_weight', 'user_height', 'male']
        widgets = {
            'user_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '25'}),
            'user_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
            'user_height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '170'}),
            'male': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('male', 'Мужчина'),
                ('female', 'Женщина')
            ]),
        }


class ExerciseMaxForm(forms.Form):
    def __init__(self, *args, **kwargs):
        exercises = kwargs.pop('exercises', [])
        super().__init__(*args, **kwargs)
        for ex in exercises:
            self.fields[f'max_{ex.id}'] = forms.FloatField(
                label=f'{ex.name} (макс. вес в кг)',
                required=False,
                min_value=0,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'например: 100'})
            )
            self.fields[f'reps_{ex.id}'] = forms.IntegerField(
                label=f'{ex.name} (количество повторений)',
                required=False,
                min_value=1,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'например: 5'})
            )