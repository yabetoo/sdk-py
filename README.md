# Yabetoo Python SDK

SDK Python officiel pour l'intégration avec l'API de paiement Yabetoo. Cette bibliothèque fournit une interface simple pour traiter les paiements Mobile Money, créer des sessions de checkout, gérer les décaissements et les transferts d'argent en Afrique Centrale.

## Fonctionnalités

- **Paiements Mobile Money** - Acceptez les paiements via MTN Mobile Money et Airtel Money
- **Sessions de Checkout** - Créez des pages de paiement hébergées avec redirection
- **Décaissements** - Envoyez de l'argent vers des comptes Mobile Money
- **Transferts (Remittances)** - Gérez les transferts d'argent internationaux
- **Environnements Sandbox/Production** - Basculez automatiquement selon votre clé API
- **Gestion des erreurs** - Erreurs typées avec codes et messages détaillés
- **Retry automatique** - Retentatives configurables pour les requêtes échouées

## Installation

```bash
pip install yabetoo-py
```

## Prérequis

- Python 3.7+
- Clé API Yabetoo (obtenez-la sur [yabetoopay.com](https://yabetoopay.com))

## Démarrage rapide

```python
from yabetoo import Yabetoo
from models.payment import CreateIntentRequest, ConfirmIntentRequest, PaymentMethodData, MomoData

# Initialiser le SDK avec votre clé secrète
# Utilisez sk_test_xxx pour le sandbox, sk_live_xxx pour la production
yabetoo = Yabetoo("sk_test_your_secret_key")

# Créer une intention de paiement
intent = yabetoo.payments.create(CreateIntentRequest(
    amount=1000,
    currency="XAF",
    description="Achat produit",
    metadata={"order_id": "123"}
))

# Confirmer le paiement avec les informations Mobile Money
result = yabetoo.payments.confirm(intent.id, ConfirmIntentRequest(
    client_secret=intent.client_secret,
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"
        )
    )
))
```

## Documentation

### Initialisation

```python
from yabetoo import Yabetoo
from models.common import HttpClientOptions

yabetoo = Yabetoo(
    secret_key="sk_test_your_secret_key",
    options=HttpClientOptions(
        timeout=30,           # Timeout en secondes
        max_retries=3,        # Nombre de retentatives
        retry_delay=1,        # Délai entre retentatives
        verify_ssl=True,      # Vérification SSL
        custom_headers={}     # Headers personnalisés
    )
)
```

### Paiements

```python
from models.payment import CreateIntentRequest, ConfirmIntentRequest, PaymentMethodData, MomoData

# Créer une intention de paiement
intent = yabetoo.payments.create(CreateIntentRequest(
    amount=5000,
    currency="XAF",
    description="Achat en ligne"
))

# Confirmer le paiement
payment = yabetoo.payments.confirm(intent.id, ConfirmIntentRequest(
    client_secret=intent.client_secret,
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"  # ou "airtel"
        )
    )
))

# Récupérer un paiement
payment = yabetoo.payments.retrieve("pi_xxx")

# Lister les paiements avec pagination
payments = yabetoo.payments.get_page(page=1, per_page=10)
```

### Sessions de Checkout

```python
from models.checkout import CreateCheckoutSession, CheckoutItem

# Créer une session de checkout hébergée
session = yabetoo.sessions.create(CreateCheckoutSession(
    account_id="acc_xxx",
    total=10000,
    currency="XAF",
    success_url="https://votre-site.com/success",
    cancel_url="https://votre-site.com/cancel",
    items=[
        CheckoutItem(
            product_id="prod_123",
            product_name="T-shirt",
            quantity=2,
            price=5000
        )
    ]
))

# Redirigez l'utilisateur vers session.url
```

### Décaissements

```python
from models.disbursement import CreateDisbursementRequest
from models.payment import PaymentMethodData, MomoData

# Envoyer de l'argent vers un compte Mobile Money
disbursement = yabetoo.disbursements.create(CreateDisbursementRequest(
    amount=5000,
    currency="XAF",
    first_name="Jean",
    last_name="Dupont",
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"
        )
    )
))
```

### Transferts (Remittances)

```python
from models.remittance import CreateRemittanceRequest
from models.payment import PaymentMethodData, MomoData

# Créer un transfert d'argent
remittance = yabetoo.remittances.create(CreateRemittanceRequest(
    amount=5000,
    currency="XAF",
    first_name="Jean",
    last_name="Dupont",
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"
        )
    )
))
```

## Gestion des erreurs

```python
from errors import YabetooError

try:
    payment = yabetoo.payments.retrieve("invalid_id")
except YabetooError as e:
    print(f"Erreur: {e.message}")
    if e.code:
        print(f"Code erreur: {e.code}")
    if e.errors:
        print("Erreurs de validation:", e.errors)
```

## Pays et opérateurs supportés

| Pays | Code | Opérateurs |
|------|------|------------|
| Congo-Brazzaville | `cg` | MTN, Airtel |
| France | `fr` | - |

## Environnements

Le SDK détecte automatiquement l'environnement selon votre clé API :

- `sk_test_xxx` → Sandbox (`https://pay.sandbox.yabetoopay.com/v1`)
- `sk_live_xxx` → Production (`https://pay.api.yabetoopay.com/v1`)

## Développement

```bash
# Cloner le dépôt
git clone https://github.com/yabetoo/yabetoo-py.git
cd yabetoo-py

# Installer les dépendances de développement
pip install -e ".[dev]"

# Lancer les tests
pytest

# Vérifier le typage
mypy .

# Formater le code
black .
isort .
```

## Exemples

Consultez le dossier [examples/](examples/) pour des exemples complets :

- [payments_example.py](examples/payments_example.py) - Paiements Mobile Money
- [checkout_example.py](examples/checkout_example.py) - Sessions de checkout
- [disbursement_example.py](examples/disbursement_example.py) - Décaissements
- [remittance_example.py](examples/remittance_example.py) - Transferts
- [error_handling_example.py](examples/error_handling_example.py) - Gestion des erreurs

## Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Support

- Documentation : [docs.yabetoopay.com](https://docs.yabetoopay.com)
- Email : contact@yabetoopay.com
- GitHub Issues : [github.com/yabetoo/yabetoo-py/issues](https://github.com/yabetoo/yabetoo-py/issues)