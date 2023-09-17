from pyrogram.client import Client
import os
class TelegramClient:
    def __init__(self) -> None:
        self._app = Client(name=os.getenv("name"), api_id=os.getenv("api_id"), api_hash=os.getenv("api_hash"))
    async def create_chat(self, title):
        async with self._app:
            my_user = await self._app.get_me()
            username = my_user.id
            my_name = my_user.username
            result =  await self._app.create_group(title, [username])
            link = await result.export_invite_link()
            return result.id, link, my_name
    async def add_to_group(self, id, user_ids):
            async with self._app:
                await self._app.add_chat_members(id, user_ids )
    async def remove_from_group(self, id, user_ids):
            async with self._app:
                chat = await self._app.get_chat(id)
                for user_id in user_ids:
                    await chat.ban_member(user_id)
    async def get_chat_usernames(self, id):
            async with self._app:
                users = []
                members =  self._app.get_chat_members(id)
                async for member in members :
                    users.append(member.user.username)
            return users
    async def delete_chat(self, id):
        async with self._app:
            my_user = await self._app.get_me()
            members =  self._app.get_chat_members(id)
            chat = await self._app.get_chat(id)
            async for member in members:
                if my_user.id!=member.user.id:
                    await chat.ban_member(member.user.id)
            await self._app.leave_chat(id, delete=True)