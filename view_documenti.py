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
<<<<<<< HEAD

from .documenti_serializer import Documentiserializer
from home.models import Documenti,Cantiere,Azienda
import json
from django.db.models import Sum
from django.conf import settings
"""
class UploadDocumento(APIView):
    serializer_class = Documentiserializer

    def post(self,request,cantiere_id):
        file = request.FILES.get('file')
        tipologia_doc = request.POST.get('tipologia_documento',None)
        caricato_da = request.POST.get('caricato_da',None)
        
        #file = [request.FILES.get('file[%d]' % i)
        #for i in range(0, len(request.FILES))]  
        #files = request.POST.getlist('file')
        #if cantiere_id == None:
        ff=[]
        #for f in file:

        d = Documenti(cantiere_id=cantiere_id)
        d.save()
        d.media=file
        d.caricato_da = caricato_da
        d.tipologia_id= tipologia_doc

        d.save()
        #ff.append(d.media.name)

        serializer = self.serializer_class(d)

        #    for f in files:

        return Response(serializer.data)
"""
=======
from rest_framework import serializers

from drf_spectacular.utils import extend_schema,extend_schema_serializer,OpenApiResponse, OpenApiExample,inline_serializer


from .documenti_serializer import Documentiserializer
from .documenti_create_serializer import DocumentiCreateserializer
from home.models import Documenti,Cantiere,Azienda
import json,os
from django.db.models import Sum
from django.conf import settings

>>>>>>> develop_backend
class UploadDocumento(APIView):
    serializer_class = Documentiserializer

    def post(self,request,doc_id):
        file = request.FILES.get('file')
        #tipologia_doc = request.POST.get('tipologia_documento',None)
        caricato_da = request.POST.get('caricato_da',None)

        d = Documenti.objects.get(id=doc_id)
        #d = ModelWithFileField(file_field=request.FILES["file"])
        #instance.save()
        
        d.media=file
        d.caricato_da = caricato_da

        d.save()

        serializer = self.serializer_class(d)

        return Response(serializer.data)
    
<<<<<<< HEAD

class DocumentiCreate(APIView):
    serializer_class = Documentiserializer

    def post(self,request,cantiere_id):
        data = json.loads(request.body)
        #data['pollo']='POLLO'
        id = Cantiere.objects.get(pk=cantiere_id)
=======
@extend_schema(
    responses={
        200: Documentiserializer(many=True),
        400: inline_serializer(
            name='ErrorResponse',
            fields={
                'message': serializers.CharField(),
                'status': serializers.IntegerField(),
                'success': serializers.BooleanField(),
            }
        )
    },
    request=Documentiserializer(many=True)
)
class DocumentiCreate(APIView):
    serializer_class = Documentiserializer
    
    def post(self,request,cantiere_id):
        """
        Inserisci una serie di documenti per il cantiere

        Attualmente e':

        "documenti": [ {},{}]

        da Cambiare in :

        [ {},{} ]

        """
        data = json.loads(request.body)
        #data['pollo']='POLLO'
        id = Cantiere.objects.get(pk=cantiere_id)
        #for one in data:
        # da proporre questo
>>>>>>> develop_backend
        for one in data['documenti']:
            d = Documenti(tipologia_id=one['tipologia'],cantiere=id)

            d.save()
<<<<<<< HEAD
            one['data']=d.data_inserimento
=======
            if 'caricato_da' in one:
                d.caricato_da= one['caricato_da']
            if 'note' in one:    
                d.note = one['note']
            
            d.save()

            one['data']=d.data_inserimento

>>>>>>> develop_backend
            one['id'] = d.id
        serializer = self.serializer_class(Documenti.objects.filter(cantiere=id),many=True)
        
        return Response(serializer.data)


