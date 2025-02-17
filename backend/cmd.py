import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User
from sqlalchemy import select, delete

engine = create_engine("sqlite:///./data/data.db")
new_session = sessionmaker(engine, expire_on_commit=False)


@click.command()
@click.argument('user_id', type=int)
@click.option('--admin-status', is_flag=True, help='Set admin status to True if present.')
def update_admin_status(user_id: int, admin_status: bool):
    """
    Change status of user <USER_ID> to <ADMIN_STATUS>.
    """
    if admin_status:
        role = "Админ"
    else:
        role = "Пользователь"
    with new_session() as session:
        query = select(User).filter_by(id=user_id)
        result = session.execute(query)
        user_field = result.scalars().first()
        if user_field is None:
            click.echo('user not found.')
            return
        user_field.role = role
        session.commit()
        click.echo(f'id={user_field.id}    role={user_field.role}')

if __name__ == '__main__':
    update_admin_status()
