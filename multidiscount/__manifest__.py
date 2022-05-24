{
    'name': 'Multidiscount',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Linda',
    'summary': 'Multidiscount', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan Inherit',
    'website': 'http://sib.petra.ac.id',
    'depends': ['sale'],  # list of dependencies, conditioning startup order
    'data': [
        'views/sale_order_views.xml'
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}