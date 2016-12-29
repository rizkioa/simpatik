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

        menu_utama = items.MenuItem(
                    title=_('Menu Izin'),
                    description='Menu Izin',
                    accesskey='menuIzin',
                    children= [
                        items.MenuItem(
                            title='Daftar Survey',
                            icon='fa fa-file-text', 
                            url=reverse('admin:semua_pengajuan'),                        
                        ),
                        items.MenuItem(
                            title=_('Daftar Laporan'),
                            description='Page Izin Terdaftar',
                            icon='icon-flag',
                            url=reverse("admin:izinterdaftar"),
                        ),
                        items.MenuItem(
                            title=_('Izin Bidang Pembangunan'),
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

        self.children += [
            menu_utama,
            menu_pengguna,
        ]
        return super(CustomMenu, self).init_with_context(context)
