from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items

from admin_tools.menus import Menu

class CustomMenu(Menu):
    """
    Custom Menu for siabjo admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        # self.children += [
        #     items.MenuItem(
        #             title=_('Dashboard'),
        #             description='Admin Home Page',
        #             icon='fa fa-dashboard fa-fw',
        #             url=reverse('admin:index'),
        #         ),
        # ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        from django.core.urlresolvers import resolve
        request = context['request']

        menu_utama = items.MenuItem(
                    title=_('Menu Utama'),
                    description='Menu Utama',
                    accesskey='menuUtama',
                    children= [
                        items.MenuItem(
                            title=_('Dashboard'),
                            description='Admin Home Page',
                            icon='fa fa-dashboard fa-fw',
                            url=reverse('admin:index'),
                        ),
                    ]
                )

        menu_pengguna = items.MenuItem(
                    title=_('Manajemen Pengguna'),
                    description='Manajemen Pengguna',
                    accesskey='menuPengguna',
                    children= [
                        items.MenuItem(
                            title='Daftar Pengguna',
                            icon='fa fa-users',
                            children= [
                                items.MenuItem(
                                    title='Pemohon',
                                    icon='fa fa-user-md',
                                    url="#",
                                ),
                                items.MenuItem(
                                    title='Pegawai',
                                    icon='fa fa-user-md',
                                    url="#",
                                ),
                                items.MenuItem(
                                    title='Administrator',
                                    icon='fa fa-user-md',
                                    url="#",
                                ),
                            ]
                        ),
                        items.MenuItem(
                            title='Hak Akses',
                            icon='fa fa-shield',
                            url=reverse('admin:auth_group_changelist'),
                        ),
                    ]
                )

        self.children += [
            menu_utama,
        ]
        if request.user.is_superuser:
            self.children += [
                menu_pengguna,
            ]
        return super(CustomMenu, self).init_with_context(context)