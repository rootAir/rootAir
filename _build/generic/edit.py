from django.views.generic.edit import (FormMixin, ProcessFormView,
                                       ModelFormMixin, DeletionMixin)

from django_modalview.generic.base import (ModalContextMixin, ModalView,
                                           ModalTemplateMixin, ModalUtilMixin)
from django_modalview.generic.component import (FORM_TEMPLATE_CONTENT,
                                                LAST_FORM_TEMPLATE,
                                                FORM_TEMPLATE, ModalButton)


class ModalEditContextMixin(ModalContextMixin):

    """
            Mixin that extends the ModalContextMixin to add some new elements in
            the modal context.

    """

    def __init__(self, *args, **kwargs):
        super(ModalEditContextMixin, self).__init__(*args, **kwargs)
        self.action = None
        self.content_template_name = FORM_TEMPLATE_CONTENT
        self.submit_button = ModalButton(value='send', button_type='primary')
        self.form_content_template_name = LAST_FORM_TEMPLATE

    def get_context_modal_data(self, **kwargs):
        kwargs.update({
            'submit_button': self.submit_button,
            'action': self.action,
            'form_template_name': self.form_content_template_name
        })
        return super(ModalEditContextMixin,
                     self).get_context_modal_data(**kwargs)


class ModalFormMixin(ModalEditContextMixin, FormMixin):

    """
            Mixin that provide a way to show and to handle a modal with a django
            form.
    """

    def get_context_modal_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form(self.get_form_class()),
        })
        return super(ModalFormMixin, self).get_context_modal_data(**kwargs)

    def _form_response(self, **kwargs):
        kwargs.update(self.get_context_modal_data())
        return self.render_to_response(context=kwargs)

    def form_valid(self, form, **kwargs):
        self._can_redirect = True
        return self._form_response(**kwargs)

    def form_invalid(self, form, **kwargs):
        return self._form_response(**kwargs)


