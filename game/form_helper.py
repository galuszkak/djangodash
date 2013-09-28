from crispy_forms.helper import FormHelper


class BaseFormHelper(FormHelper):
    form_class = 'form-horizontal'
    label_class = 'col-lg-2'
    field_class = 'col-lg-3'
    
