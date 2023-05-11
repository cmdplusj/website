from django.urls import path, re_path
from django.contrib.auth import views as auth_views
# from main.views import approval_message, home_view, mentor_signup, mentee_signup, mentor_add_tag, mentee_add_tag, account_activation_sent, account_activate, login, admin_dashboard, mentor_dashboard, browse
from main import views as main_views

handler404 = main_views.handler404
handler500 = main_views.handler500

urlpatterns = [
    path('login/', main_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', main_views.home_view, name='home'),
    path('signup/', main_views.signup, name='signup'),
    path('resources/', main_views.resources, name='resources'),
    path('about/', main_views.about, name='about'),
    path('details/mentor/', main_views.mentor_details, name='mentor_details'),
    path('signup/mentor/', main_views.mentor_signup, name='mentor_signup'),
    path('signup/mentee/', main_views.mentee_signup, name='mentee_signup'),
    path('mentor/dashboard/edit_profile', main_views.mentor_edit_profile, name='mentor_edit_profile'),
    path('mentor/dashboard/opt_out', main_views.mentor_opt_out, name='opt_out'),
    path('mentor/dashboard/opt_in', main_views.mentor_opt_in, name='opt_in'),
    path('mentee/dashboard/edit_profile', main_views.mentee_edit_profile, name='mentee_edit_profile'),
    path('mentor/bio/update', main_views.mentor_bio_update, name='mentor_bio_update'),
    path('admin_dashboard/', main_views.admin_dashboard, name='admin_dashboard'),
    path('mentor/dashboard/', main_views.mentor_dashboard, name='mentor_dashboard'),
    path('mentee/dashboard/', main_views.mentee_dashboard, name='mentee_dashboard'),
    path('mentor/dashboard/scheduled/', main_views.mentor_scheduled, name='mentor_scheduled'),
    path('browse/', main_views.browse, name='browse'),
    path('mentor/addtag/', main_views.mentor_add_tag, name='mentor_addtag'),
    path('mentee/addtag/', main_views.mentee_add_tag, name='mentee_addtag'),
    path('approval/', main_views.approval_message, name='approval_message'),
    # re_path(r'^account_activation_sent/$', main_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        main_views.account_activate, name='activate'),
    re_path(r'^admin_dashboard/accept/(?P<mentor_id>[0-9]+)/$', main_views.accept_mentor , name='accept_mentor'),
    re_path(r'^admin_dashboard/reject/(?P<mentor_id>[0-9]+)/$', main_views.reject_mentor , name='reject_mentor'),
    re_path(r'^browse/send/invitation/(?P<mentor_id>[0-9]+)/$', main_views.send_request , name='send_request'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(),{'template_name' : "main/registration/password_reset_form.html"}, name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^mentor/(?P<mentor_name>[0-9A-Za-z_\-\ ]+)/(?P<mentor_id>[0-9]+)/$', main_views.mentor_profile, name='mentor_profile'),
    re_path(r'^mentee/(?P<mentee_name>[0-9A-Za-z_\-\ ]+)/(?P<mentee_id>[0-9]+)/$', main_views.mentee_profile, name='mentee_profile'),
    re_path(r'^mentor/dashboard/schedule_reject/(?P<appointment_id>[0-9]+)/$', main_views.schedule_reject, name='schedule_reject'),
]
