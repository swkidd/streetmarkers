
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import CreateUserForm
from django.urls import reverse_lazy

class RegisterView(FormView):
    template_name = "registration/registration.html"
    form_class = CreateUserForm 
    success_url = reverse_lazy('login') 
    def form_valid(self, form):
        user = form.cleaned_data.get('username')
        messages.success(self.request, 'Account was created for ' + user)
        form.save()
        return super().form_valid(form)