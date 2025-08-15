from django.urls import path
from domestique.views import (
    HomeView, RegisterView, LoginView, LogoutView, ClientDashboardView, ProviderDashboardView,
    RequestCreateView, RequestListView, ResponseCreateView, RequestAcceptView, RequestRejectView,
    AdminClientListView, AdminClientCreateView, AdminClientUpdateView, AdminClientDeleteView,
    AdminProviderListView, AdminProviderCreateView, AdminProviderUpdateView, AdminProviderDeleteView,
    AdminServiceCreateView, AdminServiceListView, AdminServiceUpdateView, AdminServiceDeleteView,
    AdminRequestListView, AdminRequestCreateView, AdminRequestUpdateView, AdminRequestDeleteView,
    AdminResponseListView, AdminResponseCreateView, AdminResponseUpdateView, AdminResponseDeleteView,
    AdminAdminCreateView, AdminLoginView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('client/dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('provider/dashboard/', ProviderDashboardView.as_view(), name='provider_dashboard'),
    path('request/create/', RequestCreateView.as_view(), name='request_create'),
    path('requests/', RequestListView.as_view(), name='request_list'),
    path('request/<uuid:request_id>/respond/', ResponseCreateView.as_view(), name='response_create'),
    path('request/<uuid:request_id>/accept/<uuid:provider_id>/', RequestAcceptView.as_view(), name='request_accept'),
    path('response/<uuid:pk>/reject/', RequestRejectView.as_view(), name='request_reject'),
    
    
    # Admin URLs
    path('admin/admins/create/', AdminAdminCreateView.as_view(), name='admin_admin_create'),
    path('admin/clients/', AdminClientListView.as_view(), name='admin_client_list'),
    path('admin/client/create/', AdminClientCreateView.as_view(), name='admin_client_create'),
    path('admin/client/<uuid:pk>/edit/', AdminClientUpdateView.as_view(), name='admin_client_edit'),
    path('admin/client/<uuid:pk>/delete/', AdminClientDeleteView.as_view(), name='admin_client_delete'),
    path('admin/providers/', AdminProviderListView.as_view(), name='admin_provider_list'),
    path('admin/provider/create/', AdminProviderCreateView.as_view(), name='admin_provider_create'),
    path('admin/provider/<uuid:pk>/edit/', AdminProviderUpdateView.as_view(), name='admin_provider_edit'),
    path('admin/provider/<uuid:pk>/delete/', AdminProviderDeleteView.as_view(), name='admin_provider_delete'),
    path('admin/services/create/', AdminServiceCreateView.as_view(), name='admin_service_create'),
    path('admin/services/', AdminServiceListView.as_view(), name='admin_service_list'),
    path('admin/service/<int:pk>/edit/', AdminServiceUpdateView.as_view(), name='admin_service_edit'),
    path('admin/service/<int:pk>/delete/', AdminServiceDeleteView.as_view(), name='admin_service_delete'),
    path('admin/requests/', AdminRequestListView.as_view(), name='admin_request_list'),
    path('admin/request/create/', AdminRequestCreateView.as_view(), name='admin_request_create'),
    path('admin/request/<uuid:pk>/edit/', AdminRequestUpdateView.as_view(), name='admin_request_edit'),
    path('admin/request/<uuid:pk>/delete/', AdminRequestDeleteView.as_view(), name='admin_request_delete'),
    path('admin/responses/', AdminResponseListView.as_view(), name='admin_response_list'),
    path('admin/response/create/', AdminResponseCreateView.as_view(), name='admin_response_create'),
    path('admin/response/<uuid:pk>/edit/', AdminResponseUpdateView.as_view(), name='admin_response_edit'),
    path('admin/response/<uuid:pk>/delete/', AdminResponseDeleteView.as_view(), name='admin_response_delete'),
]