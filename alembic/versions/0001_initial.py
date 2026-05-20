"""initial schema
Revision ID: 0001_initial
Revises:
Create Date: 2026-05-20
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
revision='0001_initial'
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('login',sa.String(128),nullable=False), sa.Column('hashed_password',sa.String(255),nullable=True), sa.Column('github_id',sa.String(128),nullable=True), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    op.create_index('ix_users_login','users',['login'],unique=True)
    op.create_index('ix_users_github_id','users',['github_id'],unique=True)
    op.create_table('chats', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('title',sa.String(255),nullable=False), sa.Column('owner_id',sa.Integer(),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    op.create_index('ix_chats_owner_id','chats',['owner_id'])
    op.create_table('messages', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('chat_id',sa.Integer(),sa.ForeignKey('chats.id',ondelete='CASCADE'),nullable=False), sa.Column('role',sa.String(32),nullable=False), sa.Column('content',sa.Text(),nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    op.create_index('ix_messages_chat_id','messages',['chat_id'])

def downgrade():
    op.drop_index('ix_messages_chat_id',table_name='messages'); op.drop_table('messages')
    op.drop_index('ix_chats_owner_id',table_name='chats'); op.drop_table('chats')
    op.drop_index('ix_users_github_id',table_name='users'); op.drop_index('ix_users_login',table_name='users'); op.drop_table('users')
