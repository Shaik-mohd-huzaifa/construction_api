from django.core.exceptions import ValidationError


def update_inventory(order):
    if order.status == 'Completed':
        for item in order.items.all():
            material = item.material
            if material.stock < item.quantity:
                raise ValueError(f"Insufficient stock for material {material.name}")
            material.stock -= item.quantity
            material.save()



def validate_order(order):
    for item in order.items.all():
        if item.quantity <= 0:
            raise ValidationError(f"Invalid quantity for material {item.material.name}")
        if item.discount < 0 or item.discount > 100:
            raise ValidationError(f"Invalid discount for material {item.material.name}")
        if item.quantity > item.material.stock:
            raise ValidationError(f"Insufficient stock for material {item.material.name}")
