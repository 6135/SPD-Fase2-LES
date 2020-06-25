# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Administrador'


class Anfiteatro(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Anfiteatro'


class Arlivre(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArLivre'


class Atividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255)  # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(db_column='nrColaboradoresNecessario')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=64)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    professoruniversitarioutilizadorid = models.ForeignKey('Professoruniversitario', models.DO_NOTHING, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    datasubmissao = models.DateTimeField(db_column='dataSubmissao')  # Field name made lowercase.
    dataalteracao = models.DateTimeField(db_column='dataAlteracao')  # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada')  # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo')  # Field name made lowercase.
    diaabertoid = models.ForeignKey('Diaaberto', models.DO_NOTHING, db_column='diaAbertoID')  # Field name made lowercase.
    espacoid = models.ForeignKey('Espaco', models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    tema = models.ForeignKey('Tema', models.DO_NOTHING, db_column='Tema', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Atividade'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'


class Colaborador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colaborador'


class Colaboradorhorario(models.Model):
    colaboradorutilizadorid = models.OneToOneField(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey('Horario', models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ColaboradorHorario'
        unique_together = (('colaboradorutilizadorid', 'horarioid'),)


class Coordenador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='unidadeOrganicaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Coordenador'


class Curso(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=32)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    unidadeorganica = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='Unidadeorganica')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Curso'


class Departamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=32, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganicaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamento'


class Diaaberto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    enderecopaginaweb = models.CharField(db_column='EnderecoPaginaWeb', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    emaildiaaberto = models.CharField(db_column='EmailDiaAberto', max_length=255)  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    datadiaabertoinicio = models.DateTimeField(db_column='DataDiaAbertoInicio')  # Field name made lowercase.
    datadiaabertofim = models.DateTimeField(db_column='DataDiaAbertoFim')  # Field name made lowercase.
    datainscricaoatividadesinicio = models.DateTimeField(db_column='DataInscricaoAtividadesInicio')  # Field name made lowercase.
    datainscricaoatividadesfim = models.DateTimeField(db_column='DataInscricaoAtividadesFim')  # Field name made lowercase.
    datapropostasatividadesincio = models.DateTimeField(db_column='DataPropostasAtividadesIncio')  # Field name made lowercase.
    dataporpostaatividadesfim = models.DateTimeField(db_column='DataPorpostaAtividadesFim')  # Field name made lowercase.
    precoprofessores = models.FloatField(db_column='PrecoProfessores')  # Field name made lowercase.
    precoalunos = models.FloatField(db_column='PrecoAlunos')  # Field name made lowercase.
    administradorutilizadorid = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='AdministradorUtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DiaAberto'


class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=32)  # Field name made lowercase.
    campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='Campus')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Edificio'


class Envionotificacao(models.Model):
    notificacaoid = models.OneToOneField('Notificacao', models.DO_NOTHING, db_column='NotificacaoID', primary_key=True)  # Field name made lowercase.
    utilizadorid = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='UtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EnvioNotificacao'
        unique_together = (('notificacaoid', 'utilizadorid'),)


class Escola(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Escola'


class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edificio = models.ForeignKey(Edificio, models.DO_NOTHING, db_column='Edificio', blank=True, null=True)  # Field name made lowercase.
    andar = models.CharField(db_column='Andar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Espaco'


class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'


class Idioma(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    diaabertoid = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='DiaAbertoID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Idioma'


class Inscricao(models.Model):
    escola = models.ForeignKey(Escola, models.DO_NOTHING, db_column='escola')
    nalunos = models.IntegerField()
    ano = models.IntegerField()
    turma = models.CharField(max_length=255)
    areacientifica = models.CharField(max_length=255)
    participante = models.ForeignKey('Participante', models.DO_NOTHING, db_column='participante')
    diaaberto = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='diaaberto')

    class Meta:
        managed = False
        db_table = 'Inscricao'


class Inscricaosessao(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    sessao = models.ForeignKey('Sessao', models.DO_NOTHING, db_column='sessao')
    nparticipantes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Inscricaosessao'


class Inscricaotransporte(models.Model):
    transporte = models.ForeignKey('Transporte', models.DO_NOTHING, db_column='transporte')
    npassageiros = models.IntegerField()
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')

    class Meta:
        managed = False
        db_table = 'Inscricaotransporte'


class Inscricaprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    prato = models.ForeignKey('Prato', models.DO_NOTHING, db_column='prato')
    campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='campus')
    npessoas = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Inscricaprato'


class Materiais(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Materiais'


class Menu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='Campus')  # Field name made lowercase.
    diaaberto = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='diaAberto')  # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'


class Notificacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criadoem = models.CharField(db_column='CriadoEm', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notificacao'


class Participante(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Participante'


class Prato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nrpratosdisponiveis = models.IntegerField(db_column='NrPratosDisponiveis')  # Field name made lowercase.
    prato = models.CharField(db_column='Prato', max_length=255)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=32)  # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prato'


class Professoruniversitario(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='departamento')

    class Meta:
        managed = False
        db_table = 'ProfessorUniversitario'


class Recepcaonotificacao(models.Model):
    notificacaoid = models.OneToOneField(Notificacao, models.DO_NOTHING, db_column='NotificacaoID', primary_key=True)  # Field name made lowercase.
    utilizadorid = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='UtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RecepcaoNotificacao'
        unique_together = (('notificacaoid', 'utilizadorid'),)


class Responsavel(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    tel = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Responsavel'


class Sala(models.Model):
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sala'


class Sessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')  # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sessao'


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    estado = models.CharField(max_length=64)
    coordenadorutilizadorid = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    colaboradorutilizadorid = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=64)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Tarefa'


class Tarefaacompanhar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.DO_NOTHING, db_column='tarefaid', primary_key=True)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    dia = models.DateField()
    horario = models.TimeField()
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')

    class Meta:
        managed = False
        db_table = 'TarefaAcompanhar'


class Tarefaauxiliar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.DO_NOTHING, db_column='tarefaid', primary_key=True)
    sessaoid = models.ForeignKey(Sessao, models.DO_NOTHING, db_column='sessaoid')

    class Meta:
        managed = False
        db_table = 'TarefaAuxiliar'


class Tarefaoutra(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.DO_NOTHING, db_column='tarefaid', primary_key=True)
    descricao = models.TextField()
    dia = models.DateField()
    horario = models.TimeField()

    class Meta:
        managed = False
        db_table = 'TarefaOutra'


class Tema(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tema'


class Transporte(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    identificador = models.IntegerField(db_column='Identificador')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transporte'


class Transportehorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    origem = models.IntegerField(db_column='Origem')  # Field name made lowercase.
    chegada = models.IntegerField(db_column='Chegada')  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    transporteid = models.ForeignKey(Transporte, models.DO_NOTHING, db_column='TransporteID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransporteHorario'


class Transportepessoal(models.Model):
    transporteid = models.OneToOneField(Transporte, models.DO_NOTHING, db_column='TransporteID', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransportePessoal'


class Transporteuniversitario(models.Model):
    transporteid = models.OneToOneField(Transporte, models.DO_NOTHING, db_column='TransporteID', primary_key=True)  # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransporteUniversitario'


class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadeOrganica'


class Utilizador(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Utilizador'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
