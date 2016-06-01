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
                        # items.MenuItem(
                        #     title='Izin',
                        #     icon='fa fa-file-text-o',
                        #     url=reverse('admin:izin_izin_changelist'),
                        # ),
                    ]
                )
        
        # menu_master = items.MenuItem(
        #             title=_('Menu Master'),
        #             description='Menu Master',
        #             accesskey='menuMaster',
        #             children= [
                        # items.MenuItem(
                        #     title='Pertanahan',
                        #     icon='fa fa-puzzle-piece',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Jenis Tanah',
                        #             icon='fa fa-puzzle-piece',
                        #             url=reverse('admin:izin_jenistanah_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Kepemilikkan Tanah',
                        #             icon='fa fa-puzzle-piece',
                        #             url=reverse('admin:izin_kepemilikkantanah_changelist'),
                        #         ),
                        #     ]
                        # ),
                        
                        # items.MenuItem(
                        #     title='Permodalan',
                        #     icon='fa fa-money',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Jenis Modal Koprasi',
                        #             icon='fa fa-money',
                        #             url=reverse('admin:perusahaan_jenismodalkoprasi_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Jenis Penanaman Modal',
                        #             icon='fa fa-money',
                        #             url=reverse('admin:perusahaan_jenispenanamanmodal_changelist'),
                        #         ),
                        #     ]
                        # ),
                        # items.MenuItem(
                        #     title='Perizinan',
                        #     icon='fa fa-file-text-o',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Jenis Izin',
                        #             icon='fa fa-file-text-o',
                        #             url=reverse('admin:izin_jenisizin_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Jenis Permohonan Izin',
                        #             icon='fa fa-file-text-o',
                        #             url=reverse('admin:izin_jenispermohonanizin_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='KBLI',
                        #             icon='fa fa-file-text-o',
                        #             url=reverse('admin:perusahaan_kbli_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Syarat Izin',
                        #             icon='fa fa-file-text-o',
                        #             url=reverse('admin:izin_syarat_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Kelompok Jenis Izin',
                        #             icon='fa fa-file-text-o',
                        #             url=reverse('admin:izin_kelompokjenisizin_changelist'),
                        #         ),
                        #     ]
                        # ),
                        # items.MenuItem(
                        #     title='Reklame',
                        #     icon='fa fa-th-large',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Jenis Reklame',
                        #             icon='fa fa-th-large',
                        #             url=reverse('admin:izin_jenisreklame_changelist'),
                        #         ),
                        #     ]
                        # ),
                        # items.MenuItem(
                        #     title='Menu Badan Usaha',
                        #     icon='fa fa-building-o',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Perusahaan',
                        #             icon='fa fa-building-o',
                        #             url=reverse('admin:perusahaan_perusahaan_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Jenis Perusahaan',
                        #             icon='fa fa-building-o',
                        #             url=reverse('admin:perusahaan_jenisperusahaan_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Kelembagaan',
                        #             icon='fa fa-building-o',
                        #             url=reverse('admin:perusahaan_kelembagaan_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Kegiatan Usaha',
                        #             icon='fa fa-building-o',
                        #             url=reverse('admin:perusahaan_kegiatanusaha_changelist'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Jenis Kerjasama',
                        #             icon='fa fa-building-o',
                        #             url=reverse('admin:perusahaan_jeniskerjasama_changelist'),
                        #         ),
                        #     ]
                        # ),
                #     ]
                # )

        if hasattr(request.user, "pemohon"):
            menu_utama.children += [
                items.MenuItem(
                    title='Perijinan Saya',
                    icon='fa fa-tasks',
                    url="#",
                ),
                items.MenuItem(
                    title='Pendaftaran Perijinan',
                    icon='fa fa-file-text',
                    url="#",
                    children= [
                        items.MenuItem(
                            title='SIUP',
                            icon='icon-globe',
                            url="#",
                        ),
                        items.MenuItem(
                            title='TDP',
                            icon='fa fa-globe',
                            url="#",
                        ),
                        items.MenuItem(
                            title='IMB',
                            icon='icon-globe-alt',
                            url="#",
                        ),
                        items.MenuItem(
                            title='HO',
                            icon='icon-map',
                            url="#",
                        ),
                        items.MenuItem(
                            title='Huller',
                            icon='fa fa-map-marker',
                            description='Penggilingan Padi',
                            url="#",
                        ),
                        items.MenuItem(
                            title='Reklame',
                            icon='fa fa-map-marker',
                            url="#",
                        ),
                        items.MenuItem(
                            title='Kekayaan Daerah',
                            icon='fa fa-map-marker',
                            url="#",
                        ),
                    ]
                ),
            ]

        self.children += [
            menu_utama,
        ]

        if request.user.is_superuser:
            menu_pengaturan = items.MenuItem(
                title=_('Menu Pengaturan'),
                description='Menu Pengaturan',
                accesskey='menuPengaturan',
                children= [
                    items.MenuItem(
                        title='Perizinan',
                        icon='fa fa-file-text-o',
                        children= [
                            items.MenuItem(
                                title='Jenis Izin',
                                icon='fa fa-file-text-o',
                                url=reverse('admin:izin_jenisizin_changelist'),
                            ),
                            items.MenuItem(
                                title='Kelompok Jenis Izin',
                                icon='fa fa-file-text-o',
                                url=reverse('admin:izin_kelompokjenisizin_changelist'),
                            ),
                            items.MenuItem(
                                title='Syarat Izin',
                                icon='fa fa-file-text-o',
                                url=reverse('admin:izin_syarat_changelist'),
                            ),
                            items.MenuItem(
                                title='Prosedur Izin',
                                icon='fa fa-file-text-o',
                                url=reverse('admin:izin_prosedur_changelist'),
                            ),
                            items.MenuItem(
                                title='Jenis Permohonan Izin',
                                icon='fa fa-file-text-o',
                                url=reverse('admin:izin_jenispermohonanizin_changelist'),
                            ),
                            # items.MenuItem(
                            #     title='KBLI',
                            #     icon='fa fa-file-text-o',
                            #     url=reverse('admin:perusahaan_kbli_changelist'),
                            # ),                           
                        ]
                    ),
                    items.MenuItem(
                        title='Unit Kerja',
                        icon='fa fa-sitemap',
                        children= [
                            items.MenuItem(
                                title='Jenis Unit Kerja',
                                icon='fa fa-sitemap',
                                url=reverse('admin:kepegawaian_jenisunitkerja_changelist'),
                            ),
                            items.MenuItem(
                                title='Semua Unit Kerja',
                                icon='fa fa-institution',
                                url=reverse('admin:kepegawaian_unitkerja_changelist'),
                            ),
                            items.MenuItem(
                                title='Bidang / Bagian / Seksi',
                                icon='fa fa-building-o',
                                url=reverse('admin:kepegawaian_bidangstruktural_changelist'),
                            ),
                        ]
                    ),
                    items.MenuItem(
                        title='Dasar Hukum',
                        icon='fa fa-legal',
                        children= [
                            items.MenuItem(
                                title='Jenis Peraturan',
                                icon='fa fa-info-circle',
                                url=reverse('admin:izin_jenisperaturan_changelist'),
                            ),
                            items.MenuItem(
                                title='Dasar Hukum',
                                icon='fa fa-gavel',
                                url=reverse('admin:izin_dasarhukum_changelist'),
                            ),
                        ]
                    ),
                    items.MenuItem(
                        title='Daftar Lokasi',
                        icon='icon-globe',
                        children= [
                            items.MenuItem(
                                title='Negara',
                                icon='icon-globe',
                                url=reverse('admin:master_negara_changelist'),
                            ),
                            items.MenuItem(
                                title='Provinsi',
                                icon='fa fa-globe',
                                url=reverse('admin:master_provinsi_changelist'),
                            ),
                            items.MenuItem(
                                title='Kota / Kabupaten',
                                icon='icon-globe-alt',
                                url=reverse('admin:master_kabupaten_changelist'),
                            ),
                            items.MenuItem(
                                title='Kecamatan',
                                icon='icon-map',
                                url=reverse('admin:master_kecamatan_changelist'),
                            ),
                            items.MenuItem(
                                title='Desa / Kelurahan',
                                icon='fa fa-map-marker',
                                url=reverse('admin:master_desa_changelist'),
                            ),
                        ]
                    ),
                    items.MenuItem(
                        title='Jabatan',
                        icon='fa fa-star',
                        url=reverse('admin:kepegawaian_jabatan_changelist'),
                    ),
                    items.MenuItem(
                        title='Jenis Pemohon',
                        icon='fa fa-child',
                        url=reverse('admin:master_jenispemohon_changelist'),
                    ),
                    items.MenuItem(
                        title=_('Setting'),
                        description='Setting atau Konfigurasi',
                        icon='fa fa-cog fa-fw',
                        url=reverse('admin:master_settings_changelist'),
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
                                title='Administrator',
                                icon='fa fa-user-md',
                                url=reverse('admin:accounts_account_changelist'),
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
                menu_pengguna,              
                menu_pengaturan,
            ]
        if request.user.groups.filter(name='Front Desk').exists() or request.user.is_superuser:
            menu_operator = items.MenuItem(
                        title=_('Menu Operator'),
                        description='Menu Operator',
                        accesskey='menuOperator',
                        children= [
            #                 items.MenuItem(
            #                     title='Perubahan Izin',
            #                     icon='fa fa-file-text-o',
            #                     children= [
            #                         items.MenuItem(
            #                             title='SIUP',
            #                             icon='fa fa-caret-right',
            #                             url=reverse('admin:izin_pemohon_changelist'),
            #                         ),
            #                         items.MenuItem(
            #                             title='TDP',
            #                             icon='fa fa-caret-right',
            #                             url="#",
            #                         ),
            #                         items.MenuItem(
            #                             title='IMB',
            #                             icon='fa fa-toggle-right',
            #                             children= [
            #                                 items.MenuItem(
            #                                     title='IMB Gedung',
            #                                     icon='fa fa-caret-right',
            #                                     url=reverse('admin:izin_pemohon_changelist'),
            #                                 ),
            #                                 items.MenuItem(
            #                                     title='IMB Papan Reklame',
            #                                     icon='fa fa-caret-right',
            #                                     url="#",
            #                                 ),
            #                            ]
            #                         ),
            #                     ]
            #                 ),
                        ]
                    )

            self.children += [
                menu_operator,
            ]
        
        return super(CustomMenu, self).init_with_context(context)
