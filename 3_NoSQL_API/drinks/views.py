from rest_framework import status
from rest_framework.response import Response
from rest_framework. decorators import api_view
from drinks.db_controller import MongoController

@api_view(['GET', 'POST'])
def drinks(request, type):
    remote = MongoController()
    if request.method == 'GET':
        drink_detail = remote.get_by_type(type)
        return Response(drink_detail)
    elif request.method == 'POST':
        db_response = remote.insert_drink(type, request.data)
        if db_response == 1:
            return Response(status=status.HTTP_201_CREATED)
        else: 
            return Response(
                {'error': 'Failed to insert'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

@api_view(['GET', 'PUT', 'DELETE'])
def drink(request, type, id):
    remote = MongoController()
    if request.method == 'GET':
        drink_detail = remote.get_drink(type, id)
        if drink_detail is not 0:
            return Response(drink_detail)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        update_response = remote.update_drink(type, request.data)
        if update_response is not 0:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to update'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    if request.method == 'DELETE':
        remote.delete_drink(type, id)
        return Response(status=status.HTTP_200_OK)