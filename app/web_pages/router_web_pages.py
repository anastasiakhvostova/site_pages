from fastapi import APIRouter, Request, Form, HTTPException, status, Depends, Response
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app import catalog_data
from app.auth.auth_lib import AuthHandler, AuthLibrary
from app.auth import dependencies

import dao

import settings
from http import HTTPStatus
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix='/web',
    tags=['menu', 'landing'],
)

templates = Jinja2Templates(directory='app\\templates')


@router.post('/search')
@router.get('/menu')
async def get_menu(request: Request, dish_name: str = Form(None), user=Depends(dependencies.get_current_user_optional)):
    filtered_menu = []
    if dish_name:
        for dish in catalog_data.menu:
            if dish_name.lower() in dish['title'].lower():
                filtered_menu.append(dish)

    context = {
        'request': request,
        'title': f'Результати пошуку за {dish_name}' if dish_name else 'Наш каталог',
        'menu': filtered_menu if dish_name else catalog_data.menu,
        'username': 'ghshvghus',
        'is_admin': False,
        'user': user,
        'categories': catalog_data.Categories
    }

    return templates.TemplateResponse(
        'catalog.html',
        context=context,
    )


@router.get('/like')
async def about_like(request: Request,  user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Список побажань',
        'user': user,
    }

    return templates.TemplateResponse(
        'like.html',
        context=context,
    )


@router.get('/about-us')
async def about_us(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Доставка і оплата',
        'user': user,
    }

    return templates.TemplateResponse(
        'about_us.html',
        context=context,
    )


@router.get('/about-contact')
async def about_us(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Магазини і контакти',
        'user': user,
    }

    return templates.TemplateResponse(
        'about_contact.html',
        context=context,
    )


@router.get('/map')
async def map_drive(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Карта проїзду',
        'user': user,

    }

    return templates.TemplateResponse(
        'map.html',
        context=context,
    )


@router.get('/register')
@router.post('/register')
async def register(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Реєстрація',
        'user': user,
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )


@router.post('/register-final')
async def register_final(request: Request,
                         name: str = Form(),
                         login: EmailStr = Form(),
                         notes: str = Form(default=''),
                         password: str = Form()):
    is_login_already_used = await dao.get_user_by_login(login)
    if is_login_already_used:
        context = {
            'request': request,
            'title': 'Помилка користувача',
            'content': f'Користувач {login} уже існує',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    hashed_password = await AuthHandler.get_password_hash(password)
    user_data = await dao.create_user(
        name=name,
        login=login,
        password=hashed_password,
        notes=notes,
    )
    token = await AuthHandler.encode_token(user_data[0])
    context = {
        'request': request,
        'title': 'Про нас',
        'menu': catalog_data.menu,
        'user': user_data,
        'categories': catalog_data.Categories
    }
    template_response = templates.TemplateResponse(
        'catalog.html',
        context=context,
    )
    template_response.set_cookie(key='token', value=token, httponly=True)
    return template_response


@router.get('/login')
async def login(request: Request):
    context = {
        'request': request,
        'title': 'Ввійти',
    }
    return templates.TemplateResponse(
        'login.html',
        context=context,
    )


@router.post('/login-final')
async def login(request: Request, login: EmailStr = Form(), password: str = Form()):
    user = await AuthLibrary.authenticate_user(login=login, password=password)
    token = await AuthHandler.encode_token(user.id)

    context = {
        'request': request,
        'title': 'Наше меню',
        'menu': catalog_data.menu,
        'user': user,
        'categories': catalog_data.Categories
    }
    response = templates.TemplateResponse(
        'catalog.html',
        context=context,
    )

    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.post('/logout')
@router.get('/logout')
async def logout(request: Request, response: Response, user=Depends(dependencies.get_current_user_optional)):
    # response.delete_cookie('token')

    context = {
        'request': request,
        'title': 'Наше меню',
        'catalog': catalog_data.menu,
        'categories': catalog_data.Categories
    }
    result = templates.TemplateResponse(
        'catalog.html',
        context=context,
    )
    result.delete_cookie('token')
    return result


@router.get('/by_category/{category_name}')
async def by_category(category_name: str, request: Request, user=Depends(dependencies.get_current_user_optional)):
    menu = [menu for menu in catalog_data.menu if category_name in menu['categories']]

    context = {
        'request': request,
        'title': f'Наше меню - результати пошуку по категорії {category_name}',
        'menu': menu,
        'user': user,
        'categories': catalog_data.Categories
    }
    return templates.TemplateResponse(
        'catalog.html',
        context=context,
    )


@router.get('/add-like')
async def about_like(request: Request,  user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Список побажань',
        'user': user,
    }

    return templates.TemplateResponse(
        'add_to_like.html',
        context=context,
    )


@router.get('/message')
@router.post('/message')
async def message(request: Request, message:str=Form(None),  user=Depends(dependencies.get_current_user_optional)):
    if message:
        new_message = await dao.create_comment(
            comment=message,
        )
    # comments = await dao.get_comment_by_login(comment=message)
    comments = await dao.fetch_comment()
    context = {
        'request': request,
        'title': 'Написати відгук',
        'user': user,
        'data': comments
    }

    return templates.TemplateResponse(
        'message_to_all.html',
        context=context,
    )