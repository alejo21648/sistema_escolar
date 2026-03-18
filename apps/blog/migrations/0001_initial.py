from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_usuario_codigo_estudiante_usuario_codigo_hijo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250)),
                ('resumen', models.TextField(blank=True, max_length=500)),
                ('contenido', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('estado', models.CharField(
                    choices=[('BORRADOR', 'Borrador'), ('PUBLICADO', 'Publicado'), ('ARCHIVADO', 'Archivado')],
                    default='BORRADOR', max_length=20)),
                ('destacada', models.BooleanField(default=False)),
                ('creada_en', models.DateTimeField(auto_now_add=True)),
                ('actualizada', models.DateTimeField(auto_now=True)),
                ('autor', models.ForeignKey(
                    limit_choices_to={'rol__in': ['ADMINISTRADOR', 'PROFESOR']},
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='publicaciones',
                    to='usuarios.usuario')),
                ('categoria', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='publicaciones',
                    to='blog.categoria')),
            ],
            options={
                'verbose_name': 'Publicación',
                'verbose_name_plural': 'Publicaciones',
                'ordering': ['-creada_en'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=1000)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comentarios_blog',
                    to='usuarios.usuario')),
                ('publicacion', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comentarios',
                    to='blog.publicacion')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'ordering': ['creado_en'],
            },
        ),
    ]
