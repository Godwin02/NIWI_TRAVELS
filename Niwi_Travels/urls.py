from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, MyPasswordResetCompleteView
from .views import export_passenger_data_to_excel
from django.conf.urls.static import static
urlpatterns = [
    path('admins/',views.admin,name='admin'),
    path('',views.index,name='home'),
    path('register/',views.register,name='register'),
    path('dregister/',views.drireg,name='dregister'),
    path('tregister/', views.tregister, name='tregister'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_email, name='activate_email'),  # Activation view

    path('log/',views.login,name='log'),
    path('thome/',views.traveller_home,name='thome'),
    path('dhome/',views.driver_home,name='dhome'),
    path('logout/',views.logo,name='logout'),
    path('tupdate/',views.update_traveler,name='tupdate'),
    path('profile_updated',views.profile_updated,name='profile_updated'),
    path('dupdate/',views.update_driver,name='dupdate'),
    path('dpro_updated',views.dprofile_updated,name='dpro_updated'),
    #path('accounts/login/',views.login,name='login'),
    path('viewprofileT/', views.viewprofile, name='viewprofileT'),
    path('viewprofileD/', views.viewprofileD, name='viewprofileD'),

    path('accounts/profile/',views.traveller_home, name='thome'),


    path('user_list/', views.user_list, name='user_list'),
    path('travellers/', views.travellers, name='travellers'),
    path('drivers/', views.drivers, name='drivers'),
    path('update-verification-status/<int:user_profile_id>/', views.update_verification_status, name='update_verification_status'),
    path('approved-users/', views.list_approved_users, name='list_approved_users'),



    
    path('reset_password/', MyPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    

    path('activate/<str:uidb64>/<str:token>/', views.activate_email, name='activate_email'),  # Activation view


    
    path('upload_package/', views.upload_package, name='upload_package'),
    path('view-packages/', views.view_travel_packages, name='view_packages'),
    path('edit_package/<int:package_id>/', views.edit_package, name='edit_package'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('add_passenger/<int:package_id>/', views.add_passenger, name='add_passenger'),
    path('upcoming-journeys/', views.upcoming_journeys, name='upcoming_journeys'),
    path('history-journeys/', views.history_journeys, name='history_journeys'),
    path('ongoing-journeys/', views.ongoing_journeys, name='ongoing_journeys'),
    path('cancel_booking/<int:package_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/', views.upcoming_bookings, name='admin_bookings'),
    path('verified_bookings/', views.verified_bookings, name='verified_bookings'),
    path('passenger_count/<int:package_id>/', views.passenger_count, name='passenger_count'),
    path('ongoing-bookings/', views.ongoing_bookings, name='ongoing_journeys'),
    path('ongoing_passengers/<int:package_id>/', views.ongoing_passengers, name='ongoing_passengers'),
    path('history-bookings/', views.history_bookings, name='history_journeys'),
    path('history_passengers/<int:package_id>/', views.history_passengers, name='history_passengers'),
    path('update_booking_status/<int:user_id>/<int:package_id>/', views.update_booking_status, name='update_booking_status'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking_list/<int:package_id>', views.booking_list, name='booking_list'),
    path('pay/<int:booking_id>/', views.pay, name='pay'),
    path('success/<int:booking_id>/',views.success, name='success'),
    path('package_requests/<int:package_id>/', views.package_requests, name='package_requests'),
    path('passenger_details/<int:package_id>/', views.passenger_details, name='passenger_details'),
    path('delete_passenger/<int:passenger_id>/', views.delete_passenger, name='delete_passenger'),
    path('export-passenger-data/<int:package_id>/', export_passenger_data_to_excel, name='export_passenger_data_to_excel'),
    path('submit_rating/<int:package_id>/<int:stars>/', views.submit_rating, name='submit_rating'),
    path('download-receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),


    path('custom_package/', views.custom_package, name='custom_package'),
    path('honeymoon_packages/', views.honeymoon_packages, name='honeymoon_packages'),
    path('custom_package/<int:package_id>/', views.custom_package_detail, name='custom_package_detail'),
    path('admin_custom_package/',views.admin_custom_package,name='admin_custom_package') ,
    path('view_custom_package/', views.view_custom_package, name='view_custom_package'),
    path('edit_custom_package/<int:package_id>/', views.edit_custom_package, name='edit_custom_package'),




 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# # urlpatterns = [
# #     path('home/', views.home, name='home'),
# #     path('register_normal_user/', views.register_normal_user, name='register_normal_user'),
# #     path('register_college_user/', views.register_college_user, name='register_college_user'),
# #     path('', views.loginnew, name='loginnew'),
# #     path('normal_user_home/', views.normal_user_home, name='normal_user_home'),
# #     path('college_user_home/', views.college_user_home, name='college_user_home'),
# #     path('logoutnew/', views.logoutnew, name='logoutnew'),
# #     path('your_view/', views.your_view, name='your_view'),
# #     path('logoutp/', views.logoutp, name='logoutp'),
