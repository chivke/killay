from model_bakery.recipe import Recipe

from killay.admin.models import Logo, SocialMedia


logo_recipe = Recipe(
    Logo,
)

social_media_recipe = Recipe(
    SocialMedia,
)
