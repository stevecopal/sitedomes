
from django.views.generic import FormView, UpdateView, DeleteView, ListView, TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from domestique.models import Client, Provider, Admin, Service, Request, Response
from domestique.forms import UserRegistrationForm, UserLoginForm, ServiceForm

class HomeView(TemplateView):
    template_name = 'domestique/index.html'

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'domestique/register.html'
    success_url = None

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.role == 'CLIENT':
            return redirect('client_dashboard')
        elif user.role == 'PROVIDER':
            return redirect('provider_dashboard')

class AdminAdminCreateView(AdminRequiredMixin, CreateView):
    model = Admin
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'photo', 'password']
    template_name = 'domestique/admin/admin_form.html'
    success_url = reverse_lazy('admin_client_list')

    def form_valid(self, form):
        form.instance.role = 'ADMIN'
        form.instance.is_superuser = True
        form.instance.is_staff = True
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)

class LoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'domestique/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'CLIENT':
                return reverse_lazy('client_dashboard')
            elif user.role == 'PROVIDER':
                return reverse_lazy('provider_dashboard')
            elif user.role == 'ADMIN':
                return reverse_lazy('admin_client_list')
        return reverse_lazy('home')

class AdminLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'domestique/admin/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'ADMIN':
            return reverse_lazy('admin_client_list')
        return reverse_lazy('home')

class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

class ClientDashboardView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'domestique/client_dashboard.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.filter(client=self.request.user, deleted_at__isnull=True).exclude(status='EXPIRED')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_responses'] = Response.objects.filter(
            request__client=self.request.user, request__deleted_at__isnull=True, status='PENDING'
        ).count()
        return context

class ProviderDashboardView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'domestique/provider_dashboard.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(provider=self.request.user, request__deleted_at__isnull=True).exclude(request__status='EXPIRED')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_requests'] = Request.objects.filter(
            accepted_provider=self.request.user, deleted_at__isnull=True
        ).exclude(status='EXPIRED').count()
        return context

class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['service', 'description', 'location', 'price', 'task_date']
    template_name = 'domestique/request_create.html'
    success_url = reverse_lazy('client_dashboard')

    def form_valid(self, form):
        form.instance.client = Client.objects.get(pk=self.request.user.pk)  
        return super().form_valid(form)

class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'domestique/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.filter(status='PENDING', deleted_at__isnull=True).exclude(status='EXPIRED')

class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['message', 'proposed_price']
    template_name = 'domestique/response_create.html'
    success_url = reverse_lazy('provider_dashboard')

    def form_valid(self, form):
        form.instance.provider = Provider.objects.get(pk=self.request.user.pk)
        form.instance.request = Request.objects.get(id=self.kwargs['request_id'])
        return super().form_valid(form)

class RequestAcceptView(LoginRequiredMixin, UpdateView):
    model = Request
    fields = []
    template_name = 'domestique/request_accept.html'
    success_url = reverse_lazy('client_dashboard')
    pk_url_kwarg = 'request_id'

    def form_valid(self, form):
        form.instance.accepted_provider = Provider.objects.get(id=self.kwargs['provider_id'])
        form.instance.status = 'ACCEPTED'
        response = Response.objects.get(request=form.instance, provider=form.instance.accepted_provider)
        response.status = 'ACCEPTED'
        response.save()
        return super().form_valid(form)

class RequestRejectView(LoginRequiredMixin, UpdateView):
    model = Response
    fields = []
    template_name = 'domestique/request_reject.html'
    success_url = reverse_lazy('client_dashboard')
    pk_url_kwarg = 'request_id'

    def form_valid(self, form):
        form.instance.status = 'REJECTED'
        return super().form_valid(form)

class AdminClientListView(AdminRequiredMixin, ListView):
    model = Client
    template_name = 'domestique/admin/client_list.html'
    context_object_name = 'clients'

class AdminClientCreateView(AdminRequiredMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'photo', 'is_active']
    template_name = 'domestique/admin/client_form.html'
    success_url = reverse_lazy('admin_client_list')

    def form_valid(self, form):
        form.instance.role = 'CLIENT'
        return super().form_valid(form)

