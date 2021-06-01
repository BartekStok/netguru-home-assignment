from django import forms


class CreateBucketForm(forms.Form):
    bucket_name = forms.CharField(label="Bucket Name", max_length=64)


class SaveToBucketForm(forms.Form):
    bucket_name = forms.CharField(label="Bucket Name", max_length=64)
    file = forms.FileField()
    # file_name = forms.FileInput()
    # file_path = forms.FilePathField()
