from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .week_number import WeekNumber
from .contato import Contato

# get("http://localhost:8027/contatos/api/?format=json", function(data){
#     console.log(data);
# });
#
# var get = function(url, callback){
#     var xhr = new XMLHttpRequest();
#     xhr.onreadstatechange = function() {
#         if (xhr.readstate ===4){
#             callback(xhr.reponseText, xhr.status);
#         }
#     };
#     xhr.open('GET', url);
#     xhr.send(null);
# };


class ContatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contato
        fields = ('id', 'nome', 'telefone', 'data')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class WeekNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeekNumber
        fields = ('id', 'num_week', 'date_closed')