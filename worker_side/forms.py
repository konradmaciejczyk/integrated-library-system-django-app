from django.forms import ModelForm
from user_side.models import Client

class ClientRegistrationForm(ModelForm):
    # first_name = forms.CharField(max_length=40)
    # last_name = forms.CharField(max_length=40)
    # gender = forms.CharField(max_length=7)
    # date_of_birth = forms.DateField()
    # citizenship = forms.CharField(max_length=30)
    # id_card_type = forms.CharField(max_length=8)
    # id_card = forms.CharField(max_length=30)
    # email = forms.EmailField()
    # phone_num = forms.CharField(max_length=15)
    # corr_address = forms.CharField(max_length=50)
    # occupation = forms.CharField(max_length=16)

    class Meta:
        model = Client
        # fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'citizenship',
        # 'id_card_type', 'id_card', 'email', 'phone_num', 'corr_address', 'occupation']
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'citizenship', 
        'id_doc_type', 'id_card', 'email', 'phone_num', 'corr_address', 'occupation']