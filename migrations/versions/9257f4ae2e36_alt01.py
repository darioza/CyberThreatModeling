"""Alt01

Revision ID: 9257f4ae2e36
Revises: 
Create Date: 2023-09-19 15:47:30.262732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9257f4ae2e36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('CybersecurityCategories', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('category_name',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('CybersecurityRequirements', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('requirement_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('ProjectCybersecurityRequirements', schema=None) as batch_op:
        batch_op.alter_column('projeto_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('requirement_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('projeto', schema=None) as batch_op:
        batch_op.alter_column('arquiteto',
               existing_type=sa.TEXT(),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('debitos_tecnicos',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('status_projeto',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_column('previsao_termino')
        batch_op.drop_column('data_criacao')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projeto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_criacao', sa.TIMESTAMP(), nullable=True))
        batch_op.add_column(sa.Column('previsao_termino', sa.TIMESTAMP(), nullable=True))
        batch_op.alter_column('status_projeto',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('debitos_tecnicos',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('arquiteto',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('ProjectCybersecurityRequirements', schema=None) as batch_op:
        batch_op.alter_column('requirement_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('projeto_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('CybersecurityRequirements', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('requirement_name',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('CybersecurityCategories', schema=None) as batch_op:
        batch_op.alter_column('category_name',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    op.drop_table('user')
    # ### end Alembic commands ###
