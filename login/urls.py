
from django.urls import path
from . import views
from login.views import custom_404_page

handler404 = 'login.views.custom_404_page'
urlpatterns = [

    path('', views.login_view, name='login'),
    path('sign/', views.sign, name='sign'),
    path('forget/', views.forget, name='forget'),
    path('logout/', views.logout_view, name='logout'),
    path('wel/', views.wel, name='wel'),     
    path('home/', views.home, name='home'),  
    path('profile/', views.profile, name='profile'),

    path('password/', views.password, name='password'),
    path('change/', views.change, name='change'),
    path('forgot/', views.forgot, name='forgot'),
    path('recover/', views.recover, name='recover'),

    path('marchant/', views.marchant, name='marchant'),
    path('marchantbranch/', views.marchant_branch, name='marchantbranch'), 
    path('marchantaccount/', views.marchant_account, name='marchantaccount'),    
    path('marchantterminal/', views.marchant_terminal, name='marchantterminal'),    
    path('marchantpayment/', views.marchant_payment, name='marchantpayment'),    
    path('paymentsummary/', views.payment_summary, name="paymentsummary"),
    path('duesummary/', views.due_summary, name="duesummary"),
    path('duetransaction/', views.due_transaction, name="duetransaction"),
    path('dueadjustment/', views.due_adjustment, name="dueadjustment"),
    path('adadjustment/', views.ad_adjustment, name="adadjustment"),
    path('adjustmedue/', views.ad_due, name="addue"),
    path('search/', views.search, name="search"),
    path('find/', views.find, name="find"),
    path('ticket/', views.ticket, name="ticket"),
    path('createticket/', views.create_ticket, name="createticket"),
    path('complainticket/', views.complain_ticket, name="complainticket"),
    path('fetch_fault_categories/', views.fetch_fault_categories, name='fetch_fault_categories'),
    path('display_notifications/', views.display_notifications, name='display_notifications'),
    path('doc/', views.doc, name='doc'),
    path('download/<str:file_name>/', views.download_document, name='download_document'),
    path('upload_document/', views.upload_document, name='upload_document'),
    path('fetch_document_types/', views.fetch_document_types, name='fetch_document_types'),
    path('upload/', views.upload, name='upload'), 
    path('pdf', views.generate_pdf, name='pdf'),
    path('notification/', views.notifications, name='notification'),
    path('mark_notification_as_seen/', views.mark_notification_as_seen, name='mark_notification_as_seen'),
    path('PrivacyPolicy/', views.pp, name='PrivacyPolicy'),
    path('TremsOfServices/', views.tm, name='TremsOfServices'),
    path('validate/', views.validate, name='validate'),
    path('validateform/', views.validateform, name='validateform'),
    path('history/', views.history, name='history'),
    path('paymentsummary1/', views.paymentsummary, name='paymentsummary1'),
    path('postatus/', views.postatus, name='postatus')
   

]

