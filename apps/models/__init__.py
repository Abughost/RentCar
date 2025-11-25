from apps.models import news
from apps.models.cars import (Car, CarBrand, CarCategory, CarFeature, CarImage,
                              CarPrice, Feature)
from apps.models.news import New
from apps.models.rentals import Rental
from apps.models.users import User, UserProfile

__all__ = ['User', 'Car', 'CarCategory',
           'New', 'Feature', 'CarBrand',
           'CarImage', 'CarPrice', "Rental",
           'CarFeature', 'UserProfile']
