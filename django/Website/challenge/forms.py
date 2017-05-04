from django import forms

class CommentForm(forms.Form):
	comment_text = forms.CharField(label='comment_text', max_length=5000)
	challenge_id = forms.IntegerField(label='challenge_id')
	comment_id = forms.IntegerField(label='comment_id')
	