from django.contrib import admin

# Register your models here.
from django.contrib import messages,admin
from .models import CustomUser,Location,SlotDetail,SlotBooking
# Register your models here.




# admin.site.index_template = 'admin/login.html'

# admin.site.register(Product)
# admin.site.register(ProductVariant)
admin.site.register(CustomUser)
admin.site.register(Location)
admin.site.register(SlotDetail)
admin.site.register(SlotBooking)

