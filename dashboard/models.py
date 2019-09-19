from django.db import models

# Create your models here.
class Opcion(models.Model):
    texto = models.CharField(max_length=30)

class Pregunta(models.Model):
    TIPO_PREGUNTA_CHOICES = (("SINGLE", 'Single'), ("MULTIPLE", 'Multiple'))
    texto = models.CharField(max_length=270)
    tipo = models.CharField(max_length=12, choices=TIPO_PREGUNTA_CHOICES, default="SINGLE")
    opciones = models.ManyToManyField(Opcion, through='Pregunta_Opcion')

    def __str__(self):
        return self.texto

class Diploma(models.Model):
    id_diploma = models.CharField(max_length=500, primary_key=True)
    tipo_fuente = models.CharField(max_length=150)
    estilo_fuente = models.CharField(max_length=150)
    coordenada_x = models.BigIntegerField()
    coordenada_y = models.BigIntegerField()

class Pregunta_Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "dashboard_pregunta_opcion"
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    paterno = models.CharField(max_length=50)
    materno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    actividades = models.ManyToManyField('Actividad', through='Alumno_Actividad')

    def __str__(self):
        return self.nombre + ' ' + self.paterno + ' ' + self.materno + ' ' + self.telefono

class Grupo(models.Model):
    name = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    resumen_preguntas = models.ManyToManyField(Pregunta, through='Grupo_Pregunta')
    alumnos = models.ManyToManyField(Alumno, through='Grupo_Alumno')

    def __str__(self):
        return self.name
        
class Grupo_Alumno(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, null=True, blank=True)
    encuestado = models.BooleanField(default=False)
    calificacion_numero = models.DecimalField(max_digits=3, decimal_places=1)
    calificacion_letra = models.CharField(max_length=100)
    diploma_habilitado = models.BooleanField(default=False)

    class Meta:
        db_table = "dashboard_grupo_alumno"
    

class Grupo_Pregunta(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Opcion, on_delete=models.DO_NOTHING)
    cantidad = models.BigIntegerField()

    class Meta:
        db_table = "dashboard_grupo_pregunta"
    

class Sesion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class Actividad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)

class Alumno_Actividad(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_entrega = models.DateField()
    hora_entrega = models.TimeField()

    class Meta:
        db_table = "dashboard_alumno_actividad"
