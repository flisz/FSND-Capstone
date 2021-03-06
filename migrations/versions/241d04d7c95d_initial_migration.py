"""initial_migration

Revision ID: 241d04d7c95d
Revises: 
Create Date: 2020-11-01 16:12:05.795560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import ArrowType


# revision identifiers, used by Alembic.
revision = '241d04d7c95d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line1', sa.String(), nullable=False),
    sa.Column('line2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('zip_code', sa.String(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_created_at'), 'address', ['created_at'], unique=False)
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alternate_id', sa.String(length=256), nullable=False),
    sa.Column('social_id', sa.String(length=256), nullable=True),
    sa.Column('nickname', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('picture', sa.String(length=256), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('family_name', sa.String(length=256), nullable=True),
    sa.Column('given_name', sa.String(length=256), nullable=True),
    sa.Column('locale', sa.String(length=16), nullable=False),
    sa.Column('updated_at', ArrowType(), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alternate_id'),
    sa.UniqueConstraint('social_id')
    )
    op.create_index(op.f('ix_userprofile_created_at'), 'userprofile', ['created_at'], unique=False)
    op.create_index(op.f('ix_userprofile_updated_at'), 'userprofile', ['updated_at'], unique=False)
    op.create_table('manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userprofile_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['userprofile_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manager_created_at'), 'manager', ['created_at'], unique=False)
    op.create_table('patron',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userprofile_id', sa.Integer(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['userprofile_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patron_created_at'), 'patron', ['created_at'], unique=False)
    op.create_table('user_address_association',
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('userprofile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['userprofile_id'], ['userprofile.id'], )
    )
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userprofile_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['userprofile_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_created_at'), 'provider', ['created_at'], unique=False)
    op.create_table('scheduler',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userprofile_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['userprofile_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scheduler_created_at'), 'scheduler', ['created_at'], unique=False)
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('held', sa.Boolean(), nullable=False),
    sa.Column('cancelled', sa.Boolean(), nullable=False),
    sa.Column('scheduler_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.Column('start_time', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['scheduler_id'], ['scheduler.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointment_created_at'), 'appointment', ['created_at'], unique=False)
    op.create_index(op.f('ix_appointment_start_time'), 'appointment', ['start_time'], unique=False)
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patron_id', sa.Integer(), nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointment.id'], ),
    sa.ForeignKeyConstraint(['patron_id'], ['patron.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_record_created_at'), 'record', ['created_at'], unique=False)
    op.create_table('measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('value', sa.String(length=256), nullable=False),
    sa.Column('units', sa.String(length=256), nullable=False),
    sa.Column('valid', sa.Boolean(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['record.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_measurement_created_at'), 'measurement', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_measurement_created_at'), table_name='measurement')
    op.drop_table('measurement')
    op.drop_index(op.f('ix_record_created_at'), table_name='record')
    op.drop_table('record')
    op.drop_index(op.f('ix_appointment_start_time'), table_name='appointment')
    op.drop_index(op.f('ix_appointment_created_at'), table_name='appointment')
    op.drop_table('appointment')
    op.drop_index(op.f('ix_scheduler_created_at'), table_name='scheduler')
    op.drop_table('scheduler')
    op.drop_index(op.f('ix_provider_created_at'), table_name='provider')
    op.drop_table('provider')
    op.drop_table('user_address_association')
    op.drop_index(op.f('ix_patron_created_at'), table_name='patron')
    op.drop_table('patron')
    op.drop_index(op.f('ix_manager_created_at'), table_name='manager')
    op.drop_table('manager')
    op.drop_index(op.f('ix_userprofile_updated_at'), table_name='userprofile')
    op.drop_index(op.f('ix_userprofile_created_at'), table_name='userprofile')
    op.drop_table('userprofile')
    op.drop_index(op.f('ix_address_created_at'), table_name='address')
    op.drop_table('address')
    # ### end Alembic commands ###
