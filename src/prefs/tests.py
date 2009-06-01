# -*- coding: utf-8 -*-

import unittest
from django.contrib.auth.models import User


class DataEspecialTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(username='tester')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()
        
    def testCalendarioDeDatasGeral(self):
        self.user.prefs.create(key='teste', value=datetime.date(2009,1,1))
        self.assertEquals(self.data_especial.datas.count(), 2)
        
        # Verificando se acha os dois intervalos com o inicio em um e o fim no outro
        calendario = {
            datetime.date(2009, 5, 7): set([self.intervalo_1]),
            datetime.date(2009, 5, 8): set([]),
            datetime.date(2009, 5, 9): set([self.intervalo_2]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,7), datetime.date(2009,5,9)), calendario)
        
        # Verificando se encontra o intervalo com o inicio fora dele e o fim dentro
        calendario = {
            datetime.date(2009, 5, 3): set([]),
            datetime.date(2009, 5, 4): set([self.intervalo_1]),
            datetime.date(2009, 5, 5): set([self.intervalo_1]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,3), datetime.date(2009,5,5)), calendario)
        
        # Verificando se encontra o intervalo com o inicio fora dele e o fim sendo o primeiro dia dele
        calendario = {
            datetime.date(2009, 5, 3): set([]),
            datetime.date(2009, 5, 4): set([self.intervalo_1]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,3), datetime.date(2009,5,4)), calendario)
        
        # Verificando se encontra um intervalo fora do intervalo especificado
        calendario = {
            datetime.date(2009, 5, 3): set([]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,3), datetime.date(2009,5,3)), calendario)
        
        # Verificando se encontra o intervalo caso o inicio e o fim sejam iguais ao primeiro dia do intervalo
        calendario = {
            datetime.date(2009, 5, 4): set([self.intervalo_1]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,4), datetime.date(2009,5,4)), calendario)
        
        # Verificando se encontra o intervalo caso o inicio e o fim sejam iguais ao último dia do intervalo
        calendario = {
            datetime.date(2009, 5, 7): set([self.intervalo_1]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,7), datetime.date(2009,5,7)), calendario)

        # Verificando se encontra o intervalo caso o inicio seja antes dele e o fim seja depois
        calendario = {
            datetime.date(2009, 5, 3): set([]),
            datetime.date(2009, 5, 4): set([self.intervalo_1]),
            datetime.date(2009, 5, 5): set([self.intervalo_1]),
            datetime.date(2009, 5, 6): set([self.intervalo_1]),
            datetime.date(2009, 5, 7): set([self.intervalo_1]),
            datetime.date(2009, 5, 8): set([]),
            datetime.date(2009, 5, 9): set([self.intervalo_2]),
            datetime.date(2009, 5, 10): set([self.intervalo_3]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,3), datetime.date(2009,5,10)), calendario)
        
        # Verificando se encontra o intervalo caso ele inicie antes do inicio e acabe depois do fim
        calendario = {
            datetime.date(2009, 5, 5): set([self.intervalo_1]),
            datetime.date(2009, 5, 6): set([self.intervalo_1]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,5), datetime.date(2009,5,6)), calendario)
        
        # Verificando se encontra o intervalo caso o inicio, e o fim sejam iguais ao único dia do intervalo.
        calendario = {
            datetime.date(2009,5,9): set([self.intervalo_2]),
        }
        self.assertEquals(calendar_for_queryset(IntervaloDeDatas.objects.all(), datetime.date(2009,5,9), datetime.date(2009,5,9)), calendario)
        
    def testCalendarioDeDatasColaborador(self):
        # Verificando se a data ligada diretamento ao colaborador aparece no calendario dele
        self.colaborador_1
        calendario = {
            datetime.date(2009,5,9): set([self.intervalo_2]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_com, datetime.date(2009,5,9), datetime.date(2009,5,9)), calendario)
        calendario = {
            datetime.date(2009,5,9): set([]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_cargo, datetime.date(2009,5,9), datetime.date(2009,5,9)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_departamento, datetime.date(2009,5,9), datetime.date(2009,5,9)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_sem, datetime.date(2009,5,9), datetime.date(2009,5,9)), calendario)
        
        # Verificando se a data ligada ao cargo do colaborador aparece no calendario dele
        calendario = {
            datetime.date(2009,5,10): set([self.intervalo_3]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_cargo, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)
        calendario = {
            datetime.date(2009,5,10): set([]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_com, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_departamento, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_sem, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)

        # Verificando se a data ligada ao departamento do colaborador aparece no calendario dele
        calendario = {
            datetime.date(2009,5,11): set([self.intervalo_4]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_departamento, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        
        calendario = {
            datetime.date(2009,5,11): set([]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_com, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_cargo, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_sem, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        
        # Verificando se a data marcada como de toda a equipe aparece no calendario dos colaboradores
        calendario = {
            datetime.date(2009,5,12): set([self.intervalo_5]),
        }
        self.assertEquals(calendar_for_colaborador(self.colaborador_com, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_cargo, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_departamento, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
        self.assertEquals(calendar_for_colaborador(self.colaborador_sem, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)

    
    def testCalendarioDeDatasCargo(self):
        # Verificando se a data ligada ao cargo aparece no calendario dele
        calendario = {
            datetime.date(2009,5,10): set([self.intervalo_3]),
        }
        self.assertEquals(calendar_for_cargo(self.cargo_com, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)
        
        calendario = {
            datetime.date(2009,5,10): set([]),
        }
        self.assertEquals(calendar_for_cargo(self.cargo_sem, datetime.date(2009,5,10), datetime.date(2009,5,10)), calendario)

        # Verificando se a data marcada como de toda a equipe aparece no calendario dos cargos
        calendario = {
            datetime.date(2009,5,12): set([self.intervalo_5]),
        }
        self.assertEquals(calendar_for_cargo(self.cargo_com, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
        self.assertEquals(calendar_for_cargo(self.cargo_sem, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
    
    def testCalendarioDeDatasDepartamento(self):
        # Verificando se a data ligada ao departamento aparece no calendario dele
        calendario = {
            datetime.date(2009,5,11): set([self.intervalo_4]),
        }
        self.assertEquals(calendar_for_departamento(self.departamento_com, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        
        calendario = {
            datetime.date(2009,5,11): set([]),
        }
        self.assertEquals(calendar_for_departamento(self.departamento_sem, datetime.date(2009,5,11), datetime.date(2009,5,11)), calendario)
        
        # Verificando se a data marcada como de toda a equipe aparece no calendario dos departamentos
        calendario = {
            datetime.date(2009,5,12): set([self.intervalo_5]),
        }
        self.assertEquals(calendar_for_departamento(self.departamento_com, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)
        self.assertEquals(calendar_for_departamento(self.departamento_sem, datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)

    def testCalendarioDeDatasTodaEquipe(self):
        calendario = {
            datetime.date(2009,5,12): set([self.intervalo_5]),
        }
        self.assertEquals(calendar_for_toda_equipe(datetime.date(2009,5,12), datetime.date(2009,5,12)), calendario)

    def testMoverIntervaloDeDatas(self):
        """
        Verifica se a função de mover intervalo de datas está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '05/05/2009', 'soltado': '10/10/2009', 'acao': 'M'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,9,12), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,9,9)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,10,9))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,10,12))
        
    def testMergeIntervaloDeDatas(self):
        """
        Verifica se a função de juntar intervalos de datas está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '07/05/2009', 'soltado': '08/05/2009', 'acao': 'M'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(del_pk)d, %(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,9), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,5)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk, 'del_pk': self.intervalo_2.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,5))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,9))
        self.assertEquals(novo_intervalo_1.data_especial.datas.count(), 1)
    
    def testAumentarMergeIntervaloDeDatas(self):
        """
        Verifica se a função de aumentar o intervalo de datas na direção do fim está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '05/05/2009', 'soltado': '10/10/2009', 'acao': 'A'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(del_pk)d, %(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,9,12), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,4)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk, 'del_pk': self.intervalo_2.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,10,12))
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_2.pk).count(), 0)
    
    def testDiminuirIntervaloDeDatas(self):
        """
        Verifica se a função de aumentar o intervalo de datas através de uma data
        do meio, sem atingir a região externa do intervalo está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '05/05/2009', 'soltado': '04/05/2009', 'acao': 'A'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,7), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,4)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,7))
    
    def testDiminuirMuitoIntervaloDeDatas(self):
        """
        Verifica se a função aumentar o intervalo de datas na direção do início 
        está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '05/05/2009', 'soltado': '01/05/2009', 'acao': 'A'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,7), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,3,30)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,4,30))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,7))
    
    def testCopiarIntervaloDeDatas(self):
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_2.pk, 'arrastado': '09/05/2009', 'soltado': '11/05/2009', 'acao': 'C'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,11), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,11)}]}""" % {'pk': self.intervalo_2.data_especial.datas.order_by('-pk')[0].pk, 'data_especial__pk': self.intervalo_2.data_especial.pk})
        novo_intervalo = IntervaloDeDatas.objects.filter(data_especial=self.intervalo_1.data_especial).order_by('-pk')[0]
        self.assertEquals(novo_intervalo.inicio, datetime.date(2009,5,11))
        self.assertEquals(novo_intervalo.fim, datetime.date(2009,5,11))
        
    def testCopiarMergeIntervaloDeDatas(self):
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_2.pk, 'arrastado': '09/05/2009', 'soltado': '10/05/2009', 'acao': 'C'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,10), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,9)}]}""" % {'pk': self.intervalo_2.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo = IntervaloDeDatas.objects.get(pk=self.intervalo_2.pk)
        self.assertEquals(novo_intervalo.inicio, datetime.date(2009,5,9))
        self.assertEquals(novo_intervalo.fim, datetime.date(2009,5,10))
    
    def testCopiarMergeMultIntervaloDeDatas(self):
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.arrastar_data'), {'intervalo': self.intervalo_1.pk, 'arrastado': '05/05/2009', 'soltado': '09/05/2009', 'acao': 'C'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Intervalo de datas alterado com sucesso."]}, "remover": [%(pk_del)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,11), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,4)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk, 'pk_del': self.intervalo_2.pk})
        novo_intervalo = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo.inicio, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo.fim, datetime.date(2009,5,11))
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_2.pk).count(), 0)
    
    def testExcluirData(self):
        """
        Verifica se a exclusão de uma data do meio do intervalo gera um novo
        intervalo.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_1.pk, 'data': '05/05/2009', 'acao': 'D'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,4), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,4)}, {"pk": %(pk2)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,7), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,6)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk, 'pk2': self.intervalo_1.data_especial.datas.order_by('-pk')[0].pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo_1.data_especial.datas.count(), 3)
        
    def testExcluirData2(self):
        """
        Verifica se a exclusão da data inicio do intervalo desloca o inicio em direção
        ao fim.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_1.pk, 'data': '04/05/2009', 'acao': 'D'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,7), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,5)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,5))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,7))
        self.assertEquals(novo_intervalo_1.data_especial.datas.count(), 2)
    
    def testExcluirData3(self):
        """
        Verifica se a exclusão da data fim do intervalo desloca o fim em direção
        ao inicio.
        """
        c = Client()
        c.login(username='renato', password='renato')
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_1.pk, 'data': '07/05/2009', 'acao': 'D'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": [{"pk": %(pk)d, "data_especial__pk": %(data_especial__pk)d, "fim": new Date(2009,4,6), "data_especial__descricao": "Carnaval", "inicio": new Date(2009,4,4)}]}""" % {'pk': self.intervalo_1.pk, 'data_especial__pk': self.intervalo_1.data_especial.pk})
        novo_intervalo_1 = IntervaloDeDatas.objects.get(pk=self.intervalo_1.pk)
        self.assertEquals(novo_intervalo_1.inicio, datetime.date(2009,5,4))
        self.assertEquals(novo_intervalo_1.fim, datetime.date(2009,5,6))
        self.assertEquals(novo_intervalo_1.data_especial.datas.count(), 2)
    
    def testExcluirData4(self):
        """
        Verifica se a exclusão da única data do intervalo exclui também o intervalo.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_2.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_2.pk, 'data': '09/05/2009', 'acao': 'D'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": []}""" % {'pk': self.intervalo_2.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_2.pk).count(), 0)
        self.assertEquals(data_especial.datas.count(), 1)

    
    def testExcluirData5(self):
        """
        Verifica se a exclusão da única data do único intervalo de uma data especial
        exclui também a data especial.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_3.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_3.pk, 'data': '10/05/2009', 'acao': 'D'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": []}""" % {'pk': self.intervalo_3.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_3.pk).count(), 0)
        self.assertEquals(DataEspecial.objects.filter(pk=data_especial.pk).count(), 0)

    
    def testExcluirData6(self):
        """
        Verifica se a exclusão de um intervalo está funcionando.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_1.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_1.pk, 'data': '05/05/2009', 'acao': 'I'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": []}""" % {'pk': self.intervalo_1.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_1.pk).count(), 0)
        self.assertEquals(data_especial.datas.count(), 1)

    
    def testExcluirData7(self):
        """
        Verifica se a exclusão do único intervalo de uma data especial exclui
        também a data especial.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_3.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_3.pk, 'data': '10/05/2009', 'acao': 'I'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": []}""" % {'pk': self.intervalo_3.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_3.pk).count(), 0)
        self.assertEquals(DataEspecial.objects.filter(pk=data_especial.pk).count(), 0)

    def testExcluirData8(self):
        """
        Verifica se a exclusão de uma data especial exclui também todos os seus
        intervalos.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_1.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_1.pk, 'data': '05/05/2009', 'acao': 'E'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d, %(pk2)d], "adicionar": []}""" % {'pk': self.intervalo_1.pk, 'pk2': self.intervalo_2.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_1.pk).count(), 0)
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_2.pk).count(), 0)
        self.assertEquals(DataEspecial.objects.filter(pk=data_especial.pk).count(), 0)

    def testExcluirData9(self):
        """
        Verifica se a exclusão de uma data especial com um único intervalo exclui
        ele.
        """
        c = Client()
        c.login(username='renato', password='renato')
        data_especial = self.intervalo_3.data_especial
        response = c.post(reverse('colaboradores.datas_especiais.views.excluir_data'), {'intervalo': self.intervalo_3.pk, 'data': '10/05/2009', 'acao': 'E'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, """{"flash_msgs": {"sucesso": ["Data exclu\\u00edda do intervalo com sucesso."]}, "remover": [%(pk)d], "adicionar": []}""" % {'pk': self.intervalo_3.pk})
        self.assertEquals(IntervaloDeDatas.objects.filter(pk=self.intervalo_3.pk).count(), 0)
        self.assertEquals(DataEspecial.objects.filter(pk=data_especial.pk).count(), 0)
