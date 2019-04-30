from django import forms


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(questions):
            self.fields['question_%s' % i] = forms.ModelChoiceField(label=question.question_text,
                                                                    queryset=question.quizchoice_set.all(),
                                                                    widget=forms.RadioSelect,
                                                                    empty_label=None)

    # def answers(self):
    #     for name, value in self.cleaned_data.items():
    #         if name.startswith('question_'):
    #             yield (self.fields[name].label, value)