# test_disable_old_keys.py

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from moto import mock_aws
import boto3

from disable_old_keys import is_key_old, disable_old_keys

mock_iam = mock_aws("iam")

def test_is_key_old_logic():
    """is_key_old関数の単体テスト"""
    now = datetime.now(timezone.utc)
    # 判定閾値90日で、現在から100日前だったら、経過判定する
    assert is_key_old(now - timedelta(days=100),90) == True
    # 判定閾値90日で、現在から10日前だったら、経過判定しない
    assert is_key_old(now - timedelta(days=10),90) == False
    # 登録後、使用されておらず、Noneだったら、経過判定する
    assert is_key_old(None) == True

@mock_aws
def test_disable_old_keys_behavior():
    """IAMのモックを使ったdisable_old_keysの動作テスト"""
    iam = boto3.client('iam')

    # ユーザー作成
    iam.create_user(UserName='test-user')

    # アクセスキー発行
    create_response = iam.create_access_key(UserName='test-user')
    access_key_id = create_response['AccessKey']['AccessKeyId']

    # IAMユーザー及びそのアクセスキー情報ができているか確認
    users = iam.list_users()
    assert len(users['Users']) == 1
    keys = iam.list_access_keys(UserName='test-user')
    assert len(keys['AccessKeyMetadata']) == 1

    # disable_old_keysを実行し、エラーが発生しないか確認
    disable_old_keys(threshold_days=90)

    # IAMユーザ及びアクセスキーを確認する
    for user in users['Users']:
        username = user['UserName']
        keys = iam.list_access_keys(UserName=username)
        for key in keys['AccessKeyMetadata']:
            access_key_id = key['AccessKeyId']
            access_status = key['Status']
            print(f"username: {username},Status: {access_status}")