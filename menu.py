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
                        #     title='Pengajuan Izin',
                        #     icon='fa fa-file-text-o',
                        #     children= [
                        #         items.MenuItem(
                        #             title='Pengajuan Baru',
                        #             icon='fa fa-edit',
                        #             url=reverse('admin:add_wizard_izin'),
                        #         ),
                        #         items.MenuItem(
                        #             title='Pengajuan Masuk',
                        #             icon='fa fa-tasks',
                        #             url='#',
                        #         ),
                        #     ]                            
                        # ),
                        # items.MenuItem(
                        #     title='Semua Izin',
                        #     icon='fa fa-file-text', 
                        #     url=reverse('admin:izin_pengajuanizin_changelist'),                        
                        # ),
                        # items.MenuItem(
                        #     title='Semua Perusahan',
                        #     icon='fa fa-building', 
                        #     url=reverse('admin:perusahaan_perusahaan_changelist'),                        
                        # ),
                    ]
                )



        # if request.user.groups.filter(Q(name="Operator")|Q(name="Kabid")|Q(name="Pembuat Surat")|Q(name="Kadin")|Q(name="Cetak")|Q(name="Penomoran")|Q(name="Selesai")).exists():
        menu_izin = items.MenuItem(
                    title=_('Menu Izin'),
                    description='Menu Izin',
                    accesskey='menuIzin',
                    children= [
                        # items.MenuItem(
                        #     title='Notifikasi Telegram',
                        #     icon='fa fa-file-text', 
                        #     url=reverse('admin:kepegawaian_notifikasitelegram_changelist'),                        
                        # ),
                        items.MenuItem(
                            title='Semua Pengajuan',
                            icon='fa fa-file-text', 
                            url=reverse('admin:semua_pengajuan'),                        
                        ),
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
                        items.MenuItem(
                            title='Daftar Survey',
                            icon='fa fa-edit',
                            url=reverse('admin:survey'),
                        ),
                    ]
                )

        # if request.user.is_superuser:
        #     menu_utama.children += [
        #         items.MenuItem(
        #             title='Semua Pengajuan',
        #             icon='fa fa-file-text', 
        #             url=reverse('admin:semua_pengajuan'),                        
        #         ),
        #     ]

        if request.user.groups.filter(name="Operator").exists():

            menu_utama.children += [
                items.MenuItem(
                        title='Pengajuan Baru',
                        icon='fa fa-edit',
                        url=reverse('admin:add_wizard_izin'),
                    ),
                items.MenuItem(
                    title='Pengajuan Masuk',
                    icon='icon-check',
                    css_classes='operator',
                    url=reverse('admin:verifikasi_operator'),  
                )
            ]

        if request.user.groups.filter(Q(name="Tim Teknis") | Q(name="Cek Lokasi")).exists():
             menu_utama.children += [
                 items.MenuItem(
                        title='Daftar Survey',
                        icon='fa fa-file-text',
                        css_classes='cek_lokasi',
                        url=reverse('admin:izin_survey_changelist'),                        
                    ),
                    items.MenuItem(
                        title='Daftar Laporan',
                        icon='fa fa-file-text', 
                        url=reverse('admin:survey_selesai'),                        
                    ),
             ]



        if request.user.groups.filter(name="Kabid").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Pengajuan Masuk',
                    icon='icon-check',
                    css_classes='kabid_pengajuan', 
                    url=reverse('admin:verifikasi_kabid'),                
                ),
                items.MenuItem(
                    title='Draft SK',
                    icon='icon-list',
                    css_classes='kabid_skizin', 
                    url=reverse('admin:verifikasi_skizin_kabid'),                
                ),
            ]

        if request.user.groups.filter(name="Pembuat Surat").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Draft SK',
                    icon='fa fa-file-text',
                    css_classes='pembuat_surat', 
                    url=reverse('admin:verifikasi_pembuat_surat'),                
                ),
                items.MenuItem(
                    title='Perbaikan SK',
                    icon='fa fa-file-text',
                    css_classes='perbaikan_surat', 
                    url=reverse('admin:verifikasi_perbaikan_surat'),                
                ),
            ]

        if request.user.groups.filter(name='Kasir').exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Kasir',
                    icon='fa fa-file-text',
                    css_classes='kasir', 
                    url=reverse('admin:kasir'),                
                ),
            ]

        if request.user.groups.filter(name="Kadin").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Draft SK',
                    icon='fa fa-file-text',
                    css_classes='kadin_skizin', 
                    url=reverse('admin:verifikasi_skizin_kadin'),                
                ),
            ]

        if request.user.groups.filter(name="Bupati").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Draft SK',
                    icon='fa fa-file-text',
                    css_classes='bupati_skizin', 
                    url=reverse('admin:verifikasi_skizin_bupati'),                
                ),
            ]

        if request.user.groups.filter(name="Penomoran").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Penomoran Izin',
                    icon='fa fa-file-text',
                    css_classes='penomoran', 
                    url=reverse('admin:penomoran_skizin'),                
                ),
            ]

        if request.user.groups.filter(name="Cetak").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Cetak Izin',
                    icon='fa fa-file-text',
                    css_classes='cetak', 
                    url=reverse('admin:verifikasi_skizin_cetak'),                
                ),
            ]

        if request.user.groups.filter(name="Selesai").exists():
            menu_utama.children += [
                items.MenuItem(
                    title='Stemple Izin',
                    icon='fa fa-file-text',
                    css_classes='selesai',
                    url=reverse('admin:stemple_izin'),                
                ),
            ]

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
            menu_izin,
        ]

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
                        items.MenuItem(
                            title='Klasifikasi IUJK',
                            icon='fa fa-file-text-o',
                            url=reverse('admin:izin_klasifikasi_changelist'),
                        ),
                        items.MenuItem(
                            title='SubKlasifikasi IUJK',
                            icon='fa fa-file-text-o',
                            url=reverse('admin:izin_subklasifikasi_changelist'),
                        ),
                        items.MenuItem(
                            title='Izin Pariwisata',
                            icon='fa fa-file-text-o',
                            children= [
                                items.MenuItem(
                                    title='Bidang Usaha Pariwisata',
                                    icon='fa fa-file-text-o',
                                    url=reverse('admin:izin_bidangusahapariwisata_changelist'),
                                ),
                                items.MenuItem(
                                    title='Jenis Usaha Pariwisata',
                                    icon='fa fa-file-text-o',
                                    url=reverse('admin:izin_jenisusahapariwisata_changelist'),
                                ),
                                items.MenuItem(
                                    title='Sub Jenis Usaha Pariwisata',
                                    icon='fa fa-file-text-o',
                                    url=reverse('admin:izin_subjenisusahapariwisata_changelist'),
                                ),
                            ]
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
                    title='Kelembagaan',
                    icon='fa fa-user-md',
                    url=reverse('admin:perusahaan_kelembagaan_changelist'),
                ),
                items.MenuItem(
                    title='KBLI',
                    icon='fa fa-user-md',
                    url=reverse('admin:perusahaan_kbli_changelist'),
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
        
        if request.user.is_superuser:
            self.children += [
                menu_pengguna,              
                menu_pengaturan,
            ]

        if request.user.groups.filter(name="Admin Simpatik").exists():
            items.MenuItem(
                title=_('Manajemen Pengguna'),
                description='Manajemen Pengguna',
                accesskey='menuPengguna',
                children= [
                    items.MenuItem(
                        title='Daftar Pengguna',
                        icon='icon-user',
                        children= [
                            items.MenuItem(
                                title='Pegawai',
                                icon='fa fa-user-md',
                                url=reverse('admin:kepegawaian_pegawai_changelist'),
                            ),
                        ]
                    ),
                ]
            )
            self.children += [             
                menu_pengaturan,
            ]
        
        return super(CustomMenu, self).init_with_context(context)
