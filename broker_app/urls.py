from django.urls import path
from . import views

urlpatterns = [
	path(r'', views.main),
    path(r'analyse/', views.analyse),
	path(r'analyse/secur_ch/', views.secur_ch),
	path(r'analyse/secur_choice/', views.news),
	path(r'analyse/tech_analyse/', views.tech_analyse),
	path(r'analyse/companies_news/', views.comp_news),
	path(r'analyse/experts_comments/', views.exp_comments),
	path(r'analyse/secur_price/', views.secur_price),
	path(r'analyse/my_notes/', views.my_notes),
    path(r'analyse/my_notes/my_notes_add/', views.notes_add, name="notes_add"),
	path(r'analyse/sites_list/', views.comp_sites_list),
    path(r'analyse/sites_list/sites_add/', views.sites_add, name='site_add'),
	
	
	path(r'clients_window/', views.clients_window),
	path(r'clients_window/clients_add/', views.clients_add),
	path(r'clients_window/clients_view/', views.clients_view),
	path(r'clients_window/clients_delete/', views.clients_delete),
	path(r'clients_window/clients_delete/clients_modify/', views.clients_modify, name ='cl_modify'),
	path(r'clients_window/autoriz/', views.autoriz),
	
	path(r'useful_data/', views.useful_site),
    path(r'useful_data/useful_add/', views.useful_add, name= 'usef_add'),
    path(r'useful_data/useful_modify/', views.useful_modify, name="usef_modify"),
	]
