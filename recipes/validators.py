import pint
from django.core.exceptions import ValidationError
from pint.errors import UndefinedUnitError

validate_unit_of_measurement = ['pounds', 'lbs', 'oz', 'gram']

def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value.lower()]
    except UndefinedUnitError as e:
        raise ValidationError(f'{value} is not valid unit of measure')
    except:
        raise ValidationError(f"'{value}' is invalid. unknown error.")
