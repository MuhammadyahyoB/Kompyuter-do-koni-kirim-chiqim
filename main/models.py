from django.db import models

from random import sample
import string

from django.core.files import File
from io import BytesIO
import qrcode


# >>>>>>>>>>>>>> Code generator <<<<<<<<<<<<<<<
class CodeGenerate(models.Model):
    """ Code generator Modeli """
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True

# >>>>>>>>>>>>>> Category Model <<<<<<<<<<<<
class Category(CodeGenerate):
    """ Category Model """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# >>>>>>>>>>>>>>>> Product Model <<<<<<<<<<<<<
class Product(CodeGenerate):
    """ Product Model """
    name = models.CharField(max_length=100 )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    count = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_code/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def total_entered(self):
        return Enter.objects.filter(product=self).count()
    
    @property
    def total_out(self):
        return Out.objects.filter(product=self).count()
    
    # ------- QrCode ------------------
    def save(self, *args, **kwargs):
        QRcode = qrcode.QRCode()
        QRcode.add_data(self.name)
        QRcode.make()
        QRimg= QRcode.make_image()
        fname = f'qr_code{self.name}.png'
        buffer = BytesIO()
        QRimg.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False) 
        QRimg.close()
        super().save(*args, **kwargs)


# >>>>>>>>>>>>>>>> Enter Model <<<<<<<<<<<<<
class Enter(models.Model):
    """ Enter model """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)


# >>>>>>>>>>>>>>>> Out Model <<<<<<<<<<<<<<<
class Out(models.Model):
    """ Out model """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    returned = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)


# >>>>>>>>>>>>>>>> Return Modeli <<<<<<<<<<<<<
class Return(models.Model):
    """ Return model """
    out = models.ForeignKey(Out, on_delete=models.CASCADE, related_name='returned_set')


    def __str__(self):
        return f'{self.out.product.name} - {self.out.quantity}'
    
    def save(self, *args, **kwargs):
        self.out.returned = True
        super(Return, self).save(*args, **kwargs)
    


