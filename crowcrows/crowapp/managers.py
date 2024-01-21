from django.contrib.auth import models


class UserManager(models.BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        if email is None:
            raise ValueError("Email is a required field.")
        if not password:
            raise ValueError("Can't create User without a password!")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.is_staff = True
        user.is_superuser = True
        user.role = user.ADMIN

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_staffuser(self, email, role=None, password=None, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """

        if email is None:
            raise ValueError("Email is a required field.")
        if not password:
            raise ValueError("Can't create User without a password!")
        if not role:
            raise ValueError("Staffuser must have a role.")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):

        if email is None:
            raise ValueError("Email is a required field.")

        if not password:
            raise ValueError("Can't create User without a password!")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class SubscriberManager(models.UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='SUBSCRIBED_READER')


class EditorManager(models.UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='EDITOR')


class AuthorManager(models.UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='AUTHOR')
