from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext

from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    InlineFormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    PlaceForm,
    PlaceFormSet,
    PlaceAddressForm,
    PlaceAddressFormSet,
)
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.archives.models import Place


PLACE_SLUG = ContentManagerConstants.SLUG_PLACE
PLACE_EXTRA_LINKS = get_content_manager_extra_links(view_slug=PLACE_SLUG)


class PlaceListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[PLACE_SLUG]
    formset_class = PlaceFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[PLACE_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PLACE_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[PLACE_SLUG]
    extra_links = PLACE_EXTRA_LINKS


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[PLACE_SLUG]["list"],
]


admin_place_list_view = PlaceListView.as_view()


class PlaceCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = PlaceForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
    breadcrumb = [*_common_bredcrumb, {"name": "New Place"}]
    extra_links = PLACE_EXTRA_LINKS


admin_place_create_view = PlaceCreateView.as_view()


class PlaceUpdateView(UpdateAdminView):
    form_class = PlaceForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PLACE_SLUG]
    extra_links = PLACE_EXTRA_LINKS

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]

    def get_extra_actions(self):
        place_kwargs = {"slug": self.object.id}
        address_link = reverse("admin:place_address_list", kwargs=place_kwargs)
        return [
            {"name": "General"},
            {"name": ContentManagerConstants.NAME_ADDRESS, "link": address_link},
        ]

    def get_extra_data(self) -> str:
        extra_data = super().get_extra_data()
        if self.request.place and self.request.place.id == self.object.id:
            extra_data[gettext("You are in this place")] = self.request.ip_address
        return extra_data


admin_place_update_view = PlaceUpdateView.as_view()


class PlaceDeleteView(DeleteAdminView):
    form_class = PlaceForm
    main_title = ContentManagerConstants.MAIN_TITLE
    reverse_url = ContentManagerConstants.VIEWS_LIST[PLACE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
    extra_links = PLACE_EXTRA_LINKS

    def get_breadcrumb(self) -> list:
        place_kwargs = {"slug": self.object.id}
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            *_common_bredcrumb,
            {"name": self.object.name, "link": place_link},
            {"name": "Delete"},
        ]

    def get_extra_actions(self):
        place_kwargs = {"slug": self.object.id}
        address_link = reverse("admin:place_address_list", kwargs=place_kwargs)
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            {"name": "General", "link": place_link},
            {"name": ContentManagerConstants.NAME_ADDRESS, "link": address_link},
        ]

    def get_extra_data(self) -> str:
        extra_data = super().get_extra_data()
        if self.request.place and self.request.place.id == self.object.id:
            extra_data[gettext("You are in this place")] = self.request.ip_address
        return extra_data


admin_place_delete_view = PlaceDeleteView.as_view()


class PlaceAddressListView(InlineFormSetAdminView):
    parent_model = Place
    related_field = "place_id"
    formset_class = PlaceAddressFormSet
    reverse_url = "admin:place_address_list"
    search_field = "description"
    extra_links = PLACE_EXTRA_LINKS

    def get_second_title(self) -> str:
        return f"Addresses of {self.object.name}"

    def get_create_link(self):
        return reverse("admin:place_address_create", kwargs={"slug": self.object.id})

    def get_breadcrumb(self) -> list:
        place_kwargs = {"slug": self.object.id}
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            *_common_bredcrumb,
            {"name": self.object.name, "link": place_link},
            {"name": ContentManagerConstants.NAME_ADDRESS},
        ]

    def get_extra_actions(self):
        place_kwargs = {"slug": self.object.id}
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            {"name": "General", "link": place_link},
            {"name": ContentManagerConstants.NAME_ADDRESS},
        ]

    def get_extra_data(self) -> str:
        extra_data = super().get_extra_data()
        if self.request.place and self.request.place.id == self.object.id:
            extra_data[gettext("You are in this place")] = self.request.ip_address
        return extra_data


admin_place_address_list_view = PlaceAddressListView.as_view()


class PlaceAddressCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = PlaceAddressForm
    name_field = "ipv4"
    reverse_url = "admin:place_address_list"
    extra_links = PLACE_EXTRA_LINKS

    def get_slug_value(self):
        return self.object.place_id

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        place_id = self.kwargs["slug"]
        place = Place.objects_in_site.filter(id=place_id).first() if place_id else None
        if not place:
            message = gettext(f"{Place.Meta.verbose_name} not exists")
            raise Http404(message)
        self.place = place
        form.initial["place"] = place_id
        return form

    def get_extra_data(self) -> str:
        return {gettext("Your current IP"): self.request.ip_address}

    def get_breadcrumb(self) -> list:
        place_kwargs = {"slug": self.place.id}
        address_link = reverse("admin:place_address_list", kwargs=place_kwargs)
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            *_common_bredcrumb,
            {"name": self.place.name, "link": place_link},
            {"name": ContentManagerConstants.NAME_ADDRESS, "link": address_link},
            {"name": "Create Address"},
        ]

    def get_extra_actions(self):
        place_kwargs = {"slug": self.place.id}
        pattern_name = ContentManagerConstants.VIEWS_UPDATE[PLACE_SLUG]
        address_link = reverse("admin:place_address_list", kwargs=place_kwargs)
        place_link = reverse(pattern_name, kwargs=place_kwargs)
        return [
            {"name": "General", "link": place_link},
            {"name": ContentManagerConstants.NAME_ADDRESS, "link": address_link},
        ]


admin_place_address_create_view = PlaceAddressCreateView.as_view()