class ModalFormUtilMixin(ModalFormMixin, ModalUtilMixin):
    """
        Mixin that provide a way to show and to handle a modal with a django
        form
    """
    def util_on_form_valid(self, **kwargs):
        pass

    def util_on_form_invalid(self, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.kwargs.update(kwargs)
        self.kwargs.update(request.GET)
        return super(ModalFormUtilMixin, self).dispatch(request, *args,
                                                        **kwargs)

    def form_valid(self, form, **kwargs):
        self.kwargs.update(**form.cleaned_data)
        self.get_util('util_on_form_valid', **self.kwargs)
        return super(ModalFormUtilMixin, self).form_valid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        self.kwargs.update(**form.cleaned_data)
        self.get_util('util_on_form_invalid', **self.kwargs)
        return super(ModalFormUtilMixin, self).form_invalid(form, **kwargs)


class ModalModelFormMixin(ModalFormMixin, ModelFormMixin):

    """
            A mixin that provide a way to show and to handle a modelform in a
            modal
    """

    def save(self, form):
        self.object = form.save()

    def form_valid(self, form, commit=True, **kwargs):
        if commit:
            self.save(form)
        return super(ModalModelFormMixin, self).form_valid(form, **kwargs)


class BaseProcessModalView(ModalView, ProcessFormView):

    """
            A base mixin to handle a get request on a modal view that contains
            a form.
    """

    def dispatch(self, request, *args, **kwargs):
        self.action = request.path
        return super(BaseProcessModalView, self).dispatch(request, *args,
                                                          **kwargs)

    def get(self, request, *args, **kwargs):
        self.template_name = FORM_TEMPLATE
        return super(BaseProcessModalView, self).get(request, *args, **kwargs)


class ProcessModalFormView(BaseProcessModalView):

    """
            A mixin that provide a way to handle a modal view with a form on a
            GET request and to run it on a POST request.
    """

    def post(self, request, *args, **kwargs):
        self.template_name = self.content_template_name
        return super(ProcessModalFormView, self).post(request, *args,
                                                      **kwargs)


class ProcessModalPostView(BaseProcessModalView):

    """
            A mixin that provide a way to handle a modal view with a form on a
            GET request. The post request don't check if the form is valid. Usefull
            for the deletion Mixin or other modal that want to run an util on a
            POST request without analize the form
    """

    def post(self, request, *args, **kwargs):
        self.template_name = self.content_template_name
        self._can_redirect = True
        kwargs.update(self.get_context_modal_data())
        return self.render_to_response(context=kwargs)


class ModalDeletionMixin(ModalEditContextMixin):

    """
            A mixin that provide a way to delete an object.
    """

    def delete(self, request, *args, **kwargs):
        self.object.delete()


class ModalPostMixin(ModalEditContextMixin):
    '''
        A mixin that provide a way to handle a post request
    '''


class ModalPostUtilMixin(ModalPostMixin, ModalUtilMixin):

    def util_on_post(self, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.kwargs.update(kwargs)
        self.kwargs.update(request.GET)
        return super(ModalPostUtilMixin, self).dispatch(request, *args,
                                                        **kwargs)

    def post(self, request, *args, **kwargs):
        self.kwargs.update(kwargs)
        self.get_util('util_on_post', **self.kwargs)
        return super(ModalPostUtilMixin, self).post(request, **kwargs)


class BaseModalUpdateView(ModalModelFormMixin, ProcessModalFormView):

    """
            A base view that provide a way to display a modelform, in a modal,
            to update an object. The attribute that contains the instance is
            self.object.
    """


class BaseModalCreateView(BaseModalUpdateView):

    """
            A base view that provide a way to display a modelform, in a modal,
            to update an object. The attribute that contains the instance is
            self.object.
    """

    def get(self, request, *args, **kwargs):
        self.object = None
        return super(BaseModalCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(BaseModalCreateView, self).post(request, *args, **kwargs)


class BaseModalDeleteView(ModalDeletionMixin, ProcessModalPostView):

    """
            A base view that provide a way to delete an object in a modal.
            The object that sould be deleted is in the attribute self.object
    """

    def __init__(self, *args, **kwargs):
        super(BaseModalDeleteView, self).__init__(*args, **kwargs)
        self.submit_button.type = 'danger'
        self.submit_button.value = 'Delete'

    def post(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return super(BaseModalDeleteView, self).post(request, *args, **kwargs)


class BaseModalPostView(ModalPostMixin, ProcessModalPostView):

    """
            A base view that provide a way to handle a modal that can send a post
            request and handle its response.
    """


class BaseModalPostUtilView(ModalPostUtilMixin, ProcessModalPostView):
    """
            A base view that provide a way to handle a modal that can send a post
            request, run an util and handle its response.
    """


class BaseModalFormView(ModalFormMixin, ProcessModalFormView):

    """
            A base view that provide a way to handle a modal with a form.
    """


class BaseModalFormUtilView(ModalFormUtilMixin, ProcessModalFormView):

    """
        A base view that provide a way to handle a modal with form and util
    """


class ModalFormView(ModalTemplateMixin, BaseModalFormView):

    """
            A view to handle a modal with form and to render it.
    """


class ModalFormUtilView(ModalTemplateMixin, BaseModalFormUtilView):

    """
        A view to handle a modal with form/util and to render it.
    """


class ModalCreateView(ModalTemplateMixin, BaseModalCreateView):

    """
            A view to handle a modal with a create form and to render it.
    """


class ModalUpdateView(ModalTemplateMixin, BaseModalUpdateView):

    """
            A view to handle a modal with an update form and to render it.
    """


class ModalPostView(ModalTemplateMixin, BaseModalPostView):

    """
            A view to handle a modal with a post request sender and to render it.
    """


class ModalPostUtilView(ModalTemplateMixin, BaseModalPostUtilView):
    """
    """


class ModalDeleteView(ModalTemplateMixin, BaseModalDeleteView):

    """
            A view to handle a modal with delete button and to render it.
    """
