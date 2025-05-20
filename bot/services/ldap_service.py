from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import logging
import ssl

logger = logging.getLogger(__name__)

async def check_ad_login(login: str, config: dict):
    """Проверяет существование пользователя в AD и получает email"""
    try:
        server = Server(config['LDAP_SERVER'],
                        use_ssl=True,
                        port=config['LDAP_PORT'],
                        get_info=ALL)

        conn = Connection(server,
                          user=config['LDAP_BIND_USER'],
                          password=config['LDAP_BIND_PASSWORD'],
                          auto_bind=True)

        search_filter = f"(sAMAccountName={login})"
        conn.search(config['LDAP_BASE_DN'],
                    search_filter,
                    attributes=['mail', 'distinguishedName'])

        if conn.entries:
            email = conn.entries[0].mail.value if hasattr(conn.entries[0], 'mail') else None
            return True, email
        return False, None
    except Exception as e:
        logger.error(f"LDAP error: {e}")
        return False, None

async def reset_ad_password(ad_login: str, new_password: str, config: dict):
    """Сбрасывает пароль пользователя в AD"""
    try:
        server = Server(config['LDAP_SERVER'],
                        use_ssl=True,
                        port=config['LDAP_PORT'],
                        get_info=ALL)

        conn = Connection(server,
                          user=config['LDAP_BIND_USER'],
                          password=config['LDAP_BIND_PASSWORD'],
                          auto_bind=True)

        conn.search(config['LDAP_BASE_DN'],
                    f"(sAMAccountName={ad_login})",
                    attributes=['distinguishedName'])

        if not conn.entries:
            return False

        user_dn = conn.entries[0].distinguishedName.value
        encoded_password = f'"{new_password}"'.encode('utf-16-le')

        # Исправленная строка (добавлена закрывающая скобка)
        return conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_password])]})
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return False