from aiogram.types import InlineQuery, InlineQueryResultCachedVoice
from loader import dp, db

@dp.inline_query()
async def inline_voice_search(inline_query: InlineQuery):
    # So'rov matnini olamiz
    title = inline_query.query
    # Ma'lumotlar bazasida ovozli xabarlarni izlash
    audiolar = await db.search_audios_title(title)

    # Izlash natijalarini tayyorlaymiz
    results = [
        InlineQueryResultCachedVoice(
            id=f"{audio[0]}",
            voice_file_id=audio[1],
            title=audio[2]
        ) for audio in audiolar[:10]  # faqatgina 10 ta natija
    ]
    # Inline so'rovnigina javob beramiz
    await inline_query.answer(results=results)
