from shop.src.data.models.Product import Product
from shop.src.data.models.ProductDetails import ProductDetails as Details
from shop.src.controllers.ProductControl import ProductControl
from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja import File, Form, UploadedFile
from ninja_jwt.authentication import JWTAuth

router = Router()


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"


class ProductUpdateSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    status: int
    categoryId: int


class ProductDetailsUpdateSchema(Schema):
    id: int
    productId: int
    locale: str
    name: str
    description_title: str
    description_text: str
    benefits: dict
    functionalities: dict
    specifications: dict


###########################################################################
# ADD
###########################################################################


@router.post("/add", auth=JWTAuth())
def add_product(
    request,
    categoryId: int = Form(...),
    name: str = Form(...),
    status: int = Form(...),
    basePrice: int = Form(...),
    price: int = Form(...),
    discountOrder: int = Form(...),
    discountPercentage: int = Form(...),
    image1: UploadedFile = File(...),
    image2: UploadedFile = File(...),
    image3: UploadedFile = File(...),
) -> Product | HttpError:
    return ProductControl.add_product(
        request,
        {
            "categoryId": categoryId,
            "name": name,
            "status": status,
            "basePrice": basePrice,
            "price": price,
            "discountOrder": discountOrder,
            "discountPercentage": discountPercentage,
            "image1": image1,
            "image2": image2,
            "image3": image3,
        },
    )


@router.post("/add/details", auth=JWTAuth())
def add_details(
    request,
    productId: int = Form(...),
    locale: str = Form(...),
    description_title: str = Form(...),
    description_text: str = Form(...),
    benefits: dict = Form(...),
    functionalities: dict = Form(...),
    specifications: dict = Form(...),
) -> Details | HttpError:
    return ProductControl.add_product_details(
        request,
        {
            "productId": productId,
            "locale": locale,
            "description_title": description_title,
            "description_text": description_text,
            "benefits": benefits,
            "functionalities": functionalities,
            "specifications": specifications,
        },
    )


###########################################################################
# GET
###########################################################################


@router.get("/get/{id}/{locale}", auth=JWTAuth())
def get_by_id_and_locale(request, id: int, locale: str) -> Product | HttpError:
    return ProductControl.get_by_id_and_locale(id, locale)


@router.get("/getAll/{locale}", auth=JWTAuth())
def get_all_by_locale(request, locale: str) -> list[Product] | HttpError:
    return ProductControl.get_all_by_locale(locale)


@router.get("/getAllByCategory/{categoryId}/{locale}", auth=JWTAuth())
def get_all_by_category_and_locale(
    request, categoryId: int, locale: str
) -> list[Product] | HttpError:
    return ProductControl.get_all_by_category_and_locale(categoryId, locale)


# @router.get("details/{productId}/{locale}", auth=JWTAuth())
# def get_details(request, productId: int, locale: str) -> Details | HttpError:
#     return ProductControl.get_details(productId, locale)

# @router.get("/details/allByProduct/{productId}", auth=JWTAuth())
# def get_all_details_by_product(request, productId: int) -> list[Details] | HttpError:
#     return ProductControl.get_all_details_by_product(productId)

###########################################################################
# UPDATE
###########################################################################

...

###########################################################################
# DELETE
###########################################################################

...
