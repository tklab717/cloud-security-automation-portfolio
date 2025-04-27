# disable_old_keys.py

import boto3
from datetime import datetime, timezone, timedelta

def is_key_old(last_used_date, threshold_days=90):
    """アクセスキーが最後に使われた日からthreshold_days以上経過しているかを判定"""
    if last_used_date is None:
        # 一度も使用されていない場合
        return True
    delta = datetime.now(timezone.utc) - last_used_date
    return delta.days >= threshold_days

def disable_old_keys(threshold_days=90):
    """IAMユーザで、指定した日数以上アクセスがないか、一度もアクセスがない場合は無効化する"""
    iam = boto3.client('iam')
    users = iam.list_users()

    for user in users['Users']:
        username = user['UserName']
        keys = iam.list_access_keys(UserName=username)

        for key in keys['AccessKeyMetadata']:
            access_key_id = key['AccessKeyId']
            last_used_info = iam.get_access_key_last_used(AccessKeyId=access_key_id)
            last_used_date = last_used_info['AccessKeyLastUsed'].get('LastUsedDate')
            print(f"{last_used_date}")

            if is_key_old(last_used_date, threshold_days):
                print(f"無効化対象: {username} / {access_key_id}")
                iam.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive'
                )