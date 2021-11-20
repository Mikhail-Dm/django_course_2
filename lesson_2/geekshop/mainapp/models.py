from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='категория'
        verbose_name_plural='категории'
        # ordering=('-id',)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='название')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='картинка')
    short_desc = models.CharField(max_length=255, blank=True, verbose_name='краткое описание')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество на складе')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def delete(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()