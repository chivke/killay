from menus.base import Menu, NavigationNode
from cms.menu_bases import CMSAttachMenu
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from .models import VideoCategory
from django.urls import reverse


class CategoryMenu(CMSAttachMenu):
	name = _("Video category menu")
	def get_nodes(self, request):
		nodes = []
		categories = VideoCategory.objects.all()
		#nodes.append(NavigationNode(_("Video Log"), '/',1))
		# for cat in categories:
		# 	nodes.append(NavigationNode(
		# 		title=cat.title,
		# 		url=reverse('videolog:catentries', args=(cat.slug,)),
		# 		id=cat.id,)
		# 	)
		
		nodes.append(NavigationNode(
			title=categories[3].title,
			url=reverse('videolog:catentries', args=(categories[3].slug,)),
			id=categories[3].id,
			)
		)
		nodes.append(NavigationNode(
			title=categories[5].title,
			url=reverse('videolog:catentries', args=(categories[5].slug,)),
			id=categories[5].id,
			)
		)
		nodes.append(NavigationNode(
			title=categories[4].title,
			url=reverse('videolog:catentries', args=(categories[4].slug,)),
			id=categories[4].id,
			)
		)
		nodes.append(NavigationNode(
			title=categories[2].title,
			url=reverse('videolog:catentries', args=(categories[2].slug,)),
			id=categories[2].id,
			)
		)
			
		nodes.append(NavigationNode(
			title=categories[1].title,
			url=reverse('videolog:catentries', args=(categories[1].slug,)),
			id=categories[1].id,
			)
		)
		nodes.append(NavigationNode(
			title=categories[0].title,
			url=reverse('videolog:catentries', args=(categories[0].slug,)),
			id=categories[0].id,
			)
		)

		nodes.append(NavigationNode(
			title='Todo',
			url=reverse('videolog:entrieslist'),
			id=99,
			)
		)
		return nodes

menu_pool.register_menu(CategoryMenu)
