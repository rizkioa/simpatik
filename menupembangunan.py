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
                            url=reverse('admin:survey_proses'),                        
                        ),
                        items.MenuItem(
                            title='Daftar Laporan',
                            icon='fa fa-file-text', 
                            url=reverse('admin:survey_selesai'),                        
                        ),
                    ]
                )

        menu_telegram = items.MenuItem(
                    title=_('Telegram'),
                    description='Telegram',
                    accesskey='menuTelegram',
                    children= [
                        items.MenuItem(
                            title='Notifikasi Telegram',
                            icon='fa fa-file-text', 
                            url=reverse('admin:kepegawaian_notifikasitelegram_changelist'),                        
                        ),
                        items.MenuItem(
                            title='Logs Telegram',
                            icon='fa fa-file-text', 
                            url=reverse('admin:kepegawaian_logtelegram_changelist'),                        
                        ),
                    ]
                )

        

        pengguna = []

        if request.user.is_superuser:
            pengguna += [
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
            ]
        elif request.user.groups.filter(name="Admin SKPD"):
            pengguna += [
                    items.MenuItem(
                        title='Pegawai',
                        icon='fa fa-user-md',
                        url=reverse('admin:kepegawaian_pegawai_changelist'),
                    ),
            ]

        menu_pengguna = items.MenuItem(
                title=_('Manajemen Pengguna'),
                description='Manajemen Pengguna',
                accesskey='menuPengguna',
                children= pengguna
            )

        if request.user.groups.filter(Q(name="Admin Pembangunan")|Q(name="Kepala Pembangunan")|Q(name="Tim Teknis")).exists():
            self.children += [
                menu_dashboard,
                menu_utama,
            ]
        elif request.user.is_superuser:
            menu_pengguna.children += [
                items.MenuItem(
                    title='Hak Akses',
                    icon='fa fa-shield',
                    url=reverse('admin:accounts_hakakses_changelist'),
                ),
            ]

            self.children += [
                menu_utama,
                menu_telegram,
                menu_pengguna,
            ]
        elif request.user.groups.filter(name="Admin SKPD"):
            self.children += [
                menu_utama,
                menu_telegram,
                menu_pengguna,
            ]
        else:
            self.children += [
            ]
        return super(CustomMenu, self).init_with_context(context)
