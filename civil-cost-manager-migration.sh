#!/bin/bash
# civil-cost-manager-migration v1.0
# 단가DB 마이그레이션 스크립트

cd ~/.openclaw/workspace/civil-cost-manager

# 최신 JSON pull
git pull origin main

# 마이그레이션 실행 (프로젝트명 인수 전달)
# 사용법: ./civil-cost-manager-migration.sh 샘플_1공구
python3 database/init_db.py --project "$1"
