from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Credential
from .security import analyze_password

class VaultSecurityTests(TestCase):
    def setUp(self):
        self.a=User.objects.create_user('alice',password='Alice-Secure-123!')
        self.b=User.objects.create_user('bob',password='Bob-Secure-123!')
        self.item=Credential(user=self.a,title='GitHub',username='alice'); self.item.set_password('Very_Strong_Example_2026!'); self.item.set_notes('private'); self.item.save()
    def test_secret_is_encrypted_at_rest(self):
        self.assertNotIn('Very_Strong_Example_2026!',self.item.password_encrypted)
        self.assertEqual(self.item.get_password(),'Very_Strong_Example_2026!')
    def test_cross_user_reveal_is_blocked(self):
        self.client.login(username='bob',password='Bob-Secure-123!')
        r=self.client.post(reverse('vault:reveal',args=[self.item.pk]))
        self.assertEqual(r.status_code,404)
    def test_reuse_fingerprint_is_deterministic(self):
        other=Credential(user=self.a,title='Test'); other.set_password('Very_Strong_Example_2026!'); other.save()
        self.assertEqual(self.item.password_fingerprint,other.password_fingerprint)
    def test_strength_engine(self):
        self.assertGreater(analyze_password('T9!long-and-complex-password')['score'], analyze_password('password')['score'])
