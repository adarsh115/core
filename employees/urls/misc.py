from django.urls import re_path

from employees import views

other_urls = [
    re_path(r'^create-allowance/?$', views.AllowanceCreateView.as_view(),
            name='create-allowance'),
    re_path(r'^allowances-list/?$', views.AllowanceListView.as_view(),
            name='allowances-list'),
    re_path(r'^update-allowance/(?P<pk>[\w]+)/?$',
            views.AllowanceUpdateView.as_view(), name='update-allowance'),
    re_path(r'^delete-allowance/(?P<pk>[\w]+)/?$',
            views.AllowanceDeleteView.as_view(), name='delete-allowance'),
    re_path(r'^allowance-details/(?P<pk>[\w]+)/?$',
            views.AllowanceDetailView.as_view(), name='allowance-details'),
    re_path(r'^create-deduction/?$', views.DeductionCreateView.as_view(),
            name='create-deduction'),
    re_path(r'^deductions-list/?$', views.DeductionListView.as_view(),
            name='deductions-list'),
    re_path(r'^deduction-detail/(?P<pk>[\w]+)/?$',
            views.DeductionDetailView.as_view(), name='deduction-detail'),
    re_path(r'^delete-deduction/(?P<pk>[\w]+)/?$',
            views.DeductionDeleteView.as_view(), name='delete-deduction'),
    re_path(r'^update-deduction/(?P<pk>[\w]+)/?$',
            views.DeductionUpdateView.as_view(), name='update-deduction'),
    re_path(r'^create-commission/?$', views.CommissionCreateView.as_view(),
            name='create-commission'),
    re_path(r'^commissions-list/?$', views.CommissionListView.as_view(),
            name='commissions-list'),
    re_path(r'^create-payroll-tax/?$', views.PayrollTaxCreateView.as_view(),
            name='create-payroll-tax'),
    re_path(r'^payroll-tax-list/?$', views.PayrollTaxListView.as_view(),
            name='payroll-tax-list'),
    re_path(r'^payroll-tax/(?P<pk>[\w]+)/?$',
            views.PayrollTaxDetailView.as_view(), name='payroll-tax'),
    re_path(r'^payroll-tax-delete/(?P<pk>[\w]+)/?$',
            views.PayrollTaxDeleteView.as_view(), name='payroll-tax-delete'),
    re_path(r'^update-payroll-tax/(?P<pk>[\w]+)/?$',
            views.PayrollTaxUpdateView.as_view(), name='update-payroll-tax'),
    re_path(r'^delete-commission/(?P<pk>[\w]+)/?$',
            views.CommissionDeleteView.as_view(), name='delete-commission'),
    re_path(r'^update-commission/(?P<pk>[\w]+)/?$',
            views.CommissionUpdateView.as_view(), name='update-commission'),
    re_path(r'^commission-details/(?P<pk>[\w]+)/?$',
            views.CommissionDetailView.as_view(), name='commission-details'),
    re_path(r'^config/(?P<pk>[\d]+)/?$', views.PayrollConfig.as_view(),
            name='config'),
    re_path(r'^manual-config/?$', views.ManualPayrollConfig.as_view(),
            name='manual-config'),
    re_path(r'^payroll-date/create/?$',
            views.CreatePayrollDateView.as_view(), name='payroll-date-create'),
    re_path(r'^payroll-date/update/(?P<pk>[\d]+)/?$',
            views.PayrollDateUpdateView.as_view(), name='payroll-date-update'),
    re_path(r'^payroll-date/detail/(?P<pk>[\d]+)/?$',
            views.PayrollDateDetailView.as_view(), name='payroll-date-detail'),
    re_path(r'^payroll-date/delete/(?P<pk>[\d]+)/?$',
            views.PayrollDateDeleteView.as_view(), name='payroll-date-delete'),
    re_path(r'^payroll-date/list/?$',
            views.PayrollDateListView.as_view(), name='payroll-date-list'),

]
