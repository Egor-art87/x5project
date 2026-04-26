"""
Утилита: сменить роль пользователя.

Использование:
    python -m scripts.set_role <email> <admin|recruiter|candidate>

Пример:
    python -m scripts.set_role rec@test.ru recruiter
"""

import asyncio
import sys

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole


async def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    email, role_raw = sys.argv[1].lower(), sys.argv[2].lower()
    try:
        role = UserRole(role_raw)
    except ValueError:
        print(f"Недопустимая роль: {role_raw}. Допустимы: {[r.value for r in UserRole]}")
        sys.exit(1)

    async with AsyncSessionLocal() as db:
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()
        if user is None:
            print(f"Пользователь {email} не найден")
            sys.exit(1)
        user.role = role
        await db.commit()
        print(f"OK: {email} теперь {role.value}")


if __name__ == "__main__":
    asyncio.run(main())
