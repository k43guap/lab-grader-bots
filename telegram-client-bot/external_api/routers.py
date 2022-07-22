from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from core import bot
from core.models import AuthorizedStudent

router = APIRouter()


@router.post(
    "/authorize_student",
    status_code=HTTP_204_NO_CONTENT,
    operation_id="authorize_student",
)
async def authorize_student(
    request: Request,
    recipient_user_id: int,
    authorized_student: AuthorizedStudent,
) -> Response:
    await bot.send_message(recipient_user_id, 'Вас успешно авторизовал администратор!')

    auth_message = await bot.send_message(recipient_user_id, authorized_student.to_message())
    message_id = auth_message['message_id']
    try:
        await bot.unpin_all_chat_messages(recipient_user_id)
    except:  # noqa
        pass
    await bot.pin_chat_message(recipient_user_id, message_id)

    return Response(status_code=HTTP_204_NO_CONTENT)
