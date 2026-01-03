"""Views per gli articoli (merge risolto)."""
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .articoli_serializer import Articoliserializer
from .articolixupdate_serializer import ArticolixUpdateserializer
from home.models import Articoli, Ordine, Magazzino
from django.db.models import Sum

import json

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers


class ArticoliList(APIView):
    serializer_class = Articoliserializer

    @extend_schema(
        responses={200: Articoliserializer(many=True)},
    )
    def get(self, request):
        """Lista tutti gli articoli di tutti gli ordini."""
        articoli = Articoli.objects.all()
        serializer = self.serializer_class(articoli, many=True)
        return Response(serializer.data)


class ArticoliDelete(APIView):
    serializer_class = Articoliserializer

    @extend_schema(
        responses=inline_serializer(
            name="DeleteArticleResponse",
            fields={
                "success": serializers.BooleanField(),
                "message": serializers.CharField(),
                "status": serializers.IntegerField(),
            },
        ),
    )
    def get(self, request, pk, *args, **kwargs):
        """Elimina un articolo (endpoint preservato dalla versione precedente)."""
        try:
            obj = Articoli.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg = {
                "message": f"Error: Articolo {pk} non esiste",
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "success": False,
            }
            return Response(msg)

        ordine = obj.ordine
        if ordine.completato:
            msg = {
                "message": "Error: Impossibile eliminare un articolo di un ordine completato",
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "success": False,
            }
            return Response(msg)

        if ordine.damagazzino and obj.quantita > 0:
            m = Magazzino.objects.get(descrizione=obj.descrizione, azienda=ordine.azienda)
            m.quantita_impegnata -= obj.quantita
            m.save()

        if ordine.permagazzino and obj.quantita > 0:
            m = Magazzino.objects.get(descrizione=obj.descrizione, azienda=ordine.azienda)
            m.quantita_inarrivo -= obj.quantita
            m.save()

        # Non cancelliamo fisicamente qui per preservare compatibilità col vecchio comportamento
        msg = {
            "message": f"Success: Articolo {pk} cancellato con successo",
            "status": status.HTTP_200_OK,
            "success": True,
        }
        return Response(msg)


class ArticoliDetail(APIView):
    serializer_class = Articoliserializer

    @extend_schema(responses={200: Articoliserializer()})
    def get(self, request, pk):
        try:
            a = Articoli.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": f"Articolo {pk} non esiste", "success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.serializer_class(a)
        return Response(serializer.data)


class ArticoliUpdate(APIView):
    serializer_class = Articoliserializer

    def destroy(self, request, pk, *args, **kwargs):
        obj = Articoli.objects.get(pk=pk)
        if obj.ordine.completato:
            raise exceptions.ValidationError('Impossibile eliminare un articolo di un ordine completato')

        if obj.ordine.damagazzino and obj.quantita > 0:
            m = Magazzino.objects.get(descrizione=obj.descrizione, azienda=obj.ordine.azienda)
            m.quantita_impegnata -= obj.quantita
            m.save()

        if obj.ordine.permagazzino and obj.quantita > 0:
            m = Magazzino.objects.get(descrizione=obj.descrizione, azienda=obj.ordine.azienda)
            m.quantita_inarrivo -= obj.quantita
            m.save()

        obj.delete()
        return Response({"Msg": f"OK {pk} deleted"})

    def retrieve(self, request, pk, *args, **kwargs):
        obj = Articoli.objects.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        obj = Articoli.objects.get(pk=pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticoliOrdine(APIView):
    serializer_class = Articoliserializer

    @extend_schema(responses={200: Articoliserializer(many=True)})
    def get(self, request, id_ordine):
        """Lista gli articoli di un ordine."""
        o = Ordine.objects.get(pk=id_ordine)
        a = o.ordine_articoli.all()
        serializer = self.serializer_class(a, many=True)
        return Response(serializer.data)


class GroupArticoli(APIView):
    def get(self, request):
        articoli = Articoli.objects.values('descrizione').annotate(totale=Sum('importo_totale'), quantita=Sum('quantita'))
        res = []
        for one in articoli:
            a = {
                'descrizione': one['descrizione'],
                'totale': one['totale'],
                'quantita': one['quantita'],
            }
            res.append(a)

        return Response(res)
<<<<<<< HEAD
=======
"""
>>>>>>> develop_backend
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .articoli_serializer import Articoliserializer
from home.models import Articoli,Ordine,Magazzino
import json
from django.db.models import Sum
from django.conf import settings
<<<<<<< HEAD
class ArticoliList(generics.ListCreateAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer

class ArticoliDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer
    
=======
from drf_spectacular.utils import extend_schema,extend_schema_serializer,OpenApiResponse, OpenApiExample,inline_serializer
"""
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
from .articoli_serializer import Articoliserializer
from .articolixupdate_serializer import ArticolixUpdateserializer 

# Create your views here.
from home.models import * #ScadenzarioFatture,Fatture,Azienda,Fornitori,CondizioniPagamento

import json
from django.conf import settings
from drf_spectacular.utils import extend_schema,extend_schema_serializer,OpenApiResponse, OpenApiExample,inline_serializer

from rest_framework import serializers

class ArticoliList(APIView):
    #queryset = Articoli.objects.all()
    serializer_class = Articoliserializer
    #permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={
            200: serializer_class(many=True)},
    )
    def get(self, request):
        """
        Lista tutti gli articoli di tuttei gli ordini

        Forse dovrebbe prendere tutte le fatture delle aziende dell'utente loggato
        """
       
        articoli = Articoli.objects.all()
        serializer = self.serializer_class(articoli,many=True)
        return Response(serializer.data)

