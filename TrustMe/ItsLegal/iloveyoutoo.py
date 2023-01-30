import discord
from colorama import Fore, init, Style


def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[UYARI]{Style.RESET_ALL} {message}')


def print_error(message):
    print(f'{Fore.RED}[HATA]{Style.RESET_ALL} {message}')


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
            for role in guild_to.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print_delete(f"Silinen rol; {role.name}")
                except discord.Forbidden:
                    print_error(f"Rol silinirken bir hata oluştu; {role.name}")
                except discord.HTTPException:
                    print_error(f"Silinemeyen rol; {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Oluşturulan rol; {role.name}")
            except discord.Forbidden:
                print_error(f"Rol oluşturulurken bir hata oluştu; {role.name}")
            except discord.HTTPException:
                print_error(f"Oluşturulamayan rol; {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Silinen kanal; {channel.name}")
            except discord.Forbidden:
                print_error(f"Kanal silinirken bir hata oluştu; {channel.name}")
            except discord.HTTPException:
                print_error(f"Silinemeyen kanal; {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Silinen kategori; {channel.name}")
            except discord.Forbidden:
                print_error(f"Kategori silinirken bir hata oluştu; {channel.name}")
            except discord.HTTPException:
                print_error(f"Silinemeyen kategori; {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"{channel_text.name} isimli kanalda herhangi bir kategori yok!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Oluşturulan kanal; {channel_text.name}")
            except discord.Forbidden:
                print_error(f"Metin kanalı oluşturulurken bir hata oluştu; {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Oluşturulamayan metin kanalı; {channel_text.name}")
            except:
                print_error(f"Metin kanalı oluşturulurken bir hata oluştu; {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"{channel_voice.name} isimli kanalda herhangi bir kategori yok!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Oluşturulan ses kanalı; {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Ses kanalı oluşturulurken bir hata oluştu; {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Oluşturulamayan ses kanalı; {channel_voice.name}")
            except:
                print_error(f"Ses kanalı oluşturulurken bir hata oluştu; {channel_voice.name}")


    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Silinen emoji; {emoji.name}")
            except discord.Forbidden:
                print_error(f"Emoji silinirken bir hata oluştu; {emoji.name}")
            except discord.HTTPException:
                print_error(f"Emoji silinirken bir hata oluştu; {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_add(f"Oluşturulan emoji; {emoji.name}")
            except discord.Forbidden:
                print_error(f"Emoji oluşturulurken bir hata oluştu; {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Emoji oluşturulurken bir hata oluştu; {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print_error(f"Okunamayan sunucu resmi; {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_add(f"Sunucu resmi değiştirildi; {guild_to.name}")
                except:
                    print_error(f"Sunucu resmi değiştirilirken bir hata oluştu; {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Sunucu resmi değiştirilirken bir hata oluştu; {guild_to.name}")
