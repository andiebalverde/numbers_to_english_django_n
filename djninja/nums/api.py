from ninja import NinjaAPI
from nums.process_text import manage_number
from nums.models import NumToEnglishRequest, NumToEnglishResponse

api = NinjaAPI()

@api.get("/num_to_english")
def read_user_item(request, number: int):

    texted = manage_number(number)
    return texted

@api.post("/num_to_english")
def get_body(request, item: NumToEnglishRequest):
    texted = manage_number(item.number)
    return texted
