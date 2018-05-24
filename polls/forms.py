from django import forms

# forms.pyファイルでフォームのフォーマットを作成し、views.pyでcontextとしてフォーマットを渡して、
# テンプレートでフォームを生成します。


class ChoiceForm(forms.Form):

    choice_text = forms.CharField()


class ImageForm(forms.Form):

    image = forms.ImageField()