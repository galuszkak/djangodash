from .form_helper import BaseFormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import StrictButton

def form_helper(request):
    context = {}
    if request.path.startswith('/accounts/login'):
        form_helper = BaseFormHelper()
        form_helper.layout = Layout(
                                    'login',
                                    'password',
                                    'remember',
                                    Submit('Sign in', 'Sign in', css_class='btn-default'),
                                    )
        context['form_helper'] = form_helper
    elif request.path.startswith('/accounts/signup'):
        form_helper = BaseFormHelper()
        form_helper.layout = Layout(
                                    'username',
                                    'email',
                                    'password1',
                                    'password2',
                                    Submit('Sign up', 'Sign up', css_class='btn-default'),
                                    )
        context['form_helper'] = form_helper
        
    return context