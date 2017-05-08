from django import forms

class CommentForm(forms.Form):
	comment_text = forms.CharField(label='comment_text', max_length=5000)
	challenge_id = forms.IntegerField(label='challenge_id')
	comment_id = forms.IntegerField(label='comment_id')

class SubmissionForm(forms.Form):
	challenge_id = forms.IntegerField(label='challenge_id')
	user_id = forms.IntegerField(label='user_id')
	group = forms.CharField(label='group', max_length=100)
	code_files = forms.FileField(label='code_files', required=False)
	submission_file = forms.FileField(label='submission_file')
