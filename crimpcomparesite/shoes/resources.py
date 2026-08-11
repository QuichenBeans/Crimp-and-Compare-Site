from import_export import resources, fields
from import_export.widgets import DecimalWidget, CharWidget
from .models import AwinProduct

class AwinProductResource(resources.ModelResource):
    name = fields.Field(attribute='product_name', column_name='Product Name')
    price_amount = fields.Field(attribute='price', column_name='Price', widget=DecimalWidget())

    class Meta:
        model = AwinProduct
        fields = ('name', 'description', 'price_amount', 'sale_price', 
                  'currency', 'awin_product_url', 'merchant_name')
        import_id_fields = ('product_name', 'merchant_name')
        skip_unchanged = True
        report_skipped = False