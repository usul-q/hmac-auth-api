from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterUserSerializer, PublicSerializer
from .models import CustomUser
import hmac, hashlib


@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = PublicSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(RegisterUserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def verify_signature(public_key, client_signature):
        try:
            user = CustomUser.objects.get(public_key=public_key)
        except CustomUser.DoesNotExist:
            return None
        
        private_key = user.private_key

        expected_signature = hmac.new(
            key=private_key.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(expected_signature, client_signature):
            return user
        return None

@api_view(['GET'])
def get_user(request, id):
    try:
        user = CustomUser.objects.get(pk=id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PublicSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def view_details(request):
    user = request.user

    if request.method == 'PUT':
        data = request.data.copy()
        data.pop('password', None)

        serializer = RegisterUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
def reveal_secret(request): 
    public_key = request.headers.get('Public-Key')
    signature = request.headers.get('Signature')

    if not public_key or not signature:
     return Response({'error': 'Missing header'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = verify_signature(public_key, signature)

    if not user:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'secret': user.secret}, status=status.HTTP_200_OK)

