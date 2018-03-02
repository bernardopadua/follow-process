#REST FRAMEWORK Core
from rest_framework import status
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

#DJANGO Core
from django.contrib.auth.models import User

#INTERNAL Components
from followprocess.process.models import Process, UserProcess, RestrictProcess
from followprocess.process.api.views import ProcessApiView

#JWT Test Imports
payload = api_settings.JWT_PAYLOAD_HANDLER
encode  = api_settings.JWT_ENCODE_HANDLER

class ProcessTestCase(APITestCase):

    def setUp(self):
        user = User(username="test_case", email="test@case.com", is_staff=True)
        user.set_password("testcase")
        user.save()

        user2 = User(username="test_case2", email="test@case.com")
        user2.set_password("testcase")
        user2.save()

        pr = Process(numero_processo="a1", dados_processo="process data")
        pr.save()
        up = UserProcess(user=user, process=pr)
        up.save()

        pr = Process(numero_processo="a2", dados_processo="process data2")
        pr.save()
        up = UserProcess(user=user, process=pr)
        up.save()

        pr = Process(numero_processo="a3", dados_processo="process data3")
        pr.save()
        up = UserProcess(user=user2, process=pr)
        up.save()

        rp = RestrictProcess(numero_processo="a99")
        rp.save()

    def test_users(self):
        user = User.objects.count()
        self.assertEqual(user, 2)

    def test_processes(self):
        processes = Process.objects.count()
        self.assertEqual(processes, 3)

    def test_processes_user_one(self):
        user = User.objects.first()
        user_processes = UserProcess.objects.filter(user=user).count()
        self.assertEqual(user_processes, 2)

    def test_processes_user_two(self):
        user = User.objects.get(username="test_case2")
        user_processes = UserProcess.objects.filter(user=user).count()
        self.assertEqual(user_processes, 1)

    def test_list_process(self):
        data = {}
        url  = reverse("process-list")
        resp = self.client.get(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_nouser_post(self):
        """
            Trying to create a process with a non-authenticated user.
        """
        data = { 
            "numero_processo": "nn_1",
            "dados_processo": "First authenticate it!"
        }
        url  = reverse("process-list")
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_nouser_put(self):
        """
            Trying to update a process with a non-authenticated user.
        """
        data = { 
            "numero_processo": "a1",
            "dados_processo": "New content in the field"
        }
        pr   = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_nouser_delete(self):
        """
            Trying to delete a process with a non-authenticated user.
        """
        data = { 
            "numero_processo": "a1"
        }
        pr   = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        resp = self.client.delete(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_userauth_post(self):
        """
            Trying to create a process with a authenticated user.
        """
        data = { 
            "numero_processo": "nn_1",
            "dados_processo": "Creating Process with a authenticated user"
        }
        url  = reverse("process-list")
        self.client.login(username="test_case", password="testcase")
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_userauth_put(self):
        """
            Trying to update a process with a authenticated user.
        """
        data = { 
            "numero_processo": "a1",
            "dados_processo": "Updating process"
        }
        pr   = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        self.client.login(username="test_case", password="testcase")
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_userauth_delete(self):
        """
            Trying to delete a process with a authenticated user.
        """
        pr = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        self.client.login(username="test_case", password="testcase")
        resp = self.client.delete(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_userauth_post_restricted(self):
        """
            Trying to create a process with a authenticated user.
            And failing because the numero_processo is restricted.
        """
        data = { 
            "numero_processo": "a99",
            "dados_processo": "Trying create a restricted process"
        }
        url  = reverse("process-list")
        self.client.login(username="test_case", password="testcase")
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_isnt_attached_to_process(self):
        """
            Trying to update a process with a authenticated user.
            And failing because the user isn't attached to the process.
        """
        data = { 
            "numero_processo": "a3",
            "dados_processo": "Trying to put a process that belongs to another user."
        }
        pr   = Process.objects.get(numero_processo="a3")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        self.client.login(username="test_case", password="testcase")
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_attach_user_process_success(self):
        """
            Trying to attach himself (logged user) to the process.
            Success attaching a process to logged user.
        """
        pr   = Process.objects.get(numero_processo="a3")

        data = {
            "process": pr.pk
        }
        url = reverse_lazy("user_process")
        self.client.login(username="test_case", password="testcase")
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    
    def test_attach_user_process_error(self):
        """
            Trying to attach himself (logged user) to the process.
            Error attaching a process that is already attached.
        """
        pr   = Process.objects.get(numero_processo="a1")

        data = {
            "process": pr.pk
        }
        url = reverse_lazy("user_process")
        self.client.login(username="test_case", password="testcase")
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_process_attachment_success(self):
        """
            Trying to delte an attachment of UserProcess.
            Success on removing an attachment of User <> Process.

            User MUST be is_staff=True to remove an attachment.
        """
        pr  = Process.objects.get(numero_processo="a1")
        usu = User.objects.first()
        up  = UserProcess.objects.get(user=usu, process=pr)
        url = reverse_lazy("delete_user_process", kwargs={"pk": up.pk})
        self.client.login(username="test_case", password="testcase")
        resp = self.client.delete(url, {"process": pr.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_user_process_attachment_error(self):
        """
            Trying to delte an attachment of UserProcess.
            Error on removing an attachment of User <> Process.

            User is not is_staff=True so he can't remove the attachment.
        """
        pr  = Process.objects.get(numero_processo="a3")
        usu = User.objects.get(username="test_case2")
        up  = UserProcess.objects.get(user=usu, process=pr)
        url = reverse_lazy("delete_user_process", kwargs={"pk": up.pk})
        self.client.login(username="test_case2", password="testcase")
        resp = self.client.delete(url, {"process": pr.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_owned_userprocess_error(self):
        """
            Trying to delte an attachment of UserProcess.
            Error on removing an attachment of User <> Process.

            User is is_staff=True but he doesn't 'OWN' the Process.
        """
        pr  = Process.objects.get(numero_processo="a3")
        usu = User.objects.get(username="test_case2")
        up  = UserProcess.objects.get(user=usu, process=pr)
        url = reverse_lazy("delete_user_process", kwargs={"pk": up.pk})
        self.client.login(username="test_case1", password="testcase")
        resp = self.client.delete(url, {"process": pr.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_userauth_post(self):
        """
            Trying to create a process with a JWT.
        """
        data = { 
            "numero_processo": "nn_1",
            "dados_processo": "Creating Process with a authenticated user"
        }
        url  = reverse("process-list")
        
        usu = User.objects.get(username="test_case")
        payload_ = payload(usu)
        encode_token  = encode(payload_)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+encode_token)

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_jwt_userauth_put(self):
        """
            Trying to update a process with a JWT.
        """
        data = { 
            "numero_processo": "a1",
            "dados_processo": "Updating process"
        }
        pr   = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})
        
        usu = User.objects.get(username="test_case")
        payload_ = payload(usu)
        encode_token  = encode(payload_)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+encode_token)
        
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_jwt_userauth_delete(self):
        """
            Trying to delete a process with a JWT.
        """
        pr = Process.objects.get(numero_processo="a1")
        url  = reverse("process-detail", kwargs={"pk": pr.pk})

        usu = User.objects.get(username="test_case")
        payload_ = payload(usu)
        encode_token  = encode(payload_)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+encode_token)

        resp = self.client.delete(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_jwt_delete_not_owned_userprocess_error(self):
        """
            [JWT]
            
            Trying to delte an attachment of UserProcess.
            Error on removing an attachment of User <> Process.

            User is is_staff=True but he doesn't 'OWN' the Process.
        """
        pr  = Process.objects.get(numero_processo="a3")
        usu = User.objects.get(username="test_case2")
        up  = UserProcess.objects.get(user=usu, process=pr)
        url = reverse_lazy("delete_user_process", kwargs={"pk": up.pk})
        
        usu = User.objects.get(username="test_case")
        payload_ = payload(usu)
        encode_token  = encode(payload_)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+encode_token)

        resp = self.client.delete(url, {"process": pr.pk}, format="json")
        print(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)