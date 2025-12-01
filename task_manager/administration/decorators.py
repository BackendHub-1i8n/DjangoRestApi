from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(allowed_roles):
    """
    Decorador genérico para restringir el acceso a una vista basado en el rol del usuario.
    Recibe una lista de roles permitidos (ej: ['admin', 'librarian']).
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            if not request.user.is_authenticated:
                messages.warning(request, "You must be logged in to access this page.")
                return redirect('auth_login')

            if request.user.role in allowed_roles:
                print(request.user.role)
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have the necessary permissions to access this section.")
                return redirect('administration:dashboard')

        return login_required(wrapper_func)

    return decorator



def admin_required(view_func):
    """Solo permite el acceso a usuarios con el rol 'admin'."""
    return role_required(['admin'])(view_func)


def librarian_or_admin_required(view_func):
    """Permite el acceso a usuarios con rol 'librarian' o 'admin'."""
    return role_required(['librarian', 'admin'])(view_func)