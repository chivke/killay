from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.urls import reverse

from killay.admin.mixins import AdminRequiredMixin
from killay.admin.models import SiteConfiguration

from killay.admin.forms import SiteConfigurationForm, SocialMediaFormSet, LogoFormSet


class SiteConfigurationUpdateView(AdminRequiredMixin, UpdateView):
    form_class = SiteConfigurationForm
    formset_class = SocialMediaFormSet
    logo_formset_class = LogoFormSet
    template_name = "admin/site_configuration.html"

    def get_object(self):
        return SiteConfiguration.objects.current()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return {
            **context,
            "formset": self.get_formset(),
            "logo_formset": self.get_logo_formset(),
            **kwargs,
        }

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs, instance=self.object)

    def get_logo_formset(self, **kwargs):
        return self.logo_formset_class(**kwargs, instance=self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset(data=request.POST)
        logo_formset = self.get_logo_formset(data=request.POST, files=request.FILES)
        if form.is_valid() and formset.is_valid() and logo_formset.is_valid():
            return self.form_formset_valid(form, formset, logo_formset)
        else:
            return self.form_formset_invalid(form, formset, logo_formset)

    def form_formset_valid(self, form, formset, logo_formset):
        for _form in [form, formset, logo_formset]:
            if _form.has_changed():
                _form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_formset_invalid(self, form, formset, logo_formset):
        context = self.get_context_data(
            form=form, formset=formset, logo_formset=logo_formset
        )
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse("admin:configuration")


admin_configuration_view = SiteConfigurationUpdateView.as_view()
