# ANCHE QUI PRIMA RIGA
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
from .azienda_serializer import Aziendaserializer
from .cantiere_serializer import Cantiereserializer
from .cliente_serializer import Clienteserializer
from .fatture_serializer  import Fattureserializer
from .fornitori_serializer import Fornitoriserializer
from .ordine_serializer import Ordineserializer
from .magazzino_serializer import Magazzinoserializer
from .ordineupdate_serializer import OrdineUpdateserializer
from .bancafornitore_serializer import BancaFornitoriserializer
#from .personale_serializer import Personaleserializer
#from .tipologialavori_serializer import TipologiaLavoriSerializer
#from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer

#from .lavorieffettuatifornitori_serializer import LavoriEffettuatiFornitoriserializer
#from .lavorieffettuatipersonale_serializer import LavoriEffettuatiPersonaleserializer
#from .tipologiapersonale_serializer import TipologiaPersonaleserializer
#from moneyed import Money
# Create your views here.
from home.models import *

import json
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema,extend_schema_serializer,OpenApiResponse, OpenApiExample,inline_serializer

 

class FornitoriList(APIView):
    queryset = Fornitori.objects.all()
    serializer_class = Fornitoriserializer
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
       
        fatture = Fornitori.objects.all()
        serializer = self.serializer_class(fatture,many=True)
        return Response(serializer.data)


class FornitoriDetail(APIView):
    queryset = Fornitori.objects.all()
    serializer_class = Fornitoriserializer
    
    @extend_schema(
        responses={
            200: serializer_class},
    )

    def get(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')

        object = Fornitori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        serializer.data['pollo']= object.codpag
        
        return Response(serializer.data)

class FornitoriBamche(APIView):
    queryset = Fornitori.objects.all()
    serializer_class = BancaFornitoriserializer
    
    @extend_schema(
        responses={
            200: serializer_class(many=True)},
    )

    def get(self, request, fornitore_id,*args, **kwargs):
        #pk = self.kwargs.get('pk')

        object = Fornitori.objects.get(pk=fornitore_id) #kwargs['pk'])
        bf = object.fornitori_banca.all()
        serializer = self.serializer_class(bf,many=True)
        #serializer.data['pollo']= object.codpag
        
        return Response(serializer.data)


"""

class PersonaleList(generics.ListCreateAPIView):
    queryset = Personale.objects.all()
    serializer_class = Personaleserializer


class PersonaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personale.objects.all()
    serializer_class = Personaleserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Personale.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Personale.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)


class GroupMagazzino(APIView):
    def get(self,request):
        articolimag = Magazzino.objects.values('descrizione').annotate(totale=Sum('importo_totale'),quantita=Sum('quantita'))
        res=[]
        for one in articolimag:
            a={}
            a['descrizione']=one['descrizione']
            a['importo_totale'] = one['totale']
            a['quantita'] = one['quantita']
            res.append(a)

        return Response(res  )

class MagazzinoList(generics.ListCreateAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer

class MagazzinoDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer
     
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk).delete() #kwargs['pk'])
        #object.magazzino = False
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' Non piu in magazzino'})

    
class MagazzinoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer
     
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk).delete() #kwargs['pk'])
        #object.magazzino = False
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' Non piu in magazzino'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
        

class MagazzinoArticoli(APIView):
    
    #queryset = Magazzino.objects.all()
    serializer_class = Articoliserializer
    #model = Magazzino
    
    def get(self,request):
        queryset = Magazzino.objects.all()
        tret=[]
        for one in queryset:
            a = one.articolo
            ret = self.serializer_class(a)
            
            o = a.ordine
            os = Ordineserializer(o)
            ret.data['ordine']= os.data

            tret.append(ret)


        
        #ret = self.serializer_class(tret,many=True)
        #ret.data[0]['ordine']= os.data
        return Response(tret)

"""
    
