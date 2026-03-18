from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Contraseña'
        })
    )


class UsuarioForm(forms.ModelForm):
    """Formulario para CREAR un usuario nuevo (incluye contraseña)."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model  = Usuario
        fields = ['username', 'first_name', 'last_name', 'email',
                  'rol', 'telefono', 'fecha_nacimiento', 'foto', 'codigo_estudiante', 'codigo_hijo']
        widgets = {
            'username':        forms.TextInput(attrs={'class': 'form-control'}),
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'rol':             forms.Select(attrs={'class': 'form-select'}),
            'telefono':        forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto':            forms.FileInput(attrs={'class': 'form-control'}),
            'codigo_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_hijo':     forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        rol = cleaned.get('rol')
        if rol == Usuario.ROL_ESTUDIANTE:
            codigo = cleaned.get('codigo_estudiante')
            if not codigo:
                self.add_error('codigo_estudiante', 'El código de estudiante es requerido para estudiantes.')
            elif Usuario.objects.filter(codigo_estudiante=codigo).exclude(pk=self.instance.pk if self.instance else None).exists():
                self.add_error('codigo_estudiante', 'Este código de estudiante ya está en uso.')
        elif rol == Usuario.ROL_ACUDIENTE:
            codigo_hijo = cleaned.get('codigo_hijo')
            if codigo_hijo:
                if not Usuario.objects.filter(codigo_estudiante=codigo_hijo, rol=Usuario.ROL_ESTUDIANTE).exists():
                    self.add_error('codigo_hijo', 'El código del hijo no corresponde a ningún estudiante.')
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class RegistroEstudianteForm(forms.ModelForm):
    """Formulario de registro público para estudiantes."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model  = Usuario
        fields = ['username', 'first_name', 'last_name', 'email',
                  'telefono', 'fecha_nacimiento', 'foto', 'codigo_estudiante']
        widgets = {
            'username':        forms.TextInput(attrs={'class': 'form-control'}),
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono':        forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto':            forms.FileInput(attrs={'class': 'form-control'}),
            'codigo_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        codigo = cleaned.get('codigo_estudiante')
        if not codigo:
            self.add_error('codigo_estudiante', 'El código de estudiante es requerido.')
        elif Usuario.objects.filter(codigo_estudiante=codigo).exists():
            self.add_error('codigo_estudiante', 'Este código de estudiante ya está en uso.')
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.ROL_ESTUDIANTE
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UsuarioEditForm(forms.ModelForm):
    """Formulario para EDITAR usuario (sin cambiar contraseña)."""

    class Meta:
        model  = Usuario
        fields = ['first_name', 'last_name', 'email',
                  'rol', 'telefono', 'fecha_nacimiento', 'foto', 'codigo_estudiante', 'codigo_hijo']
        widgets = {
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'rol':             forms.Select(attrs={'class': 'form-select'}),
            'telefono':        forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto':            forms.FileInput(attrs={'class': 'form-control'}),
            'codigo_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_hijo':     forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        rol = cleaned.get('rol')
        codigo_estudiante = cleaned.get('codigo_estudiante')

        # Validar código de estudiante si se asigna ese rol
        if rol == Usuario.ROL_ESTUDIANTE and codigo_estudiante:
            if Usuario.objects.filter(codigo_estudiante=codigo_estudiante).exclude(pk=self.instance.pk).exists():
                self.add_error('codigo_estudiante', 'Este código de estudiante ya está en uso.')
        
        # Validar código del hijo si es acudiente
        if rol == Usuario.ROL_ACUDIENTE:
            codigo_hijo = cleaned.get('codigo_hijo')
            if codigo_hijo:
                if not Usuario.objects.filter(codigo_estudiante=codigo_hijo, rol=Usuario.ROL_ESTUDIANTE).exists():
                    self.add_error('codigo_hijo', 'El código del hijo no corresponde a ningún estudiante.')
        
        return cleaned
