from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.urls import reverse

from cmpirque.admin.mixins import AdminRequiredMixin
from cmpirque.admin.models import SiteConfiguration

from cmpirque.admin.forms import SiteConfigurationForm, SocialMediaFormSet


class SiteConfigurationUpdateView(AdminRequiredMixin, UpdateView):
    form_class = SiteConfigurationForm
    formset_class = SocialMediaFormSet

    def get_object(self):
        return SiteConfiguration.objects.current()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {**context, "formset": self.get_formset(), **kwargs}

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs, instance=self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset(data=request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_formset_valid(form, formset)
        else:
            return self.form_formset_invalid(form, formset)

    def form_formset_valid(self, form, formset):
        form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_formset_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse("admin:configuration")


admin_configuration_view = SiteConfigurationUpdateView.as_view()
