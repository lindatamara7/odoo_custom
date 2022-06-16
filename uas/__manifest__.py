{
    'name': 'UAS',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Linda',
    'summary': 'UAS Konfigurasi ERP', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/supplier_views.xml',
        'views/item_views.xml',
        'wizard/wiz_uas_employee_views.xml',
        'views/transaksi2_views.xml',
        'views/delivery_views.xml'

    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}