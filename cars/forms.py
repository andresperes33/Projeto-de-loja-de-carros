from django import forms
from .models import Car, Message



class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'value': forms.TextInput(),
        }
        labels = {
            'model': 'Modelo',
            'brand': 'Marca',
            'factory_year': 'Ano de Fabricação',
            'model_year': 'Ano do Modelo',
            'plate': 'Placa',
            'value': 'Valor',
            'photo': 'Foto',
            'bio': 'Descrição',
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')

        if value < 20000:
            self.add_error(
                'value',
                'O valor mínimo do carro deve ser de R$ 20.000'
            )

        return value
        

    def clean_factory_year(self):
         factory_year = self.cleaned_data.get('factory_year')

         if factory_year < 1975:
             self.add_error(
            'factory_year',
            'Não é possível cadastrar carros fabricados antes de 1975'
        )

         return factory_year
    

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
             self.add_error(
            'photo',
            'É obrigatório cadastrar o carro com uma imagem.'
        )

        return photo
    
    



    

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Seu Nome',
            'email': 'Seu E-mail',
            'subject': 'Assunto',
            'message': 'Mensagem',
        }
