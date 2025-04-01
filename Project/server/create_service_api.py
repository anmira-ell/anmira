from celery.bin.upgrade import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.server.models import Server, Service
from apps.company.models import Company
from apps.api.serializers import ServiceSerializer
from apps.server.cloudflare import CloudflageClient
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

"""
API View Пошаговое создание сервера, получение и активация токена
"""


class ServerWizardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Валидация данных
            name = request.data.get('name', '').strip()
            if not name:
                raise ValidationError('Название сервера обязательно')

            # Получаем компанию пользователя
            company = request.user.company

            # Создаем туннель в Cloudflare
            cloudflare = CloudflageClient(company_id=str(company.id))
            tunnel_response = cloudflare.create_tunnel()

            if not tunnel_response.success:
                raise Exception(f"Cloudflare error: {tunnel_response.errors}")

            access_token = tunnel_response.result.credentials_file.secret

            # Создаем сервер с данными из Cloudflare
            server = Server.objects.create(
                company=company,
                name=name,
                description=request.data.get('description', ''),
                tunnel_id=tunnel_response.result.id,
                access_token=access_token,
                tunnel_name=tunnel_response.result.name
            )

            return Response({
                'server_id': str(server.id),
                'access_token': access_token
            }, status=201)

        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return Response({'error': str(e)}, status=500)


class CloudflareStatusAPI(APIView):
    def post(self, request):
        response_template = {
            "errors": [],
            "messages": [],
            "result": None,
            "success": False
        }

        # Валидация входных данных
        server_id = request.data.get('server_id')
        access_token = request.data.get('access_token')

        if not server_id or not access_token:
            response_template["errors"].append({
                "code": 400,
                "message": "Требуются server_id и access_token"
            })
            return Response(response_template, status=status.HTTP_400_BAD_REQUEST)

        try:
            server = Server.objects.get(id=server_id, access_token=access_token)
        except Server.DoesNotExist:
            response_template["errors"].append({
                "code": 404,
                "message": "Сервер не найден"
            })
            return Response(response_template, status=status.HTTP_404_NOT_FOUND)

        # Запрос к Cloudflare API
        try:
            url = f"https://api.cloudflare.com/client/v4/accounts/{settings.ACCOUNT_ID}/cfd_tunnel/{server.tunnel_id}"

            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {settings.CLOUDFLARE_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            response.raise_for_status()

            cf_data = response.json()
            print(f"{response=}")
            print(f"{cf_data=}")
            response_template.update({
                "success": cf_data["success"],
                "result": {
                    "status": cf_data["result"].get("status", "unknown")
                }
            })

            return Response(response_template)

        except requests.exceptions.HTTPError as e:
            logger.error(f"Cloudflare API Error: {e.response.text}")
            response_template["errors"].append({
                "code": 503,
                "message": "Ошибка подключения к Cloudflare"
            })
            return Response(response_template, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            response_template["errors"].append({
                "code": 500,
                "message": "Внутренняя ошибка сервера"
            })
            return Response(response_template, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceSetupAPI(APIView):
    permission_classes = [IsAuthenticated]

    # Шаг 4: Добавление сервисов
    def post(self, request, server_id):
        try:
            server = Server.objects.get(
                id=server_id,
                company=request.user.company
            )
        except Server.DoesNotExist:
            return Response(
                {'error': 'Сервер не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        protocols = request.data.get('protocols', [])
        created_services = []

        for protocol in protocols:
            # Определение порта по умолчанию
            default_port = 3389 if protocol == 'rdp' else 22

            # Создание сервиса
            service, created = Service.objects.get_or_create(
                server=server,
                protocol=protocol,
                defaults={
                    'port': default_port,
                    'status': 'pending'
                }
            )

            if created:
                created_services.append(ServiceSerializer(service).data)

        return Response({
            'message': f'Создано {len(created_services)} сервисов',
            'services': created_services
        }, status=status.HTTP_201_CREATED)
