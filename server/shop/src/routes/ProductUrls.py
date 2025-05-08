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


class DetailsAddSchema(Schema):
    productId: int
    locale: str
    descriptionTitle: str
    descriptionText: str
    benefits: list[dict]
    specifications: list[dict]
    functionalities: list[dict]


class ProductUpdateSchema(Schema):
    id: int
    categoryId: int
    name: str
    type: int
    status: int
    price: int
    discountOrder: int
    discountPercentage: int


class ProductDetailsUpdateSchema(Schema):
    id: int
    descriptionTitle: str
    descriptionText: str
    benefits: list[dict]
    specifications: list[dict]
    functionalities: list[dict]


###########################################################################
# ADD
###########################################################################


@router.post("/add", auth=JWTAuth())
def add_product(
    request,
    categoryId: int = Form(...),
    name: str = Form(...),
    type: int = Form(...),
    status: int = Form(...),
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
            "type": type,
            "status": status,
            "price": price,
            "discountOrder": discountOrder,
            "discountPercentage": discountPercentage,
            "image1": image1,
            "image2": image2,
            "image3": image3,
        },
    )


@router.post("/add/details", auth=JWTAuth())
def add_details(request, data: DetailsAddSchema) -> Details | HttpError:
    return ProductControl.add_product_details(request, data)


###########################################################################
# GET
###########################################################################


@router.get("/get/{id}/{locale}", auth=JWTAuth())
def get_by_id_and_locale(request, id: int, locale: str) -> Product | HttpError:
    return ProductControl.get_by_id_and_locale(id, locale)


@router.get("/get-all")
def get_all(request) -> list[Product] | HttpError:
    return ProductControl.get_all()


@router.get("/get-all/{locale}", auth=JWTAuth())
def get_all_by_locale(request, locale: str) -> list[Product] | HttpError:
    return ProductControl.get_all_by_locale(locale)


@router.get("/get-all-by-category/{category_id}/{locale}", auth=JWTAuth())
def get_all_by_category_and_locale(
    request, category_id: int, locale: str
) -> list[Product] | HttpError:
    return ProductControl.get_all_by_category_and_locale(category_id, locale)


# @router.get("details/{productId}/{locale}", auth=JWTAuth())
# def get_details(request, productId: int, locale: str) -> Details | HttpError:
#     return ProductControl.get_details(productId, locale)

# @router.get("/details/allByProduct/{productId}", auth=JWTAuth())
# def get_all_details_by_product(request, productId: int) -> list[Details] | HttpError:
#     return ProductControl.get_all_details_by_product(productId)

###########################################################################
# UPDATE
###########################################################################


@router.put("/update", auth=JWTAuth())
def update(request, data: ProductUpdateSchema) -> Product | HttpError:
    return ProductControl.update(request, data)


@router.patch("/update/image1", auth=JWTAuth())
def update_image1(
    request, productId: int, image: UploadedFile = File(...)
) -> bool | HttpError:
    return ProductControl.update_image1(
        request, {"productId": productId, "image": image}
    )


@router.patch("/update/image2", auth=JWTAuth())
def update_image2(
    request, productId: int, image: UploadedFile = File(...)
) -> bool | HttpError:
    return ProductControl.update_image2(
        request, {"productId": productId, "image": image}
    )


@router.patch("/update/image3", auth=JWTAuth())
def update_image3(
    request, productId: int, image: UploadedFile = File(...)
) -> bool | HttpError:
    return ProductControl.update_image3(
        request, {"productId": productId, "image": image}
    )


@router.put("/update/details", auth=JWTAuth())
def update_details(request, data: ProductDetailsUpdateSchema) -> Details | HttpError:
    return ProductControl.update_details(request, data)


###########################################################################
# DELETE
###########################################################################


@router.delete("/delete/{id}", auth=JWTAuth())
def delete_by_id(request, id: int) -> Product | HttpError:
    return ProductControl.delete_by_id(id)


@router.delete("/delete/details/{id}", auth=JWTAuth())
def delete_by_id_details(request, id: int) -> Details | HttpError:
    return ProductControl.delete_by_id_details(id)
