from apps.models import news
from apps.models.cars import (Car, CarBrand, CarCategory, CarFeature, CarImage,
                              CarPrice, Feature)
from apps.models.rentals import Rental
from apps.models.users import User, UserProfile

__all__ = ['User','Car', 'CarCategory', 'Feature', 'CarBrand', 'CarImage', 'news', 'CarPrice', "Rental",'CarFeature','UserProfile']