class AdminClientUpdateView(AdminRequiredMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'photo', 'is_active']
    template_name = 'domestique/admin/client_form.html'
    success_url = reverse_lazy('admin_client_list')

    def form_valid(self, form):
        form.instance.role = 'CLIENT'
        return super().form_valid(form)

class AdminClientDeleteView(AdminRequiredMixin, DeleteView):
    model = Client
    template_name = 'domestique/admin/client_confirm_delete.html'
    success_url = reverse_lazy('admin_client_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)

class AdminProviderListView(AdminRequiredMixin, ListView):
    model = Provider
    template_name = 'domestique/admin/provider_list.html'
    context_object_name = 'providers'

class AdminProviderCreateView(AdminRequiredMixin, CreateView):
    model = Provider
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'photo', 'is_active', 'is_approved', 'skills']
    template_name = 'domestique/admin/provider_form.html'
    success_url = reverse_lazy('admin_provider_list')

    def form_valid(self, form):
        form.instance.role = 'PROVIDER'
        return super().form_valid(form)

class AdminProviderUpdateView(AdminRequiredMixin, UpdateView):
    model = Provider
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'photo', 'is_active', 'is_approved', 'skills']
    template_name = 'domestique/admin/provider_form.html'
    success_url = reverse_lazy('admin_provider_list')

    def form_valid(self, form):
        form.instance.role = 'PROVIDER'
        return super().form_valid(form)

class AdminProviderDeleteView(AdminRequiredMixin, DeleteView):
    model = Provider
    template_name = 'domestique/admin/provider_confirm_delete.html'
    success_url = reverse_lazy('admin_provider_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)

class AdminServiceCreateView(AdminRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'domestique/admin/service_form.html'
    success_url = reverse_lazy('admin_service_list')

class AdminServiceListView(AdminRequiredMixin, ListView):
    model = Service
    template_name = 'domestique/admin/service_list.html'
    context_object_name = 'services'

class AdminServiceUpdateView(AdminRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'domestique/admin/service_form.html'
    success_url = reverse_lazy('admin_service_list')

class AdminServiceDeleteView(AdminRequiredMixin, DeleteView):
    model = Service
    template_name = 'domestique/admin/service_confirm_delete.html'
    success_url = reverse_lazy('admin_service_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)

class AdminRequestListView(AdminRequiredMixin, ListView):
    model = Request
    template_name = 'domestique/admin/request_list.html'
    context_object_name = 'requests'

class AdminRequestCreateView(AdminRequiredMixin, CreateView):
    model = Request
    fields = ['client', 'service', 'description', 'location', 'price', 'status', 'accepted_provider', 'task_date']
    template_name = 'domestique/admin/request_form.html'
    success_url = reverse_lazy('admin_request_list')

class AdminRequestUpdateView(AdminRequiredMixin, UpdateView):
    model = Request
    fields = ['client', 'service', 'description', 'location', 'price', 'status', 'accepted_provider', 'task_date']
    template_name = 'domestique/admin/request_form.html'
    success_url = reverse_lazy('admin_request_list')

class AdminRequestDeleteView(AdminRequiredMixin, DeleteView):
    model = Request
    template_name = 'domestique/admin/request_confirm_delete.html'
    success_url = reverse_lazy('admin_request_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)

class AdminResponseListView(AdminRequiredMixin, ListView):
    model = Response
    template_name = 'domestique/admin/response_list.html'
    context_object_name = 'responses'

class AdminResponseCreateView(AdminRequiredMixin, CreateView):
    model = Response
    fields = ['request', 'provider', 'message', 'proposed_price']
    template_name = 'domestique/admin/response_form.html'
    success_url = reverse_lazy('admin_response_list')

class AdminResponseUpdateView(AdminRequiredMixin, UpdateView):
    model = Response
    fields = ['request', 'provider', 'message', 'proposed_price']
    template_name = 'domestique/admin/response_form.html'
    success_url = reverse_lazy('admin_response_list')

class AdminResponseDeleteView(AdminRequiredMixin, DeleteView):
    model = Response
    template_name = 'domestique/admin/response_confirm_delete.html'
    success_url = reverse_lazy('admin_response_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)