<<<<<<< HEAD
class DocumentiList(generics.ListCreateAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
=======

@extend_schema(
    responses={
        200: Documentiserializer(many=True),
        400: inline_serializer(
            name='ErrorResponse',
            fields={
                'message': serializers.CharField(),
                'status': serializers.IntegerField(),
                'success': serializers.BooleanField(),
            }
        )
    },
    request=Documentiserializer(many=True)
)
class DocumentiCreate2(APIView):
    serializer_class = Documentiserializer
    
    def post(self,request,cantiere_id):
        """
        Inserisci una serie di documenti per il cantiere
        Non gestisce l'upload del file.
        Usare api/docupload/<int:doc_id>
        
        Response:
        Ritorna tutti i documenti di quel cantiere anche quelli create in precedenza.

        QUESTA API DOVREBBE ESSERE USATA a=AL POSTO 

        /api/documenticreate/<cantiere_id>

        """
        data = json.loads(request.body)
        #data['pollo']='POLLO'
        id = Cantiere.objects.get(pk=cantiere_id)
        #for one in data:
        # da proporre questo
        for one in data:
            d = Documenti(tipologia_id=one['tipologia'],cantiere=id)

            d.save()
            if 'caricato_da' in one:
                d.caricato_da= one['caricato_da']
            if 'note' in one:    
                d.note = one['note']
            
            d.save()

            one['data']=d.data_inserimento

            one['id'] = d.id
        
        serializer = self.serializer_class(Documenti.objects.filter(cantiere=id),many=True)
        
        return Response(serializer.data)

"""

class DocumentiList(APIView):
    
    serializer_class = Documentiserializer
    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        #queryset = self.get_queryset()
        queryset = Documenti.objects.all()
>>>>>>> develop_backend
        serializer = self.serializer_class(queryset, many=True)
        for one in serializer.data:
            c=Cantiere.objects.get(pk=one['cantiere'])
            a=c.cliente.azienda
<<<<<<< HEAD
            one['aziendaSS']=a.id
        return Response(serializer.data)

class DocumentiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
=======
            one['azienda']=a.id
        return Response(serializer.data)

"""
class DocumentiUpdate(APIView):
    serializer_class = Documentiserializer

    @extend_schema(
        responses={
            200: Documentiserializer(),
            400: inline_serializer(
                name="DocumentiUpdate",
                fields={"success": serializers.BooleanField() , "message": serializers.CharField(), "status":serializers.IntegerField()},
            ),
            },
            #request=Personaleserializer(),
            
    )
    def post(self,request,doc_id):
        """
        Documenti Update: <br>

        """
        data = json.loads(request.body)

        
        try:
            doc = Documenti.objects.get(pk=doc_id)
        except ObjectDoesNotExist:
            msg={}
            self.message_field = f"Documento {doc_id} non esiste"
            self.status_field = status.HTTP_400_BAD_REQUEST

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            
            return Response(msg ,status.HTTP_400_BAD_REQUEST)
        
        
        if 'tipologia' in data:
            doc.tipologia_id=data['tipologia']
        if 'note' in data:    
            doc.note = data['note']
        if 'caricato_da' in data:
            doc.caricato_da= data['caricato_da']
        if 'cantiere' in data:
            try:
                c=Cantiere.objects.get(pk=data['cantiere'])
            except ObjectDoesNotExist:
                msg={}
                self.message_field = f"Cantiere specificato  {data['cantiere']} non esiste"
                self.status_field = status.HTTP_400_BAD_REQUEST

                msg['message']= self.message_field
                msg['status'] = self.status_field
                msg['success']= False
                
                return Response(msg ,status.HTTP_400_BAD_REQUEST)
        

            doc.cantiere=c


        doc.save()
        serializer = self.serializer_class(doc)
        return Response(serializer.data)

       
class DocumentiDetail(APIView):
    serializer_class = Documentiserializer

    @extend_schema(
        responses={
            200: Documentiserializer(),
            400: inline_serializer(
                name="DocumentiDetail",
                fields={"success": serializers.BooleanField() , "message": serializers.CharField(), "status":serializers.IntegerField()},
            ),
            },
            #request=Personaleserializer(),
            
    )
    def get(self,request,doc_id):
        
        try:
            doc = Documenti.objects.get(pk=doc_id)
        except ObjectDoesNotExist:
            msg={}
            self.message_field = f"Documento {doc_id} non esiste"
            self.status_field = status.HTTP_400_BAD_REQUEST

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            
            return Response(msg ,status.HTTP_400_BAD_REQUEST)

        
        serializer=self.serializer_class(doc)


        
        
        return Response(serializer.data,status.HTTP_200_OK)


        


@extend_schema(
    responses={
        200: Documentiserializer(),
        400: inline_serializer(
            name='ErrorResponse',
            fields={
                'message': serializers.CharField(),
                'status': serializers.IntegerField(),
                'success': serializers.BooleanField(),
            }
        )
    }
)
class DocumentiDelete(APIView):
    serializer_class = Documentiserializer
    
    def get(self, request, doc_id,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        try:
            object = Documenti.objects.get(pk=pk)
        except ObjectDoesNotExist:
            msg={}
            self.message_field = f"Documento {pk} non esiste"
            self.status_field = status.HTTP_400_BAD_REQUEST

            msg['message']= self.message_field
            msg['status'] = self.status_field
            msg['success']= False
            
            return Response(msg ,status.HTTP_400_BAD_REQUEST)
        
        #object = Documenti.objects.get(pk=pk)#.delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        if object.media:
            if os.path.exists(object.get_media_path):            
                #os.remove(object.get_media_path)
                objid = object.id
                object.delete()
                msg={}
                self.message_field = "Documento %s rimosso e file   %s  cancellato" % (objid,object.get_media_path)
                self.status_field = status.HTTP_200_OK

                msg['message']= self.message_field
                msg['status'] = self.status_field
                msg['success']= False
                return Response(msg,status.HTTP_200_OK)
            else:
                object.delete()
                msg={}
                self.message_field = "File  non trovato. Documento %s rimosso dal database" % (object.id)
                self.status_field = status.HTTP_200_OK

                msg['message']= self.message_field
                msg['status'] = self.status_field
                msg['success']= False
                return Response(msg,status.HTTP_200_OK)
        object.delete()
        msg={}
        self.message_field = "Nessun file  caricato. Documento %s rimosso dal database" % (object.id)
        self.status_field = status.HTTP_200_OK

        msg['message']= self.message_field
        msg['status'] = self.status_field
        msg['success']= False
        return Response(msg,status.HTTP_200_OK)

>>>>>>> develop_backend
class DocumentiCantiere(APIView):
    serializer_class = Documentiserializer

    def get(self,request,cantiere_id):
        c = Cantiere.objects.get(pk=cantiere_id)
        d=c.cantiere_documenti.all()
        
        serializer = self.serializer_class(d,many=True)
        return Response(serializer.data)


class DocumentiAzienda(APIView):
    serializer_class = Documentiserializer

    def get(self,request,azienda_id):
        a = Azienda.objects.get(pk=azienda_id)
        clienti = a.azienda_cliente.all()
        #serialzer = self.serializer_class(clienti,many=True)
        resp = []
        
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            for c in cantieri:
                d=c.cantiere_documenti.all()
                serializer = self.serializer_class(d,many=True)
                resp.append(serializer.data)

            
        return Response(resp)
        