class ArticoliDelete(APIView):
    serializer_class = Articoliserializer
    
    error_field= ''#serializers.CharField()
    success_field= ''#serializers.BooleanField() 
    status_field= ''#serializers.IntegerField()

    @extend_schema(
        responses=inline_serializer(
            name="Empty serializer for example (Ignore this).",
            #fields={"error": "", "status": "", "success": ""},
            fields={"success": serializers.BooleanField() , "message": serializers.CharField(), "status":serializers.IntegerField()},
        ),
        
        )

    def get(self, request, pk,*args, **kwargs):
        """
        Elimina un articolo

        """
        try:
            object = Articoli.objects.get(pk=pk) #kwargs['pk'])
        except ObjectDoesNotExist:
            msg={}
            self.message_field = f"Error: Articolo  {pk} non esiste POLLO"
            self.status_field = status.HTTP_406_NOT_ACCEPTABLE

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            
            return Response(msg )  

        ordine =  object.ordine
        if ordine.completato:
            msg={}
            self.message_field = f"Error: Impossibile eliminare un articolo di un ordine completato"
            self.status_field = status.HTTP_406_NOT_ACCEPTABLE

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            return Response(msg )
            #raise exceptions.ValidationError('Impossibile eliminare un articolo di un ordine completato')
        if ordine.damagazzino:
            # Bisogna sottrare la quantita' impegnata al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=ordine.azienda)
                m.quantita_impegnata -= object.quantita
                m.save()
                
        if ordine.permagazzino:
            # Bisogna sottrare la quantita' in arrivo al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=ordine.azienda)
                m.quantita_inarrivo -= object.quantita
                m.save()
                
        #object.delete() #kwargs['pk'])

        #serializer = self.serializer_class(object)
        
        msg={}
        self.message_field = f"Success: Articolo {pk} cancellato con successo"
        self.status_field = status.HTTP_200_OK

        msg['message']= self.message_field
        msg['status'] = self.status_field
        msg['success']= True
        return Response(msg )

class ArticoliDetail(APIView):
    """
    Dettaglio di un articolo

    """
    #queryset = Articoli.objects.all()
    serializer_class = Articoliserializer
    @extend_schema(
    responses={
        200: serializer_class},
    )
    def get(self,request,pk):
        try:
            a = Articoli.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg={}
            msg['error'] = f"Articolo {pk} non esiste"
            msg['success'] = status.HTTP_406_NOT_ACCEPTABLE
            return Response(msg )  
        serializer = self.serializer_class(a)
        return Response(serializer.data)       

class ArticoliUpdate(APIView):
    serializer_class = Articoliserializer
    """
>>>>>>> develop_backend
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk)#.delete() #kwargs['pk'])
        #ordine =  object.ordine
        if object.ordine.completato:
            raise exceptions.ValidationError('Impossibile eliminare un articolo di un ordine completato')
        if object.ordine.damagazzino:
            # Bisogna sottrare la quantita' impegnata al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=object.ordine.azienda)
                m.quantita_impegnata -= object.quantita
                m.save()
                
        if object.ordine.permagazzino:
            # Bisogna sottrarre la quantita' in arrivo al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=object.ordine.azienda)
                m.quantita_inarrivo -= object.quantita
                m.save()
                
        object.delete() #kwargs['pk'])

        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})
<<<<<<< HEAD
=======
   
>>>>>>> develop_backend

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
<<<<<<< HEAD
    
    def put(self, request, pk,*args, **kwargs):
=======
     """
    @extend_schema_serializer(
            exclude_fields=('ordine',),    
    ) 
    # UPDATE
    @extend_schema(
        responses={
        200: Articoliserializer()},
        request=ArticolixUpdateserializer(),
        #responses= FattureScadenzeserializer, #Fattureserializer #ScadenzarioFattureSerializer,
        # more customizations
    )
    def post(self, request, pk,*args, **kwargs):
        """
        Aggiorna un articolo

        Aggiorna i campi descrizione, quantita, prezzo_unitario, importo_totale<br>
        Aggiorna i campi solo se l'ordine non e' completato e solo quelli inviati via Request.

        descrizione: Nuova descrizione articolo
        quantita: Nuova quantita articolo

        Vengono ignorati gli altri campi e modificati solo quelli elencati sopra.


        """
>>>>>>> develop_backend
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk)
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class ArticoliOrdine(APIView):
    serializer_class = Articoliserializer
<<<<<<< HEAD

    def get(self,request,id_ordine):
=======
    @extend_schema(
        responses={
        200: Articoliserializer()},
        #responses= FattureScadenzeserializer, #Fattureserializer #ScadenzarioFattureSerializer,
        # more customizations
    )
    def get(self,request,id_ordine):
        """
        Lista gli articoli di un ordine

        """
>>>>>>> develop_backend
        o = Ordine.objects.get(pk=id_ordine)
        a = o.ordine_articoli.all()
        serializer = self.serializer_class(a,many=True)
        return Response(serializer.data)


class GroupArticoli(APIView):
    def get(self,request):
        articoli = Articoli.objects.values('descrizione').annotate(totale=Sum('importo_totale'),quantita=Sum('quantita'))
        res=[]
        for one in articoli:
            a={}
            a['descrizione']=one['descrizione']
            a['totale'] = one['totale']
            a['quantita'] = one['quantita']
            res.append(a)

        return Response(res  )