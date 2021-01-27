import hashlib

from django.db.models.signals import post_save

from .iamport import payments_prepare, find_transaction
from django.db import models
from django.conf import settings
from products.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='orders')
    name = models.CharField(max_length=20, verbose_name='이름')
    email = models.EmailField(verbose_name='이메일')
    postal_code = models.CharField(max_length=20, verbose_name='우편번호')
    address = models.CharField(max_length=100, verbose_name='주소')
    detail_address = models.CharField(max_length=100, verbose_name='상세주소')
    extra_address = models.CharField(max_length=100, verbose_name='참고항목')
    phone_number = models.CharField(max_length=11, verbose_name='연락처')
    ordered_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = '주문'
        verbose_name_plural = '주문'

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_products')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_item_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.order} - {self.product}"

    class Meta:
        verbose_name = '주문_상세'
        verbose_name_plural = '주문_상세'


class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 정보 오류")

        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email_hash = str(order.email).split("@")[0]
        final_hash = hashlib.sha1((order_hash+email_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = str(final_hash)
        payments_prepare(merchant_order_id, amount)
        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None


class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']


def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        import_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)
        merchant_order_id = import_transaction['merchant_order_id']
        imp_id = import_transaction['imp_id']
        amount = import_transaction['amount']

        local_transaction = OrderTransaction.objects.filter(merchant_order_id=merchant_order_id, transaction_id=imp_id,
                                                            amount=amount).exists()
        if not import_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")


post_save.connect(order_payment_validation, sender=OrderTransaction) # OrderTransaction 모델 저장 후 함수 실행