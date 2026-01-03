#AGGIUNTO RIGA
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from datetime import date
from .scadenzariofatture_serializer import ScadenzarioFattureSerializer
from .fatture_serializer import Fattureserializer
from .fornitori_serializer import Fornitoriserializer,CondizioniPagamentoserializer
<<<<<<< HEAD


# Create your views here.
from home.models import ScadenzarioFatture,Fatture,Azienda,Fornitori,CondizioniPagamento

import json
from django.conf import settings

=======
from .fatture_scadenze_serializer import *

from .simplemessage_serializer import SimpleMessageSerializer

# Create your views here.
from home.models import * #ScadenzarioFatture,Fatture,Azienda,Fornitori,CondizioniPagamento

import json
from django.conf import settings
from drf_spectacular.utils import extend_schema,extend_schema_serializer,OpenApiResponse, OpenApiExample,inline_serializer
>>>>>>> develop_backend

class FatturaCreate(APIView):
    fatture_serialize = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer
    fornitore_serializer = Fornitoriserializer
<<<<<<< HEAD
    def post(self,request):
        data = json.loads(request.body)
        del data['id']
=======

    @extend_schema(
        responses={
        200: FattureScadenzeserializer()},
        request=FattureScadenzeserializer(),
        #responses= FattureScadenzeserializer, #Fattureserializer #ScadenzarioFattureSerializer,
        # more customizations
    )

    def post(self,request):
        """
        FATTURA Create 

        Crea una fattura con tutte le sue scadenze inviate via request

        """
        data = json.loads(request.body)
        #del data['id']
>>>>>>> develop_backend

        if 'azienda' not in data.keys() :
            msg = 'Azienda non specificata'
            return Response(msg)
        if 'fornitore' not in data.keys() :
            msg = 'Fornitore non specificato'
            return Response(msg)
        


        
        azienda_id = data['azienda']
        azienda = Azienda.objects.get(pk=azienda_id)
        fornitore_id = data['fornitore']
        fornitore = Fornitori.objects.get(id=fornitore_id)
        #numerorate = fornitore.codpag.numrate
        #codpag = data['codpag']
        


        pagato = None
        if 'pagato'  in data.keys():
            pagato = data['pagato']
                
        if 'importo' in data.keys():
            importo = data['importo']
        else:
            importo = 0.0
        if 'data_fattura' in data.keys():
            data_fattura = data['data_fattura']
        else:
            data_fattura = None

        if 'n_fattura' in data.keys():
            n_fattura = data['n_fattura']
        else:
            n_fattura = None

        if 'data_scadenza' in data.keys():
            data_scadenza = data['data_scadenza']
        else:
            data_scadenza = None

        if 'codpag' in data.keys():
            codpag = data['codpag']
            condizionipag = CondizioniPagamento.objects.get(pk=codpag)
            numerorate = condizionipag.numrate
            tipologiapagamento = condizionipag.tipopag
        else:
            condizionipag = fornitore.codpag
            tipologiapagamento = fornitore.codpag.tipopag
            numerorate = fornitore.codpag.numrate

        


        fattura = Fatture(
        pagato=pagato,
        fornitore=fornitore,
        importo=importo,
        data_scadenza= data_scadenza,
        data_fattura=data_fattura,
        n_fattura=n_fattura,
        #tipologiapagamento = fornitore.codpag.tipopag,
        tipologiapagamento = tipologiapagamento,
        azienda=azienda,
        codpag= condizionipag)

        fattura.save()

        if 'scadenze' in data.keys():
            scadenze = data['scadenze']
            if len(scadenze) != numerorate:
                fattura.tipologiapagamento = 3000
                fattura.save()
            

            

            for scadenza in scadenze:
                if 'scadenza_rata' in scadenza.keys():
                    scadenza_rata = scadenza['scadenza_rata']
                else:
                    scadenza_rata = None
                if scadenza_rata == '':
                    scadenza_rata = None

                if 'importo_pagato' in scadenza.keys():
                    importo_pagato = scadenza['importo_pagato']
                else:
                    importo_pagato = 0.0

                if 'importo_rata' in scadenza.keys():
                    importo_rata = scadenza['importo_rata']
                else:
                    importo_rata = 0.0

                if 'data_pagamento' in scadenza.keys():
                    data_pagamento = scadenza['data_pagamento']
                else:
                    data_pagamento = ''
                if data_pagamento == '':
                    data_pagamento = None

                if 'status' in scadenza.keys():
                    status = scadenza['status']
                else:
                    status = False
                

                sf = ScadenzarioFatture.objects.create(
                    fattura=fattura,
                    scadenza_rata=scadenza_rata,
                    importo_pagato=importo_pagato,
                    data_pagamento=data_pagamento,
                    status=status,
                    importo_rata=importo_rata
                )
                sf.save()

        
        resp={}

        os = self.fatture_serialize(fattura)
        resp['fattura']=os.data
        f = self.fornitore_serializer(fornitore)
        resp['fornitore'] = f.data
        scadenze =[]
        for one in fattura.fatture_scadenzario.all():
            scadenze.append(self.scadenza_serializer(one).data)
        resp['scadenze'] = scadenze
        return Response(resp)


class FatturaUpdate(APIView):
<<<<<<< HEAD
=======

>>>>>>> develop_backend
    fatture_serialize = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer
    codpag_serializer = CondizioniPagamentoserializer
    fornitore_serializer = Fornitoriserializer

<<<<<<< HEAD
=======
    @extend_schema(
        responses={
            200: FattureScadenzeserializer},
    )
>>>>>>> develop_backend
    def get(self,request,pk):
        try:
            f = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response( f" Fattura {pk} non esiste ")        
        
        fornitore = Fornitori.objects.get(pk=f.fornitore.id)
        codpag = self.codpag_serializer(f.codpag)


        sf = f.fatture_scadenzario.all()
        fatture_serializer = self.fatture_serialize(f)
        #serializer.data['articoli'] =[]
        scadenze=[]
        #ars = Articoliserializer(ar,many=True)
        for one in sf:
            sfs = ScadenzarioFattureSerializer(one)
            scadenze.append(sfs.data)
        #serializer.data['articoli']=a
        resp = {}
        resp['fattura']=fatture_serializer.data
        resp['scadenze'] = scadenze
        resp['codpag'] = codpag.data
        return Response(resp)

<<<<<<< HEAD
    def post(self,request,pk):
=======
    @extend_schema(
        responses={
        200: FattureScadenzeserializer()},
        request=ScadenzarioFattureSerializer(many=True),
        #responses= FattureScadenzeserializer, #Fattureserializer #ScadenzarioFattureSerializer,
        # more customizations
    )
    def post(self,request,pk):
        """
        Fattura Update: <br>
        Cancella le scadenze esistenti e li sostituisce con quelle in Request


        Request:

        {'scadenze': [ {'scadenza_rata': '<data>',<br>
                      'importo_rata': nnn,<br>
                      'importo_pagato': nnnn,<br>
                      'data_pagamento': '<data>',<br>
                      'status': False},<br>
                      {.....},<br>
                      {.....}<br>
                    ]}<br>


        Fa un check sul numero delle rate della tipologia di pagamento.<br>
        Se il numrate =! da numero di scadenze inviate setta la tipologia di pagamento a 3000


        

        """
>>>>>>> develop_backend
        data = json.loads(request.body)

        
        try:
            fattura = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response( " Fattura non esiste ")

        
        azienda_id =fattura.azienda.id
        fornitore_id = fattura.fornitore.id

        sf = fattura.fatture_scadenzario.all()
        lensf_indb = len(sf)

       
        
        if 'scadenze' in data.keys():
            scadenze = data['scadenze']
            lenscadenze = len(scadenze)
            if lensf_indb != lenscadenze:
                tipopag = 3000
                fattura.tipologiapagamento = tipopag
                
            #else:
            #    fattura.tipologiapagamento = fattura.fornitore.codpag.tipopag
            fattura.save()

            for one in sf:
                one.delete()



            for scadenza in scadenze:
                if 'scadenza_rata' in scadenza.keys():
                    scadenza_rata = scadenza['scadenza_rata']
                else:
                    scadenza_rata = None
                if scadenza_rata == '':
                    scadenza_rata = None

                if 'importo_pagato' in scadenza.keys():
                    importo_pagato = scadenza['importo_pagato']
                else:
                    importo_pagato = 0.0

                if 'importo_rata' in scadenza.keys():
                    importo_rata = scadenza['importo_rata']
                else:
                    importo_rata = 0.0

                if 'data_pagamento' in scadenza.keys():
                    data_pagamento = scadenza['data_pagamento']
                else:
                    data_pagamento = ''
                if data_pagamento == '':
                    data_pagamento = None

                if 'status' in scadenza.keys():
                    status = scadenza['status']
                else:
                    status = False
                

                sf = ScadenzarioFatture.objects.create(
                    fattura=fattura,
                    scadenza_rata=scadenza_rata,
                    importo_pagato=importo_pagato,
                    data_pagamento=data_pagamento,
                    status=status,
                    importo_rata=importo_rata
                )
                sf.save()

        
        
        resp={}

        os = self.fatture_serialize(fattura)
        resp['fattura']=os.data
        f = self.fornitore_serializer(fattura.fornitore)
        resp['fornitore'] = f.data
        scadenze =[]
        for one in fattura.fatture_scadenzario.all():
            scadenze.append(self.scadenza_serializer(one).data)
        resp['scadenze'] = scadenze
        return Response(resp)

<<<<<<< HEAD


=======
class FattureList(APIView):
    #queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    #permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={
            200: serializer_class(many=True)},
    )
    def get(self, request):
        """
        Lista tutte le fatture di tutte le aziende

        Forse dovrebbe prendere tutte le fatture delle aziende dell'utente loggato
        """
       
        fatture = Fatture.objects.all()
        serializer = self.serializer_class(fatture,many=True)
        return Response(serializer.data)

class FatturaDelete(APIView):

    #serializer_class = Fattureserializer
    @extend_schema(
        responses={

            'error': 'message Fattura  non esiste',
            'success': 'messageFattura  cancellata con successo',
        }
    )
    

    def get(self, request, pk):
        """
        Fattura Delete: <br>
        Cancella la fattura specificata dal pk

        """
        try:
            fattura = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg={}
            msg['error'] = f"Fattura {pk} non esiste"
            msg['success'] = status.HTTP_406_NOT_ACCEPTABLE
            return Response(msg )      
        
        fattura.delete()
        msg={}
        msg['success'] = f"Fattura {pk} cancellata con successo"
        msg['success_code'] = status.HTTP_200_OK
        return Response(msg )

class FatturaDetail(APIView):
    serializer_class = Fattureserializer
    @extend_schema(
    responses={
        200: serializer_class},
    )
    def get(self,request,pk):
        try:
            f = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg={}
            msg['error'] = f"Fattura {pk} non esiste"
            msg['success'] = status.HTTP_406_NOT_ACCEPTABLE
            return Response(msg )  
        serializer = self.serializer_class(f)
        return Response(serializer.data)          

"""
>>>>>>> develop_backend
class FattureList(generics.ListCreateAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    #permission_classes = [IsAuthenticated]

    

class FattureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer

    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fatture.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        fattura = Fatture.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(fattura)
        scadenze =[]
        #for one in fattura.fatture_scadenzario.all():
        #    scadenze.append(self.scadenza_serializer(one).data)
        #serializer.data['scadenze'] = scadenze
        return Response(serializer.data)
<<<<<<< HEAD
 


  
class ScadenzarioFattureList(generics.ListCreateAPIView):
    queryset = ScadenzarioFatture.objects.filter(status=False) #
    serializer_class = ScadenzarioFattureSerializer
    serializer_sp = CondizioniPagamentoserializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
=======


""" 

  
class ScadenzarioFattureCreate(APIView):
    #queryset = ScadenzarioFatture.objects.filter(status=False) #
    serializer_class = ScadenzarioFattureSerializer
    #serializer_sp = CondizioniPagamentoserializer
    @extend_schema(
        responses={
            200: serializer_class,
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea una scadenza fattura Fornitre 
        """
        #queryset = self.filter_queryset(self.get_queryset())
        data = json.loads(request.body)
        fattura_id = data['fattura']
        fattura = Fatture.objects.get(pk=fattura_id)
        scadenza_rata = data['scadenza_rata']
        importo_rata = data['importo_rata']
        importo_pagato = data.get('importo_pagato',0.0)
        data_pagamento = data.get('data_pagamento',None)
        status_fattura = data.get('status',False)      
        sf = ScadenzarioFatture.objects.create(
            fattura=fattura,
            scadenza_rata=scadenza_rata,
            importo_rata=importo_rata,
            importo_pagato=importo_pagato,
            data_pagamento=data_pagamento,
            status=status_fattura
        )
        sf.save()
        serializer = self.serializer_class(sf)
        resp={}
        resp=serializer.data     
        return Response(resp)

  
class ScadenzarioFattureList(APIView):
    #queryset = ScadenzarioFatture.objects.filter(status=False) #
    serializer_class = ScadenzarioFattureSerializer
    serializer_sp = CondizioniPagamentoserializer
    @extend_schema(
        responses={
            200: serializer_class(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        Lista tutte le scadenze fatture di tutte le aziende non ancora pagate

        Forse dovrebbe prendere tutte le fatture delle aziende dell'utente loggato
        """
        queryset = ScadenzarioFatture.objects.filter(status=False)
>>>>>>> develop_backend
        resp=[]
        for one in queryset:
            ss ={}
            #codpag = one.fattura.fornitore.codpag
            codpag = CondizioniPagamento.objects.get(pk=one.fattura.codpag.id)
            serializer_sf = self.serializer_class(one)
            serializer_codpag = self.serializer_sp(codpag)
            serializer_sf.data['codpag'] = serializer_codpag.data
            ss = serializer_sf.data   
            ss['codpag'] = serializer_codpag.data        
            resp.append(ss)
<<<<<<< HEAD



        return Response(resp)


class ScadenzarioFattureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScadenzarioFatture.objects.all()
    serializer_class = ScadenzarioFattureSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = ScadenzarioFatture.objects.get(pk=pk).delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
=======
        return Response(resp)


class ScadenzarioFattureDelete(APIView):
    #queryset = ScadenzarioFatture.objects.all()
    serializer_class = ScadenzarioFattureSerializer
    #messaggiosuccess={}
    #messaggioerrore={}
    """
    messaggiosuccess['success'] = f"Fattura  cancellata con successo"
    messaggiosuccess['status_code'] = status.HTTP_200_OK
    messaggioerrore['error'] = f"Scadenza Fattura non esiste"
    messaggioerrore['status_code'] = status.HTTP_406_NOT_ACCEPTABLE
    """
    error_field=serializers.CharField()
    success_field=serializers.BooleanField() 
    status_field=serializers.IntegerField()

    @extend_schema(
        responses=inline_serializer(
            name="Empty serializer for example (Ignore this).",
            #fields={"error": serializers.CharField(), "status": serializers.IntegerField()},
            fields={"success": success_field, "message": error_field, "status": status_field},
        ),
        
        )
    def get(self, request, pk,*args, **kwargs):
        """
        Cancella la scadenza fattura specificata dal id

        
        """
        #pk = self.kwargs.get('pk')
        #object = ScadenzarioFatture.objects.get(pk=pk).delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        #return Response({'Msg':'OK '+str(pk) +' deleted'})

        try:
            object = ScadenzarioFatture.objects.get(pk=pk)

        except ObjectDoesNotExist:
            msg={}
            self.message_field = f"Error: Scadenza Fattura {pk} non esiste"
            self.status_field = status.HTTP_406_NOT_ACCEPTABLE

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            #serialize = SimpleMessageSerializer(msg)
            return Response( msg )    

        object.delete()
        msg={}
        self.message_field = f"Success: Scadenza Fattura {pk} cancellata con successo"
        self.status_field = status.HTTP_200_OK

        msg['message']= self.message_field
        msg['status'] = self.status_field
        msg['success']= True
        #serialize = SimpleMessageSerializer(msg)
        return Response(msg )



class ScadenzaFatturaUpdate(APIView):
    @extend_schema(
        request=inline_serializer(
            name="Update  serializer for example.",
            #fields={"error": serializers.CharField(), "status": serializers.IntegerField()},
            fields={"importo_rata": serializers.FloatField(), 
                    "importo_pagato": serializers.FloatField(), 
                    "scadenza_rata": serializers.DateField(),
                    "data_pagamento": serializers.DateField(),
                    "status": serializers.BooleanField()},
        ),
        responses={
            200: ScadenzarioFattureSerializer,
        }
        
        )
    def post(self, request, pk):
        """
        Update  Scadenza Fattura Fornitore: <br>
        
        Nella request inviare solo i campi che si vogliono aggiornare 
        
        e/o settare Null a quelli che non si vogliono modificare

        Ex:<br>
        importo_rata = 345.23 <br>
        importo_pagato = Null <br>

        importo_rata viene aggiornato a 345.23 <br>
        importo_pagato non viene modificato <br>

        Anche tutti gli altri non vengono modificati

        """
        try:
            scadenza = ScadenzarioFatture.objects.get(pk=pk,status=False)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("ScadenzarioFatture not found.")
        #scadenza.pagato = True
        #scadenza.save()
        importo_rata = request.data.get('importo_rata', None)
        importo_pagato = request.data.get('importo_pagato', None)
        scadenza_rata = request.data.get('scadenza_rata', None)
        data_pagamento = request.data.get('data_pagamento', None)
        status_fattura = request.data.get('status', None)

        if importo_rata is not None:
            scadenza.importo_rata = importo_rata
        if scadenza_rata is not None:
            scadenza.scadenza_rata = scadenza_rata
        if data_pagamento is not None:
            scadenza.data_pagamento = data_pagamento
        if status_fattura is not None:
            scadenza.status = status_fattura
        if importo_pagato is not None:
            scadenza.importo_pagato = importo_pagato
        scadenza.save()
        serializer = ScadenzarioFattureSerializer(scadenza)
        return Response(serializer.data)
            
    """
    def get(self, request, scadenza_id):
        try:
            scadenza = ScadenzarioFatture.objects.get(pk=scadenza_id)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("ScadenzarioFatture not found.")
        
        today = date.today()
        #scadenza.data_pagamento = today
        serializer = ScadenzarioFattureSerializer(scadenza)
        
        return Response(serializer.data)
    """


class ScadenzarioFattureDetail(APIView):
    #queryset = ScadenzarioFatture.objects.all()
    serializer_class = ScadenzarioFattureSerializer
    
    @extend_schema(
        responses={
            200: serializer_class,
        })
    def get(self, request, pk,*args, **kwargs):
        """

        Recupera la scadenza fattura specificata dal id

        """
>>>>>>> develop_backend
        #pk = self.kwargs.get('pk')
        object = ScadenzarioFatture.objects.get(pk=pk) #kwargs['pk'])
        
        serializer = self.serializer_class(object)
        return Response(serializer.data)

<<<<<<< HEAD
class PagamentoScadenzaFatturaFornitori(APIView):
    def post(self, request, scadenza_id):
=======

class PagamentoScadenzaFatturaFornitori(APIView):
    @extend_schema(
        request=inline_serializer(
            name="Empty serializer for example.",
            #fields={"error": serializers.CharField(), "status": serializers.IntegerField()},
            fields={"importo_rata": serializers.FloatField(), 
                    "importo_pagato": serializers.FloatField(), 
                    "scadenza_rata": serializers.DateField()},
        ),
        responses={
            200: ScadenzarioFattureSerializer,
        }
        
        )
    def post(self, request, scadenza_id):
        """
        Pagamento Scadenza Fattura Fornitore: <br>
        Registra il pagamento della scadenza fattura specificata dal scadenza_id

        Se l'importo pagato e' uguale all'importo della rata la scadenza viene chiusa.

        Se l'importo pagato e' inferiore all'importo della rata viene creata 
        una nuova scadenza con l'importo residuo se non esiste gia' una scadenza successiva.
        Altrimenti la rata residua viene sommata alla prossima scadenza.

        """
>>>>>>> develop_backend
        try:
            scadenza = ScadenzarioFatture.objects.get(pk=scadenza_id,status=False)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("ScadenzarioFatture not found.")
        #scadenza.pagato = True
        #scadenza.save()
        importo_rata = request.data.get('importo_rata', None)
        importo_pagato = request.data.get('importo_pagato', None)
        scadenza_rata = request.data.get('scadenza_rata', None)

        if importo_pagato is not None and importo_pagato == importo_rata:
            scadenza.status = True
            scadenza.data_pagamento = date.today()
            scadenza.importo_pagato = importo_pagato
            scadenza.save()
            serializer = ScadenzarioFattureSerializer(scadenza)
            #return Response(serializer.data)

        else:
            nextsca = ScadenzarioFatture.objects.filter(scadenza_rata__gt = scadenza.scadenza_rata , fattura=scadenza.fattura).order_by('scadenza_rata')  
            if nextsca:
                nextsca[0].importo_rata = nextsca.importo_rata + (importo_rata - importo_pagato)
                nextsca[0].save()
                serializer = ScadenzarioFattureSerializer(nextsca[0])

            else:
                nsf = ScadenzarioFatture()
                nsf.impoto_pagato =  None
                nsf.importo_rata = importo_rata - importo_pagato
                nsf.scadenza_rata = scadenza_rata
                nsf.fattura = scadenza.fattura
                #nsf.data_pagamento = date.today()
                nsf.status = False
                nsf.save()
                serializer = ScadenzarioFattureSerializer(nsf)

            scadenza.status = True
            scadenza.data_pagamento = date.today()
            scadenza.importo_pagato = importo_pagato
            scadenza.save()
            serializer = ScadenzarioFattureSerializer(nsf)
        return Response(serializer.data)

<<<<<<< HEAD
=======
    """
>>>>>>> develop_backend
    def get(self, request, scadenza_id):
        try:
            scadenza = ScadenzarioFatture.objects.get(pk=scadenza_id)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("ScadenzarioFatture not found.")
        
        today = date.today()
        #scadenza.data_pagamento = today
        serializer = ScadenzarioFattureSerializer(scadenza)
        
        return Response(serializer.data)
<<<<<<< HEAD
=======
    """

>>>>>>> develop_backend
