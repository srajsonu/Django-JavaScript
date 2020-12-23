from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm, FileField
from .humanize import naturalsize
from .models import Ad


class CreateForm(ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_uplaod_limit_text = naturalsize(max_upload_limit)

    picture = FileField(
        required=False,
        label='File to upload <=' + str(max_uplaod_limit_text)
    )
    upload_field_name = 'picture'

    class Meta:
        model = Ad
        fields = ['title', 'text', 'picture']

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if not pic: return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', 'File must be <' + self.max_uplaod_limit_text + 'bytes')

    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance
