from django.conf.urls import url
from users import views as users_views

urlpatterns = [ 
    # {% url "api:sign_up" %}
    url(
        regex=r"^auth/sign_up/$",
        view=users_views.CreateUserView.as_view(),
        name="sign_up_user"
    ),
    # {% url "api:log_in" %}
    url(
        regex=r"^auth/log_in/$",
        view=users_views.LoginView.as_view(),
        name="log_in_user"
    ),
    # {% url "api:log_in" %}
    url(
        regex=r"^auth/user/$",
        view=users_views.UserView.as_view(),
        name="user"
    ),
    url(
        regex=r"^perfiles/user/(?P<id>[-\w]+)/$",
        view=users_views.UserInfoView.as_view(),
        name="user"
    ),
    # {% url "api:rubros_organizacion" %}
    url(
        regex=r"^perfiles/rubros_organizacion/$",
        view=users_views.RubroOrganizacionCreateReadView.as_view(),
        name="get_post_rubro_organizacion"
    ),
    # {% url "api:rubros_organizacion" rubro_organizacion.id %}
    url(
        regex=r"^perfiles/rubros_organizacion/(?P<id>[-\w]+)/$",
        view=users_views.RubroOrganizacionReadUpdateDeleteView.as_view(),
        name="get_put_delete_rubro_organizacion"
    ),
    # {% url "api:perfil_organizacion" usuario.id %}
    url(
        regex=r"^perfiles/perfil_organizacion/$",
        view=users_views.OrgProfileCreateReadView.as_view(),
        name="get_post_perfil_organizacion"
    ),
    # {% url "api:perfil_organizacion" usuario.id %}
    url(
        regex=r"^perfiles/perfil_organizacion/(?P<usuario>[-\w]+)/$",
        view=users_views.OrgProfileReadUpdateDeleteView.as_view(),
        name="get_put_delete_perfil_organizacion"
    ),
    # {% url "api:perfil_empresa" usuario.id %}
    url(
        regex=r"^perfiles/perfil_empresa/(?P<usuario>[-\w]+)/$",
        view=users_views.EmpresaProfileReadUpdateDeleteView.as_view(),
        name="get_put_delete_perfil_empresa"
    ),
    # {% url "api:perfil_voluntario" usuario.id %}
    url(
        regex=r"^perfiles/perfil_voluntario/(?P<usuario>[-\w]+)/$",
        view=users_views.VoluntarioProfileReadUpdateDeleteView.as_view(),
        name="get_put_delete_perfil_voluntario"
    ),
    url(
        regex=r"^verify_email/$",
        view=users_views.VerifyMailView.as_view(),
        name="user"
    ),
    url(
      regex=r"^imgurToken/$",
      view=users_views.ImgurTokenView.as_view(),
      name="get_imgur_access_token"
    ),
    # {% url "api:device_id" %}
    url(
        regex=r"^perfiles/device_id/$",
        view=users_views.DeviceIDCreateReadView.as_view(),
        name="get_post_device_id"
    ),
    # {% url "api:device_id" device_id.player_id %}
    url(
        regex=r"^perfiles/device_id/(?P<player_id>[-\w]+)/$",
        view=users_views.DeviceIDReadUpdateDeleteView.as_view(),
        name="get_put_delete_device_id"
    ),
    #####
    # {% url "api:suscripciones"  %}
    url(
        regex=r"^user/suscripciones/$",
        view=users_views.SuscripcionCreateView.as_view(),
        name="get_put_delete_device_id"
    ),
    # {% url "api:suscripciones" id:(id de la suscripcion) %}
    url(
        regex=r"^user/suscripcion/(?P<id>[-\w]+)/$",
        view=users_views.SuscripcionDestroyView.as_view(),
        name="get_put_delete_device_id"
    ),
    # {% url "api:suscripciones" usuario:(usuario)  %}
    url(
        regex=r"^user/suscripciones/(?P<usuario>[-\w]+)/$",
        view=users_views.SuscripcionListUserView.as_view(),
        name="get_put_delete_device_id"
    ),
]