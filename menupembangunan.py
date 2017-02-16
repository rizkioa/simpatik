from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items
from django.db.models import Q
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

        menu_dashboard = items.MenuItem(
                    title=_('Menu Utama'),
                    description='Menu Utama',
                    accesskey='menuUtama',
                    children= [
                        items.MenuItem(
                            title='Dashboard',
                            icon='fa fa-dashboard', 
                            url=reverse('admin:index'),                        
                        ),
                    ]
                )

        menu_utama = items.MenuItem(
                    title=_('Menu Izin'),
                    description='Menu Izin',
                    accesskey='menuIzin',
                    children= [
                        items.MenuItem(
                            title='Daftar Survey',
                            icon='fa fa-file-text', 
                            url=reverse('admin:izin_survey_changelist'),                        
                        ),
                        items.MenuItem(
                            title='Daftar Laporan',
                            icon='fa fa-file-text', 
                            url=reverse('admin:survey_selesai'),                        
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
                        icon='icon-user',
                        children= [
                            items.MenuItem(
                                title='Pemohon',
                                icon='fa fa-user-md',
                                url=reverse('admin:izin_pemohon_changelist'),
                            ),
                            items.MenuItem(
                                title='Pegawai',
                                icon='fa fa-user-md',
                                url=reverse('admin:kepegawaian_pegawai_changelist'),
                            ),
                            items.MenuItem(
                                title='Pengguna Lainnya',
                                icon='fa fa-user-md',
                                url=reverse('admin:accounts_account_changelist'),
                            ),
                        ]
                    ),
                    items.MenuItem(
                        title='Hak Akses',
                        icon='fa fa-shield',
                        url=reverse('admin:accounts_hakakses_changelist'),
                    ),
                ]
            )

        if request.user.groups.filter(Q(name="Admin Pembangunan")|Q(name="Kepala Pembangunan")|Q(name="Tim Teknis")).exists():
            self.children += [
                menu_dashboard,
                menu_utama,
            ]
        elif request.user.is_superuser:
            menu_utama.children+= [
                    items.MenuItem(
                        title=_('Izin Terdaftar'),
                        description='Page Izin Terdaftar',
                        icon='icon-flag',
                        url=reverse("admin:izinterdaftar"),
                    ),
                    items.MenuItem(
                        title=_('Pemohon Terdaftar'),
                        description='Page Pemohon Terdaftar',
                        icon='icon-user-following',
                        url=reverse("admin:izin_pemohon_changelist"),
                    ),
                    items.MenuItem(
                        title=_('Perusahaan Terdaftar'),
                        description='Page Perusahaan Terdaftar',
                        icon='icon-globe',
                        url=reverse("admin:perusahaan_terdaftar"),
                    ),
                ]
            self.children += [
                menu_utama,
                menu_pengguna,
            ]
        else:
            self.children += [
            ]
        return super(CustomMenu, self).init_with_context(context)
