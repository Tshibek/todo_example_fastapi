"""empty message

Revision ID: 4a23e9d2b3e9
Revises: 5d16bf4e74c2
Create Date: 2023-10-25 00:19:35.366534

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4a23e9d2b3e9"
down_revision = "5d16bf4e74c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users_model",
        sa.Column("email", sa.String(length=255), nullable=False),
    )
    op.create_unique_constraint(None, "users_model", ["email"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users_model", type_="unique")
    op.drop_column("users_model", "email")
    # ### end Alembic commands ###
