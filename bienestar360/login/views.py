from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser, Faculty
from django.contrib.auth import login
from django.contrib.auth.models import Group



# Create your views here.
#Changed it to the class-based views
class LoginView(FormView):
    #Looks for the template
    template_name = "login/login.html"
    #Consumes the form
    form_class = CustomAuthenticationForm

    #When the form is valid, this method is called
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Redirect based on group
        if user.does_belong_group("basic user"):
            return redirect("homepageUser:homepageUser")
        elif user.does_belong_group("admin"):
            return redirect("homepageCADI:homepageCADI")

        # fallback
        return redirect("login:login")

    # #When the form is invalid, this method is called
    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))

#Same as the other class view but for the registration part.
class RegisterView(FormView):
    template_name = "login/registration.html"
    form_class = CustomUserCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.filter(is_superuser=False).order_by("username")
        context["faculties"] = Faculty.objects.all()
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        #Now assign the "basic user" group(role) to the new user
        basic_group = Group.objects.get(name="basic user")
        user.groups.add(basic_group)
        
        return redirect("login:login")