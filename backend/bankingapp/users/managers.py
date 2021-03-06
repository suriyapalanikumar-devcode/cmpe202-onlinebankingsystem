from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, email, password,  **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)
        # if role=="ADMIN":
        #     is_admin = True
        #     is_superuser =True
        #     is_staff = True
        # else:
        #     is_admin = False
        #     is_superuser = False
        #     is_staff = False


        # user = self.model(email=email, is_admin=is_admin, is_superuser= is_superuser, 
        #                     is_staff=is_staff, **extra_fields)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', "ADMIN")
        extra_fields.setdefault('is_staff', 1)
        extra_fields.setdefault('is_admin', 1)
        extra_fields.setdefault('is_superuser', 1)

        if extra_fields.get('role') != 'ADMIN':
            raise ValueError('Superuser must have role of Global Admin')
        return self.create_user(email, password, **extra_fields)