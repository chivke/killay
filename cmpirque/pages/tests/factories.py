from factory import Faker
from factory.django import DjangoModelFactory

from cmpirque.pages.models import Page


class PageFactory(DjangoModelFactory):

    title = Faker("user_name")
    slug = Faker("slug")

    class Meta:
        model = Page
        django_get_or_create = ["slug"]


class HomePageFactory(PageFactory):
    slug = "home"
