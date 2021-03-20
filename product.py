from stdnum import get_cc_module
import stdnum.exceptions
from sql import Null, Column, Literal
from sql.functions import CharLength, Substring, Position
from sql.operators import Equal

from trytond.i18n import gettext
from trytond.model import (ModelView, ModelSQL, MultiValueMixin, ValueMixin,
    DeactivableMixin, fields, Unique, sequence_ordered, Exclude)

from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pyson import Eval, Bool, Not
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond import backend
from trytond.tools.multivalue import migrate_property
from trytond.tools import lstrip_wildcard
# from .exceptions import (
#     Invalidlocation, EraseError)
from datetime import datetime, timedelta

from trytond.config import config

if config.getboolean('attachment', 'filestore', default=True):
    file_id = 'image_id'
    store_prefix = config.get('attachment', 'store_prefix', default=None)
else:
    file_id = None
    store_prefix = None


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    images = fields.One2Many('product.images', 'name', 'Galeria')


class ProductImages(sequence_ordered('sequence', 'Orden de Listado'),
                ModelView, ModelSQL):
    'Product Images'
    __name__ = 'product.images'

    name = fields.Many2One('product.product', 'Producto')
    image_name = fields.Function(fields.Char('File Name'), 'get_image_name')
    image_id = fields.Char('File ID', readonly=True, states={'invisible': True})
    image = fields.Binary('Imagen', filename='image_name',
        file_id=file_id, store_prefix=None)

    def get_img(self):
        foto = None
        if self.image_id:
            return '/static/img_db/' + self.image_id[:2] + '/' + self.image_id[2:4] + '/' + self.image_id

        if self.image:
            import base64
            foto = base64.b64encode(self.image).decode()
            return "data:image/JPEG;base64,"+foto
        return None

    def get_image_name(self, name):
        file_name = ''
        if self.name.rec_name:
            file_name = self.name.rec_name + ".jpg"
        return file_name
